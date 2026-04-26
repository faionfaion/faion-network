#!/usr/bin/env python3
"""Convert a 5x7 lifecycle matrix YAML into per-focus-area stage-gate checklists.

Input YAML structure:
  cells:
    - focus: Initiating|Planning|Executing|MnC|Closing
      domain: Governance|Scope|Schedule|Finance|Stakeholders|Resources|Risk
      artefact: "name or null"
      owner: "name or UNASSIGNED"
      process_used: "PMBoK process name or tailored"

Output: markdown checklist per focus area on stdout.
"""
import sys
import yaml

FOCUS_ORDER = ["Initiating", "Planning", "Executing", "MnC", "Closing"]
DOMAINS = ["Governance", "Scope", "Schedule", "Finance", "Stakeholders", "Resources", "Risk"]


def main(path):
    data = yaml.safe_load(open(path))
    cells = data["cells"]
    by_focus = {f: [] for f in FOCUS_ORDER}
    for cell in cells:
        if cell.get("artefact") and cell["artefact"] != "null":
            by_focus[cell["focus"]].append(cell)

    for focus in FOCUS_ORDER:
        items = sorted(by_focus[focus], key=lambda x: DOMAINS.index(x["domain"]))
        if not items:
            continue
        print(f"\n## {focus} — Stage Gate Checklist\n")
        for c in items:
            owner = c.get("owner") or "UNASSIGNED"
            proc = c.get("process_used") or "tailored"
            print(f"- [ ] **{c['domain']}** — {c['artefact']}  (owner: {owner}; process: {proc})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: matrix-to-checklist.py lifecycle-matrix.yaml")
    main(sys.argv[1])
