# Idea Generation Methods

## Summary

**One-sentence:** Bundle of four complementary pre-validation methods (7P framework, PG four questions, pain-point mining, 5-dimension niche matrix) producing a scored candidate list for downstream validation.

**One-paragraph:** Different ideation moments need different methods. This bundle pins four complementary frameworks: (1) 7P (Pain / Passion / Profession / Process / Platform / People / Product), (2) Paul Graham's four diagnostic questions, (3) systematic pain-point mining (complaint audit + workaround inventory), (4) 5-dimension niche scoring matrix. Output: a candidate list with the source method per candidate, the diagnostic answers, and a scored matrix for the top 5 — feeding niche-evaluation downstream.

**Ефективно для:**

- Operator who already ran skills-inventory ideation and needs a different angle.
- Founder evaluating a pivot vs a new product.
- Indie builder wanting a method beyond 'brainstorm with LLM'.
- PM auditing an existing roadmap against the PG four questions.

## Applies If (ALL must hold)

- Operator can answer the 7P prompts honestly (passion, profession, etc).
- ≥1 pain-point source is available (complaints, Reddit threads, support tickets).
- Downstream scoring step is committed (niche-evaluation).
- Operator has ≥2 hours to run one full bundle pass.

## Skip If (ANY kills it)

- No pain-point source available — collect signals first.
- Operator wants a single-method run — pick one (idea-generation) instead of the bundle.
- Scoring matrix is contested between operator and stakeholder — resolve weights first.
- Operator already has a validated MVP — skip to pricing or validation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 7P prompts answered | md | operator self-assessment |
| PG four questions answered | md | operator self-assessment |
| Pain-point inventory | csv / md | complaint audit / Reddit / tickets |
| 5-dimension scoring matrix template | csv / md | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/idea-generation` | the upstream 7-framework ideation that this bundle extends |
| `solo/research/market-researcher/niche-evaluation` | downstream scoring rubric |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-idea-generation-methods` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idea-generation-methods.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/idea-generation-methods.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-idea-generation-methods.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[idea-generation]]`
- `[[niche-evaluation]]`
- `[[pain-point-research]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
