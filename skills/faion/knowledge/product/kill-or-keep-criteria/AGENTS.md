# Kill Or Keep Criteria

## Summary

**One-sentence:** Produces a checklist that scores a side-project against MRR-floor / traffic-floor / joy-floor / opportunity-cost thresholds and outputs a binary kill-or-keep decision with cited evidence.

**Ефективно для:** Solopreneurs auditing a side-project portfolio quarterly who lack a binary, evidence-anchored kill rubric and default to 'one more month' indefinitely.

**One-paragraph:** Sunsetting a side-project is taboo and underdocumented. This methodology produces a checklist that scores the project against four floors (MRR, traffic, joy, opportunity cost), demands verbatim evidence for each score, and yields a single binary kill-or-keep verdict with the next action attached. Output is consumed by the operator's portfolio review log.

## Applies If (ALL must hold)

- Operator runs a portfolio scan at a published cadence (weekly / monthly / quarterly).
- The project has been live ≥30 days so floors have signal.
- Operator has read access to MRR + traffic dashboards.
- A named owner exists to act on the verdict (write access, sign-off rights).

## Skip If (ANY kills it)

- Project is <30 days post-launch — floors are noise, not signal.
- Operator cannot access dashboards / MRR source-of-truth — paraphrased numbers are worse than skipping.
- Project is a contractual obligation — kill is blocked anyway.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| MRR snapshot | currency | Stripe / Lemonsqueezy |
| traffic snapshot | number | Plausible / GA4 |
| joy-score self-rating | 1-10 | operator |
| opportunity-cost candidate | string | operator's roadmap |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/portfolio-triage-indie` | Parent triage that consumes the verdict. |
| `solo/product/kill-criteria-template` | Upstream — pre-registered thresholds that this rubric checks against. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `kill_or_keep_criteria_template_fill` | haiku | Template fill, no judgement. |
| `kill_or_keep_criteria_evidence_check` | sonnet | Bounded comparison + judgement. |
| `kill_or_keep_criteria_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|---|---|
| `templates/kill-or-keep-criteria.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/kill-or-keep-criteria.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-kill-or-keep-criteria.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[kill-criteria-template]] — related methodology.
- [[portfolio-triage-indie]] — related methodology.
- [[sunset-failed-product-playbook]] — related methodology.
- [[pivot-vs-quit-decision-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
