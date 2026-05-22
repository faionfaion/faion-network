#!/usr/bin/env python3
"""validate-vector-db-setup-dev.py — validate dev-setup.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["db_kind", "image_tag", "data_volume", "client_version", "smoke_passed", "gitignore_entries"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    tag = obj.get("image_tag", "")
    if tag.endswith(":latest"):
        errs.append("image_tag must not end with :latest (r1-pin-image-version)")
    if not obj.get("data_volume"):
        errs.append("data_volume required (r2-persistent-volume)")
    if obj.get("smoke_passed") is not True:
        errs.append("smoke_passed must be true (r4-smoke-test)")
    return errs


FIXTURE_VALID = """
db_kind: qdrant
image_tag: "qdrant/qdrant:v1.10.0"
data_volume: "./qdrant_storage"
client_version: "qdrant-client==1.10.0"
smoke_passed: true
gitignore_entries: ["qdrant_storage/"]
"""

FIXTURE_INVALID = """
db_kind: qdrant
image_tag: "qdrant/qdrant:latest"
data_volume: ""
client_version: "qdrant-client==0.9"
smoke_passed: false
gitignore_entries: []
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
    ap = argparse.ArgumentParser(prog="validate-vector-db-setup-dev", description=__doc__,
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
