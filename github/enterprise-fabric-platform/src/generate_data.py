"""Small, deterministic fixtures; deliberately contains invalid events and replay."""
import json
from pathlib import Path

def event(seq, order, quantity=1, price=1000, operation='UPSERT', region='East'):
    return dict(event_id=seq, order_id=order, operation=operation, order_date='2026-01-01',
                region=region, product_id=(order % 3)+1, quantity=quantity, unit_price_cents=price)

def generate(output):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    first=[event(1,101,2,1500),event(2,102,1,4000,region='West'),event(3,103,3,1000)]
    second=[event(4,101,3,1500),event(5,102,1,4000,'DELETE',region='West'),
            event(6,104,2,2500,region='South'),event(7,105,-2,1000),event(8,106,1,2000,region='Mars')]
    third=[event(9,105,2,1000),event(10,106,1,2000,region='West')]
    for name, rows in [('batch_001',first),('batch_002',second+[second[0]]),('batch_003_corrections',third)]:
        (output/(name+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rows))
if __name__=='__main__':
    generate(Path(__file__).resolve().parents[1]/'data')
