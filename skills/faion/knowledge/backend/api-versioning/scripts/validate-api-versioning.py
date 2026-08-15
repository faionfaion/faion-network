#!/usr/bin/env python3
"""validate-api-versioning.py

Validate the artefact produced by the api-versioning methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('spec_id', 'decision', 'rationale',)
ENUMS: dict[str, list] = {
    'decision': ['additive', 'create_v_next', 'skip'],
    'scheme': ['url-path', 'accept-header', 'header-key'],
}
PUBLIC_WINDOW_DAYS = 90


def _major(version: object) -> int | None:
    """Parse 'v2' / '2' / '2.1.0' into its major integer; None if unparseable."""
    text = str(version or "").lstrip("vV")
    head = text.split(".")[0]
    try:
        return int(head)
    except ValueError:
        return None


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")

    # Cross-field checks. A create_v_next decision is the breaking path, so it
    # must actually raise the major and must carry a long enough window.
    if obj.get("decision") == "create_v_next":
        from_major = _major(obj.get("from_version"))
        to_major = _major(obj.get("to_version"))
        if from_major is None or to_major is None:
            errs.append("from_version and to_version must be parseable as vN (additive-first)")
        elif to_major <= from_major:
            errs.append("breaking change requires a major version bump (additive-first)")
        window = obj.get("deprecation_window_days")
        if isinstance(window, int) and window < PUBLIC_WINDOW_DAYS:
            errs.append(
                f"deprecation_window_days must be >= {PUBLIC_WINDOW_DAYS} for a public API "
                "(deprecation-window-declared)"
            )
        if obj.get("deprecation_date") and obj.get("sunset_date") and \
                str(obj["sunset_date"]) <= str(obj["deprecation_date"]):
            errs.append("sunset_date must fall after deprecation_date (deprecation-window-declared)")
    return errs


OK = {'spec_id': 'openapi.yaml', 'decision': 'create_v_next', 'scheme': 'url-path', 'from_version': 'v1', 'to_version': 'v2', 'deprecation_date': '2026-06-01', 'sunset_date': '2026-12-01', 'deprecation_window_days': 183, 'rationale': 'Removed email_verified field; breaking diff ids: response-property-removed.', 'breaking_diff_ids': ['response-property-removed']}
BAD = {'decision': 'BUMP', 'from_version': '1'}
BAD_WINDOW = {'spec_id': 'openapi.yaml', 'decision': 'create_v_next', 'from_version': 'v1', 'to_version': 'v1', 'deprecation_window_days': 30, 'rationale': 'Breaking change shipped without a major bump.'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    errs_window = validate(BAD_WINDOW)
    if not errs_window:
        sys.stderr.write("self-test FAIL: BAD_WINDOW fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-api-versioning.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
