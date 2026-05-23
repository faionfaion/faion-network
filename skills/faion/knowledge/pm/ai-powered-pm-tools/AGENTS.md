# Ai Powered Pm Tools

## Summary

**One-sentence:** 2026 survey of AI-augmented PM platforms (Jira+Rovo, Monday AI, ClickUp Brain, Linear AI, Asana AI) — buyer's decision record by stack + role + budget fit.

**One-paragraph:** 2026 survey of AI-augmented PM platforms (Jira+Rovo, Monday AI, ClickUp Brain, Linear AI, Asana AI) — buyer's decision record by stack + role + budget fit. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Покупцю AI-PM tool — щоб вибір був за реальними інтеграціями, не за рекламою.

## Applies If (ALL must hold)

- Org is evaluating or already on a major PM platform.
- Budget exists for AI-tier upgrade.
- Named buyer owns the procurement decision.
- Integration baseline exists (SSO, audit log, connectors).

## Skip If (ANY kills it)

- Team < 10 seats — per-seat uplift seldom pays back.
- Custom in-house tracker — these vendor AIs do not integrate.
- Org already invested in custom Claude / OpenAI workflows — fork instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current contract | PDF | procurement |
| Usage baseline | vendor dashboard | platform owner |
| Integration inventory | list | IT/security |
| Named buyer | person | VPE / procurement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-powered-pm-tools` | Twin survey from the pm-agile angle. |
| `geek/pm/project-manager/ai-pm-tool-integration-recipes` | Recipes the tool can replace OR plug into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `price-fit-extract` | haiku | Pure data pull from vendor pricing pages. |
| `integration-gap-analysis` | sonnet | Bounded judgement against current stack. |
| `ROI-narrative` | opus | Cross-vendor synthesis for buyer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Decision record: incumbent + AI-tier price + integration fit + ROI gate + outcome. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-powered-pm-tools.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-pm-tool-integration-recipes]]
- [[ai-in-project-management]]
- [[ai-assisted-velocity-anomaly-detection]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the selection (platform + ≥10 seats + buyer + budget), block (no budget), or skip (small team / custom stack). Run before vendor demo calendar is filled.
