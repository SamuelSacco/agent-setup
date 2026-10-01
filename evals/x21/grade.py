#!/usr/bin/env python3
"""X21 grader: exact match (stripped, case-sensitive) over saved raw outputs."""
import json, pathlib
RAW = pathlib.Path(__file__).resolve().parent/"raw"
scores={}
rows=[]
for p in sorted(RAW.glob("*.json")):
    r=json.loads(p.read_text())
    ok = r["error"] is None and r["text"].strip()==r["expected"]
    scores.setdefault((r["gen"],r["style"]),0)
    scores[(r["gen"],r["style"])]+= 1 if ok else 0
    rows.append({**r,"score":1 if ok else 0,"raw_path":f"evals/x21/raw/{p.name}"})
print(json.dumps({"scores":{f"{k[0]}/{k[1]}":v for k,v in sorted(scores.items())},
                  "rows":rows},indent=2))
pathlib.Path(__file__).resolve().parent.joinpath("grades.json").write_text(
    json.dumps({"scores":{f"{k[0]}/{k[1]}":v for k,v in sorted(scores.items())},"rows":rows},indent=2)+"\n")
