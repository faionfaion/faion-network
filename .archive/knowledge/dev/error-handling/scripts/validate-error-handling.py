#!/usr/bin/env python3
"""validate-error-handling.py — validate an HTTP error response against the ProblemDetails schema.

Usage:
    validate-error-handling.py --body response.json --content-type application/problem+json --status 400
    validate-error-handling.py --self-test

Inputs:
    --body PATH              path to JSON response body file
    --content-type STRING    actual response Content-Type header
    --status INT             actual HTTP status code (used to verify body.status match)
Outputs: stdout JSON {ok, violations:[...]}
Exit codes: 0 = pass, 1 = violations found, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["type", "title", "status"],
    "additionalProperties": True,
    "properties": {
        "type": {"type": "string"},
        "title": {"type": "string"},
        "status": {"type": "integer", "minimum": 100, "maximum": 599},
        "detail": {"type": "string"},
        "instance": {"type": "string"},
        "traceId": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["field", "code", "message"],
                "properties": {
                    "field": {"type": "string"},
                    "code": {"type": "string"},
                    "message": {"type": "string"},
                },
            },
        },
    },
}

LEAK_TOKENS = ("Traceback", "OperationalError", "psycopg2", "sqlalchemy.exc", "java.lang.", "at /opt/")


def validate(body: dict, content_type: str, http_status: int) -> list[dict]:
    violations: list[dict] = []
    if not content_type.startswith("application/problem+json"):
        violations.append({"rule": "r2", "message": f"content-type {content_type!r}, expected application/problem+json"})
    for key in ("type", "title", "status"):
        if key not in body:
            violations.append({"rule": "r1", "message": f"missing required key {key!r}"})
    if "status" in body and body["status"] != http_status:
        violations.append({"rule": "r3", "message": f"body.status={body['status']} != http_status={http_status}"})
    if "traceId" not in body or not body.get("traceId"):
        violations.append({"rule": "r4", "message": "traceId missing or empty"})
    if http_status >= 500:
        detail = body.get("detail", "") or ""
        for tok in LEAK_TOKENS:
            if tok in detail:
                violations.append({"rule": "r5", "message": f"5xx detail leaks internals: contains {tok!r}"})
    if "errors" in body and not (400 <= http_status < 500):
        violations.append({"rule": "r6", "message": "errors[] present on non-4xx response"})
    try:
        import jsonschema

        jsonschema.validate(body, SCHEMA)
    except ImportError:
        pass
    except Exception as e:
        violations.append({"rule": "schema", "message": str(e)})
    return violations


def self_test() -> int:
    good = {"type": "https://x/y", "title": "Bad Request", "status": 400, "traceId": "abc"}
    bad = {"type": "https://x/y", "title": "Oops", "status": 500, "traceId": "abc",
           "detail": "Traceback (most recent call last)"}
    v_good = validate(good, "application/problem+json", 400)
    assert not v_good, f"good case should pass: {v_good}"
    v_bad = validate(bad, "application/json", 500)
    rules = {x["rule"] for x in v_bad}
    assert "r2" in rules and "r5" in rules, f"bad case must flag r2+r5: {v_bad}"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--body", type=Path)
    ap.add_argument("--content-type", default="")
    ap.add_argument("--status", type=int, default=0)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.body or not args.content_type or not args.status:
        ap.error("--body, --content-type, --status required (or use --self-test)")
        return 2
    body = json.loads(args.body.read_text(encoding="utf-8"))
    violations = validate(body, args.content_type, args.status)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
