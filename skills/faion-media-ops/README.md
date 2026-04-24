# faion-media-ops

Media Pipeline Factory: build and operate complete AI media publishing pipelines.
All outlets managed centrally by **media-manager** (@nero_media_manager_bot).

## Entry Point

`/faion-media-ops` or via `/faion-net`

## What It Does

| Phase | Action | Output |
|-------|--------|--------|
| 1. Discovery | Structured interview (8 questions) | Requirements spec |
| 2. Propose | Suggest architecture + content plan | Approved blueprint |
| 3. Scaffold | Create project from templates | Full project structure |
| 4. Infrastructure | TG channel, DNS, nginx, Gatsby | Running infrastructure |
| 5. Content | Generate seed articles batch | 10-20 initial articles |
| 6. Register | Add to media-manager + landing page | Centralized management |
| 7. Iterate | Review, improve, expand | Evolving media |

## Pipeline Complexity Levels

| Level | Stages | LOC | Best For |
|-------|--------|-----|----------|
| Minimal | 5 | ~500 | Simple blog, single topic |
| Standard | 8 | ~1200 | News outlet, moderate volume |
| Full | 12+ | ~2500 | Professional multi-lang media |

## Active Outlets (4)

| Project | Type | TG | Languages | Pipeline |
|---------|------|----|-----------|----------|
| neromedia-faion-net | AI/tech news | 8 channels | 8 (EN + 7 translations) | Full (15 stages) |
| pashtelka-faion-net | UA diaspora in PT | @pashtelka_news | 1 (Ukrainian) | Standard (11 stages) |
| longlife-faion-net | Health & longevity | @long_life_media | 1 (Ukrainian) | Standard (11 stages) |
| ender-faion-net | Roblox for kids | @ender_faion_ua + @ender_faion_en | 2 (UA + EN) | Standard (12 stages) |

## Central Control Plane

`~/workspace/projects/media-manager-faion-net/` manages all outlets:
- **Bot:** @nero_media_manager_bot — 20 commands (status, generate, publish, ask, fix, etc.)
- **Dashboard:** media-manager.faion.net — landing page with live data
- **Scheduler:** cron every minute — queue processing, health monitoring, morning briefing
- **Security:** 10 guardrails (injection detection, rate limiting, audit logging)
- **Agent:** Claude SDK integration (ask, analyze, fix, improve)

## Key Patterns (extracted from production)

- **SDK**: structured_query (no tools, JSON) + agent_query (with tools, text)
- **Prompts**: inline strings or Jinja2 XML templates with ===SPLIT=== marker
- **Review loop**: min 1 revision, max 3 cycles, structured feedback
- **Batch generation**: editorial plan → loop topics → single deploy
- **TG publishing**: text links (not buttons), OG preview, silent mode
- **State**: JSON files for plans, teasers, summaries, run reports
- **Characters**: each outlet can have named characters with distinct voices
- **Image generation**: OpenAI gpt-image-1, character-consistent visuals
- **Scheduling**: media-manager handles all cron, NOT individual crontabs

## Files

| Path | Purpose |
|------|---------|
| `skill.md` | Full skill instructions with interview + process |
| `templates/pipeline/` | Python code templates (SDK, context, stages) |
| `templates/prompts/` | XML prompt templates + JSON schemas |
| `templates/gatsby/` | Static site templates (Gatsby 5) |
| `templates/scripts/` | Cron runner, TG sender, state management |

## Monitoring

- Health checks: `~/workspace/scripts/media-monitoring-checklist.md`
- Operations guide: `~/workspace/scripts/media-healthcheck-guide.md`
