<!--
purpose: Frontend design spec template — captures fixed brief, variant set, chosen variant, tokens, Storybook config, planned components.
consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
produces: a frontend-design artefact that validates against scripts/validate-frontend-design.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~500-1800 tokens once filled
variables:
  - name: spec_id
    type: string
    required: true
    description: Kebab-case id for this spec, naming the surface and the year - "acme-dashboard-2026". Screenshots and token files are filed under it, so pick one you can still type in six months.
  - name: owner
    type: string
    required: true
    description: The person who picks the winning variant. Selection by consensus produces a fourth variant that is all of them averaged, and averaging distinct directions is how you get a templated default.
  - name: email
    type: string
    required: true
    description: The owner's email, reachable after they change teams. This is the address the next engineer writes to before undoing what this document decided.
  - name: date
    type: string
    required: true
    description: The day this was agreed, ISO - not the day it was typed up. Downstream reviews are scheduled off it, so a placeholder date silently disables the review.
  - name: app_type
    type: text
    required: true
    description: What is being designed, in the terms a user would use - "SaaS dashboard for warehouse supervisors", "mobile-first booking flow". Density and navigation follow from this, so be concrete.
  - name: style_direction
    type: text
    required: true
    description: The aesthetic commitment, named - neo-brutalist, editorial, playful-glass. Pick one and say what it rules out; "clean and modern" is what every templated default already claims.
  - name: tech_stack
    type: string
    required: true
    description: Framework, styling layer and component primitives you are actually committed to. It constrains the variants - a command-palette-first direction is a different amount of work on each stack.
  - name: variant_count
    type: integer
    required: true
    default: "3"
    description: How many genuinely distinct directions you will produce, 3 to 5. Distinct means different navigation and density, not the same screen in three accent colours - the validator checks the count, only you can check the distinctness.
  - name: chosen_variant
    type: integer
    required: true
    description: Which variant number won, decided after all of them existed. If you already know the answer before generating them, you are producing evidence for a decision, not making one.
-->
---
spec_id: {{spec_id}}
owner: {{owner}} <{{email}}>
version: 1.0.0
last_reviewed: {{date}}
variant_count: {{variant_count}}
chosen_variant: {{chosen_variant}}
tokens_defined: false
storybook_version_pinned: false
components_planned: 0
validated_at: 2026-05-23T00:00:00Z
---

## Brief (fixed before variant generation)

- App type: {{app_type}}
- Style direction: {{style_direction}}
- Tech stack: {{tech_stack}}
- Constraints: [a11y target, perf budget, i18n footprint]

## Variants (3-5 distinct directions, NOT iterations of one)

| # | Name | Navigation pattern | Information density | Screenshot path |
|---|------|--------------------|---------------------|-----------------|
| 1 | [name] | [e.g. left-rail collapsed] | [low/medium/high] | screenshots/v1.png |
| 2 | [name] | [e.g. top-bar mega-menu] | [low/medium/high] | screenshots/v2.png |
| 3 | [name] | [e.g. command-palette-first] | [low/medium/high] | screenshots/v3.png |

## Chosen variant + rationale

- Variant: #{{chosen_variant}}
- Reasoning: [one paragraph: why this beat the others on the brief]

## Design tokens (defined BEFORE components)

| Group | Token | Value |
|-------|-------|-------|
| color | primary | [hex] |
| color | surface | [hex] |
| typography | font-display | [stack] |
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
