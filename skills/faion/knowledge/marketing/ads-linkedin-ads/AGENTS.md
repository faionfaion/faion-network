# LinkedIn Ads Campaign Strategy

## Summary

**One-sentence:** Produces a B2B LinkedIn campaign plan: objective + audience + ad format + bid strategy tuned for the high-CPC LinkedIn auction, with creative + matched-audiences playbook.

**One-paragraph:** LinkedIn paid is the most expensive B2B channel (CPC $5-15, CPM $30-80) and only pays back on high-LTV ICP segments. This methodology forces ICP-fit, account-list seeding, and lead-quality metrics over volume. Output is a campaign plan covering objective (awareness / lead-gen / convert), audience layering (job + company + interest), ad format (single image / video / document / conversation), bid strategy, and a creative brief tailored to the LinkedIn feed.

**Ефективно для:**

- B2B продукт з LTV ≥ $5k, де LinkedIn CPC окупається.
- ABM-кампанії на matched account list 100-1000 компаній.
- Senior-ICP (Director+) де LinkedIn job-title targeting найточніший.
- Lead gen forms або gated content для warm leads.

## Applies If (ALL must hold)

- B2B campaign with LTV ≥ $5k that can absorb $5-15 CPC.
- Targeting senior decision-makers (Director / VP / C-level).
- Account-based marketing with a 100-1000 company target list.
- Lead-gen or content-syndication objective with a clear MQL definition.

## Skip If (ANY kills it)

- B2C / low-LTV products — LinkedIn CPC will not pay back.
- Budget under $5k/mo — auction floor + frequency caps yield no statistical signal.
- No CRM-side MQL definition — you cannot judge lead quality, only volume.
- Cold prospecting without ICP signal — LinkedIn is most effective when audience is narrowed first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP definition | JSON / table | GTM / sales |
| Matched audiences | company list CSV / email hash | ABM ops |
| CRM MQL definition | schema doc | RevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Insight Tag must fire on MQL events before reporting on CPL / cost-per-MQL. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-linkedin-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audience-layering` | sonnet | ICP + matched-account + filter composition needs judgement. |
| `creative-brief` | sonnet | Hook + value-prop draft tied to ICP. |
| `kpi-target-derivation` | haiku | Mechanical: LTV × close_rate → max cost-per-MQL. |

## Templates

| File | Purpose |
|------|---------|
| `templates/campaign-plan.md` | LinkedIn campaign plan skeleton with objective, audience, format, bid, creative. |
| `templates/abm-account-list.csv` | Matched-account list CSV header for ABM seeding. |
| `templates/campaign-plan.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-linkedin-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-targeting]]
- [[ads-conversion-tracking]]
- [[growth-paid-acquisition]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
