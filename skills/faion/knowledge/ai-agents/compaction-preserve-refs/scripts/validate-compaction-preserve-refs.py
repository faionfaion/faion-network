#!/usr/bin/env python3
"""validate-compaction-preserve-refs.py

Purpose:
    Validate a compacted-state YAML against the schema declared in
    ../content/02-output-contract.xml.

Inputs:
    --file PATH          YAML file to validate (omit when using --self-test)
    --self-test          Validate the built-in smoke fixture

Outputs:
    Stdout: human-readable validation report
    Exit 0 on pass, 1 on validation failure, 2 on usage error.

Dependencies: stdlib only + pyyaml (optional; falls back to lightweight parser
for the smoke fixture).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_KEYS = {
    "goal",
    "files_touched",
    "decisions",
    "errors_open",
    "refs",
    "next_action",
}
ALLOWED_REF_KINDS = {"pr", "issue", "log", "adr", "url", "ticket"}

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.yaml"


def load_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        # Minimal hand-roll for the smoke fixture: not a real YAML parser.
        out: dict = {}
        current_key: str | None = None
        for raw in text.splitlines():
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            if line.startswith("  - "):
                if current_key is None:
                    continue
                out.setdefault(current_key, []).append(line[4:].strip())
            elif ":" in line and not line.startswith(" "):
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip()
                if val == "":
                    out[key] = []
                    current_key = key
                elif val == "[]":
                    out[key] = []
                    current_key = None
                else:
                    out[key] = val.strip('"').strip("'")
                    current_key = None
        return out


def validate(state: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["root is not a mapping"]

    extra = set(state.keys()) - REQUIRED_KEYS
    if extra:
        errors.append(f"unexpected top-level keys: {sorted(extra)}")
    missing = REQUIRED_KEYS - set(state.keys())
    if missing:
        errors.append(f"missing required keys: {sorted(missing)}")

    for k in ("goal", "next_action"):
        v = state.get(k)
        if not isinstance(v, str) or len(v) < 4:
            errors.append(f"{k}: must be a non-empty string of >= 4 chars")

    for k in ("files_touched", "decisions", "errors_open"):
        v = state.get(k)
        if not isinstance(v, list):
            errors.append(f"{k}: must be a list (use [] for empty)")
            continue
        for i, item in enumerate(v):
            if isinstance(item, str) and item.strip() == "":
                errors.append(f"{k}[{i}]: empty string is not allowed")

    refs = state.get("refs")
    if not isinstance(refs, list):
        errors.append("refs: must be a list")
    else:
        for i, ref in enumerate(refs):
            if isinstance(ref, str):
                # Allow {kind: x, id: y} flow-style strings only if they parse.
                m = re.match(r"\{kind:\s*([a-z]+),\s*id:\s*[\"']?([^\"'}]+)[\"']?\}", ref)
                if not m:
                    errors.append(f"refs[{i}]: not a valid ref object")
                    continue
                kind, id_ = m.group(1), m.group(2)
            elif isinstance(ref, dict):
                kind = ref.get("kind")
                id_ = ref.get("id")
            else:
                errors.append(f"refs[{i}]: must be a mapping with kind+id")
                continue
            if kind not in ALLOWED_REF_KINDS:
                errors.append(f"refs[{i}].kind: {kind!r} not in {sorted(ALLOWED_REF_KINDS)}")
            if not id_:
                errors.append(f"refs[{i}].id: missing")

    if "summary" in state:
        errors.append("forbidden key 'summary' present; this methodology forbids free-text summaries")

    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path, help="YAML compacted state to validate")
    p.add_argument("--self-test", action="store_true", help="Validate the built-in smoke fixture")
    args = p.parse_args(argv)

    if not args.file and not args.self_test:
        p.error("either --file or --self-test must be given")

    target = SMOKE if args.self_test else args.file
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1

    state = load_yaml(target.read_text(encoding="utf-8"))
    errs = validate(state if state is not None else {})
    if errs:
        sys.stdout.write("FAIL\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {target} matches schema (keys={sorted(state.keys())})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
