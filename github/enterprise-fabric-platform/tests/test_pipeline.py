import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from src.generate_data import generate, event
from src.pipeline import load, export

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.db=self.root/'test.db'; generate(self.root)
    def tearDown(self): self.tmp.cleanup()
    def batch(self,n): return self.root/(n+'.jsonl')
    def query(self,sql):
        with sqlite3.connect(self.db) as c: return c.execute(sql).fetchall()
    def write(self,rows):
        p=self.root/'custom.jsonl'; p.write_text(''.join(json.dumps(r)+'\n' for r in rows)); return p
    def first(self): return load(self.db,self.batch('batch_001'))
    def second(self): return load(self.db,self.batch('batch_002'))
    def test_full_load_reconciles(self):
        self.assertEqual(self.first()['accepted'],3)
        self.assertEqual(self.query('SELECT SUM(revenue_cents) FROM fact_orders'),[(10000,)])
    def test_replay_is_noop(self):
        self.first(); r=self.first()
        self.assertEqual(r['new_events'],0)
        self.assertEqual(self.query('SELECT COUNT(*) FROM orders'),[(3,)])
    def test_updates_deletes_duplicates_quarantine(self):
        self.first(); r=self.second()
        self.assertEqual((r['received'],r['new_events'],r['accepted'],r['rejected']),(6,5,3,2))
        self.assertEqual(self.query('SELECT SUM(revenue_cents) FROM fact_orders'),[(12500,)])
        self.assertEqual(self.query('SELECT is_deleted FROM orders WHERE order_id=102'),[(1,)])
    def test_failure_rolls_back_and_audits(self):
        self.first()
        with self.assertRaisesRegex(RuntimeError,'injected'): load(self.db,self.batch('batch_002'),True)
        self.assertEqual(self.query('SELECT last_event_id FROM checkpoint'),[(3,)])
        self.assertEqual(self.query('SELECT COUNT(*) FROM bronze_events'),[(3,)])
        self.assertEqual(self.query('SELECT COUNT(*) FROM quarantine'),[(0,)])
        self.assertEqual(self.query("SELECT COUNT(*) FROM runs WHERE status='FAILED'"),[(1,)])
        self.second()
        self.assertEqual(self.query('SELECT SUM(revenue_cents) FROM fact_orders'),[(12500,)])
    def test_gap_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'sequence_gap'): load(self.db,self.write([event(2,100)]))
        self.assertEqual(self.query('SELECT last_event_id FROM checkpoint'),[(0,)])
    def test_conflicting_replayed_id_fails(self):
        self.first()
        with self.assertRaisesRegex(ValueError,'conflicting'): load(self.db,self.write([event(1,999)]))
    def test_conflicting_same_batch_fails(self):
        with self.assertRaisesRegex(ValueError,'conflicting'): load(self.db,self.write([event(1,100),event(1,101)]))
    def test_invalid_ordering_key_fails(self):
        r=event(1,100); r['event_id']='1'
        with self.assertRaisesRegex(ValueError,'invalid_event_id'): load(self.db,self.write([r]))
    def test_schema_drift_quarantined(self):
        r=event(1,100); r['new_field']='unexpected'
        result=load(self.db,self.write([r]))
        self.assertEqual(result['rejected'],1)
        self.assertEqual(self.query('SELECT reason FROM quarantine'),[('schema_mismatch',)])
    def test_correction_requires_new_event(self):
        self.first(); self.second(); load(self.db,self.batch('batch_003_corrections'))
        self.assertEqual(self.query('SELECT COUNT(*),SUM(revenue_cents) FROM fact_orders'),[(5,16500)])
        self.assertEqual(self.query('SELECT COUNT(*) FROM quarantine'),[(2,)])
    def test_empty_batch_does_not_move_checkpoint(self):
        self.first(); self.assertEqual(load(self.db,self.write([]))['checkpoint'],3)
    def test_unsorted_batch_sorted_by_commit_sequence(self):
        load(self.db,self.write([event(2,100,2),event(1,100,1)]))
        self.assertEqual(self.query('SELECT quantity FROM orders'),[(2,)])
    def test_export_has_star_tables(self):
        self.first(); export(self.db,self.root/'out')
        self.assertTrue((self.root/'out/fact_orders.csv').exists())
        self.assertIn('revenue_cents',(self.root/'out/fact_orders.csv').read_text())
    def test_invalid_json_does_not_mutate(self):
        p=self.root/'broken.jsonl'; p.write_text('{')
        with self.assertRaises(json.JSONDecodeError): load(self.db,p)
        self.assertEqual(self.query('SELECT COUNT(*) FROM bronze_events'),[(0,)])
    def test_bad_types_and_dates_quarantined(self):
        rows=[event(i,i) for i in range(1,4)]
        rows[0]['quantity']=True; rows[1]['order_date']='2026-02-30'; rows[2]['unit_price_cents']='100'
        self.assertEqual(load(self.db,self.write(rows))['rejected'],3)

if __name__=='__main__': unittest.main()
