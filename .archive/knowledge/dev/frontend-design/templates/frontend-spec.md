# purpose: Frontend design spec template — captures fixed brief, variant set, chosen variant, tokens, Storybook config, planned components.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a frontend-design artefact that validates against scripts/validate-frontend-design.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~500-1800 tokens once filled
---
spec_id: <kebab-case slug, e.g. acme-dashboard-2026>
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
variant_count: <3..5>
chosen_variant: <1..5>
tokens_defined: false
storybook_version_pinned: false
components_planned: 0
validated_at: 2026-05-23T00:00:00Z
---

## Brief (fixed before variant generation)

- App type: <e.g. SaaS dashboard | marketing site | mobile-first PWA>
- Style direction: <e.g. neo-brutalist | editorial | playful-glass>
- Tech stack: <e.g. Next.js 14 + Tailwind + Radix>
- Constraints: <a11y target, perf budget, i18n footprint>

## Variants (3-5 distinct directions, NOT iterations of one)

| # | Name | Navigation pattern | Information density | Screenshot path |
|---|------|--------------------|---------------------|-----------------|
| 1 | <name> | <e.g. left-rail collapsed> | <low/medium/high> | screenshots/v1.png |
| 2 | <name> | <e.g. top-bar mega-menu> | <low/medium/high> | screenshots/v2.png |
| 3 | <name> | <e.g. command-palette-first> | <low/medium/high> | screenshots/v3.png |

## Chosen variant + rationale

- Variant: #<n> — <name>
- Reasoning: <one paragraph: why this beat the others on the brief>

## Design tokens (defined BEFORE components)

| Group | Token | Value |
|-------|-------|-------|
| color | primary | <hex> |
| color | surface | <hex> |
| typography | font-display | <stack> |
| spacing | unit | 4px |
| radius | md | 8px |

## Storybook scaffold (pinned versions)

| Package | Pinned version |
|---------|----------------|
| @storybook/react | 8.x.x exact |
| @storybook/addon-a11y | x.y.z exact |
| @storybook/test-runner | x.y.z exact |

## Components planned (colocated story + test + component)

| Component | Story file | Test file | Status |
|-----------|------------|-----------|--------|
| Button | Button.stories.tsx | Button.test.tsx | planned |
| Card | Card.stories.tsx | Card.test.tsx | planned |

## Validation

Run `scripts/validate-frontend-design.py --file path/to/spec.json` before merge. Fails on variant_count out of 3..5, missing chosen_variant, or unpinned Storybook deps.
