# Agent Integration — Threads Basics

## When to use
- Standing up a brand or founder presence on Meta Threads while leveraging an existing Instagram audience.
- Auditing an account that cross-posts from X/Twitter and underperforms on Threads.
- Drafting daily content packs (3-10 posts) for a SMM operator who already has voice guidelines.
- Hot-take and conversation-starter ideation, where engagement bait is acceptable for the brand.
- Bootstrapping a new niche account that needs cadence + format scaffolding before going manual.

## When NOT to use
- Audience does not overlap with Instagram's demographic (e.g. enterprise security buyers — use LinkedIn instead).
- Brand voice forbids "hot takes", personal stories, or unmoderated conversation.
- The team has zero capacity for replies; Threads' algorithm rewards reply velocity, agents alone cannot sustain it.
- Regulated industries (finance, healthcare) where each post needs human compliance review and the cadence is incompatible.

## Where it fails / limitations
- No official scheduling API at the start of 2026; tools that "schedule" Threads use unofficial automation that breaks regularly.
- Algorithm rewards conversation, not posting volume — agents that only post (do not reply) plateau within weeks.
- Cross-posting from X verbatim is a known anti-pattern; agents must rewrite, not duplicate, which costs tokens.
- Engagement metrics in native insights are limited; attribution to revenue is near-zero for organic Threads.
- Trend-jacking has a 24-48h half-life; agents running on slow cadence (daily) miss the window.

## Agentic workflow
A Claude subagent can ideate the daily post pack from a content pillar mix, rewrite Twitter/X posts into native Threads voice, and draft reply scaffolds for the operator to send manually. The agent should NOT auto-post: there is no stable scheduling API, and Meta is aggressive about automation detection. Best division of labor — agent drafts and ranks 20 candidates, operator picks 7-10 and posts manually within the day's prime windows.

### Recommended subagents
- `faion-social-agent` (suggested per-skill agent referenced in README) — sonnet for daily ideation, opus when developing a new content pillar strategy, haiku for rewrite/format-only tasks.
- `faion-content-marketer` subagent (cross-skill) — when Threads is one channel in a multi-channel content brief.
- A reply-scaffold subagent — given a target post, drafts 3 candidate replies in brand voice; never sends.

### Prompt pattern
```
Brand voice: <attached>. Pillars: opinions (40%), value (30%), questions (20%),
personal (10%). Yesterday's top post: <text+stats>. Draft 12 candidate posts
for tomorrow, each <500 chars, with the pillar tag and a hook score (1-5).
No emojis unless brand voice file allows them.
```

```
Rewrite this X/Twitter thread (5 posts) into 1 standalone Threads post +
1 optional reply continuation. Match Threads' conversational register:
question hook, personal anchor, no link, single CTA at the end.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `instagrapi` (Python) | Unofficial Instagram/Threads access — read only, breakage risk | https://github.com/subzeroid/instagrapi |
| `threads-api` (Node, community) | Read public posts; rate-limited and unstable | https://github.com/junhoyeo/threads-api |
| `imagemagick` / `ffmpeg` | Prep optional 9:16 visuals for Threads posts | https://imagemagick.org/ , https://ffmpeg.org/ |
| `pandoc` | Convert markdown content packs into operator-friendly docs | https://pandoc.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Threads API (Graph) | SaaS (official) | Partial | Posting + insights for approved Meta apps; OAuth required, limited rollout |
| Buffer | SaaS | Yes (API) | Native Threads scheduling via official integration |
| Hootsuite | SaaS | Yes (API) | Native Threads support since 2024 |
| Later | SaaS | Yes (API) | Threads scheduling, link-in-bio |
| Typefully | SaaS | Yes (API) | Better for cross-posting X→Threads with rewrites |
| Metricool | SaaS | Yes (API) | Threads analytics + scheduling |
| Postiz (OSS) | OSS | Yes (self-hosted) | OSS scheduler with Threads support — operator hosts |

## Templates & scripts
See `templates.md` for daily post, multi-post thread, and bio templates. Inline ideation helper:

```bash
#!/usr/bin/env bash
# threads-pack.sh — emit 12 ideation prompts pinned to a pillar mix.
set -euo pipefail
PILLARS=(opinion opinion opinion opinion value value value question question personal personal curated)
for P in "${PILLARS[@]}"; do
  echo "[$P] write a candidate post in brand voice (max 500 chars), 1 hook + 1 line + 1 question"
done
```

## Best practices
- Cap agent-generated posts at 50% of weekly volume; the other 50% comes from operator's lived context (replies, real-time reactions).
- Keep one human-written reply per outbound post — replies drive the algorithm more than the post itself.
- Tag every draft with its content pillar; without tags, the agent drifts toward whatever style won last week.
- Rotate prime windows weekly (8-10 / 12-14 / 18-21) and let the agent A/B test cadence within those slots.
- Strip URLs from agent output unless explicitly allowed; Threads suppresses link-heavy posts.
- Maintain a "do not post" list (tickers, regulated claims, named competitors) and inject it into every prompt as a hard constraint.

## AI-agent gotchas
- The agent will reuse identical hooks across drafts ("Hot take:", "Honest question:"). Force diversity via banned-bigram lists.
- Engagement-bait phrasing flagged by Meta drops reach; instruct the agent to avoid "comment X for Y", "tag a friend", "follow for more".
- Trend-jacking requires fresh data; if the agent has stale knowledge it confidently posts dead trends. Inject the day's trending topics as context.
- LLMs are bad at character-count limits — always include `<500 chars` in the prompt and validate post-generation.
- Cross-posting agents lose Twitter-specific irony; force a register-shift step ("rewrite for warmth").
- No emoji rule must be repeated in every prompt; agents default to peppered emojis.
- Replies generated by an agent and posted at scale read as bots; operator should always be the human reading and sending.

## References
- Meta, "Threads API documentation" — https://developers.facebook.com/docs/threads
- Meta Newsroom, "Threads launch and milestones" — https://about.fb.com/news/tag/threads/
- Buffer, "Threads marketing guide" — https://buffer.com/resources/threads/
- Hootsuite, "How to use Threads for business" — https://blog.hootsuite.com/threads/
- Postiz OSS scheduler — https://github.com/gitroomhq/postiz-app
