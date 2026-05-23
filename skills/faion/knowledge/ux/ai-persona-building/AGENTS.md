# AI Persona Building (Single-Pass)

## Summary

**One-sentence:** Produces a lightweight single-pass persona report (Sonnet + Haiku) for early exploration when full clustering is overkill, with explicit not-validated labelling.

**One-paragraph:** Early ideation often needs directional personas before the budget exists for full research. Single-pass agent generation (Sonnet for structure + Haiku for detail) is cheap and fast but produces unvalidated output. This methodology produces a persona report explicitly labelled not-validated, with each persona showing source-data references (analytics segments, secondary research) and a 'validation required before product decision' flag — so downstream consumers do not mistake it for the two-pass validated report.

**Ефективно для:** founder / PM на pre-research phase, що потребує 3–5 directional personas за годину для discovery, не для рішень.

## Applies If (ALL must hold)

- Pre-research ideation phase: directional personas needed before research budget exists.
- Source data is secondary (analytics segments, market reports) — not primary interviews.
- Output is explicitly not used for product decisions without validation.

## Skip If (ANY kills it)

- Personas will drive product decisions — use [[ai-assisted-persona-building]] two-pass instead.
- Primary research data exists — two-pass methodology has higher ROI.
- Stakeholders may treat single-pass output as final — process not strong enough to prevent misuse.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Analytics segments / secondary research | JSON / CSV | data team |
| Industry context brief | markdown | PM |
| Persona count target (3–5) | integer | PM |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-assisted-persona-building]] | Upgrade path for validated personas. |
| [[synthetic-users]] | Companion ideation tool. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-report` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/persona-report.json` | JSON skeleton: personas + validated + use_for + next_step. |
| `templates/prompt-sonnet-scaffold.txt` | Sonnet prompt for persona scaffold pass. |
| `templates/prompt-haiku-detail.txt` | Haiku prompt for detail pass. |
| `templates/_smoke-test.json` | Filled discovery-phase persona report. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-persona-building.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-assisted-persona-building]]
- [[synthetic-users]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
