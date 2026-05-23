#!/usr/bin/env python3
"""wbs-check.py — lint a YAML WBS file for common violations.

Usage: python wbs-check.py wbs.yaml
Checks: noun-led names, max depth 5, leaf estimates in 8-80h range.
Exit 0 = clean, exit 1 = violations found.
"""
import sys
import yaml

VERBS = {"build", "design", "test", "deploy", "write", "do", "create",
         "implement", "develop", "configure", "install", "plan", "review"}

data = yaml.safe_load(open(sys.argv[1]))
errs = []


def walk(n, depth, pid):
    nid = f"{pid}.{n.get('seq', '?')}".strip(".")
    name = n.get("name", "")
    if name and name.split()[0].lower() in VERBS:
        errs.append(f"verb-led {nid}: {name!r}")
    if depth >= 5 and n.get("children"):
        errs.append(f"too deep {nid} (depth {depth + 1} > 5)")
    if not n.get("children"):
        h = n.get("est_hours") or 0
        if h and not (8 <= h <= 80):
            errs.append(f"out of 8/80 rule {nid}: {h}h")
    for c in n.get("children") or []:
        walk(c, depth + 1, nid)


items = data if isinstance(data, list) else [data]
for i, root in enumerate(items):
    root.setdefault("seq", i + 1)
    walk(root, 0, "")

print("\n".join(errs) if errs else "ok")
sys.exit(1 if errs else 0)
