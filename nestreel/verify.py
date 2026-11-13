from __future__ import annotations
import json
from pathlib import Path

def rows(path):
    if not Path(path).is_file():
        return []
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]

def run_verify(args) -> int:
    out=Path(args.out)
    exp=json.loads(Path(args.expect).read_text())
    lake=rows(out/"lake.jsonl")
    quar=rows(out/"quarantine.jsonl")
    errors=[]
    got_ids=set(r["record_id"] for r in lake)
    missing=[i for i in exp.get("required_record_ids",[]) if i not in got_ids]
    if missing:
        errors.append(f"missing record_ids {missing}")
    if len(lake) < exp.get("lake_min", 0):
        errors.append(f"lake count {len(lake)} < {exp['lake_min']}")
    for item in exp.get("invoices",[]):
        rec=next((r for r in lake if r.get("invoice_no")==item["invoice_no"]), None)
        if not rec:
            errors.append(f"missing invoice {item['invoice_no']}")
            continue
        if sorted(rec.get("sources") or []) != sorted(item["sources"]):
            errors.append(f"{item['invoice_no']} sources {rec.get('sources')} != {item['sources']}")
        if rec.get("kind")!="invoice":
            errors.append(f"{item['invoice_no']} kind {rec.get('kind')}")
    reasons=sorted({q.get("reason") for q in quar})
    if reasons!=sorted(exp["quarantine_reasons"]):
        errors.append(f"quarantine reasons {reasons} != {exp['quarantine_reasons']}")
    if len(quar) < exp.get("quarantine_min", 0):
        errors.append(f"quarantine count {len(quar)} < {exp['quarantine_min']}")
    if errors:
        print("verify failed:")
        for e in errors:
            print(" -", e)
        return 1
    print("verify ok")
    return 0
