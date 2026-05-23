# Product Explainability (PM Angle)

## Summary

**One-sentence:** PM-side communication discipline producing one canonical feature narrative (problem -> behaviour change -> outcome) and audience-specific renders for execs / sales / support / customers.

**One-paragraph:** One canonical narrative artefact owned by PM containing {problem, who, behaviour_change, outcome_metric, evidence_link}; derived audience renders never authored independently; 90-second test for brevity + clarity; outcome line is a customer-state change, not a feature-shipped statement. Output: feature-narrative YAML + per-audience renders.

**Ефективно для:**

- Pre-roadmap review: exec питає 'що цей продукт robi?', три PM відповідають по-різному.
- Pre-launch story prep для sales/support/customer-success без Loom.
- Board narrative: 6 місяців роботи у 90-секундну відповідь.
- Cross-team feature-to-impact mapping: який OKR/outcome зрушив.

## Applies If (ALL must hold)

- Pre-roadmap-review: an exec asks 'what does this product actually do?' and three PMs answer differently.
- Pre-launch story prep for sales/support/customer-success.
- Board / investor / all-hands narrative distilling work into a 90-second answer.
- Cross-team feature-to-impact mapping.
- Post-mortem on miscommunication where customer expected X, got Y.

## Skip If (ANY kills it)

- Infra-only release with no customer-visible change.
- Pre-launch where canonical narrative belongs to GTM, not PM.
- Pure internal-tool product with no external customer narrative needed.
- Stage so early no behaviour change yet observable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Verbatim user quotes | list | continuous-discovery output |
| Outcome metric | string + baseline | product-analytics |
| Audience inventory | list {exec, sales, support, customer} | stakeholder-management |
| Feature spec | markdown | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[continuous-discovery-habits]] | Supplies verbatim quotes grounding the evidence link. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: one canonical, derived renders, evidence link, 90-second test, outcome-not-feature | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for feature-narrative | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: three-versions, independent-renders, evidence-free, feature-as-outcome | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: extract -> author canonical -> render audiences -> 90s test -> publish | 800 |
| `content/05-examples.xml` | medium | Worked feature-narrative for a checkout-redesign release | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on customer-visibility + audience count | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `story-extract` | sonnet | Extract narrative from spec/research. |
| `audience-render` | haiku | Templated per-audience render derived from canonical. |
| `ninety-second-test` | haiku | Mechanical brevity + clarity check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-narrative.yaml` | Canonical feature-narrative skeleton. |
| `templates/feature-narrative-gate.sh` | Gate script enforcing 90s + outcome-not-feature. |
| `templates/prompt-audience-render.txt` | Audience-render prompt template. |
| `templates/prompt-story-extraction.txt` | Story-extraction prompt template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-explainability.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[continuous-discovery-habits]]
- [[stakeholder-management]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
