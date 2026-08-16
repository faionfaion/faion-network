# Resource Management

## Summary

**One-sentence:** Plan to 70% utilisation (not 100%), map skills to tasks from YAML roster in git, level resource load via critical-path analysis, track allocations weekly against actuals.

**One-paragraph:** Plan to 70% utilisation (not 100%), map skills to tasks from YAML roster in git, level resource load via critical-path analysis, track allocations weekly against actuals. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-resource-management.py` enforces the output contract.

**Ефективно для:**

- Programs with shared resources across multiple projects.
- PMO capacity planning across teams.
- Skill-matrix-based assignment when work demands specific competencies.
- Detection of over-allocation hot spots before they slip schedules.

## Applies If (ALL must hold)

- Roster (people × skills × availability) is available.
- Tasks have effort estimates + critical-path knowledge.
- Weekly allocation tracking is feasible.

## Skip If (ANY kills it)

- Single dedicated team with no shared resources.
- Roster not maintained — fix data quality first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource roster | YAML (person × skills × availability) | PMO / HR |
| Task effort estimates | hours per task | PM |
| Critical path | list of tasks | scheduler |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | effort estimates feed resource demand |
| [[team-development]] | skills matrix is the per-team feed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-utilisation` | haiku | Mechanical: hours assigned / hours available. |
| `level-load` | sonnet | Judgement: which task to defer to relieve over-allocation. |
| `flag-skill-gaps` | haiku | Mechanical: task requires skill X, no person has X. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-check.py` | Capacity check: roster + tasks → per-person utilisation + over-allocation flags |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[cost-estimation]]
- [[team-development]]
- [[scrum-ceremonies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capacity-check.py`

```python
"""capacity_check.py — flag overloaded resources per ISO week.

Usage:
  python capacity_check.py resources/roster.yaml resources/allocations.yaml
  python capacity_check.py resources/roster.yaml resources/allocations.yaml 0.75

roster.yaml shape:
  resources:
    - id: alice
      name: Alice Chen
      hours_per_week: 40

allocations.yaml shape:
  allocations:
    - resource_id: alice
      weeks:
        "2026-W17": 38
        "2026-W18": 42

Exit 0 = all within threshold, exit 1 = overloads found.
"""

import sys
from collections import defaultdict

import yaml
import pathlib


def main(roster_path: str, alloc_path: str, threshold: float = 0.85) -> int:
    roster = {
        r["id"]: r
        for r in yaml.safe_load(pathlib.Path(roster_path).read_text())["resources"]
    }
    allocations = yaml.safe_load(pathlib.Path(alloc_path).read_text())["allocations"]

    load: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for alloc in allocations:
        for week, hours in alloc["weeks"].items():
            load[alloc["resource_id"]][week] += hours

    over: list[tuple[str, str, str, float]] = []
    for rid, weeks in load.items():
        if rid not in roster:
            continue
        capacity = roster[rid]["hours_per_week"]
        for week, hours in weeks.items():
            ratio = hours / capacity
            if ratio > threshold:
                over.append((rid, roster[rid]["name"], week, ratio))

    for rid, name, week, ratio in sorted(over, key=lambda x: (-x[3], x[2])):
        sys.stdout.write(f"OVERLOAD  {rid:<12}  {name:<25}  {week}  {ratio*100:.0f}%\n")

    if over:
        sys.stderr.write(f"\n{len(over)} overload(s) found (threshold {threshold*100:.0f}%)\n")
        return 1
    sys.stdout.write("All resources within capacity threshold.\n")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        sys.stderr.write("Usage: capacity_check.py <roster.yaml> <allocations.yaml> [threshold]\n")
        sys.exit(2)
    threshold = float(args[2]) if len(args) > 2 else 0.85
    sys.exit(main(args[0], args[1], threshold))
```
