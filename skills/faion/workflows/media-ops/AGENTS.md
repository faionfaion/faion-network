---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
content_id: 9b69e99f0b6a7925
success_criteria:
  - Discovery interview answers (Phase 1) cover every required question group before scaffolding starts.
  - The new outlet's project tree matches the canonical scaffold in `content/05-scaffold-structure.xml`.
  - Outlet is registered with the central media-manager (cron, monitoring, bot commands) before content goes live.
  - Pipeline runs end-to-end at least once (Phase 6 seed content) before the workflow exits.
---

# Media-Ops Workflow

## Summary

Build a complete AI media publishing pipeline from scratch (Telegram channel + static site + automation): discovery interview → propose format → scaffold project → setup infrastructure → seed content → register in central media-manager → iterate. Seven phases, four production reference implementations (neromedia, pashtelka, longlife, ender).

## Why

Media outlets are built repeatedly with the same shape. Without a workflow each one drifts: different folder structure, missing review loops, ad-hoc cron entries on the host, no central registration. This workflow encodes the centralized pattern proven across the four reference outlets, so a new outlet inherits monitoring, scheduling, and operator commands by construction.

## When To Use

- New media outlet (Telegram + site, or just Telegram).
- AI-driven content pipeline (RSS or web search → LLM → publish).
- Multi-language news bot.
- Branded blog with auto-image generation.

## When NOT To Use

- Manual blog with no automation.
- Single-post project (overhead too high).
- Modifying an existing outlet — use that outlet's own AGENTS.md instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle, role split, reference outlets, language convention. |
| `content/02-phases.xml` | The seven phases with trigger, output, and constraints each. |
| `content/03-discovery-interview.xml` | Eight interview question groups with options and rules. |
| `content/04-pipeline-complexity.xml` | Three complexity levels (Minimal, Standard, Full) with stages and LOC budgets. |
| `content/05-scaffold-structure.xml` | Canonical project tree plus SDK, prompt-split, review-loop, batch, and TG-link patterns. |
| `content/06-templates-index.xml` | Templates index by category (pipeline, prompts, schemas, gatsby, admin, scripts). |
| `content/07-anti-patterns.xml` | Process and operations anti-patterns (rejection-on-sight). |

## Templates

| Folder | Purpose |
|--------|---------|
| `templates/pipeline/` | Python pipeline package skeleton (sdk, context, config, cli, stages, modes). |
| `templates/prompts/` | Jinja2 prompt templates with system / ===SPLIT=== / task envelope. |
| `templates/schemas/` | JSON schemas validating each structured_query stage output. |
| `templates/gatsby/` | Gatsby 5 static site starter with markdown content pipeline. |
| `templates/admin/` | Optional Flask admin panel for review-mode outlets. |
| `templates/scripts/` | Cron entry point, Telegram sender, state utility. |

## Related

- `.aidocs/conventions/workflows/workflow-spec.md` — workflow authoring spec.
- `skills/faion/workflows/sdd-batch-orchestrator/` — sibling workflow, reference impl for content/* shape.
- `~/workspace/projects/media-manager-faion-net/` — central control plane (cron, monitoring, bot commands).
- `~/workspace/projects/neromedia-faion-net/` — reference outlet (8 languages, 8 channels).
- `~/workspace/projects/pashtelka-faion-net/` — reference outlet (single channel, diaspora).
- `~/workspace/projects/longlife-faion-net/` — reference outlet (health, mascot Vita).
- `~/workspace/projects/ender-faion-net/` — reference outlet (Roblox, kids, bilingual).
