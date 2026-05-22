#!/usr/bin/env python3
"""Validate a django-quality-logging audit report against its JSON Schema.

Inputs:
    path to a Markdown file whose YAML frontmatter must validate against the
    schema embedded in content/02-output-contract.xml.

Outputs:
    stdout: PASS or list of violations.
    exit 0 on pass, 1 on any violation.

Exit codes:
    0 -- validation passed
    1 -- validation failed (or file unreadable / missing frontmatter)
    2 -- invalid CLI usage

Dependencies: stdlib + pyyaml (already required by faion-network scripts).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - documented requirement
    sys.stderr.write("pyyaml is required: pip install pyyaml\n")
    sys.exit(2)


SCHEMA = {
    "required": [
        "methodology",
        "target_repo",
        "django_version",
        "python_version",
        "structlog_status",
        "sentry_status",
        "check_deploy_verdict",
        "findings",
    ],
    "methodology": "django-quality-logging",
    "structlog_required": ["installed", "middleware_registered", "json_renderer", "issues"],
    "sentry_required": [
        "dsn_present",
        "traces_sample_rate",
        "send_default_pii",
        "before_send_present",
    ],
    "verdicts": {"pass", "warning", "error"},
    "severities": {"error", "warning", "info"},
    "rule_ids": {
        "r1-structlog",
        "r2-sentry",
        "r3-llm-context",
        "r4-no-print",
        "r5-no-debug-sql",
    },
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def validate(report: dict) -> list[str]:
    errors: list[str] = []
    for key in SCHEMA["required"]:
        if key not in report:
            errors.append(f"missing required key: {key}")
    if report.get("methodology") != SCHEMA["methodology"]:
        errors.append(f"methodology must be {SCHEMA['methodology']!r}")
    structlog = report.get("structlog_status") or {}
    for key in SCHEMA["structlog_required"]:
        if key not in structlog:
            errors.append(f"structlog_status missing key: {key}")
    sentry = report.get("sentry_status") or {}
    for key in SCHEMA["sentry_required"]:
        if key not in sentry:
            errors.append(f"sentry_status missing key: {key}")
    rate = sentry.get("traces_sample_rate")
    if rate is not None and not (0 <= rate <= 1):
        errors.append(f"traces_sample_rate out of [0,1]: {rate}")
    if report.get("check_deploy_verdict") not in SCHEMA["verdicts"]:
        errors.append(f"check_deploy_verdict invalid: {report.get('check_deploy_verdict')!r}")
    findings = report.get("findings") or []
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            errors.append(f"finding[{i}] must be an object")
            continue
        for key in ("rule_id", "severity", "file", "line", "fix"):
            if key not in f:
                errors.append(f"finding[{i}] missing key: {key}")
        if f.get("rule_id") not in SCHEMA["rule_ids"]:
            errors.append(f"finding[{i}].rule_id invalid: {f.get('rule_id')!r}")
        if f.get("severity") not in SCHEMA["severities"]:
            errors.append(f"finding[{i}].severity invalid: {f.get('severity')!r}")
    return errors


def self_test() -> int:
    good = {
        "methodology": "django-quality-logging",
        "target_repo": "owner/repo",
        "django_version": "5.2",
        "python_version": "3.12",
        "structlog_status": {
            "installed": True,
            "middleware_registered": True,
            "json_renderer": True,
            "issues": [],
        },
        "sentry_status": {
            "dsn_present": True,
            "traces_sample_rate": 0.1,
            "send_default_pii": False,
            "before_send_present": True,
        },
        "check_deploy_verdict": "pass",
        "findings": [],
    }
    assert validate(good) == []
    bad = dict(good)
    bad["sentry_status"] = {**good["sentry_status"], "traces_sample_rate": 1.5}
    assert validate(bad), "expected violation on traces_sample_rate=1.5"
    sys.stdout.write("self-test: PASS\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", help="path to audit report Markdown file")
    parser.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.report:
        parser.print_usage()
        return 2
    path = Path(args.report)
    if not path.is_file():
        sys.stderr.write(f"not a file: {path}\n")
        return 1
    text = path.read_text()
    fm = extract_frontmatter(text)
    if fm is None:
        sys.stderr.write("no YAML frontmatter found\n")
        return 1
    errors = validate(fm)
    if errors:
        sys.stdout.write("FAIL\n")
        for e in errors:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
