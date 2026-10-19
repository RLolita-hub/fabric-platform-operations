"""SQLite contract test for ordered Snowflake upserts, not Snowflake execution."""
import sqlite3
import json
from pathlib import Path

def apply(db, events):
    # Validate a whole batch before touching the database.
    versions={}
    for e in events:
        if not isinstance(e["order_id"],str) or not e["order_id"]:raise ValueError("Invalid key")
        if type(e["version"]) is not int or e["version"]<1:raise ValueError("Invalid version")
        if type(e["amount_cents"]) is not int or e["amount_cents"]<0:raise ValueError("Invalid amount")
        if e["op"] not in ("UPSERT","DELETE"):raise ValueError("Invalid op")
        k=(e["order_id"],e["version"])
        if k in versions and versions[k]!=e:raise ValueError("Conflicting same-version event")
        versions[k]=e
    con=sqlite3.connect(db)
    try:
        con.execute("CREATE TABLE IF NOT EXISTS orders(order_id TEXT PRIMARY KEY,version INTEGER,amount_cents INTEGER,op TEXT)")
        con.execute("BEGIN IMMEDIATE")
        for e in sorted(versions.values(),key=lambda r:(r["order_id"],r["version"])):
            old=con.execute("SELECT version,amount_cents,op FROM orders WHERE order_id=?",(e["order_id"],)).fetchone()
            incoming=(e["version"],e["amount_cents"],e["op"])
            if old and old[0]==e["version"] and old!=incoming:raise ValueError("Conflict with current version")
            con.execute("INSERT INTO orders VALUES(?,?,?,?) ON CONFLICT(order_id) DO UPDATE SET version=excluded.version,amount_cents=excluded.amount_cents,op=excluded.op WHERE excluded.version>orders.version",(e["order_id"],*incoming))
        con.commit()
        return con.execute("SELECT count(*),coalesce(sum(amount_cents),0) FROM orders WHERE op='UPSERT'").fetchone()
    except Exception:
        con.rollback();raise
    finally:con.close()

if __name__=="__main__":
    Path("output").mkdir(exist_ok=True)
    for batch in json.loads(Path("data/batches.json").read_text()):
        print(apply("output/orders.db",batch))
