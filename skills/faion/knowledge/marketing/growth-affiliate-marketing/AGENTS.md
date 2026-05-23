# Growth Affiliate Marketing

## Summary

**One-sentence:** Partner-driven affiliate channel spec: commission structure + cookie duration + recruitment + asset library + onboarding + fraud detection + payout ops.

**One-paragraph:** Partner-driven affiliate channel spec: commission structure + cookie duration + recruitment + asset library + onboarding + fraud detection + payout ops. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- B2C / B2B SaaS з viable LTV для багаторівневого commission share.
- Перед запуском paid retargeting — affiliate як diversification.
- Якщо CAC blended > 30% LTV, affiliate може бути дешевший channel.
- При scaling > $50k MRR — affiliate ops стає sustainable.

## Applies If (ALL must hold)

- LTV documented + >= 40% gross margin per customer.
- Tracking infra (affiliate platform / FirstPromoter / Tapfiliate / PartnerStack) configured.
- Compliance owner для FTC / disclosure rules (US, UK, EU).

## Skip If (ANY kills it)

- Pre-LTV / pre-product-market-fit — affiliates burn budget on poor retention.
- Margin < 25% — commission math kills unit economics.
- Heavily-regulated vertical (health, finance) without legal sign-off — DO NOT run.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | Growth Affiliate Marketing skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Growth Affiliate Marketing. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-affiliate-marketing.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[growth-influencer-marketing]]
- [[reference-program-playbook]]
- [[growth-referral-programs]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
