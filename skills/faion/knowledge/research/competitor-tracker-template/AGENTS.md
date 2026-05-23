# Competitor Tracker Template (Solo)

## Summary

**One-sentence:** Monthly competitor matrix + weekly scan schema (channels watched, last delta, action queued) so competitor signal doesn't devolve into noise.

**One-paragraph:** Solo operators check competitors reactively, miss launches, then overreact to noise. This methodology pins the cadence: a monthly matrix (positioning + price + segment + last-major-change), and a weekly scan schema with named channels (pricing page diff, release notes feed, X handle, newsletter, SERP) and a triage rule (delta → action: ignore / log / queue / urgent). Output: a versioned spec living in the research repo and refreshed on the cadence.

**Ефективно для:**

- Solo founder reactive about competitors and easily distracted.
- PM who learns about competitor launches from Reddit two weeks late.
- Indie operator over-pivoting on a single competitor's launch.
- Researcher building a weekly market-signal habit.

## Applies If (ALL must hold)

- ≥3 named competitors are pre-identified.
- Operator can spend ≥30 minutes weekly on the scan.
- Tracker artefact will be referenced in roadmap conversations.
- Operator has a triage habit (ignore vs queue) to apply to deltas.

## Skip If (ANY kills it)

- Operator has fewer than 3 competitors — collect a competitor list first.
- Existing competitive-intelligence tool already runs the scan.
- Operator over-pivots on every competitor delta — fix decision discipline before adding signal.
- Competitor list is in a regulated space requiring counsel-vetted intel only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Competitor list | csv (name + URL + segment + notes) | competitor scan |
| Channel inventory per competitor | list (pricing page + release feed + X + newsletter) | manual setup |
| Tracker template | md / Notion / spreadsheet | this methodology |
| Triage rule sheet | ignore / log / queue / urgent | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/niche-evaluation` | niche definition pins which competitors matter |

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
| `draft-competitor-tracker-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-tracker-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/competitor-tracker-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitor-tracker-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[niche-evaluation]]`
- `[[pain-point-research]]`
- `[[problem-validation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
