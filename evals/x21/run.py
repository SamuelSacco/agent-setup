#!/usr/bin/env python3
"""X21 runner: 2 generations x 2 styles x 5 tasks, one attempt per cell."""
import json, sys, pathlib, urllib.request, urllib.error
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT/"raw"; RAW.mkdir(exist_ok=True)
MODELS = {"newer":"claude-opus-5-5","older":"claude-opus-5"}
prompts = json.loads((ROOT/"prompts.json").read_text())
def call(model, system, user):
    payload={"model":model,"max_tokens":64,  # temperature omitted: newer model returns HTTP 400 "`temperature` is deprecated for this model" (see results amendment)
             "messages":[{"role":"user","content":user}]}
    if system: payload["system"]=system
    req=urllib.request.Request("https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(), method="POST",
        headers={"content-type":"application/json","anthropic-version":"2023-06-01"})
    add_surrogate_to_request(req,"custom.anthropic",allowed_hosts=["api.anthropic.com"])
    try:
        with urllib.request.urlopen(req,timeout=60) as r: return read_json_response(r),None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
total_in=total_out=0
for gen,model in MODELS.items():
    for style in ("legacy","modern"):
        system = prompts["legacy_system"] if style=="legacy" else prompts["modern_system"]
        for t in prompts["tasks"]:
            user = t[f"{style}_user"]
            resp,err = call(model,system,user)
            text=""
            usage={}
            if resp:
                text="".join(b.get("text","") for b in resp.get("content",[]) if b.get("type")=="text")
                usage=resp.get("usage",{})
            total_in+=usage.get("input_tokens",0); total_out+=usage.get("output_tokens",0)
            rec={"gen":gen,"model":model,"style":style,"task":t["id"],"expected":t["expected"],
                 "text":text,"usage":usage,"error":err,"response_model":(resp or {}).get("model")}
            out=RAW/f"{gen}__{style}__{t['id']}.json"
            out.write_text(json.dumps(rec,indent=2)+"\n")
            cost=(total_in*15+total_out*75)/1_000_000
            print(f"{gen} {style} {t['id']}: err={err} text={text!r} cum_est=${cost:.4f}",flush=True)
            if cost>3.50:
                print("CAP EXCEEDED, stopping"); sys.exit(1)
print(json.dumps({"input_tokens":total_in,"output_tokens":total_out,
  "est_cost_usd_at_opus_15_75_per_mtok":round((total_in*15+total_out*75)/1_000_000,4)}))
(ROOT/"usage.json").write_text(json.dumps({"input_tokens":total_in,"output_tokens":total_out,
  "est_cost_usd_at_opus_15_75_per_mtok":round((total_in*15+total_out*75)/1_000_000,4)},indent=2)+"\n")
