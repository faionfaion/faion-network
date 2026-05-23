# Kill Criteria Template

## Summary

**One-sentence:** Produces a one-page kill-criteria artefact (pre-registered MRR/traffic/joy/runway thresholds + calendared review) so portfolio rotation stays disciplined and zombie bets are sunset on schedule.

**Ефективно для:** Solopreneurs running 2+ small bets per year who notice old projects lingering past usefulness because no pre-committed kill threshold exists.

**One-paragraph:** A one-page artefact filled in BEFORE a bet ships, naming the conditions under which the bet will be killed. Removes the future founder's permission to negotiate with reality — kill criteria are pre-registered while incentives are clean. Outcome: every bet in the portfolio has a written, calendared kill date and threshold set, and the founder reviews them on a fixed cadence rather than ad hoc.

## Applies If (ALL must hold)

- Operator runs a portfolio of 2+ small bets per year (indie hacker, micro-studio).
- Operator has noticed at least one prior project that lingered past usefulness.
- The bet has a defined launch event (PH day, soft-launch cohort, first paid customer).
- Operator can name the single metric that, if zero, makes the bet pointless.

## Skip If (ANY kills it)

- The bet is the operator's only product and pivoting is the alternative to killing.
- The bet is a learning project with no revenue goal (research, OSS) — kill thresholds are not the right gate.
- Less than 14 days post-launch — too early to evaluate against thresholds.
- Inside a contractual obligation window (paying customers, refund window) where kill is blocked.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| bet brief | doc | founder |
| named primary metric | string | founder decision |
| baseline numbers (current MRR / traffic / runway) | snapshot | dashboard |
| review calendar slot | calendar entry | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/portfolio-triage-indie` | Parent triage method that consumes kill thresholds. |
| `solo/product/sunset-failed-product-playbook` | Downstream shutdown sequence triggered by the kill. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scaffold_kill_card` | haiku | Fill canonical fields from inputs; no judgement. |
| `calibrate_thresholds` | sonnet | Bounded judgement: pick MRR/traffic floors anchored in baseline. |
| `review_against_outcome` | opus | Cross-cycle synthesis when reviewing whether the kill triggered as designed. |

## Templates

| File | Purpose |
|---|---|
| `templates/kill-criteria-template.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/kill-criteria-template.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-kill-criteria-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[portfolio-triage-indie]] — related methodology.
- [[sunset-failed-product-playbook]] — related methodology.
- [[kill-or-keep-criteria]] — related methodology.
- [[indie-portfolio-scorecard]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
