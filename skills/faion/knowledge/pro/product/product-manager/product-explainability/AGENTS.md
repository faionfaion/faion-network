# Product Explainability

## Summary

A PM communication discipline that turns engineering output into a single canonical `feature-narrative.json` and derives audience-specific renders from it: exec memo, sales one-pager, support runbook, customer changelog, and AI-readable KB delta. The source narrative is structured (purpose + behavior_change + measurable_outcome + limit + affected_personas); renders are generated, never hand-edited.

## Why

In 2026, product discovery and buying guidance are AI-mediated. A PM who only writes for humans leaves the product mis-described in AI answers and pre-sales conversations. Beyond AI: translation drift across PM → sales → support → customer erodes limits from the story with each hop, causing mis-selling and churn. One canonical JSON source with generated renders prevents drift and forces the PM to state limits before benefits.

## When To Use

- Pre-roadmap-review: three PMs give three different framings for the same product.
- Pre-launch: enabling sales, support, and CS teams who must explain the feature without a Loom.
- Board / investor / all-hands narrative: distilling six months of work into a 90-second answer.
- Cross-team feature-to-impact mapping: every release should answer which OKR moved by how much.
- Post-mortem on mis-sell or churn traced to a story gap, not a product gap.
- Onboarding a new PM, designer, or engineer — the narrative artifact is the fastest shared mental model.

## When NOT To Use

- Inside the engineering loop — explainability framing slows iteration on technical specs; use ADRs there.
- Experiment-stage features behind a flag with less than 5% rollout — premature explainability hardens hypotheses.
- When rigorous PMM already owns this artifact — collaborate, do not re-author.
- Deeply technical APIs whose only audience is engineers with the OpenAPI spec.
- Weekly tactical standups — this is a strategy and stakeholder artifact.

## Content

| File | What's inside |
|------|---------------|
| `content/01-narrative-structure.xml` | feature-narrative.json schema, field rules (limit before benefit, outcome with isolation method, persona-anchored), authoring discipline. |
| `content/02-render-pipeline.xml` | Three-loop pipeline: extract → translate (5 audience renders) → validate (comprehension probe). Agent rules per render. |
| `content/03-antipatterns.xml` | Feature-list trap, outcome-washing, hero-narrative bias, stale story, AI-readability blindness, limit erosion across renders. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-narrative-gate.sh` | Validates feature-narrative.json: required fields, limit length, banned marketing adjectives. Blocks release if narrative is missing or invalid. |
| `templates/prompt-story-extraction.txt` | LLM prompt for extract loop: reads PRD + release notes + telemetry + research clips, emits structured narrative JSON. |
| `templates/prompt-audience-render.txt` | LLM prompt for translate loop: renders narrative for exec / sales / support / customer / AI with per-audience constraints and banned-token list. |
