# Affinity Diagramming

## Summary

**One-sentence:** Cluster atomic interview insights into named themes via affinity diagramming — produces a labelled cluster board with size + confidence per cluster.

**One-paragraph:** Interview transcripts produce 30–200 atomic insights per cycle. Without clustering, themes drift across stakeholders. Affinity diagramming pins the synthesis: each atomic insight is one card, cards are grouped by similarity (silent sort), groups are labelled, and labels carry size (card count) + confidence (sources × recency). Output: a labelled cluster board feeding the opportunity tree, with explicit 'orphan' bucket for un-clusterable cards.

**Ефективно для:**

- Solo researcher synthesising 5–20 interviews into themes.
- PM whose stakeholders dispute the theme set.
- Founder running discovery without a research lead.
- Team migrating from ad-hoc notes to a cluster-based research deliverable.

## Applies If (ALL must hold)

- ≥30 atomic insights captured.
- Insights are tagged at the atomic card level (one claim per card).
- Downstream consumer reads themes, not raw interviews.
- Operator (or pair) can dedicate ≥2 focused hours.

## Skip If (ANY kills it)

- <30 insights — clustering is premature; collect more.
- Single-stakeholder sync where raw notes suffice.
- Existing tag schema already produces cluster-like output.
- Team disputes basic segment definitions — resolve segments first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Atomic insight cards | Miro / FigJam / md | insight-evidence-card-template |
| Tagging schema | controlled vocabulary | interview-insight-tagging-schema |
| Segment map | list of named segments | research plan |
| Synthesis surface (board) | Miro / FigJam / paper | operator setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/insight-evidence-card-template` | card shape consumed as input |
| `solo/research/interview-insight-tagging-schema` | tag categories used during cluster naming |

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
| `draft-affinity-diagramming` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/affinity-diagramming.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/affinity-diagramming.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-affinity-diagramming.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[insight-evidence-card-template]]`
- `[[interview-insight-tagging-schema]]`
- `[[interview-hot-take-template]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
