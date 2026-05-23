#!/usr/bin/env python3
# purpose: Product-Qualified-Lead scorer from usage signals
# consumes: JSON stdin: {workspaces, integrations, invited_collaborators, depth_events}
# produces: stdout: PQL score + tier
# depends-on: stdlib (json)
# token-budget-impact: low

import argparse, json, sys

WEIGHTS = {"workspaces": 2, "integrations": 3, "invited_collaborators": 4, "depth_events": 1}

def score(d):
    s = 0
    for k, w in WEIGHTS.items():
        s += min(d.get(k, 0), 10) * w
    return s

def tier(s):
    if s >= 60: return "hot"
    if s >= 30: return "warm"
    return "cold"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        d = {"workspaces": 3, "integrations": 4, "invited_collaborators": 5, "depth_events": 8}
        s = score(d); t = tier(s)
        ok = s > 30 and t in ("warm", "hot")
        sys.stdout.write(f"self-test s={s} t={t} pass={ok}\n")
        sys.exit(0 if ok else 1)
    d = json.load(sys.stdin)
    s = score(d)
    sys.stdout.write(json.dumps({"score": s, "tier": tier(s)}) + "\n")

if __name__ == "__main__":
    main()
