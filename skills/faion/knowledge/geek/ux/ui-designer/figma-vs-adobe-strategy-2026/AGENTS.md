# Figma vs Adobe Strategy 2026

## Summary

A structured decision methodology for choosing between Figma and Adobe Creative Cloud as the primary design platform for a team. The methodology produces a scored recommendation document based on team size, task types, budget, and agent-automation requirements. The optimal 2026 stack for most product teams is Figma (design, collaboration, handoff) + Firefly API (asset generation) — they are not mutually exclusive. Revisit the decision every 6 months; both platforms ship major capability changes at their annual conferences.

## Why

Figma and Adobe serve different strengths: Figma excels at collaboration, developer handoff, and API-first automation; Adobe CC excels at visual asset creation, video, and enterprise licensing. Choosing the wrong platform for a team's primary workflow creates friction and forces round-trips between tools. The comparison goes stale quarterly — any analysis older than 6 months may be misleading.

## When To Use

- Conducting a toolchain audit for a product team deciding which design platform to standardize on
- Evaluating whether to migrate an existing Adobe XD or Photoshop workflow to Figma
- Advising a solopreneur or small team on which subscription gives the best agent-automation surface
- Documenting a multi-tool design stack decision for a project AGENTS.md

## When NOT To Use

- The team is already fully committed to one platform — comparison adds friction, not value
- The decision is driven purely by individual tool features rather than workflow fit
- The client dictates tooling — tool choice is not up for internal deliberation in that context
- Budget or expertise constraints make the comparison moot

## Content

| File | What's inside |
|------|---------------|
| `content/01-comparison.xml` | Market position comparison, 2026 strategy focus areas, decision rules |
| `content/02-agent-integration.xml` | Agent workflow for toolchain audits, scoring prompt, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoring.py` | Weighted scoring script for Figma vs Adobe with team-type presets |
| `templates/toolchain-audit-prompt.txt` | Claude prompt for scoring a team's workflow against both platforms |
