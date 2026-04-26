# Persona Building

## Summary

A five-step process for creating semi-fictional customer archetypes grounded in real interview data: gather data from at least 10 interviews, cluster utterances by goals/frustrations/behaviours, define at most one primary and one negative persona, validate against real cohort behaviour, and refresh quarterly. Every claim must cite a source interview ID — no invented demographics.

## Why

Teams without research-grounded personas default to "everyone is our customer," producing weak positioning, features built for nobody, and messaging that resonates with no one. Fictional personas (stock photos, made-up details) are worse than none: they justify wrong decisions with false confidence. Evidence-anchored personas give product, marketing, and sales a shared archetype that can be falsified and updated.

## When To Use

- After running 10+ customer interviews and the team needs a shared archetype to anchor product/marketing/sales decisions.
- A pivot or new market entry where the prior persona is stale.
- Pre-launch positioning to align messaging across landing page, ads, and onboarding.
- Internal alignment when product and sales describe customers in incompatible terms.
- Annual or post-pivot review of an existing persona library.

## When NOT To Use

- Before any real research — fictional personas are worse than none.
- Where the audience is well-understood from quantitative data alone (analytics, CRM cohorts) and segments, not personas, are needed.
- For one-off campaigns where a single value-prop test is cheaper.
- For B2B enterprise sales with named accounts — ICPs and buyer maps outperform personas there.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-step process, data sources, clustering dimensions, persona elements |
| `content/02-examples.xml` | Two worked examples (SaaS for writers, agency PM tool) with antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-full.md` | Full persona template with demographics, goals, frustrations, buying behaviour |
| `templates/persona-lean.md` | Lean 6-field persona for rapid iteration |
| `templates/persona-negative.md` | Negative persona template (who NOT to target) |
| `templates/build-persona.py` | Anthropic SDK script: transcript clustering → persona JSON with citation IDs |
