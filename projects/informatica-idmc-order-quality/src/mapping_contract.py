"""Local reference for a CDI mapping; not an IDMC runtime or native export."""
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

def transform(rows):
    accepted, rejected, seen = [], [], {}
    for line, row in enumerate(rows, start=2):
        reason = None
        key = (row["source"].strip(),row["order_id"].strip())
        try:
            amount=Decimal(row["amount"])
            if not amount.is_finite() or amount < 0 or amount*100 != (amount*100).to_integral_value():
                raise ValueError("invalid money")
            cents=int(amount*100)
        except (InvalidOperation,ValueError,OverflowError):
            reason="INVALID_AMOUNT"
            cents=0
        if not all(key):reason="MISSING_KEY"
        elif row["currency"].strip().upper()!="USD":reason="UNSUPPORTED_CURRENCY"
        if reason:
            rejected.append({"line":line,"reason":reason})
            continue
        normalized={"source":key[0],"order_id":key[1],"amount_cents":cents,"currency":"USD"}
        if key in seen:
            if seen[key]!=normalized:raise ValueError("Conflicting duplicate source key")
            continue
        seen[key]=normalized
        accepted.append(normalized)
    return {"accepted":accepted,"rejected":rejected,"revenue_cents":sum(r["amount_cents"] for r in accepted)}

if __name__=="__main__":
    with open("data/orders.csv",newline="") as f:result=transform(list(csv.DictReader(f)))
    Path("output").mkdir(exist_ok=True)
    Path("output/result.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
