# Agent Integration — Community-Led Growth (CLG)

## When to use
- Acquisition channels (paid ads, SEO) are degrading and CAC is rising — need an owned-audience moat with measurable retention lift.
- Product has natural sharing, template, or peer-help surface (design tools, no-code builders, dev tools, learning products).
- You already have 50–500 power users you can convert into a seeded community before opening it publicly.
- Building a 2026-style micro-community (≤2K members, high engagement) rather than a large vanity Discord.

## When NOT to use
- Pre-PMF products with < 50 active users — there is no community to seed; defer.
- Highly transactional products with no conversation surface (utility tools, one-shot purchases).
- Compliance-sensitive verticals (medical, financial advice) where moderation and liability risk exceed acquisition value.
- Solo-founder bandwidth-locked situations where moderation cannot meet the "consistent nurturing" bar in the README.

## Where it fails / limitations
- Methodology promises ROI numbers ("$6.40 per $1", "32% CAC reduction") sourced from CMX/McKinsey reports — these are aggregate; individual products often see 2–6 month payback only when value-aligned.
- Discord-as-default advice ages quickly: AI moderation tooling and platform ToS shift; verify before recommending any specific bot stack.
- Tokenized rewards section assumes regulatory comfort agents cannot evaluate; treat as opt-in only after legal review.
- "10K+ members with 1 mod via AI moderation" is best-case under tight category rules; realistic ratio is 1 mod per 1–2K active members.

## Agentic workflow
A CLG agent loop typically runs on a daily/weekly cron: a listener subagent ingests platform events (Discord/Slack/Reddit) into a structured store, a sentiment + topic subagent classifies them, an engagement subagent drafts member-spotlight posts, AMA prompts, and contributor-recognition messages, and an analytics subagent computes the McKinsey-style health metrics (DAU/MAU, retention, expansion). All outbound posts and DMs go through a human-approval gate; only metric reports and internal alerts post autonomously.

### Recommended subagents
- `community-listener` — polls Discord/Slack/Reddit APIs, normalizes events, stores to vector DB for topic clustering.
- `community-engagement-drafter` — generates spotlight posts, weekly digest, AMA questions from listener output; never auto-posts.
- `community-health-reporter` — computes DAU/MAU, retention, top-contributor list; produces weekly report card.
- `moderation-triage` — flags ToS violations, doxxing, spam for human mod review; only auto-deletes on high-confidence spam.

### Prompt pattern
```
You are community-engagement-drafter. Read knowledge/pro/marketing/conversion-optimizer/community-led-growth/README.md.
Input: { platform, last_7d_events, top_threads, top_contributors }.
Output JSON: { spotlight_post, ama_prompt, digest_bullets, recognition_dms[] }.
Mark each item draft=true; do NOT post.
```

```
You are community-health-reporter. Compute: DAU, WAU, MAU, DAU/MAU ratio, message volume per channel,
new-member D7 retention, top 10 contributors by reactions+replies.
Output a markdown table only. Flag any metric that dropped > 20% week-over-week.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `discord.py` / `discord-api-types` | Read messages, members, reactions; post via webhook with approval | https://discordpy.readthedocs.io/ |
| Slack `bolt-python` SDK | Event API, channel analytics, slash-command DM workflows | https://slack.dev/bolt-python/ |
| `praw` (Reddit) | Subreddit listening, modlog, saved-thread digest | https://praw.readthedocs.io/ |
| `circle.so` API | Course-creator community CRUD (members, posts, spaces) | https://api.circle.so/ |
| `commsor` / `orbit` (orbit.love) | Member graph + engagement scoring, ORBIT Levels | https://docs.orbit.love/ |
| `n8n` / Pipedream | No-code orchestration of cross-platform community events | https://docs.n8n.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Discord | SaaS | Yes — bots, webhooks, slash commands | Highest engagement (94 min/day per README); default for 2026 |
| Slack | SaaS | Yes — Events API + Bolt | Best for B2B; per-seat cost limits scale |
| Circle.so | SaaS | Partial — read API solid, automation paid tier | Owned community, less platform risk |
| Reddit | SaaS | Yes via PRAW | Public discovery; cannot own audience |
| Orbit / Commsor | SaaS | Yes | Member-health graph; agents can drive ORBIT Levels |
| Common Room | SaaS | Yes | Aggregates Discord+Slack+GitHub; good agent ingest source |
| Discourse | OSS | Yes — full REST API | Self-hosted, owned; less real-time than Discord |
| Mighty Networks | SaaS | Limited API | Works for course-creator CLG, weak for agent automation |

## Templates & scripts
Inline weekly health snapshot agents can run:

```python
# clg_health.py — minimal DAU/MAU + contributor digest
from collections import Counter
from datetime import datetime, timedelta, timezone

