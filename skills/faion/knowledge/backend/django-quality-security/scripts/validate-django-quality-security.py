#!/usr/bin/env python3
"""Validate a django-quality-security audit report against its JSON Schema.

Inputs:
    path to Markdown audit report.

Outputs:
    stdout: PASS or list of violations.
    exit 0 on pass, 1 on fail, 2 on bad CLI.

Dependencies: stdlib + pyyaml.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("pyyaml required\n")
    sys.exit(2)


REQUIRED_TOP = (
    "methodology",
    "target_repo",
    "django_version",
    "https_baseline",
    "rate_limits",
    "input_validation",
    "secrets",
    "check_deploy_verdict",
    "findings",
)
RULE_IDS = {
    "r1-https-headers",
    "r2-rate-limits",
    "r3-input-validation",
    "r4-specific-exceptions",
    "r5-secrets",
}
CSP_MODES = {"off", "report-only", "enforce"}
VERDICTS = {"pass", "warning", "error"}
SEVERITIES = {"error", "warning", "info"}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    return yaml.safe_load(m.group(1)) if m else None


def _check_section(report, name, required_keys, errors):
    section = report.get(name)
    if not isinstance(section, dict):
        errors.append(f"{name} must be an object")
        return
    for k in required_keys:
        if k not in section:
            errors.append(f"{name} missing key: {k}")


def validate(report: dict) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED_TOP:
        if k not in report:
            errors.append(f"missing required key: {k}")
    if report.get("methodology") != "django-quality-security":
        errors.append("methodology must be 'django-quality-security'")
    _check_section(
        report,
        "https_baseline",
        ("debug_false", "ssl_redirect", "hsts_seconds", "csp_mode", "cookie_secure"),
        errors,
    )
    https = report.get("https_baseline") or {}
    hsts = https.get("hsts_seconds")
    if hsts is not None and (not isinstance(hsts, int) or hsts < 0):
        errors.append("hsts_seconds must be a non-negative integer")
    if https.get("csp_mode") is not None and https["csp_mode"] not in CSP_MODES:
        errors.append(f"csp_mode invalid: {https['csp_mode']!r}")
    _check_section(
        report,
        "rate_limits",
        ("auth_endpoints_throttled", "axes_installed", "stacked_libraries"),
        errors,
    )
    _check_section(
        report,
        "input_validation",
        ("all_inputs_validated", "raw_sql_findings", "file_upload_magic_check"),
        errors,
    )
    _check_section(report, "secrets", ("env_loaded", "secret_key_default_check", "sentry_scrubber"), errors)
    if report.get("check_deploy_verdict") not in VERDICTS:
        errors.append(f"check_deploy_verdict invalid: {report.get('check_deploy_verdict')!r}")
    findings = report.get("findings") or []
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            errors.append(f"finding[{i}] must be an object")
            continue
        for k in ("rule_id", "severity", "file", "line", "fix"):
            if k not in f:
                errors.append(f"finding[{i}] missing key: {k}")
        if f.get("rule_id") not in RULE_IDS:
            errors.append(f"finding[{i}].rule_id invalid: {f.get('rule_id')!r}")
        if f.get("severity") not in SEVERITIES:
            errors.append(f"finding[{i}].severity invalid: {f.get('severity')!r}")
    return errors


def self_test() -> int:
    good = {
        "methodology": "django-quality-security",
        "target_repo": "owner/repo",
        "django_version": "5.2",
        "https_baseline": {
            "debug_false": True,
            "ssl_redirect": True,
            "hsts_seconds": 31536000,
            "csp_mode": "enforce",
            "cookie_secure": True,
        },
        "rate_limits": {
            "auth_endpoints_throttled": True,
            "axes_installed": True,
            "stacked_libraries": False,
        },
        "input_validation": {
            "all_inputs_validated": True,
            "raw_sql_findings": 0,
            "file_upload_magic_check": True,
        },
        "secrets": {"env_loaded": True, "secret_key_default_check": True, "sentry_scrubber": True},
        "check_deploy_verdict": "pass",
        "findings": [],
    }
    assert validate(good) == []
    bad = {**good, "https_baseline": {**good["https_baseline"], "csp_mode": "maybe"}}
    assert validate(bad)
    sys.stdout.write("self-test: PASS\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?")
    parser.add_argument("--self-test", action="store_true")
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
    fm = extract_frontmatter(path.read_text())
    if fm is None:
        sys.stderr.write("no YAML frontmatter\n")
        return 1
    errs = validate(fm)
    if errs:
        sys.stdout.write("FAIL\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
