#!/usr/bin/env python3
# sensitivity.py — weight perturbation and brittleness detection for scoring matrices.
# Usage: python sensitivity.py matrix.json
# Input JSON: {
#   "criteria": [{"id": "fit", "weight": 0.25}, ...],
#   "options": [{"id": "A", "scores": {"fit": 4, "tech": 5, ...}}, ...]
# }
import json
import sys
import copy


def weighted(opts, crits):
    return sorted(
        ({"id": o["id"],
          "total": round(sum(o["scores"][c["id"]] * c["weight"] for c in crits), 3)}
         for o in opts),
        key=lambda r: r["total"],
        reverse=True,
    )


def perturb(crits, idx, delta):
    out = copy.deepcopy(crits)
    out[idx]["weight"] = max(0, out[idx]["weight"] + delta)
    s = sum(c["weight"] for c in out)
    if s == 0:
        return out
    for c in out:
        c["weight"] /= s  # re-normalize
    return out


m = json.load(open(sys.argv[1]))
weight_sum = sum(c["weight"] for c in m["criteria"])
if abs(weight_sum - 1.0) > 0.001:
    print(json.dumps({"error": f"weights sum to {weight_sum:.3f}, must equal 1.0"}))
    sys.exit(1)

base = weighted(m["options"], m["criteria"])
print(f"baseline ranking: {[r['id'] for r in base]}")
print(f"baseline totals:  {base}")

flips = 0
flip_details = []
for i, c in enumerate(m["criteria"]):
    for d in (+0.10, -0.10):
        rk = weighted(m["options"], perturb(m["criteria"], i, d))
        if rk[0]["id"] != base[0]["id"]:
            flips += 1
            flip_details.append(f"FLIP at {c['id']} {d:+.0%} -> winner={rk[0]['id']}")
            print(f"  {flip_details[-1]}")

brittleness = "high" if flips else "low"
print(f"\nbrittleness: {brittleness} ({flips} flip(s) under +/-10% perturbation)")
if brittleness == "high":
    print("ACTION REQUIRED: require human review before publishing this recommendation.")
