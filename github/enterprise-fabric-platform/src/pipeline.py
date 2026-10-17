"""Deterministic single-writer CDC learning implementation. Standard library only."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sqlite3
import uuid
from datetime import date, datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'event_id', 'order_id', 'operation', 'order_date', 'region', 'product_id', 'quantity', 'unit_price_cents'}


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=30)
    db.executescript((ROOT / 'sql/schema.sql').read_text())
    return db


def canonical(row):
    return json.dumps(row, sort_keys=True, separators=(',', ':'))


def validate(row):
    if set(row) != FIELDS:
        return 'schema_mismatch'
    for field in ('order_id', 'product_id', 'quantity', 'unit_price_cents'):
        if type(row[field]) is not int:
            return 'invalid_' + field
    if row['order_id'] <= 0 or row['product_id'] <= 0:
        return 'invalid_business_key'
    if row['operation'] not in ('UPSERT', 'DELETE'):
        return 'invalid_operation'
    try:
        if date.fromisoformat(row['order_date']).isoformat() != row['order_date']:
            return 'invalid_date'
    except (TypeError, ValueError):
        return 'invalid_date'
    if row['region'] not in ('East', 'West', 'South', 'Central'):
        return 'invalid_region'
    if not 1 <= row['quantity'] <= 100000 or not 0 <= row['unit_price_cents'] <= 100000000:
        return 'invalid_amount'
    return None


def load(db_path, input_path, fail_after_merge=False):
    """Atomic bronze/quarantine/current-state/checkpoint publication, plus durable audit.

    Input must be a complete committed sequence interval from ONE ordered stream.
    Transport duplicates allowed; conflicting reuse of an event ID fails closed.
    Business-invalid events are acknowledged only after durable quarantine.
    """
    db = connect(db_path)
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc).isoformat()
    fingerprint = None
    try:
        raw = Path(input_path).read_bytes()
        fingerprint = hashlib.sha256(raw).hexdigest()
        records = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
        unique = {}
        for row in records:
            if not isinstance(row, dict) or type(row.get('event_id')) is not int or row['event_id'] <= 0:
                raise ValueError('invalid_event_id: cannot acknowledge unordered event')
            key = row['event_id']
            if key in unique and canonical(unique[key]) != canonical(row):
                raise ValueError('conflicting_event_id')
            unique[key] = row
        db.execute('BEGIN IMMEDIATE')  # serialize writers; acquire before reading checkpoint
        previous = db.execute('SELECT last_event_id FROM checkpoint WHERE stream=?', ('orders',)).fetchone()[0]
        for key, row in unique.items():
            saved = db.execute('SELECT payload FROM bronze_events WHERE event_id=?', (key,)).fetchone()
            if saved and saved[0] != canonical(row):
                raise ValueError('conflicting_event_id')
        pending = sorted((r for k, r in unique.items() if k > previous), key=lambda r: r['event_id'])
        high = pending[-1]['event_id'] if pending else previous
        if [r['event_id'] for r in pending] != list(range(previous + 1, high + 1)):
            raise ValueError('sequence_gap: input must contain every committed event in interval')
        rejected = 0
        accepted = 0
        for row in pending:
            payload = canonical(row)
            db.execute('INSERT INTO bronze_events VALUES (?, ?, ?)', (row['event_id'], payload, run_id))
            reason = validate(row)
            if reason:
                db.execute('INSERT INTO quarantine VALUES (?, ?, ?, ?)', (row['event_id'], reason, payload, run_id))
                rejected += 1
                continue
            db.execute('''INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT(order_id) DO UPDATE SET
                order_date=excluded.order_date,region=excluded.region,product_id=excluded.product_id,
                quantity=excluded.quantity,unit_price_cents=excluded.unit_price_cents,
                is_deleted=excluded.is_deleted,last_event_id=excluded.last_event_id,run_id=excluded.run_id
                WHERE excluded.last_event_id > orders.last_event_id''',
                (row['order_id'],row['order_date'],row['region'],row['product_id'],row['quantity'],
                 row['unit_price_cents'],int(row['operation']=='DELETE'),row['event_id'],run_id))
            accepted += 1
        if fail_after_merge:
            raise RuntimeError('injected_failure_after_merge')
        bronze = db.execute('SELECT COUNT(*) FROM bronze_events WHERE run_id=?', (run_id,)).fetchone()[0]
        if bronze != accepted + rejected or bronze != len(pending):
            raise RuntimeError('reconciliation_failed')
        db.execute('UPDATE checkpoint SET last_event_id=? WHERE stream=?', (high, 'orders'))
        result = dict(run_id=run_id,status='SUCCEEDED',received=len(records),new_events=len(pending),
                      accepted=accepted,rejected=rejected,previous_checkpoint=previous,checkpoint=high)
        db.execute('INSERT INTO runs VALUES (?,?,?,?,?,?)',
                   (run_id, started, 'SUCCEEDED', fingerprint, canonical(result), None))
        db.commit()
        return result
    except Exception as exc:
        db.rollback()
        # Data transaction is rolled back; failure telemetry survives independently.
        db.execute('INSERT INTO runs VALUES (?,?,?,?,?,?)',
                   (run_id,started,'FAILED',fingerprint,'{}',str(exc)))
        db.commit()
        raise
    finally:
        db.close()


def export(db_path, output):
    db = connect(db_path)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for table in ('fact_orders', 'dim_region', 'dim_product', 'dim_date', 'sales_by_region', 'runs', 'quarantine'):
        cursor = db.execute('SELECT * FROM ' + table)  # fixed allowlist above
        with (output / (table + '.csv')).open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([col[0] for col in cursor.description])
            writer.writerows(cursor.fetchall())
    db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='build/platform.db')
    sub = parser.add_subparsers(dest='command', required=True)
    ingest = sub.add_parser('load')
    ingest.add_argument('input')
    ingest.add_argument('--fail-after-merge', action='store_true')
    out = sub.add_parser('export')
    out.add_argument('--output', default='build/exports')
    args = parser.parse_args()
    if args.command == 'load':
        print(json.dumps(load(args.db, args.input, args.fail_after_merge), indent=2))
    else:
        export(args.db, args.output)

if __name__ == '__main__':
    main()
