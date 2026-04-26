# Agent Integration — Community Building

## When to use
- Drafting community launch materials: welcome messages, guidelines, onboarding sequences, ritual prompts
- Generating member invitation scripts tailored to specific ICP profiles
- Producing weekly ritual content (standup prompts, AMA question lists, challenge briefs, roundup newsletters)
- Analyzing community health metrics from platform exports (Discord, Circle, Slack) to identify churn risk
- Writing community guidelines and moderation playbooks for a specific community type

## When NOT to use
- Real-time community moderation — requires human judgment on nuance, context, and tone
- Automated mass-invitation campaigns — platforms detect and ban bots; personal invitations require human send
- Replacing the community manager role entirely — member trust is built through perceived human presence
- Communities with fewer than 10 seeded members — agent-generated ritual content in an empty community reads hollow

## Where it fails / limitations
- Agent cannot observe actual member behavior; it can only analyze exported data — real engagement signals require human observation
- Ritual design must be adapted to platform-specific features (Discord channels vs Circle spaces vs Slack threads); agent output is platform-agnostic by default
- Member matching and pairing logic requires member profile data the agent typically does not have access to
- AMA curation requires knowing which questions are genuinely interesting to the community — generic question lists produce weak AMAs
- Community guidelines are starting points; the real guidelines emerge from moderation decisions over weeks of operation

## Agentic workflow
Use the agent primarily for content production and analysis, not community management. A drafting subagent generates a month of ritual prompts and newsletter templates given the community purpose and member profile. A separate analysis pass runs on exported member activity data (DAU/MAU, post rate, response time) to flag health score changes. Human community manager reviews all output and decides what to post. For launch, the agent generates the full onboarding sequence and guidelines in one pass from the README.md framework.

### Recommended subagents
- `faion-sdd-executor-agent` — execute community launch SDD tasks in sequence
- `password-scrubber-agent` — sanitize member email/name data before feeding into analysis prompts

### Prompt pattern
```
You are a community strategist. Given:
- Community purpose: <purpose>
- Platform: <platform>
- Member type: <member_type>
- Stage: seed / nurture / scale

Generate: (1) 4-week ritual calendar with daily/weekly/monthly cadence, (2) welcome message for new members, (3) community guidelines (adapt from template), (4) first 5 conversation starters.
```

```
Analyze this community health data export:
<csv_or_json_data>

Identify: (1) members at churn risk (low activity, no posts in 14+ days), (2) top contributors to spotlight, (3) which rituals have lowest participation. Recommend 3 actions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `discord.py` | Read channel stats, member lists, message counts | `pip install discord.py` / https://discordpy.readthedocs.io |
| `slack-sdk` | Export Slack channel analytics, member activity | `pip install slack-sdk` / https://slack.dev/python-slack-sdk |
| `orbit-cli` | Community analytics across platforms | https://orbit.love/developers |
| `common-room` API | Cross-platform member activity aggregation | https://www.commonroom.io/docs |
| `circle-api` | Circle community REST API | https://api.circle.so |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Discord | SaaS | Yes (Bot API) | Real-time events, member data, channel analytics |
| Slack | SaaS | Yes (REST API) | Message counts, member activity; analytics limited on free plan |
| Circle | SaaS | Yes (REST API) | Member management, spaces, post creation |
| Orbit | SaaS | Yes (REST API) | Cross-platform community analytics; member scoring |
| Common Room | SaaS | Yes (REST API) | Unified member activity from Discord/Slack/GitHub/Twitter |
| Memberful | SaaS | Yes (REST API) | Paid membership management |
| Zapier | SaaS | Yes (triggers) | Automate welcome flows on new member join events |
| Beehiiv / Substack | SaaS | Yes (API) | Weekly community newsletter distribution |

## Templates & scripts
See `templates.md` for Community Launch Checklist and Community Guidelines Template.

```python
# Score community health from Circle or Discord export
# Expects list of dicts with keys: member_id, posts_30d, replies_30d, last_active_days_ago

def health_score(members):
    total = len(members)
    active = sum(1 for m in members if m["last_active_days_ago"] <= 30)
    posters = sum(1 for m in members if m["posts_30d"] > 0)
    dau_mau = active / total if total else 0
    post_rate = posters / total if total else 0
    score = (dau_mau * 0.5 + post_rate * 0.5) * 100
    churn_risk = [m for m in members if m["last_active_days_ago"] > 14 and m["posts_30d"] == 0]
    return {
        "health_score": round(score, 1),
        "dau_mau": round(dau_mau, 2),
        "post_rate": round(post_rate, 2),
        "churn_risk_count": len(churn_risk),
        "churn_risk_members": [m["member_id"] for m in churn_risk[:10]],
    }
```

## Best practices
- Seed the community with 5-10 planted conversations before inviting the first wave — an empty platform kills momentum before it starts
- Rituals must be low-friction: a "what are you working on today?" standup beats a weekly essay prompt for participation rate
- The first 48 hours after a new member joins are the highest-churn window — trigger a personal welcome within that window
- Identify and invest in 3-5 ambassadors early; they create a self-sustaining culture before the founder steps back
- Do not open new channels/spaces until existing ones are active — too many empty spaces signal low community health
- Track reply rate per post, not just post count; a community where 30% of posts get zero replies is dying

## AI-agent gotchas
- **Platform rate limits:** Discord bot API and Circle API have per-minute call limits; batch analytics pulls must be throttled
- **Privacy in analysis:** Member activity data often contains email addresses and real names — scrub before feeding into external LLM calls
- **Ritual fatigue:** Agent-generated ritual templates repeated verbatim week after week feel mechanical; vary wording and theme even if the structure repeats
- **Moderation edge cases:** Agent moderation policy documents will not cover every real scenario; the first novel moderation call must be made by a human and then documented as precedent
- **Platform churn:** Threads-linked communities (Threads/Instagram) have different feature sets than established platforms; agent advice based on Discord/Slack may not translate

## References
- https://communityroundtable.com/resources/ — Community Roundtable research
- https://cmxhub.com/ — CMX community management guides
- https://orbit.love/blog — Community analytics and health scoring
- https://review.firstround.com/build-a-community-not-an-audience
- Mahar, D. & Spier, T. (2021). *The Business of Belonging*. Wiley.
