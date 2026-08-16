# Opportunity Solution Trees

## Summary

**One-sentence:** Builds and maintains a Torres-style OST with one outcome at the root, opportunities scored on freq x sev x addressability, and solutions branching only off opportunities with falsifiable assumptions.

**One-paragraph:** Authoring + maintenance methodology for Opportunity Solution Trees (Teresa Torres). One outcome at the root; opportunities (unmet user needs) branch off; solutions (only) branch off opportunities, each carrying at least one falsifiable assumption test. Scoring is numeric (frequency x severity x addressability) with week-over-week deltas. Lives as YAML in .aidocs/product_docs/discovery/opportunity-solution-tree.md.

**Ефективно для:**

- Свіжий продукт без discovery infra - треба завести OST.
- Discovery працює, але без єдиного root outcome - треба зафіксувати метрику.
- Накопичились opportunities без рангу - треба numeric scoring.
- Solutions з'являлись без opportunities - треба rewire.
- Monthly review: pruning + kill list для OST.

## Applies If (ALL must hold)

- Fresh product with no discovery infrastructure; OST is being stood up.
- Discovery is running but no single root outcome was ever pinned.
- Opportunity backlog grew without ranking; numeric scoring is needed.
- Solutions appeared without parent opportunities; tree must be rewired.
- Monthly review: pruning + kill list maintenance.

## Skip If (ANY kills it)

- Pre-PMF with no users to interview.
- Hardware / regulated medical where solution iteration is months, not weeks.
- Crisis mode (outage / churn cliff) - skip OST hygiene; do root-cause first.
- OST already healthy with <30 nodes and active pruning.
- Team rejects continuous discovery framing; pick a different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Root outcome metric | name + current value + target | product strategy |
| Existing opportunities (or empty) | markdown / YAML | discovery output |
| Open assumptions register | markdown | previous cycle |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[continuous-discovery]] | supplies the cadence that feeds opportunities into the OST |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-opportunities` | sonnet | Apply freq x sev x addr scoring with deltas. |
| `rewire-orphans` | sonnet | Move dangling solutions under correct opportunities. |
| `prune` | sonnet | Identify dead branches; emit kill list. |
| `audit-falsifiable` | haiku | Mechanical check: every solution has a falsifiable assumption. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | Canonical OST YAML structure (outcome -> opportunities -> solutions -> assumptions) |
| `templates/ost-render.sh` | Render OST YAML to a Markdown tree visualisation |
| `templates/ost-audit-checklist.md.j2` | OST hygiene audit (8 binary checks) |
| `templates/ost-audit-checklist.md` | OST hygiene audit (8 binary checks) Generated from `templates/ost-audit-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-opportunity-solution-trees.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[continuous-discovery]]
- [[persona-building]]
- [[risk-assessment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ost.yaml`

```yaml
# ost.yaml — canonical agent-friendly OST schema
# Source of truth for the tree; Miro/Vistaly/FigJam are render targets only.
# All passes read and write this file. Use stable IDs for all nodes.

outcome:
  id: O-1
  metric: "Activation rate W1"
  target: "30% to 45% by Q3"

opportunities:
  - id: OP-1
    parent: O-1
    statement: "New users can't tell what to do first after signup"
    evidence: [INT-04, INT-09, TKT-211]  # interview/ticket IDs — min 2 required
    sizing:
      reach: high
      impact: high
      confidence: med
    status: open  # open | tested | parked | killed

solutions:
  - id: S-1
    parent: OP-1
    statement: "Interactive 3-step product tour"
    assumption_types: [desirability, usability]
  - id: S-2
    parent: OP-1
    statement: "Templated starter project on first login"
    assumption_types: [desirability, feasibility]
  - id: S-3
    parent: OP-1
    statement: "Contextual tooltip overlay on empty states"
    assumption_types: [usability, technical]

experiments:
  - id: E-1
    parent: S-1
    type: prototype-test
    riskiest_assumption: "users will complete a 3-step tour without abandoning"
    success_metric: "60% or more complete all 3 steps"
    falsifier: "less than 40% complete — drop S-1"
    status: open
```

### `templates/ost-render.sh`

```bash
#!/usr/bin/env bash
# ost-render.sh — convert ost.yaml to Mermaid diagram and render to SVG
# Requires: yq, jq, mmdc (npm i -g @mermaid-js/mermaid-cli)
# Usage: ./ost-render.sh [ost.yaml] [output.svg]
set -euo pipefail

INPUT="${1:-ost.yaml}"
OUTPUT="${2:-ost.svg}"
MMD="$(mktemp /tmp/ost-XXXX.mmd)"

yq -o=json "$INPUT" | jq -r '
  "graph TD",
  (.outcome | "O[\(.id): \(.metric | gsub(" "; "_"))]"),
  (.opportunities[] | "O --> \(.id)[\(.statement | gsub(" "; "_") | .[0:40])]"),
  (.solutions[] | "\(.parent) --> \(.id)((\(.statement | gsub(" "; "_") | .[0:30])))"),
  (.experiments[] | "\(.parent) --> \(.id)>\(.type)]")
' > "$MMD"

mmdc -i "$MMD" -o "$OUTPUT"
rm -f "$MMD"
echo "Rendered: $OUTPUT"
```
