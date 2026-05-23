# 30 Day Post Launch Review Template

## Summary

**One-sentence:** Produces a 30-day post-launch review report (funnel snapshot + pre-launch-hypotheses outcome + ≥3 ranked next-bets) so the launch window stops being a moment and becomes a learning.

**Ефективно для:** Solopreneurs who ship a launch and never close the loop — pre-launch hypotheses live or die without verdict and the next-bet decision is improvised.

**One-paragraph:** Most launches end the moment the announce-tweet ships; the operator pivots to the next thing without comparing pre-launch hypotheses against the observed funnel. This methodology produces a 30-day review report: funnel snapshot per channel, per-hypothesis verdict (confirmed / refuted / inconclusive with evidence), ≥3 ranked next-bets with budget. Output is consumed by the operator's quarterly roadmap and the launch-tier-decision-frame for the next launch.

## Applies If (ALL must hold)

- Launch event is ≥30 days in the past.
- Pre-launch hypotheses were written (e.g. in launch-comms-kit-template).
- Funnel events instrumented per mvp-instrumentation-checklist are firing.
- Operator can dedicate a 2h review slot.

## Skip If (ANY kills it)

- Launch is <30 days old — signal is not stable.
- No pre-launch hypotheses recorded — there's nothing to compare against; start a fresh hypothesis log instead.
- Funnel events not instrumented — retro-derivation is hypothesis-by-folklore.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| pre-launch hypotheses | array | launch-comms-kit-template artefact |
| funnel snapshot per channel | object | analytics tool |
| MRR + signup count at T+30 | snapshot | Stripe + analytics |
| budget pool for next bets | currency | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/launch-comms-kit-template` | Upstream — provides hypotheses being reviewed. |
| `solo/product/mvp-instrumentation-checklist` | Upstream — instrumentation must be live. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `snapshot_funnel` | haiku | Bounded data pull per channel. |
| `verdict_hypotheses` | sonnet | Per-hypothesis judgement: confirmed / refuted / inconclusive. |
| `rank_next_bets` | opus | Cross-bet synthesis at retro write-up. |

## Templates

| File | Purpose |
|---|---|
| `templates/30-day-post-launch-review-template.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/30-day-post-launch-review-template.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-30-day-post-launch-review-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[launch-comms-kit-template]] — related methodology.
- [[launch-tier-decision-frame]] — related methodology.
- [[mvp-instrumentation-checklist]] — related methodology.
- [[what-you-dont-know-about-launch-pre-mortem]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
