# Influencer Marketing

## Summary

**One-sentence:** Four-phase influencer spec: discover micro-influencers by engagement quality, vet for audience match + fraud, personalized outreach, FTC-compliant disclosures, ROI tracking.

**One-paragraph:** Four-phase influencer spec: discover micro-influencers by engagement quality, vet for audience match + fraud, personalized outreach, FTC-compliant disclosures, ROI tracking. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Consumer / prosumer brand з viable AOV для influencer commission.
- Перед paid social scale — influencer як diversification + creative library.
- Якщо brand awareness flat, micro-influencer wave може зрушити.
- При перейті від solo influencer experiments до repeatable program.

## Applies If (ALL must hold)

- AOV / LTV дозволяє flat fee + commission per partnership.
- Brand voice + visual guidelines defined — influencer asset alignment.
- Tracking infra (UTM links / promo codes / influencer platforms).

## Skip If (ANY kills it)

- B2B enterprise з complex buying committee — influencer ROI weak.
- Pre-launch без real product — авторитет creators не врятує bad product.
- Regulated vertical (health / pharma / finance) без legal sign-off.

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
| `templates/spec-skeleton.md` | Influencer Marketing skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Influencer Marketing. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-influencer-marketing.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[growth-affiliate-marketing]]
- [[growth-press-coverage]]
- [[growth-brand-positioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