def compute_health(events):
    now = datetime.now(timezone.utc)
    d1 = now - timedelta(days=1)
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    dau = {e["user_id"] for e in events if e["ts"] >= d1}
    wau = {e["user_id"] for e in events if e["ts"] >= d7}
    mau = {e["user_id"] for e in events if e["ts"] >= d30}

    contributors = Counter(e["user_id"] for e in events if e["ts"] >= d7)
    top = contributors.most_common(10)

    return {
        "dau": len(dau),
        "wau": len(wau),
        "mau": len(mau),
        "dau_mau_ratio": round(len(dau) / max(len(mau), 1), 2),  # README target: 0.73 (Discord)
        "top_contributors": top,
    }

# Wire into discord.py / Slack Bolt event stream; emit to weekly report.
```

See `templates.md` and `examples.md` in this directory for community-launch checklist and platform-comparison tables.

## Best practices
- Seed before launch: 30+ "founding member" 1:1 invites with custom role + welcome thread; do this manually, not via bot.
- Codify a single concrete value drop per week (AMA, template release, behind-the-scenes) — agents can draft it, but a human ships it.
- Track the McKinsey-style trio: % MAU active, peer-help response rate, member-sourced revenue. Anything else is vanity.
- Use private channels for power users (ORBIT Level 3+) to retain them as the public space scales.
- Move conversations from Discord/Slack chat → searchable Discourse/forum for any thread that gets ≥10 replies — protects future SEO + onboarding.
- For 2026 micro-communities: cap public size or add a low-friction application step after ~1K members; the README's "2.3x engagement" lift dies above that.
- Recognize top contributors weekly with named call-outs; agent generates the draft, mod posts it.

## AI-agent gotchas
- LLMs will draft over-eager "we love you" community posts that read as corporate. Force a tone-check subagent against existing top member posts before any draft ships.
- Never let an agent auto-DM new members at scale — Discord/Slack ToS treats this as spam and platform bans cascade fast.
- Sentiment classifiers misread sarcasm and in-jokes that define healthy communities; require human mod review for any "negative sentiment" auto-flag.
- Tokenized-rewards advice in the README assumes 2026 regulatory comfort — agents must NOT mint, distribute, or advise on tokens without explicit human + legal sign-off.
- AMA / event scheduling agents should never commit external speakers' calendars — generate proposed slots, human confirms.
- Beware of moderation-loop hallucinations: agent flags a member as "spam", auto-mutes, member churns. Always require human approval for mute/ban; only auto-delete on classifier confidence > 0.95 AND keyword match.
- Don't conflate community size with health — the agent's KPIs must be DAU/MAU and contributor count, not member count.

## References
- `README.md` (this directory)
- CMX Community Industry Report 2026 — https://cmxhub.com/community-industry-report/
- McKinsey, Business Value of Online Communities — https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/the-business-value-of-online-communities
- David Spinks, "The Business of Belonging" (book) — community-led growth playbook
- Orbit Model docs — https://orbitmodel.com/
- Common Room community-led-growth guides — https://www.commonroom.io/blog/
