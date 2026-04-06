# faion-media-ops

Media operations skill: setup and run any media resource — Telegram channels, news sites, podcasts, newsletters, social media.

## Entry Point

`/faion-media-ops` or via `/faion-net`

## What It Does

1. **Discovery** — interviews user to understand media resource requirements
2. **Setup** — creates project structure, scripts, prompts, site, channels
3. **Content** — generates initial content batch with parallel agents
4. **Automation** — configures `/loop` + sub-agents for ongoing operation
5. **Operations** — monitoring, analytics, content calendar management

## Supported Media Types

| Type | Channels | Site | Automation |
|------|----------|------|------------|
| **telegram-news** | TG channels (multi-lang) | Gatsby/SSG site | /loop + sub-agents |
| **newsletter** | Email (subscribe form) | Landing page | Scheduled sends |
| **podcast** | TG + RSS feed | Episode pages | Script generation |
| **social-media** | TG + X/Twitter | Link hub | Cross-posting |
| **blog** | — | Full blog site | Content calendar |

## Methodologies

1. **Media Resource Setup** — from requirements to running system
2. **Character/Brand Creation** — AI persona, voice, visual identity
3. **Content Pipeline** — research → write → image → publish
4. **Multi-Channel Distribution** — site + TG + email + social
5. **Automated Operations** — scheduling, dedup, state, silent hours

## Reference Implementation

`~/workspace/projects/neromedia-faion-net/` — full working example with 86 articles, 2 TG channels, Gatsby site, image generation pipeline.

## Files

- `README.md` — this file
- `skill.md` — full skill instructions (loaded by Claude Code)
- `templates/` — reusable project templates
- `methodologies/` — detailed methodology guides
