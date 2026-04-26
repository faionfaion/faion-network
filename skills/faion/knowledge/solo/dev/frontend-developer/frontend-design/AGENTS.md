# Frontend Design

## Summary

A four-phase workflow for UI surfaces where multiple visual directions are explored before
committing: (1) capture requirements (type, style, tech), (2) brainstorm 3–5 distinct variants via
`faion-frontend-brainstormer-agent` into `designs/variant-N-<slug>/`, each with working code and
a rationale, (3) user selects and refines, (4) `faion-storybook-agent` builds stories and
`faion-frontend-component-agent` finalizes typed components. Variants must differ in typeface,
density, color, and motion — not just palette.

## Why

LLMs given a single "design this" prompt converge on one SaaS-average aesthetic. Structured
divergence forces 3–5 meaningfully distinct directions, accelerates human decision-making, and
persists design rationale so future agents know why a direction was chosen. The 3–5-variant ceiling
prevents decision paralysis; more than 5 options reliably delays selection.

## When To Use

- Starting a new UI surface (landing, dashboard, form, component set) with no visual decisions yet.
- Solo dev or small team wanting LLM-driven design exploration before implementation.
- Requirements exist but visual direction does not; brainstorming variants accelerates kickoff.
- Storybook is the deliverable — each variant must be explorable in isolation.

## When NOT To Use

- Existing product with a mature design system — converging is more important than diverging.
- One-off internal tool where any reasonable UI suffices.
- Marketing pages where copy and photography drive design more than component patterns.
- Strict brand guideline enforcement: variant exploration generates ineligible options.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules: variant diversity constraints, token persistence, a11y gate per variant, 3–5 ceiling, rationale requirement. |
| `content/02-workflow.xml` | Phase-by-phase agent workflow: requirements capture, brainstorm, selection, Storybook/component finalization. |

## Templates

| File | Purpose |
|------|---------|
| `templates/new-variant.sh` | Scaffold a `designs/variant-N-<slug>/` directory with README template. |
| `templates/prompt-brainstorm.txt` | LLM prompt template for generating 3–5 contrastive design variants. |
