# Niche Evaluation (Market Researcher)

## Summary

**One-sentence:** Six-step framework producing a niche-evaluation report: niche one-sentence formula, TAM/SAM/SOM with cited sources, competitor matrix, audience accessibility, monetization, and personal fit.

**One-paragraph:** After idea-generation, operators struggle to evaluate which niche is worth pursuing. This methodology pins a six-step report: (1) one-sentence niche formula ('[audience] who do [job] when [trigger]'), (2) TAM/SAM/SOM with cited sources, (3) competitor matrix (quality × number-of-players), (4) audience accessibility (channels + cost-to-reach), (5) monetization potential (price × volume signal), (6) personal fit (skills + interest + cycle). Output: a scored report with a single GO/PASS/PIVOT verdict.

**Ефективно для:**

- Solopreneur with 3–5 candidate niches needing a defensible pick.
- Indie operator pre-MVP wanting to size a target market.
- Founder evaluating a pivot into an adjacent niche.
- Researcher producing a niche-evaluation report for stakeholder review.

## Applies If (ALL must hold)

- Candidate niche(s) named — ≥1 specific niche to evaluate.
- Operator can cite at least two market sources (industry report, public data).
- Competitor list ≥3 can be assembled.
- Operator has 2–4 focused hours per niche.

## Skip If (ANY kills it)

- Niche is undefined — run idea-generation first.
- Operator wants intuition-driven choice — methodology cannot help.
- Niche is regulated and operator is unwilling to research compliance — defer.
- Three previous evaluations failed and operator is fatigued — switch methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate niche definition | 1 sentence + audience tag | ideation output |
| Industry sources | URLs to reports / public data | research |
| Competitor list | csv (name + URL + price + segment) | competitor scan |
| Operator skills + cycle | self-assessment | operator brief |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/idea-generation` | upstream candidate list this evaluates |
| `solo/research/market-researcher/pricing-research` | monetization estimates feed scoring |

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
| `draft-niche-evaluation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/niche-evaluation.md.j2` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/niche-evaluation.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml Generated from `templates/niche-evaluation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/niche-evaluation.schema.json` | JSON Schema seed + filled fixture for the report artefact |
| `templates/niche-scorecard.md.j2` | 5-factor weighted niche scorecard (market size, competition, accessibility, monetization, personal fit) with a decision band. |
| `templates/niche-scorecard.md` | 5-factor weighted niche scorecard (market size, competition, accessibility, monetization, personal fit) with a decision band. Generated from `templates/niche-scorecard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `[[idea-generation]]`
- `[[pricing-research]]`
- `[[naming-and-domains]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/niche-evaluation.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Niche Evaluation (Market Researcher) engagement",
  "rules_applied": [
    "REPLACE-WITH-RULE-ID"
  ],
  "evidence": [
    {
      "rule_id": "REPLACE-WITH-RULE-ID",
      "citation": "REPLACE-WITH-VERIFIABLE-CITATION",
      "source_type": "url"
    }
  ],
  "output_payload": {
    "status": "draft"
  },
  "consumer": "REPLACE-WITH-NAMED-CONSUMER",
  "owner": "REPLACE-WITH-NAMED-OWNER",
  "last_touched": "2026-05-23T10:00:00Z"
}
```
