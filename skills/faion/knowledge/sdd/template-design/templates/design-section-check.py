"""
design-section-check.py

Verify design.md has all required sections, count ADs, and check FR traceability.

Usage:
    python design-section-check.py design.md

Exit codes:
    0 — all checks pass
    1 — one or more checks failed
"""

import re
import sys


REQUIRED_SECTIONS = [
    "## Reference Documents",
    "## Overview",
    "## Architecture Decisions",
    "## Components",
    "## Data Flow",
    "## Files",
    "## Testing Strategy",
    "## Risks",
    "## FR Coverage",
]


def check_design_sections(design_text: str) -> list[str]:
    """Return list of missing required sections."""
    return [s for s in REQUIRED_SECTIONS if s not in design_text]


def count_ads(design_text: str) -> int:
    """Count AD entries (### AD-N: patterns)."""
    return len(re.findall(r"^### AD-\d+", design_text, re.MULTILINE))


def check_fr_traceability(design_text: str) -> list[str]:
    """Return list of AD-X blocks missing 'Traces to' field."""
    ad_blocks = re.findall(
        r"(### AD-\d+.*?)(?=### AD-\d+|\Z)", design_text, re.DOTALL
    )
    missing_traces = []
    for block in ad_blocks:
        ad_id_match = re.search(r"AD-\d+", block)
        if ad_id_match and "Traces to" not in block:
            missing_traces.append(ad_id_match.group())
    return missing_traces


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python design-section-check.py design.md")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        design_text = f.read()

    failed = False

    missing = check_design_sections(design_text)
    if missing:
        print(f"MISSING SECTIONS: {missing}")
        failed = True

    ad_count = count_ads(design_text)
    print(f"AD count: {ad_count}")
    if ad_count < 1:
        print("WARNING: no ADs found — typical features have 3-7 ADs")

    missing_traces = check_fr_traceability(design_text)
    if missing_traces:
        print(f"ADs missing 'Traces to': {missing_traces}")
        failed = True

    if not failed:
        print("All checks passed.")
    sys.exit(1 if failed else 0)
