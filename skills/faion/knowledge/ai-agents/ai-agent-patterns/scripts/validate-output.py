#!/usr/bin/env python3
"""validate-output.py — validate an ai-agent-patterns decision record.

Exit codes: 0 valid; 1 violations; 2 usage; 3 load.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

PATTERNS = {"cot","react","plan-and-execute","tool-use"}
FRAMEWORKS = {"raw-sdk","langgraph","autogen","crewai","openai-agents-sdk","claude-code"}

def validate(p):
    v = []
    for k in ["task_id","classification","chosen_pattern","chosen_framework",
              "framework_pin","caps","tools","rationale","rejected","owner","version","produced_at"]:
        if k not in p: v.append(f"missing {k}")
    if v: return v
    c = p["classification"]
    for ck in ["needs_tools","step_count","branching"]:
        if ck not in c: v.append(f"classification.{ck} missing")
    if p["chosen_pattern"] not in PATTERNS: v.append(f"chosen_pattern must be in {sorted(PATTERNS)}")
    if p["chosen_framework"] not in FRAMEWORKS: v.append(f"chosen_framework must be in {sorted(FRAMEWORKS)}")
    if not re.search(r"==\d+\.\d+", p["framework_pin"] or ""):
        v.append("f2: framework_pin must be exact version (e.g. langgraph==0.2.34)")
    caps = p["caps"]
    if not isinstance(caps.get("max_steps"), int) or caps["max_steps"] < 1 or caps["max_steps"] > 50:
        v.append("f3: caps.max_steps required, 1..50")
    if not p["tools"] and p["chosen_pattern"] != "cot":
        v.append("f4: tools[] must be non-empty for non-cot patterns")
    if not c.get("needs_tools") and p["chosen_pattern"] in {"react","plan-and-execute","tool-use"}:
        v.append("f1: needs_tools=false but tool-using pattern chosen")
    if not p["rejected"]:
        v.append("f5: rejected must be non-empty")
    if not re.fullmatch(r"\d+\.\d+\.\d+", p["version"]):
        v.append("version must be semver")
    return v

def main(argv):
    if "--help" in argv or "-h" in argv: sys.stdout.write(__doc__); return 0
    if "--self-test" in argv:
        good = {"task_id":"t","classification":{"needs_tools":True,"step_count":4,"branching":False},
                "chosen_pattern":"react","chosen_framework":"raw-sdk","framework_pin":"anthropic==0.39.0",
                "caps":{"max_steps":15,"loop_detect":True},
                "tools":[{"name":"web_search","description":"Full-text web search returns top 10 results"}],
                "rationale":"Task needs tools but step count small.","rejected":[{"pattern":"cot","framework":"raw-sdk","reason":"x"}],
                "owner":"a@b","version":"1.0.0","produced_at":"2026-05-22T10:00:00Z"}
        vs = validate(good)
        if vs: sys.stderr.write(f"FAIL: {vs}\n"); return 1
        sys.stdout.write("self-test passed\n"); return 0
    if len(argv) < 2: sys.stderr.write("usage: validate-output.py <record.json>\n"); return 2
    try: payload = json.loads(Path(argv[1]).read_text())
    except Exception as e: sys.stderr.write(f"load: {e}\n"); return 3
    vs = validate(payload)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__": sys.exit(main(sys.argv))
