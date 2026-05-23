# Content Distribution Orchestration

## Summary

**One-sentence:** Spec for AI-assisted content atomization pipeline: one source asset (long-form post / podcast / video) → 10 channel-specific variants (Twitter thread, LinkedIn post, TikTok script, YT Short, newsletter, etc.) with cadence, owner, and channel-fit scoring.

**One-paragraph:** Spec for AI-assisted content atomization pipeline: one source asset (long-form post / podcast / video) → 10 channel-specific variants (Twitter thread, LinkedIn post, TikTok script, YT Short, newsletter, etc.) with cadence, owner, and channel-fit scoring. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team produces ≥ 1 long-form source asset per week (blog / podcast / video).
- Team has ≥ 5 channels under management (LinkedIn / Twitter / TikTok / YT / newsletter / etc.).
- Named content owner can act on the daily / weekly cadence.

## Skip If (ANY kills it)

- No source content cadence yet — focus on production cadence before orchestrating distribution.
- Single-channel team (e.g. newsletter-only) — atomization overhead does not pay back.
- No AI-pipeline budget (token / compute) — start with manual atomization for 2-4 weeks first.

**Ефективно для:**

- Solopreneurs що публікують 1-2 long-form items / тиждень і хочуть розтягнути на 10 каналів.
- Growth marketers що автоматизують atomization під AI-pipeline (Claude / GPT).
- Команди що мають content surface > distribution surface (мало каналів використовується).
- Аудит-ready середовища з вимогою channel-fit evidence per variant.

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
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-distribution-orchestration.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[competitor-creative-scrape-ai]]
- [[content-distribution-orchestration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
