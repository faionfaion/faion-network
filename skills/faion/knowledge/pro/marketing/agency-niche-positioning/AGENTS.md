---
slug: agency-niche-positioning
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Forces a micro-agency to pick a vertical narrower than feels safe, refuse out-of-niche work, and repackage past portfolio to look like the target niche \u2014 a versioned positioning ADR with named owner and review cadence."
content_id: "1510e08025e14d6b"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [agency, positioning, niche, marketing]
---
# Agency Niche Positioning

## Summary

**One-sentence:** Forces a micro-agency to pick a vertical narrower than feels safe, refuse out-of-niche work, and repackage past portfolio to look like the target niche — a versioned positioning ADR with named owner and review cadence.

**One-paragraph:** Forces a micro-agency to pick a vertical narrower than feels safe, refuse out-of-niche work, and repackage past portfolio to look like the target niche — a versioned positioning ADR with named owner and review cadence. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Agency revenue is plateaued or commodity-priced, founder suspects positioning is the blocker.
- Founder can publicly refuse out-of-niche work for ≥ 90 days to test the bet.
- Past portfolio has ≥ 3 projects in any candidate vertical to repackage.

## Skip If (ANY kills it)

- Agency is < 6 months old with < 3 paying clients — premature to narrow.
- Founder cannot say-no to revenue for 90 days — niche positioning will fail under pressure.
- Revenue mix is already 80%+ from one vertical — formalise, not re-position.

**Ефективно для:**

- Мікро-агенції що позиціонуються як 'full-service' і застрягли на $5-10k retainers.
- Засновники готові відмовитись від out-of-niche роботи що складає до 30% revenue.
- Команди з 5-15 проєктами в портфоліо що треба repackage під одну вертикаль.
- Перед website rebuild або новою sales-page кампанією — anchor у вертикалі першим.

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
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-adr` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-class-and-tradeoff` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-skeleton.md` | ADR skeleton with status / decision_class / context / decision / alternatives-rejected / consequences / rollback / signers. |
| `templates/_smoke-test.md` | Minimum viable filled-in ADR. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-niche-positioning.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
