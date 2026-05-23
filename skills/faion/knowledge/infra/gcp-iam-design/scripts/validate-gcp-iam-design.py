#!/usr/bin/env python3
"""validate-gcp-iam-design.py — F-066 output-contract validator for `gcp-iam-design`.

Validates a config artefact (JSON / YAML / Markdown front-matter) against the
schema declared in content/02-output-contract.xml. Stdlib + pyyaml optional.

Inputs:
    --file PATH       artefact to validate (json / yaml / markdown with YAML front-matter)
    --self-test       run built-in fixtures
    --help            print this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable / parse error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["principal", "role", "scope", "condition"]
FORBIDDEN_PATTERNS = ["T" + "BD", "FIX" + "ME", "TO" + "DO"]  # constructed to avoid self-trip on grep


def parse_artefact(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() in (".json",):
        return json.loads(text)
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError:
            sys.stderr.write("pyyaml required for yaml inputs\n")
            sys.exit(2)
        return yaml.safe_load(text) or {}
    if path.suffix.lower() in (".md", ".markdown"):
        # Extract YAML front-matter
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end > 0:
                try:
                    import yaml  # type: ignore
                except ImportError:
                    sys.stderr.write("pyyaml required for markdown front-matter\n")
                    sys.exit(2)
                return yaml.safe_load(text[3:end]) or {}
        # Fallback: treat as section-headers
        out: dict = {}
        cur_key = None
        cur_val: list[str] = []
        for line in text.splitlines():
            if line.startswith("## "):
                if cur_key is not None:
                    out[cur_key] = "\n".join(cur_val).strip()
                cur_key = line[3:].strip()
                cur_val = []
            elif cur_key is not None:
                cur_val.append(line)
        if cur_key is not None:
            out[cur_key] = "\n".join(cur_val).strip()
        return out
    raise ValueError(f"unsupported extension: {path.suffix}")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object/mapping"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        else:
            v = obj[k]
            if isinstance(v, str):
                for fp in FORBIDDEN_PATTERNS:
                    if fp in v:
                        errs.append(f"forbidden placeholder '{fp}' in field {k}")
    return errs


OK_FIXTURE = {"principal": "example-principal", "role": "example-role", "scope": "example-scope", "condition": "example-condition"}
BAD_FIXTURE = {"_invalid": "missing-required"}


def self_test() -> int:
    rc = 0
    if validate(OK_FIXTURE):
        sys.stderr.write("self-test: OK fixture wrongly rejected\n")
        rc = 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("self-test: BAD fixture wrongly accepted\n")
        rc = 1
    if rc == 0:
        sys.stdout.write("self-test OK\n")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = parse_artefact(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
