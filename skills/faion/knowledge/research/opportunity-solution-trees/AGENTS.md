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
| `templates/ost-audit-checklist.md` | OST hygiene audit (8 binary checks) |

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
