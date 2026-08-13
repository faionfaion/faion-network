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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/asset-harvest-checklist.json",
  "type": "object",
  "required": [
    "checklist_id",
    "page_url",
    "items"
  ],
  "properties": {
    "checklist_id": {
      "type": "string",
      "pattern": "^AH-[A-Z0-9-]{2,40}$"
    },
    "page_url": {
      "type": "string",
      "minLength": 4
    },
    "items": {
      "type": "array",
      "minItems": 5,
      "items": {
        "type": "object",
        "required": [
          "category",
          "name",
          "status",
          "required_by_launch",
          "source"
        ],
        "properties": {
          "category": {
            "type": "string",
            "enum": [
              "visual",
              "textual",
              "legal",
              "analytics",
              "seo"
            ]
          },
          "name": {
            "type": "string"
          },
          "status": {
            "type": "string",
            "enum": [
              "done",
              "in-progress",
              "missing"
            ]
          },
          "required_by_launch": {
            "type": "boolean"
          },
          "source": {
            "type": "string",
            "minLength": 2
          }
        }
      }
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "checklist_id": "AH-LANDING-Q2",
  "page_url": "https://example.com/launch",
  "items": [
    {
      "category": "visual",
      "name": "og-image-1200x630",
      "status": "done",
      "required_by_launch": true,
      "source": "design/og/launch.png"
    },
    {
      "category": "visual",
      "name": "favicon",
      "status": "done",
      "required_by_launch": true,
      "source": "public/favicon.ico"
    },
    {
      "category": "textual",
      "name": "meta-description",
      "status": "done",
      "required_by_launch": true,
      "source": "pages/launch.mdx frontmatter"
    },
    {
      "category": "legal",
      "name": "privacy-page-link",
      "status": "done",
      "required_by_launch": true,
      "source": "/privacy"
    },
    {
      "category": "analytics",
      "name": "plausible-script",
      "status": "done",
      "required_by_launch": true,
      "source": "_app.tsx"
    },
    {
      "category": "analytics",
      "name": "consent-gate",
      "status": "done",
      "required_by_launch": true,
      "source": "components/CookieBanner.tsx"
    },
    {
      "category": "seo",
      "name": "canonical-url",
      "status": "done",
      "required_by_launch": true,
      "source": "head meta"
    }
  ]
}
```
