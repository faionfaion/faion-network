# Persona Building

## Summary

A 5-step process for creating semi-fictional buyer archetypes grounded in real interview data: gather data (minimum 10 interviews), cluster patterns, define 1-3 segments (primary / secondary / negative), build the persona with cited traits, then validate by showing the doc to actual customers. Outputs `user-personas.md` in `.aidocs/product_docs/`.

## Why

Personas built from imagination produce "demographic theatre" — stock-photo characters that never change a real product or marketing decision. Research-backed personas with transcript citations force the team to confront actual user language, purchasing triggers, and frustrations, making positioning and onboarding decisions testable rather than aesthetic.

## When To Use

- Raw transcripts from 8+ customer interviews exist and need clustering into buyer archetypes before writing positioning or landing copy.
- Landing page has poor conversion and the team disagrees on "who this is for".
- Sales closes one segment 3x faster than others — codify that segment as primary persona.
- Pivoting into an adjacent market and needing a new primary persona before rewriting home page and pricing tiers.
- A multi-agent pipeline needs a shared persona artifact as input (`faion-research-agent` → `faion-marketing-manager` → `faion-content-marketer`).

## When NOT To Use

- Pre-PMF / pre-interview: zero customer conversations — run `user-interviews` and `pain-point-research` first.
- B2B enterprise with named-account selling and fewer than 20 logos — use account profiles and buying-committee maps.
- Highly heterogeneous marketplaces where the segmentation axis is transactional behavior — use `audience-segmentation` instead.
- Single-feature internal tools where the user is unambiguous — a 1-line role description beats a 2-page persona doc.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 5-step persona building process with rules and data source table |
| `content/02-examples.xml` | Two worked personas (Newsletter Nate, Agency Amy) with full field sets; common mistakes table |
| `content/03-gotchas.xml` | LLM hallucination of quotes, demographic stereotypes, PII in transcripts, human-in-the-loop checkpoints |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-full.md` | Full persona template (demographics, goals, frustrations, day-in-life, tools, buying behavior, messaging) |
| `templates/persona-lean.md` | Lean 6-field persona for working use and quick handoffs |
| `templates/persona-negative.md` | Negative persona template: who NOT to target and why |
| `templates/cluster-personas.py` | Python script: regex-based first-draft trait clustering from transcript directory |
