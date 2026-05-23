# Twitter X Monetization Thread To Product

## Summary

**One-sentence:** Produces a thread-to-product funnel spec (audience signal → 7-tweet thread → email gate → paid product) for distribution-first idea validation before any product is built.

**Ефективно для:** Indie hackers building audience before product who lack a deterministic path from a high-impression thread to a paid SKU — and keep losing the audience signal to inbox noise.

**One-paragraph:** Distribution-first idea validation needs a deterministic path: audience signal → high-impression thread → email gate → paid product. This methodology produces a funnel spec naming the thread shape, the email-gate offer (one piece of derivative value), the lifecycle that warms subscribers, and the paid product SKU at the end. It refuses to ship without a validated audience signal AND a paid product (or pre-order) on file.

## Applies If (ALL must hold)

- Operator has an X audience (≥1k) with ≥3 high-impression threads in the last 90 days.
- A paid product OR pre-order page exists.
- Operator can manage an email lifecycle (ESP + welcome sequence).
- An audience-validated topic / pain is identified.

## Skip If (ANY kills it)

- No audience signal yet — switch to audience-build playbook first.
- No paid product / pre-order — funnel without endpoint is theatre.
- ESP not set up — emails leak the audience.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| audience signal evidence (3+ threads ≥10k imp) | list of URLs | X analytics |
| paid product URL + SKU + price | URL + string + price | founder decision |
| ESP account + welcome sequence (≥5 emails) | credentials + drafts | operator |
| email-gate offer (one derivative asset) | PDF / template / kit | internal asset |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Audience source. |
| `solo/marketing/swipe-file-tweet-hooks` | Hook bank for the thread. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_thread_for_funnel` | sonnet | 7-tweet funnel-mode thread. |
| `score_audience_signal` | haiku | Bounded threshold check. |
| `audit_funnel_for_leaks` | opus | End-to-end leak audit. |

## Templates

| File | Purpose |
|---|---|
| `templates/twitter-x-monetization-thread-to-product.json` | JSON Schema for the output contract. |
| `templates/twitter-x-monetization-thread-to-product.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-twitter-x-monetization-thread-to-product.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-twitter-x-growth]] — audience source.
- [[swipe-file-tweet-hooks]] — hook bank.
- [[substack-to-product-funnel]] — adjacent newsletter funnel.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
