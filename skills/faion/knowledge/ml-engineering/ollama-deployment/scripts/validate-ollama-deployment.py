#!/usr/bin/env python3
"""validate-ollama-deployment.py — validate an output artefact against the ollama-deployment contract.

Inputs:
  path  Path to a JSON artefact emitted by the methodology.

Outputs:
  stdout: human-readable violation list (empty on pass).
  exit 0 on pass, 1 on schema violation, 2 on usage error.

Flags:
  --help        Show this message.
  --self-test   Run an in-process smoke test using the built-in fixture.

Exit codes:
  0 — valid
  1 — schema violations
  2 — usage error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED = ['slug', 'version', 'date', 'produces', 'signature', 'payload', 'forbidden_seen']
PAYLOAD_REQUIRED = ['env', 'keys']
SLUG = 'ollama-deployment'
PRODUCES = 'config'
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEX16_RE = re.compile(r"^[0-9a-f]{16}$")


def expected_signature(doc: dict) -> str:
    raw = f"{doc.get('slug', '')}{doc.get('version', '')}{doc.get('date', '')}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    if doc.get("slug") != SLUG:
        errs.append(f"slug mismatch: expected {SLUG!r}, got {doc.get('slug')!r}")
    if "version" in doc and not SEMVER_RE.match(str(doc["version"])):
        errs.append(f"version not semver: {doc.get('version')!r}")
    if "date" in doc and not DATE_RE.match(str(doc["date"])):
        errs.append(f"date not ISO-8601: {doc.get('date')!r}")
    if doc.get("produces") != PRODUCES:
        errs.append(f"produces mismatch: expected {PRODUCES!r}, got {doc.get('produces')!r}")
    sig = str(doc.get("signature", ""))
    if not HEX16_RE.match(sig):
        errs.append(f"signature not 16 hex chars: {sig!r}")
    elif sig != expected_signature(doc):
        errs.append(f"signature mismatch: expected {expected_signature(doc)!r}, got {sig!r}")
    fs = doc.get("forbidden_seen")
    if fs is None:
        errs.append("missing forbidden_seen array")
    elif not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif len(fs) > 0:
        errs.append(f"forbidden_seen non-empty: {fs}")
    payload = doc.get("payload")
    if not isinstance(payload, dict):
        errs.append("payload missing or not an object")
    else:
        for k in PAYLOAD_REQUIRED:
            if k not in payload:
                errs.append(f"payload.{k} missing")
    return errs


SMOKE = {'slug': 'ollama-deployment', 'version': '1.0.0', 'date': '2026-05-22', 'produces': 'config', 'signature': '94c78c7fd9f816c5', 'payload': {'env': 'prod', 'keys': {'timeout': 30}}, 'forbidden_seen': []}


def main() -> int:
    parser = argparse.ArgumentParser(description=f"Validate {SLUG} output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test with a built-in fixture.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            print("self-test failed:", errs, file=sys.stderr)
            return 1
        print("self-test ok")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2

    try:
        doc = json.loads(p.read_text())
    except Exception as e:
        print(f"json parse error: {e}", file=sys.stderr)
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            print(e)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
