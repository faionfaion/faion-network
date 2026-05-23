# Shutdown Customer Email Pack

## Summary

**One-sentence:** Generates a three-email shutdown spec (T-30 announce, T-14 refund/migrate, T+1 final thanks) so an indie product sunsets without scorching customer goodwill.

**Ефективно для:** Solo founders sunsetting a paid product with real paying customers — the recurring high-emotion moment most founders postpone until it is too late.

**One-paragraph:** Sunsetting a paid product is a recurring indie task that founders write from scratch under emotional pressure — usually too late and usually skipping refunds. This methodology codifies the three emails every shutdown needs, the 30-day minimum notice window, the named-human-from-line rule, and the no-corporate-speak honesty requirement. Output is a versioned email spec consumed by the founder's ESP. The goal is not saving the product but preserving trust capital for the next launch.

## Applies If (ALL must hold)

- You are sunsetting a paid (subscription or one-time) product with paying customers on file.
- You own an email channel reaching those customers (not just social followers).
- The shutdown decision is firm — not a 'maybe pivot' trial balloon.
- A named human can sign each email (founder + photo + signature).

## Skip If (ANY kills it)

- Free product with no transactional relationship — use a single farewell post instead.
- Acquisition or merger where new entity owns the comms plan.
- Legal force majeure shortens timeline below 30 days — defer to counsel.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| customer roster with email + plan + last-charge date | csv | Stripe / billing export |
| named human signing each email | name + photo + signature block | founder profile |
| real reason for shutdown in one honest sentence | string | internal decision log |
| refund or migration target with terms | string | internal commercial decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/sunset-customer-comms-template` | Adjacent comms template — non-paid sunset variant. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_announce_email` | sonnet | Per-instance copy with concrete reason + dates. |
| `compute_refund_split` | haiku | Deterministic arithmetic on the roster. |
| `review_for_honesty_tone` | opus | Catch corporate-speak before it ships. |

## Templates

| File | Purpose |
|---|---|
| `templates/shutdown-customer-email-pack.json` | JSON Schema for the output contract. |
| `templates/shutdown-customer-email-pack.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-shutdown-customer-email-pack.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[sunset-customer-comms-template]] — broader sunset variant for non-paid products.
- [[social-proof-harvest]] — preserves goodwill quotes from sunset survey.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
