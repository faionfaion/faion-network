#!/usr/bin/env python3
"""validate-csharp-aspnet-core.py — validate csharp-aspnet-core output against the 02-output-contract schema.

Flags:
  --help        Print usage and exit (provided by argparse).
  --self-test   Run an internal fixture-based smoke test and exit.

Exit codes:
  0 — input passes the schema and forbidden-pattern checks.
  1 — input fails; violations printed to stderr.
  2 — usage / file error.

Inputs:
  - Positional: path to JSON file to validate, OR `--self-test`.

Outputs:
  - stdout: "ok" on pass.
  - stderr: one violation per line on fail.

Dependencies: stdlib only.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ['artefact_id', 'owner', 'file_path', 'language', 'build_passes', 'tests_passing', 'rules_checked', 'version', 'last_reviewed']
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
ID_RE = re.compile(r"^[a-z][a-z0-9-]+$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}

# Optional design_profile block (02-output-contract.xml). When present, every
# field is pinned by the core rule named in the comment.
DESIGN_PROFILE_REQUIRED = (
    'layering', 'dbcontext_lifetime', 'cancellation_token_propagated',
    'error_format', 'dto_kind', 'time_provider', 'test_db_strategy',
    'pagination', 'loading', 'transactions',
)
DESIGN_PROFILE_EXPECTED = {
    'dbcontext_lifetime': 'scoped',                  # dbcontext-scoped-lifetime
    'cancellation_token_propagated': True,           # cancellation-token-threaded
    'error_format': 'problem-details-rfc7807',       # problem-details-error-contract
    'dto_kind': 'record',                            # record-dtos-at-boundary
    'time_provider': True,                           # timeprovider-injected
    'test_db_strategy': 'testcontainers',            # testcontainers-not-ef-inmemory
    'pagination': 'keyset',                          # keyset-pagination
    'loading': 'eager-include',                      # eager-include-no-lazy-loading
    'transactions': 'explicit',                      # explicit-transaction-multi-step-writes
}
DESIGN_PROFILE_LAYERING = {'controller-service-repository', 'vertical-slice'}


def _validate_design_profile(profile: object) -> list[str]:
    """Check the optional design_profile block against the pinned rule values."""
    if not isinstance(profile, dict):
        return ["design_profile must be a JSON object"]
    violations: list[str] = []
    for key in DESIGN_PROFILE_REQUIRED:
        if key not in profile:
            violations.append(f"design_profile missing required key: {key}")
    layering = profile.get("layering")
    if layering is not None and layering not in DESIGN_PROFILE_LAYERING:
        violations.append(
            f"design_profile.layering must be one of {sorted(DESIGN_PROFILE_LAYERING)}: {layering!r}"
        )
    for key, expected in DESIGN_PROFILE_EXPECTED.items():
        if key in profile and profile[key] != expected:
            violations.append(
                f"design_profile.{key} must be {expected!r}, got {profile[key]!r}"
            )
    return violations


def validate(doc: dict) -> list[str]:
    violations: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be a JSON object"]
    for key in REQUIRED:
        if key not in doc:
            violations.append(f"missing required key: {key}")
    if "design_profile" in doc:
        violations.extend(_validate_design_profile(doc["design_profile"]))
    owner = (doc.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        violations.append(f"forbidden owner value: {owner!r} (must be named human or role-with-rotation)")
    artefact_id = doc.get("artefact_id", "")
    if artefact_id and not ID_RE.match(artefact_id):
        violations.append(f"artefact_id does not match pattern ^[a-z][a-z0-9-]+$: {artefact_id!r}")
    version = doc.get("version", "")
    if version and not SEMVER.match(version):
        violations.append(f"version not semver: {version!r}")
    return violations


def self_test() -> int:
    good = {
        "artefact_id": "sample-2026-q2",
        "owner": "ruslan@faion.net",
        "version": "1.0.0",
        "last_reviewed": "2026-05-23",
    }
    # Populate required keys with placeholders for self-test.
    for key in REQUIRED:
        good.setdefault(key, "x")
    v = validate(good)
    if v:
        print(f"self-test FAIL on valid doc: {v}", file=sys.stderr)
        return 1
    bad = {"artefact_id": "BAD ID", "owner": "team", "version": "draft"}
    v = validate(bad)
    if not v:
        print("self-test FAIL: invalid doc passed", file=sys.stderr)
        return 1
    # design_profile: complete + compliant block must pass, non-compliant must fail.
    good_profile = dict(good)
    good_profile["design_profile"] = {
        "layering": "controller-service-repository",
        "dbcontext_lifetime": "scoped",
        "cancellation_token_propagated": True,
        "error_format": "problem-details-rfc7807",
        "dto_kind": "record",
        "time_provider": True,
        "test_db_strategy": "testcontainers",
        "pagination": "keyset",
        "loading": "eager-include",
        "transactions": "explicit",
    }
    v = validate(good_profile)
    if v:
        print(f"self-test FAIL on compliant design_profile: {v}", file=sys.stderr)
        return 1
    bad_profile = dict(good_profile)
    bad_profile["design_profile"] = dict(good_profile["design_profile"],
                                         dbcontext_lifetime="singleton",
                                         loading="lazy")
    if not validate(bad_profile):
        print("self-test FAIL: non-compliant design_profile passed", file=sys.stderr)
        return 1
    print("self-test ok")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="validate-csharp-aspnet-core.py",
        description="Validate csharp-aspnet-core output against 02-output-contract schema. Exit 0 on pass, 1 on fail, 2 on usage error.",
    )
    p.add_argument("path", nargs="?", help="Path to JSON file to validate")
    p.add_argument("--self-test", action="store_true", help="Run an internal fixture-based smoke test and exit")
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.path:
        p.print_help(sys.stderr)
        return 2
    try:
        doc = json.loads(Path(args.path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"json parse error: {e}", file=sys.stderr)
        return 1
    violations = validate(doc)
    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
