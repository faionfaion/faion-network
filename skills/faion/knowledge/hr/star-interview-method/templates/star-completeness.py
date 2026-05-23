# purpose: Helper to score STAR completeness from a transcript
# consumes: see AGENTS.md Prerequisites
# produces: STAR Interview Method playbook-step
# depends-on: content/02-output-contract.xml schema
# token-budget-impact: ~300 tokens of agent context to invoke

#!/usr/bin/env python3
"""
star-completeness.py — Deterministic STAR component detection.
Flags missing components and "we"-only answers before LLM transcript analysis.
Run BEFORE any LLM scoring pass to gate on completeness.

Input (stdin): JSON array
  [{"question": "Tell me about a time...", "answer": "..."}, ...]

Output (stdout): JSON array
  [{"q": "...", "S": bool, "T": bool, "A": bool, "R": bool,
    "pronoun_we_only": bool, "complete": bool}, ...]

Usage:
  python3 star-completeness.py < interview.json
  cat qa.json | python3 star-completeness.py | jq '.[] | select(.complete == false)'
"""
import sys
import json
import re

CUES: dict[str, list[str]] = {
    "S": [
        r"\b(when|at the time|context was|background|last (year|quarter|month|week))\b",
        r"\b(20\d\d|in (january|february|march|april|may|june|july|august|september|october|november|december))\b",
        r"\b(while i was|during my time at|at my (previous|last|current) (job|company|role))\b",
    ],
    "T": [
        r"\b(my (role|responsibility|task|goal|job|objective))\b",
        r"\b(i was (responsible|asked|tasked|expected|required) (for|to))\b",
        r"\b(it was (up to|my job) to)\b",
    ],
    "A": [
        r"\bi (decided|did|built|wrote|led|created|negotiated|shipped|coded|hired|coached|designed|implemented|fixed|resolved|managed|organized|proposed|initiated)\b",
        r"\bmy (approach|first step|solution|decision) was\b",
        r"\bso i (reached out|set up|drafted|called|scheduled|reviewed|analyzed)\b",
    ],
    "R": [
        r"\b(\d+\s*%|\$\s*\d+[kmb]?)\b",
        r"\b(reduced|increased|improved|grew|saved|cut|delivered|achieved|exceeded|reached|completed) (by|to|from)?\b",
        r"\b(the (result|outcome|impact|effect) was)\b",
        r"\b(as a result|in the end|ultimately|we (ended up|achieved|hit|delivered))\b",
    ],
}


def check(answer: str) -> dict:
    flags: dict[str, bool] = {}
    for component, patterns in CUES.items():
        flags[component] = any(re.search(p, answer, re.IGNORECASE) for p in patterns)

    text_lower = " " + answer.lower() + " "
    has_we = bool(re.search(r"\bwe\b", text_lower))
    has_i = bool(re.search(r"\bi\b", text_lower))
    flags["pronoun_we_only"] = has_we and not has_i
    flags["complete"] = all(flags[k] for k in "STAR")
    return flags


if __name__ == "__main__":
    data = json.load(sys.stdin)
    output = [{"q": item["question"], **check(item["answer"])} for item in data]
    json.dump(output, sys.stdout, indent=2)
    print()

    incomplete = [o for o in output if not o["complete"]]
    if incomplete:
        print(f"\n{len(incomplete)} answer(s) missing STAR components:", file=sys.stderr)
        for o in incomplete:
            missing = [c for c in "STAR" if not o[c]]
            print(f"  Q: {o['q'][:60]}... → missing: {missing}", file=sys.stderr)
        sys.exit(1)
