#!/usr/bin/env python3
"""validate-spec.py — check required sections, FR-to-AC traceability, and measurable goals.

Input:  path to a Markdown spec file
Output: FAIL lines per violation, exits 1 if any found.
"""
import re
import sys


REQUIRED_SECTIONS = [
    "## Overview",
    "## Problem",
    "## Goals",
    "## Non-Goals",
    "## User Stories",
    "## Requirements",
    "## Acceptance Criteria",
    "## Out of Scope",
    "## Open Questions",
]


def validate(path: str) -> list[str]:
    text = open(path).read()
    errs: list[str] = []

    for sect in REQUIRED_SECTIONS:
        if sect not in text:
            errs.append(f"missing section: {sect}")

    frs = set(re.findall(r"\bFR-\d+\b", text))
    ac_lines = [
        ln for ln in text.splitlines()
        if any(kw in ln for kw in ("Given", "When ", "Then "))
    ]
    ac_refs = set(re.findall(r"\bFR-\d+\b", "\n".join(ac_lines)))
    orphans = frs - ac_refs
    if orphans:
        errs.append(f"FRs without acceptance criteria: {sorted(orphans)}")

    if not re.search(r"^\| Metric \| Current \| Target \|", text, re.M):
        errs.append("missing measurable success metrics table (Metric | Current | Target)")

    if re.search(r"\bNon-Goals\b", text):
        ngsect = re.search(
            r"## Non-Goals\s*(.*?)(?=\n##|\Z)", text, re.S
        )
        if ngsect and ngsect.group(1).strip() in ("", "- none", "- None"):
            errs.append("Non-Goals section is empty — explicitly list what is excluded")

    if re.search(r"\bOpen Questions\b", text):
        oqsect = re.search(
            r"## Open Questions\s*(.*?)(?=\n##|\Z)", text, re.S
        )
        if oqsect and len(oqsect.group(1).strip()) < 10:
            errs.append("Open Questions section appears empty — list unknowns explicitly")

    impl_hints = re.findall(
        r"\b(schema:|table name|SELECT |ALTER TABLE|import |require\(|\.py|\.js|<div|className)",
        text,
    )
    if impl_hints:
        errs.append(f"possible implementation leak — review: {impl_hints[:3]}")

    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-spec.py <spec.md>")
        sys.exit(2)

    errors = validate(sys.argv[1])
    for e in errors:
        print("FAIL:", e)
    sys.exit(1 if errors else 0)
