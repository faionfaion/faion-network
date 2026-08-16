# PM Framework Focus Areas

## Summary

**One-sentence:** ADR mapping a project's lifecycle into PMBOK 8 method-agnostic Focus Areas (Initiating, Planning, Executing, Monitoring & Controlling, Closing) with chosen practices per area.

**One-paragraph:** PM Framework Focus Areas defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- PMO standardising vocabulary across teams running mixed methods (Scrum, Kanban, Predictive).
- Project coaches who want a single ADR per project naming the practices in each area.
- Audit / compliance environments that map deliverables to lifecycle phases.
- Onboarding new leads who need a structured map of 'where we are' in the lifecycle.

## Applies If (ALL must hold)

- Project lifecycle is enumerable (start date + planned phases or release plan).
- An ADR owner exists who can ratify the chosen practices per area.
- Team has agreed on the practice set per area before drafting the ADR.
- At least two of the five focus areas have concrete practices already in flight.

## Skip If (ANY kills it)

- Project lifecycle is too volatile to commit to focus-area practices (research/exploration).
- Team rejects PMBOK 8 vocabulary entirely — switch to a method-specific framework.
- Single-person project — focus-area scaffolding is overhead without benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pm-framework-focus-areas_template_fill` | haiku | Bounded template fill, no judgement. |
| `pm-framework-focus-areas_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `pm-framework-focus-areas_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the focus-areas ADR artefact. |
| `templates/scaffold_focus_areas.sh` | Shell helper that scaffolds an empty ADR markdown for the 5 focus areas. |
| `templates/adr-skeleton.md.j2` | Markdown skeleton ADR listing the 5 focus areas with practice tables. |
| `templates/adr-skeleton.md` | Markdown skeleton ADR listing the 5 focus areas with practice tables. Generated from `templates/adr-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

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
  "$id": "https://faion.net/schemas/pm-framework-focus-areas.json",
  "type": "object",
  "required": [
    "adr_id",
    "project_id",
    "focus_areas",
    "decision_owner",
    "review_due"
  ],
  "properties": {
    "adr_id": {
      "type": "string"
    },
    "project_id": {
      "type": "string"
    },
    "focus_areas": {
      "type": "object",
      "required": [
        "initiating",
        "planning",
        "executing",
        "monitoring_and_controlling",
        "closing"
      ],
      "additionalProperties": {
        "type": "object",
        "required": [
          "practices"
        ],
        "properties": {
          "practices": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": [
                "name",
                "evidence"
              ]
            }
          }
        }
      }
    },
    "decision_owner": {
      "type": "string"
    },
    "review_due": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/scaffold_focus_areas.sh`

```bash
# scaffold_focus_areas.sh — Create a docs/ tree with one folder and default
# artifacts per PMBOK 8 focus area.
#
# Usage: ./scaffold_focus_areas.sh [root-dir]
# Default root-dir: docs
#
# Output: folder tree under <root-dir>/ with placeholder files.
set -euo pipefail

ROOT="${1:-docs}"
mkdir -p "$ROOT"

for fa in initiating planning executing monitoring-controlling closing; do
    d="$ROOT/$fa"
    mkdir -p "$d"
    case "$fa" in
        initiating)
            files=(charter.md vision.md stakeholder-register.md)
            ;;
        planning)
            files=(spec.md design.md risk-register.md plan.md)
            ;;
        executing)
            files=(decisions.md status-reports/.gitkeep)
            ;;
        monitoring-controlling)
            files=(metrics.md change-log.md burn-up.md)
            ;;
        closing)
            files=(lessons-learned.md acceptance.md final-report.md)
            ;;
    esac
    for f in "${files[@]}"; do
        mkdir -p "$(dirname "$d/$f")"
        touch "$d/$f"
    done
done

echo "Scaffolded focus areas under $ROOT/"
```
