#!/usr/bin/env python3
# vui-utterance-lint.py — flag verbose or unnatural system utterances
# Input (stdin): JSON {"turns":[{"role":"system"|"user","text":"..."},...]}
# Output: per-turn issues; exits 1 if any found, 0 if clean
import json
import re
import sys

MAX_CHARS = 120
MAX_CLAUSES = 2  # commas + semicolons + 1

FILLER = re.compile(
    r"\b(I'?d be happy to|Just to confirm|I have successfully|Currently|"
    r"I'm so sorry|As an AI|Please note that)\b",
    re.I,
)
TERMINAL = re.compile(r"[?.!]$")


def lint(text: str) -> list[str]:
    issues: list[str] = []
    if len(text) > MAX_CHARS:
        issues.append(f"too-long:{len(text)}chars")
    clauses = text.count(",") + text.count(";") + 1
    if clauses > MAX_CLAUSES:
        issues.append(f"too-many-clauses:{clauses}")
    m = FILLER.search(text)
    if m:
        issues.append(f"filler:{m.group()!r}")
    if not TERMINAL.search(text.strip()):
        issues.append("missing-terminal-punctuation")
    return issues


def main() -> int:
    data = json.load(sys.stdin)
    issues_found = False
    for i, turn in enumerate(data.get("turns", [])):
        if turn.get("role") == "system":
            problems = lint(turn["text"])
            if problems:
                print(f"turn {i}: {problems}  → {turn['text'][:60]!r}")
                issues_found = True
    if not issues_found:
        print("OK: all system utterances pass lint")
    return 1 if issues_found else 0


if __name__ == "__main__":
    sys.exit(main())
