# Content Audit Process

## Summary

**One-sentence:** Six-step inventory and evaluation of every content asset: crawl/inventory, classify by type, score by multiple criteria, assign action (Keep / Update / Consolidate / Rewrite / Remove / Review), prioritise, output an action plan.

**One-paragraph:** Without a content audit, sites accumulate broken pages, duplicated explanations, outdated information, and SEO drag that no single team owns. This methodology pins the six-step process: (1) crawl inventory all content URLs; (2) classify by type (landing / docs / blog / product / legal); (3) score per multi-criterion rubric (accuracy, traffic, conversion, freshness, SEO, brand fit); (4) assign one of six actions (Keep / Update / Consolidate / Rewrite / Remove / Review); (5) prioritise by impact × effort; (6) output an action plan spec. Downstream consumers (content marketing, SEO, dev / migration) read the plan.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-redesign content cleanup when the new IA will not absorb the old volume.
- Quarterly SEO health pass on a content-heavy site.
- Post-merger / post-rebrand consolidation.
- Migration to a new CMS where every page needs an action decision.

## Skip If (ANY kills it)

- The site has fewer than ~20 pages — manual review is cheaper than the audit overhead.
- A current audit < 6 months old exists.
- The team has no authority to remove pages (legal hold) — Remove cannot be exercised; the audit becomes documentation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Crawl access | sitemap or crawler permissions | devops |
| Analytics data | page-level traffic + conversion | analytics tool |
| SEO data | keyword rankings + backlinks | SEO tool |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/competitive-analysis` | supplies competitive benchmarks for content depth |
| `solo/ux/ux-researcher/consistency-standards` | supplies verbal-layer consistency criteria |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-audit-process.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-content-audit-process.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-audit-process.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[competitive-analysis]]
- [[consistency-standards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
