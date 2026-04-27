# AI Plugin Ecosystem

## Summary

Figma AI plugins (Magician, Automator, Content Reel, Stark, Similayer, Diagram) automate repetitive design tasks within the Figma canvas. Critically, agents cannot trigger plugin runs programmatically — the Figma REST API is the actual agent integration surface. Use plugins for human-driven workflows; use the REST API for automated pipelines.

## Why

Most Figma AI plugins have no CLI or webhook interface; they operate only inside the Figma desktop/browser UI. An agent that "runs a plugin" always requires a human at the keyboard. The REST API offers a deterministic, repeatable integration surface for accessibility audits, content injection, and style extraction — the tasks designers most want to automate.

## When To Use

- Automating repetitive Figma operations (renaming layers, bulk style changes, exporting assets) via Figma REST API
- Running accessibility audits across a design file before handoff (contrast ratio computation from REST API data)
- Generating placeholder content at scale and pushing it via Figma REST `PATCH /v1/files/{key}/nodes`
- Evaluating which plugin combination covers a team's workflow gaps before investing in custom UXP development
- Running WCAG contrast checks externally without requiring the Stark plugin

## When NOT To Use

- Plugin output must be reproducible without human intervention — most AI plugins are not deterministic
- Design decisions require brand or strategic judgment — plugins are automation tools, not decision-makers
- A plugin relies on a third-party AI API that could expose proprietary design data to external servers
- The design system is unstable — plugins that reference tokens/styles break when foundations change

## Content

| File | What's inside |
|------|---------------|
| `content/01-plugin-catalog.xml` | Plugin catalog, agent integration boundary, REST API rules |
| `content/02-accessibility-pattern.xml` | WCAG contrast check pattern, gotchas, service catalog |

## Templates

| File | Purpose |
|------|---------|
| `templates/contrast-check.py` | WCAG contrast ratio checker using Figma REST API data |
| `templates/accessibility-audit-prompt.txt` | Claude prompt for auditing Figma file JSON for contrast violations |
