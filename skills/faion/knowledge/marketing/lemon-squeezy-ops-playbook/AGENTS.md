# Lemon Squeezy Ops Playbook

## Summary

**One-sentence:** Operate a Lemon Squeezy store as Stripe alternative — store config, License API, EU VAT (Lemon Squeezy as Merchant of Record), affiliate program, dunning recovery, monthly review.

**One-paragraph:** Lemon Squeezy (LS) is the default Merchant-of-Record alternative to Stripe for non-US indie operators — global tax handled, dispute risk on LS, payouts in USD/EUR. This playbook closes the gap: store + variant model (1 store, ≤8 active variants), License API for software protection, EU VAT remitted by LS (you do NOT collect VAT yourself), affiliate program with 30-50% commission, dunning email cadence for failed renewals, monthly catalogue review with promote/demote. Output is the LS store config + variant table + ops checklist.

**Ефективно для:**

- Non-US founders avoiding Stripe Atlas / US LLC overhead for global tax compliance.
- SaaS or digital product with EU buyer share &gt; 20% (VAT load is real).
- License-keyed software needing LS License API verification.
- Affiliate-driven launches where commission tracking via LS is acceptable.

## Applies If (ALL must hold)

- Product is digital (file, license, subscription) compatible with LS terms.
- Founder is comfortable with LS's ~5% + payment fees in exchange for MoR + tax handling.
- Founder has at least one variant (price point) defined.
- Founder accepts USD or EUR payouts to a supported bank.

## Skip If (ANY kills it)

- Enterprise NET-30 invoicing required — LS does not support invoicing terms.
- Product violates LS terms (NSFW, certain crypto, regulated services).
- High-ARPU SaaS where Stripe-direct margin difference outweighs MoR convenience.
- Founder already on Stripe with Atlas + tax software — switching cost not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Store name + ≤8 variant definitions | YAML | founder |
| Refund policy (one of LS enums) | string | founder |
| License API decision (on/off per variant) | bool | founder |
| Affiliate commission % decision (0-90) | scalar | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gumroad-ops-playbook]] | Sibling MoR — used when Gumroad fits better (smaller catalogue). |
| [[pricing-experiment-runbook]] | LS supports A/B price testing; the runbook discipline carries over. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 6-field store, MoR not self-VAT, License API for software, dunning email cadence, affiliate 30-50%, monthly review | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for store + variants + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix): double-VAT, license bypass, dunning gap, affiliate drop | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: store setup → variants → license → affiliate → dunning → monthly review | 800 |
| `content/05-examples.xml` | essential | Worked example: 3-variant LS store with EU buyer 35% | 700 |
| `content/06-decision-tree.xml` | essential | Tree routing observables → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `store_field_fill` | haiku | Template fill once decisions are made. |
| `dunning_copy` | sonnet | Tone-sensitive sequence for failed renewals. |
| `affiliate_program_setup` | sonnet | Commission + payout + recruitment. |
| `monthly_review` | sonnet | Aggregate metrics + narrate top variants. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ls-store.yaml` | Store + variants skeleton ready to fill |
| `templates/dunning-sequence.md` | 3-email dunning sequence for failed renewals |
| `templates/_smoke-test.json` | Minimum viable LS store config for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lemon-squeezy-ops-playbook.py` | Validate LS store config against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[gumroad-ops-playbook]]
- [[pricing-experiment-runbook]]
- [[ih-build-update-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps product type, MoR acceptance, license needs, EU share, and affiliate intent to a rule from `01-core-rules.xml`, telling the agent whether to publish, block on a missing gate, or skip LS for Stripe-direct. Walk it on every fresh store change; do not cache outcomes across products.
