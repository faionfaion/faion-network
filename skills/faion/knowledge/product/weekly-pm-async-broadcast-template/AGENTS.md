# Weekly PM Async Broadcast Template

## Summary

**One-sentence:** Pins a Monday async PM update format (problem/decision/next-step + named owner) so weekly broadcasts decay into a reviewable artefact, not a Slack scroll.

**One-paragraph:** Solo and small-team PMs need a repeatable async-update format that survives the week without re-deriving rationale. The methodology fixes a one-page weekly broadcast: pinned context, decisions made this week (each with one named input), open questions, next-step block, and an explicit owner. The artefact is versioned, sponsor-signed, and reviewed alongside the roadmap. Stops broadcasts from becoming opinion-streams and gives downstream consumers a stable shape to diff week-over-week.

**Ефективно для:**

- Solo PM losing Monday on roadmap restatement.
- Founder running async-only product team.
- PM whose stakeholders re-litigate the same questions every week.
- Indie operator coordinating contractors via Slack.

## Applies If (ALL must hold)

- Team runs an async-first product cadence (no daily standup).
- PM (or operator) signs off on weekly written broadcasts.
- Downstream consumers (eng, sales, support) read the broadcast.
- ≥3 decisions surface per week worth pinning.

## Skip If (ANY kills it)

- Team is fully sync (daily standup) and broadcast is redundant.
- Operator has <3 decisions per week to report — write inline notes.
- Regulated channel that mandates a different broadcast template.
- Last week's broadcast still represents the current state — link, do not redo.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last-week broadcast | md / Notion / wiki | broadcast log |
| Decisions made this week | list with named input per item | decision log |
| Open questions surface | list | stakeholder threads |
| Named owner handle | string | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/pm/solo-weekly-cadence-template` | cadence shape feeding this broadcast |

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
| `draft-weekly-pm-async-broadcast-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-pm-async-broadcast-template.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/weekly-pm-async-broadcast-template.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-pm-async-broadcast-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[solo-weekly-cadence-template]]`
- `[[anti-roadmap-template]]`
- `[[discovery-research-handoff-template]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
