# Cannibalization Detection SOP

## Summary

**One-sentence:** Detects keyword cannibalization on mature sites via query-page mapping, intent-overlap scoring, and consolidation/de-optimization recommendations — a versioned report owned by the SEO-manager and tied to the annual SEO refresh.

**One-paragraph:** Detects keyword cannibalization on mature sites via query-page mapping, intent-overlap scoring, and consolidation/de-optimization recommendations — a versioned report owned by the SEO-manager and tied to the annual SEO refresh. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Site has ≥ 500 indexed pages with overlapping topical coverage.
- Named SEO owner can run the audit and act on consolidation/de-optimization findings.
- Search Console + Ahrefs / Semrush access is available for query-page mapping.

## Skip If (ANY kills it)

- Site has < 100 pages — cannibalization is unlikely at this scale.
- All pages are programmatic with unique modifiers (city / SKU) — that is intentional pattern, not cannibalization.
- Site is < 6 months old — wait for indexing to stabilise before auditing.

**Ефективно для:**

- Mature site з 500+ сторінок де декілька цілять на той самий запит.
- SEO-менеджери що ведуть annual SEO Audit & Refresh 6-week cycle.
- Команди що бачать ranking drift: сторінки міняються місцями для того ж запиту.
- Аудит-ready середовища з вимогою evidence-anchored consolidation decisions.

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
| `pro/marketing/seo-manager` or `pro/marketing/growth-marketer` | Parent role context — SEO / growth discipline. |
| `solo/marketing/content-marketer` | Adjacent content production context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Per-row evidence link + summary judgment. |
| `outcome-synthesis` | opus | Cross-cycle synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Report skeleton with frontmatter + sections + evidence anchors per row. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cannibalization-detection-sop.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[cannibalization-detection-sop]]
- [[anchor-diversification-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
