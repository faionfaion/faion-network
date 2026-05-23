#!/usr/bin/env python3
"""validate-tool-use-function-calling.py — validate tools.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["version", "tools", "audit_sink"]
SAFETY = {"read-only", "mutating", "destructive"}
NAME_RE = re.compile(r"^[a-z][a-z0-9_]+$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    audit = obj.get("audit_sink")
    if not isinstance(audit, dict) or "kind" not in audit or "location" not in audit:
        errs.append("audit_sink.kind + audit_sink.location required (r5-audit-every-call)")
    tools = obj.get("tools", [])
    if not isinstance(tools, list) or not tools:
        errs.append("tools must be non-empty list")
        return errs
    for t in tools:
        if not isinstance(t, dict):
            continue
        name = t.get("name", "")
        if not NAME_RE.match(name):
            errs.append(f"tool name invalid: {name}")
        sch = t.get("args_schema", {})
        if not isinstance(sch, dict) or sch.get("type") != "object" or "properties" not in sch:
            errs.append(f"tool {name}.args_schema missing type=object+properties (r1-typed-schema)")
        sc = t.get("safety_class")
        if sc not in SAFETY:
            errs.append(f"tool {name}.safety_class must be in {sorted(SAFETY)} (r3-side-effect-class)")
        if sc == "destructive" and not t.get("human_gate"):
            errs.append(f"tool {name} destructive requires human_gate=true (r4-human-gate-irreversible)")
        if t.get("rate_limit_per_minute", 0) < 1:
            errs.append(f"tool {name}.rate_limit_per_minute >= 1 required")
    return errs


FIXTURE_VALID = """
version: 1.0.0
audit_sink: {kind: clickhouse, location: ch://x}
tools:
  - name: lookup_customer
    description: "Returns customer record by ID. No side effects."
    safety_class: read-only
    rate_limit_per_minute: 60
    args_schema: {type: object, properties: {customer_id: {type: string}}, required: [customer_id]}
"""

FIXTURE_INVALID = """
version: 1.0.0
audit_sink: {}
tools:
  - name: BadName
    description: "x"
    safety_class: destructive
    rate_limit_per_minute: 0
    args_schema: {}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-tool-use-function-calling", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
