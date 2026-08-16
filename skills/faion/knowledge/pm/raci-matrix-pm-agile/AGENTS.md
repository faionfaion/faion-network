# RACI Matrix

## Summary

**One-sentence:** Generic cross-functional RACI matrix assigning exactly one of R / A / C / I per stakeholder per task, with one Accountable per row and explicit C-vs-I discipline.

**One-paragraph:** RACI Matrix defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Cross-functional initiative with >=3 disciplines (eng / design / marketing / ops).
- Recurring confusion about 'who owns this' or 'who should I tell'.
- PM running an audit before a milestone with multiple gates.
- Onboarding new lead who needs the accountability map for the program.

## Applies If (ALL must hold)

- Tasks / deliverables can be enumerated (rows of the matrix).
- Stakeholders can be enumerated (columns of the matrix).
- A lead exists who can ratify ambiguous assignments.
- Authority to publish + maintain the RACI is granted.

## Skip If (ANY kills it)

- Solo work — RACI is not meaningful with one person.
- Highly volatile scope where tasks rotate weekly — RACI rots within the cycle.
- Use launch-raci-template for launches specifically; this generic RACI is for ongoing work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-matrix_template_fill` | haiku | Bounded template fill, no judgement. |
| `raci-matrix_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `raci-matrix_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the RACI matrix artefact. |
| `templates/raci-template.md.j2` | Markdown skeleton for the RACI matrix table. |
| `templates/raci-template.md` | Markdown skeleton for the RACI matrix table. Generated from `templates/raci-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/raci-lint.py` | Reference script enforcing one-A-per-row + non-empty R. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/raci-matrix.json",
  "type": "object",
  "required": [
    "matrix_id",
    "program_id",
    "tasks",
    "stakeholders",
    "assignments",
    "lead",
    "review_due"
  ],
  "properties": {
    "matrix_id": {
      "type": "string"
    },
    "program_id": {
      "type": "string"
    },
    "tasks": {
      "type": "array",
      "minItems": 1
    },
    "stakeholders": {
      "type": "array",
      "minItems": 2
    },
    "assignments": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "task",
          "R",
          "A"
        ],
        "properties": {
          "task": {
            "type": "string"
          },
          "R": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string"
            }
          },
          "A": {
            "type": "string"
          },
          "C": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "I": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    },
    "lead": {
      "type": "string"
    },
    "review_due": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/raci-lint.py`

```python
"""


"""raci-lint.py — validate a Markdown RACI table from stdin.

Rules enforced:
  - Exactly one A per task row
  - At least one R per task row
  - Maximum 3 C per task row

Exit 0 if valid, exit 1 if violations found.

Usage:
    python3 raci-lint.py < RACI.md
    cat RACI.md | python3 raci-lint.py
"""
from __future__ import annotations

import sys


def main() -> int:
    text = sys.stdin.read()
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("|") and "---" not in line
    ]
    if len(rows) < 2:
        print("No RACI table found in input.", file=sys.stderr)
        return 2

    # Skip header row
    violations: list[str] = []
    for row in rows[1:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 2:
            continue
        task = cells[0]
        vals = cells[1:]

        a_count = sum(1 for v in vals if "A" in v)
        r_count = sum(1 for v in vals if "R" in v)
        c_count = sum(1 for v in vals if v.strip() == "C")

        if a_count != 1:
            violations.append(f"Row '{task}': A_count={a_count} (must be exactly 1)")
        if r_count < 1:
            violations.append(f"Row '{task}': no R assigned")
        if c_count > 3:
            violations.append(f"Row '{task}': too many C ({c_count}, max 3)")

    if violations:
        for v in violations:
            print(v)
        return 1

    print("RACI table is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
