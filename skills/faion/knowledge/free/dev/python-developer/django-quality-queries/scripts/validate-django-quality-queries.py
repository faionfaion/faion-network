#!/usr/bin/env python3
"""Validate a django-quality-queries audit report against its JSON Schema.

Inputs:
    path to a Markdown file whose YAML frontmatter must validate against the
    schema embedded in content/02-output-contract.xml.

Outputs:
    stdout: PASS or list of violations.
    exit 0 on pass, 1 on any violation.

Exit codes:
    0 -- validation passed
    1 -- validation failed
    2 -- invalid CLI usage

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
    sys.stderr.write("pyyaml is required: pip install pyyaml\n")
    sys.exit(2)


REQUIRED = (
    "methodology",
    "target_repo",
    "endpoints_audited",
    "n_plus_one_count",
    "indexes_recommended",
    "tests_added",
    "findings",
)
RULE_IDS = {
    "r1-select-related",
    "r2-prefetch-related",
    "r3-bulk-ops",
    "r4-indexes",
    "r5-assertnumqueries",
}
SEVERITIES = {"error", "warning", "info"}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    return yaml.safe_load(m.group(1)) if m else None


def validate(report: dict) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED:
        if k not in report:
            errors.append(f"missing required key: {k}")
    if report.get("methodology") != "django-quality-queries":
        errors.append("methodology must be 'django-quality-queries'")
    for k in ("endpoints_audited", "n_plus_one_count", "indexes_recommended", "tests_added"):
        v = report.get(k)
        if v is not None and (not isinstance(v, int) or v < 0):
            errors.append(f"{k} must be a non-negative integer")
    findings = report.get("findings") or []
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            errors.append(f"finding[{i}] must be an object")
            continue
        for k in ("rule_id", "severity", "file", "line", "fix", "before_queries", "after_queries"):
            if k not in f:
                errors.append(f"finding[{i}] missing key: {k}")
        if f.get("rule_id") not in RULE_IDS:
            errors.append(f"finding[{i}].rule_id invalid: {f.get('rule_id')!r}")
        if f.get("severity") not in SEVERITIES:
            errors.append(f"finding[{i}].severity invalid: {f.get('severity')!r}")
        for k in ("line", "before_queries", "after_queries"):
            v = f.get(k)
            if v is not None and (not isinstance(v, int) or v < 0):
                errors.append(f"finding[{i}].{k} must be a non-negative integer")
    return errors


def self_test() -> int:
    good = {
        "methodology": "django-quality-queries",
        "target_repo": "owner/repo",
        "endpoints_audited": 5,
        "n_plus_one_count": 1,
        "indexes_recommended": 1,
        "tests_added": 1,
        "findings": [
            {
                "rule_id": "r1-select-related",
                "severity": "error",
                "file": "views.py",
                "line": 42,
                "fix": "move to selector with select_related",
                "before_queries": 1001,
                "after_queries": 3,
            }
        ],
    }
    assert validate(good) == []
    bad = dict(good, n_plus_one_count=-1)
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
