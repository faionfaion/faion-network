#!/usr/bin/env python3
"""cpm.py — minimal Critical Path Method (CPM) from a YAML activity list.

Usage: python cpm.py activities.yaml
Input YAML: list of {id, dur, preds: [{id, lag}]}
Output: critical path, duration, float per activity.
"""
import sys
import yaml

acts = {a["id"]: a for a in yaml.safe_load(open(sys.argv[1]))}


def es(a):
    if "_es" in a:
        return a["_es"]
    a["_es"] = max(
        (es(acts[p["id"]]) + acts[p["id"]]["dur"] + p.get("lag", 0)
         for p in a.get("preds", [])),
        default=0,
    )
    a["_ef"] = a["_es"] + a["dur"]
    return a["_es"]


for a in acts.values():
    es(a)

end = max(a["_ef"] for a in acts.values())


def lf(a):
    if "_lf" in a:
        return a["_lf"]
    succ = [s for s in acts.values()
            if any(p["id"] == a["id"] for p in s.get("preds", []))]
    a["_lf"] = min(
        (lf(s) - s["dur"] - next(
            p for p in s["preds"] if p["id"] == a["id"]
        ).get("lag", 0) for s in succ),
        default=end,
    )
    a["_ls"] = a["_lf"] - a["dur"]
    a["_float"] = a["_ls"] - a["_es"]
    return a["_lf"]


for a in acts.values():
    lf(a)

crit = [a["id"] for a in acts.values() if a["_float"] == 0]
near_crit = [a["id"] for a in acts.values() if 0 < a["_float"] <= 2]

print(f"Project duration: {end} days")
print(f"Critical path: {' -> '.join(crit)}")
if near_crit:
    print(f"Near-critical (float <= 2d): {near_crit}")

for a in sorted(acts.values(), key=lambda x: x["_es"]):
    print(f"  {a['id']}: ES={a['_es']} EF={a['_ef']} "
          f"LS={a['_ls']} LF={a['_lf']} float={a['_float']}")
