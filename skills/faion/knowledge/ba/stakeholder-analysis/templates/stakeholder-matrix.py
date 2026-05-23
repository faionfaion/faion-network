#!/usr/bin/env python3
"""stakeholder-matrix.py — validate YAML register and emit Mermaid quadrant chart.

Input: stakeholders/register.yaml with structure:
  stakeholders:
    - id: S-01
      name: "Name"
      influence: H|M|L
      impact: H|M|L
      attitude: "+|0|-|unknown"

Output: Mermaid quadrantChart to stdout (pipe to mmdc or embed in docs).
Validation errors go to stderr; exit 1 if errors found.

Usage: python stakeholder-matrix.py [register.yaml]
"""
from __future__ import annotations

import sys
import pathlib

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

LEVELS = {"H": 0.85, "M": 0.55, "L": 0.20}
QUADRANT = {
    ("H", "H"): "Manage Closely",
    ("H", "L"): "Keep Satisfied",
    ("L", "H"): "Keep Informed",
    ("L", "L"): "Monitor",
}


def norm_quadrant(infl: str, impact: str) -> str:
    i = "H" if infl == "H" else "L"
    p = "H" if impact == "H" else "L"
    return QUADRANT[(i, p)]


def main(path_str: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path_str).read_text())
    errors: list[str] = []

    print("quadrantChart")
    print("    title Influence vs Impact")
    print("    x-axis Low Impact --> High Impact")
    print("    y-axis Low Influence --> High Influence")
    print("    quadrant-1 Manage Closely")
    print("    quadrant-2 Keep Satisfied")
    print("    quadrant-3 Monitor")
    print("    quadrant-4 Keep Informed")

    for s in data.get("stakeholders", []):
        sid = s.get("id", "?")
        infl = s.get("influence")
        imp = s.get("impact")
        att = s.get("attitude", "unknown")

        if infl not in LEVELS or imp not in LEVELS:
            errors.append(f"{sid}: invalid influence={infl!r} or impact={imp!r}")
            continue

        if att == "unknown":
            label = f"{sid} {s.get('name', '?')} [?]"
        else:
            label = f"{sid} {s.get('name', '?')} [{att}]"

        x = LEVELS[imp]
        y = LEVELS[infl]
        print(f'    "{label}": [{x:.2f}, {y:.2f}]')
        s["quadrant"] = norm_quadrant(infl, imp)

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "stakeholders/register.yaml"))
