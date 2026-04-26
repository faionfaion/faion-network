#!/usr/bin/env python3
# vui-lint.py — score voice copy against length and tone rules
# Input (stdin): JSON {"nodes":[{"id":"..","type":"..","utterances":[".."],"hint":".."}]}
# Output: list of issues; exits 1 if any found, 0 if clean
import json
import re
import sys

WPM = 150
BLAME = re.compile(r"\b(you (didn'?t|forgot|need to|must)|wrong)\b", re.I)
FILLER = re.compile(r"\b(I'd be happy to|Just to confirm|I have successfully|currently)\b", re.I)


def spoken_secs(text: str) -> float:
    return len(text.split()) / WPM * 60


issues = []
for node in json.load(sys.stdin)["nodes"]:
    for u in node.get("utterances", []):
        secs = spoken_secs(u)
        if secs > 8:
            issues.append(f"too-long ({secs:.1f}s) [{node['id']}]: {u[:60]}")
        if BLAME.search(u):
            issues.append(f"blames-user [{node['id']}]: {u[:60]}")
        if FILLER.search(u):
            issues.append(f"filler-phrase [{node['id']}]: {u[:60]}")
    if node.get("type") == "error" and "say " not in (node.get("hint") or "").lower():
        issues.append(f"error-node-missing-example [{node['id']}]")

if issues:
    for issue in issues:
        print(issue)
    sys.exit(1)
else:
    print("OK: all utterances pass lint")
    sys.exit(0)
