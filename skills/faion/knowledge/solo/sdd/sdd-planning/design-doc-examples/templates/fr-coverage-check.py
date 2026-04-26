"""
fr-coverage-check.py

Verify every FR-X from spec.md appears in design.md's FR Coverage table.

Usage:
    python fr-coverage-check.py spec.md design.md

Output:
    Dict with spec_frs, design_frs, missing_in_design, coverage_pct
"""

import re
import sys


def check_fr_coverage(spec_text: str, design_text: str) -> dict:
    """Return coverage report: which FRs are in spec but missing from design."""
    spec_frs = set(re.findall(r"FR-\d+", spec_text))
    design_frs = set(re.findall(r"FR-\d+", design_text))
    missing = spec_frs - design_frs
    coverage_pct = (
        round(len(design_frs & spec_frs) / len(spec_frs) * 100)
        if spec_frs
        else 100
    )
    return {
        "spec_frs": sorted(spec_frs),
        "design_frs": sorted(design_frs),
        "missing_in_design": sorted(missing),
        "coverage_pct": coverage_pct,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fr-coverage-check.py spec.md design.md")
        sys.exit(1)

    spec_path, design_path = sys.argv[1], sys.argv[2]

    with open(spec_path) as f:
        spec_text = f.read()
    with open(design_path) as f:
        design_text = f.read()

    result = check_fr_coverage(spec_text, design_text)
    print(f"Coverage: {result['coverage_pct']}%")
    if result["missing_in_design"]:
        print(f"Missing in design: {', '.join(result['missing_in_design'])}")
        sys.exit(1)
    else:
        print("All FRs covered.")
