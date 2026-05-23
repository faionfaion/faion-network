# Insight Evidence Card Template

## Summary

**One-sentence:** Pins a single interview insight to a fixed card (claim + evidence count + quote + segment) so synthesis decays into reviewable evidence, not opinion.

**One-paragraph:** Synthesis without an evidence-card format yields opinion-shaped insights stakeholders dismiss. This methodology pins one insight per card: a claim sentence, the count of distinct evidence sources, the strongest verbatim quote, the segment the claim applies to, the confidence band, and the next-action link. Cards live in a flat list, get tagged by tagging-schema, and get aggregated upward into opportunity-tree nodes only when ≥3 evidence sources back the claim.

**Ефективно для:**

- Researcher synthesising 5+ interviews into themes.
- PM whose 'insights' get rejected as 'just opinion' by sales.
- Solo founder running their own discovery research without a research lead.
- Team that wants insight-to-opportunity-tree traceability.

## Applies If (ALL must hold)

- ≥3 interviews completed and transcribed (text or notes).
- Synthesis output will feed an opportunity tree, roadmap, or report.
- Operator can tag each card to a segment.
- Insights need to survive a stakeholder pushback ('show me the evidence').

## Skip If (ANY kills it)

- <3 interviews — defer synthesis until cohort matures.
- Single-stakeholder review only — inline notes suffice.
- Research is internal (process improvement, not product) — use a different shape.
- Insights destined for a one-shot decision, not a tree.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview transcripts or coded notes | md / Dovetail / Notion | research repo |
| Tagging schema for atomic-insight tags | controlled vocabulary | interview-insight-tagging-schema |
| Segment map | list of named segments | research plan |
| Opportunity-tree path | md / Miro / Productboard | research deliverable |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/interview-insight-tagging-schema` | controlled tags feed the card |
| `solo/research/researcher/affinity-diagramming` | upstream synthesis grouping |

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
| `draft-insight-evidence-card-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/insight-evidence-card-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/insight-evidence-card-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-insight-evidence-card-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[interview-insight-tagging-schema]]`
- `[[affinity-diagramming]]`
- `[[interview-hot-take-template]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
