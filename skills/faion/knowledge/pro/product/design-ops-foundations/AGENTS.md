---
slug: design-ops-foundations
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rituals, tooling stack, design-team capacity model for the missing 'design-ops' sibling of marketing-ops and dev-ops.
content_id: "8fe90a978d44d73f"
complexity: medium
produces: spec
est_tokens: 4400
tags: [design-ops-foundations, product, pro]
---
# Design Ops Foundations

## Summary

**One-sentence:** Rituals, tooling stack, design-team capacity model for the missing 'design-ops' sibling of marketing-ops and dev-ops.

**One-paragraph:** Design Ops is a real industry sub-discipline (NN/g, DesignOps Assembly). Corpus has marketing-ops and dev-ops siblings but no design-ops methodology covering rituals, tooling stack, design-team capacity model. Output: ritual calendar + tool inventory + capacity model + critique cadence.

**Ефективно для:**

- Маленька дизайн-команда створює перший design-ops setup без enterprise overhead.
- Потрібна capacity model, ritual-stack, tooling-stack як стартова основа.
- Дизайн-ops як sibling до dev-ops і marketing-ops — без копіювання enterprise шаблонів.

## Applies If (ALL must hold)

- design team ≥3 people OR 1 design lead + 2+ engineers consuming design
- design assets serve ≥2 surfaces (web + mobile, or product + marketing)
- design lead has authority to set rituals + standardize tooling

## Skip If (ANY kills it)

- solo designer — use solo/ux/ui-designer instead
- design fully outsourced — different governance
- ad-hoc team with no continuity — establish design hiring first

## Prerequisites

- list of current tools (Figma, FigJam, Linear, Notion, etc.) with seat counts
- weekly design throughput (designs shipped or PRs reviewed)
- named design lead

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/ux/ux-ui-designer` | peer methodology — produces inputs or consumes outputs |
| `pro/pm/pm-agile` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-ops-foundations.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/design-ops-foundations.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-design-ops-foundations.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-ops-foundations.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/ux/ux-ui-designer`
- peer methodology: `pro/pm/pm-agile`
- external: https://www.nngroup.com/articles/design-ops-101/ (NN/g DesignOps 101); https://designopsassembly.com/

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
