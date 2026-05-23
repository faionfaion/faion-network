# Asset Harvest Checklist

## Summary

**One-sentence:** Generates a pre-launch checklist that inventories every visual + textual + legal + analytics asset a landing page needs, with status and source per item.

**One-paragraph:** Pre-launch checklists drift between teams; the same launch ships missing favicons, social-card images, privacy pages, and analytics scripts. This methodology emits an asset-harvest list across five categories — visual (favicon / og-image / hero / screenshots), textual (page copy / meta description / page title), legal (privacy / terms / cookie banner), analytics (tracking script / consent gate / event taxonomy), and SEO (sitemap / robots.txt / canonical) — with per-item source, status, and required-by-launch flag. Output: checklist artefact with 0 outstanding required items at launch.

**Ефективно для:**

- Solo dev launching a new landing page in two days and afraid to forget anything.
- Standardising launch checklists across 5 landing pages so each one ships with the same minimum.
- Adding analytics + consent gate before a public launch where GDPR matters.
- Catching missing og-image before the post goes viral and shows a blank Twitter card.

## Applies If (ALL must hold)

- Launching a public web surface (landing page / product / docs).
- Author has access to repo + DNS + analytics tooling.
- Audience is large enough to care about cards + SEO (not a private experiment).

## Skip If (ANY kills it)

- Internal-only page behind auth.
- Pre-MVP draft where polish is premature.
- One-off campaign page that will be deleted in a week.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Page URL or path | URL | repo / staging |
| Brand guidelines | tokens + logo files | design system |
| Analytics tool | Plausible / GA4 / PostHog | platform |
| Legal pages | /privacy + /terms URLs | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens-basics]] | Brand colours + logo come from design tokens. |
| [[accessibility]] | Each asset must pass the a11y floor at launch. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `asset_harvest_checklist_draft` | sonnet | Bounded synthesis. |
| `asset_harvest_checklist_validate` | haiku | Mechanical schema check. |
| `asset_harvest_checklist_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the asset-harvest-checklist artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in asset-harvest-checklist artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-asset-harvest-checklist.py` | Validate asset-harvest-checklist artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[design-tokens]]
- [[frontend-design]]
- [[pwa-development]]
- [[seo-for-spas]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
