# Requirement Quality Scorecard

## Summary

**One-sentence:** Deterministic scorecard for every requirement before baseline: atomicity, testability, traceability, value, ambiguity, completeness — 0/1/2 per axis with rules.

**One-paragraph:** Requirement Quality Scorecard pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource engagements where BA hands written requirements to a foreign delivery team.
- AI-assisted drafting workflows where consistency drifts fast.
- Regulated engagements where requirement-quality is auditable.
- Migration engagements where legacy requirements must be re-baselined.

## Applies If (ALL must hold)

- BA writes or reviews requirements that will be baselined.
- Engagement contains AI-assisted requirement drafting (where consistency drifts fast).
- There is a recurring pattern of requirements bouncing back from QA or engineering.
- Sponsor expects an objective requirement-quality signal.

## Skip If (ANY kills it)

- Engagement is too small for formal scoring (under 20 requirements).
- Requirements are not baselined — pure exploratory write-up.
- Team has a different formal quality model (e.g. EARS-only) already in use.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements draft | markdown / yaml / DOORS | BA repo |
| Traceability target (test plan / design) | csv / matrix | BA toolkit |
| Acceptance criteria template | markdown | Team standard |
| Glossary (canonical terms) | yaml | Project glossary |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-requirement-quality-scorecard` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirement-quality-scorecard.md` | Markdown rubric template with scoring axes + thresholds |
| `templates/requirement-quality-scorecard.schema.json` | JSON Schema for the structured rubric output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirement-quality-scorecard.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
