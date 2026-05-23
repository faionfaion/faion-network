#!/usr/bin/env python3
"""validate-prompt-basics.py — Validate a rendered PromptTemplate messages array.

Inputs:
  - <messages.json>  Path to a JSON file containing the messages array.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - messages array validates.
  1 - violates output contract.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in valid + invalid fixtures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROLES = {"system", "user", "assistant"}

VALID_FIXTURE = [
    {"role": "system", "content": "You are a sentiment classifier. Respond with: positive, negative, or neutral."},
    {"role": "user", "content": "Classify: I love this!"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "Classify: This exceeded expectations."},
]
INVALID_FIXTURE = [{"role": "user", "content": "Write something about AI"}]


def validate(msgs: list) -> list[str]:
    out: list[str] = []
    if not isinstance(msgs, list) or len(msgs) < 2:
        out.append("messages must be array of >= 2 items")
        return out
    if msgs[0].get("role") != "system":
        out.append("first message must be role=system")
    if msgs[0].get("role") == "system" and not (msgs[0].get("content") or "").strip():
        out.append("system content must be non-empty")
    if msgs[-1].get("role") != "user":
        out.append("last message must be role=user")
    examples = [m for m in msgs[1:-1] if m.get("role") in ("user", "assistant")]
    fewshot_pairs = len(examples) // 2
    if fewshot_pairs > 5:
        out.append(f"too many few-shot pairs ({fewshot_pairs}); max 5")
    for i, m in enumerate(msgs):
        if not isinstance(m, dict):
            out.append(f"messages[{i}] not object")
            continue
        if m.get("role") not in ROLES:
            out.append(f"messages[{i}].role must be in {sorted(ROLES)}")
        c = m.get("content")
        if not isinstance(c, str) or not c.strip():
            out.append(f"messages[{i}].content must be non-empty string")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if any(a in ("--help", "-h") for a in argv) else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        msgs = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(msgs)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
