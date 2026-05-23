# Multi Product Portfolio Management

## Summary

**One-sentence:** Produces a portfolio config (per-product mode tag + weekly time-budget + capital allocation + cross-product kill rule) for a solopreneur running ≥3 products.

**Ефективно для:** Solopreneurs running 3-8 products in parallel who treat them as one mental pile and lose track of which product gets which attention this week.

**One-paragraph:** Indie hackers run 3-8 side projects in parallel and the corpus only supports single-product prioritisation (RICE on one backlog). This methodology produces a portfolio config that tags each product with a mode (build / grow / maintain / sunset), assigns a weekly time-budget per mode, allocates capital, and pins a cross-product kill rule so the portfolio rotates instead of bloating. Output is consumed by the operator's weekly time block + portfolio review.

## Applies If (ALL must hold)

- Operator runs ≥3 products in parallel.
- Total weekly time available ≤40h (solo cap).
- Each product is on a known revenue + traffic baseline.
- Operator can name modes explicitly (no 'all are growing' wishful thinking).

## Skip If (ANY kills it)

- Operator runs ≤2 products — portfolio config is overkill, single-product prioritisation suffices.
- Operator unwilling to tag products with mode (build/grow/maintain/sunset) — config has nothing to organise.
- Time budget is unlimited (employed team / VC) — capital allocation is not solopreneur-shaped.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| product list | array of named products | operator |
| MRR + traffic per product | object | Stripe + Plausible |
| weekly time available | hours | operator |
| capital pool | currency | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/portfolio-triage-indie` | Upstream — triage method that feeds verdicts here. |
| `solo/product/maintain-mode-sops-solo` | Downstream — maintain-mode products use those SOPs. |

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
| `tag_modes` | haiku | Per-product mode assignment from inputs. |
| `allocate_time_and_capital` | sonnet | Bounded judgement: time + capital per mode. |
| `portfolio_rotation_review` | opus | Cross-product synthesis at quarterly portfolio review. |

## Templates

| File | Purpose |
|---|---|
| `templates/multi-product-portfolio-management.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/multi-product-portfolio-management.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-multi-product-portfolio-management.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[portfolio-triage-indie]] — related methodology.
- [[maintain-mode-sops-solo]] — related methodology.
- [[kill-criteria-template]] — related methodology.
- [[sunset-failed-product-playbook]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
