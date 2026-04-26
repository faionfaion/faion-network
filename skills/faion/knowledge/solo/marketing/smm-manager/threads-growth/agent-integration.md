# Agent Integration — Threads Growth

## When to use
- Generating daily Threads post batches (5-7 posts) across the conversation-starter types in the README (hot takes, this-or-that, fill-in-blank, experience prompts)
- Drafting high-quality reply templates for a specific niche — to be adapted and sent by a human
- Planning a cross-platform content flow: which Instagram content to cross-post to Threads and what adaptations to make
- Writing a Month 2-3 optimization plan: which post types to double down on, which accounts to build relationships with
- Repurposing Twitter/X thread content into Threads-native conversational format

## When NOT to use
- Automated posting or replying — Threads has no official third-party API for posting as of 2026; all posting is manual
- Engagement pod coordination — Threads community norms strongly penalize inauthentic-feeling engagement
- Generating posts that mimic Threads trends without knowing current platform culture — training data lags real-time Threads discourse
- Long-form content — Threads rewards punchy, conversational posts; agent-generated long posts will underperform

## Where it fails / limitations
- Threads API access is extremely limited (Meta opened a read-only API in 2024); agent cannot post, read DMs, or pull analytics programmatically
- Platform tone is more casual and conversational than LinkedIn or even Twitter — agent output tends toward polished and formal; heavy editing required
- Cross-post adaptation is a heuristic process; there is no reliable rule for what Twitter content translates to Threads successfully
- Reply personalization requires knowing the specific post being replied to; generic reply templates lose authenticity on contact
- Threads growth metrics are not publicly benchmarkable — the README's "starting/growing/established" thresholds are community estimates, not platform data

## Agentic workflow
Use the agent as a content ideation and adaptation engine, not an execution tool. Given the week's content pillars and ICP, a single Sonnet call produces 20-30 post draft options across all conversation-starter types. The human selects, edits for personal voice, and posts manually. For cross-platform adaptation, feed the agent the original Twitter or Instagram caption and ask it to rewrite in Threads tone (conversational, lower-stakes, question-ending). No agent subagents are needed for posting; all execution is human.

### Recommended subagents
- `faion-sdd-executor-agent` — for planning and tracking the Month 2-3 Threads growth SDD tasks

### Prompt pattern
```
You are a Threads content strategist for <niche>. ICP: <icp>. Tone: casual, direct, curiosity-driven.

Generate 20 Threads post drafts. Distribute across:
- 5 hot takes ("Unpopular opinion: ...")
- 5 this-or-that questions
- 5 fill-in-the-blank prompts
- 3 personal experience stories (2-3 sentences)
- 2 predictions for <year>

Each post: max 300 characters, no hashtags, end with an implicit or explicit invitation to respond.
```

```
Adapt this Twitter/X thread for Threads:
<twitter_thread>

Rules:
- Shorten to 1-3 posts max
- Remove thread numbering
- Make it conversational, not declarative
- Add a genuine question at the end
- Remove any promotional language
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Meta Graph API (Threads) | Read public Threads posts and basic profile data | https://developers.facebook.com/docs/threads |
| `requests` (Python) | Call Threads API endpoints | `pip install requests` |
| Buffer | Schedule Threads posts (added Threads support 2024) | https://buffer.com/threads |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Threads (Meta) | SaaS | Partial (read API) | Official API is limited; write access via Meta partnership only |
| Buffer | SaaS | Yes (API) | Added Threads scheduling in 2024; basic analytics |
| Metricool | SaaS | Yes (API) | Threads analytics + scheduling where API permits |
| Later | SaaS | Partial | Limited Threads support; check current API status |
| Meta Business Suite | SaaS | Yes (Graph API) | Threads insights at account level |

## Templates & scripts
See `templates.md` for Hot Take, Question, and Story post templates.

```python
# Adapt Twitter thread to Threads-native format
def adapt_for_threads(tweets: list[str], max_posts: int = 3) -> list[str]:
    """
    Takes a list of tweet strings (thread) and produces max_posts
    Threads-native posts. Strips thread numbers, truncates, adds question.
    Agent should then refine each output for tone.
    """
    import re
    combined = " ".join(tweets)
    # Strip tweet numbering (1/, 2/, etc.)
    cleaned = re.sub(r"\d+/", "", combined).strip()
    # Split into chunks of ~280 chars at sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    posts, current = [], ""
    for s in sentences:
        if len(current) + len(s) < 280:
            current += " " + s
        else:
            if current:
                posts.append(current.strip())
            current = s
        if len(posts) >= max_posts - 1:
            break
    if current:
        posts.append(current.strip())
    if posts:
        posts[-1] += "\n\nHave you experienced this?"
    return posts[:max_posts]
```

## Best practices
- Post volume on Threads (5+ posts/day) is higher than any other text platform; batch-generate 35+ posts per week but only post what feels genuinely on-voice
- Replies to large accounts drive disproportionate discovery — one early, thoughtful reply on a 100K-follower post outperforms 5 standalone posts
- Threads rewards authenticity signals: genuine disagreement, admitted uncertainty, and follow-up questions outperform polished takes
- Do not include links in posts — Threads does not render links and promotional posts are heavily suppressed
- Cross-promote from Instagram Stories by sharing a specific Threads post with "join the conversation on Threads" — this is the fastest follower import mechanism
- Build reply conversations by replying to your own posts with follow-up thoughts; algorithmic signals treat thread-style self-replies as active conversations

## AI-agent gotchas
- **Tone overfitting:** Agent defaults to polished, authoritative voice; Threads culture rewards rough edges and genuine curiosity — always rewrite agent output before posting
- **No posting API:** Agent cannot schedule or post to Threads autonomously; all output is drafts for human posting
- **Analytics gap:** Threads provides almost no exportable analytics data; growth measurement requires manual tracking in a spreadsheet
- **Platform immaturity:** Threads features and algorithms were still evolving rapidly as of early 2026; agent knowledge of "best practices" should be treated as provisional
- **Instagram account dependency:** Threads account is tied to Instagram; any Instagram account issue (ban, restriction) affects Threads access — do not treat them as independent

## References
- https://help.instagram.com/788669719351544 — Threads Help Center
- https://developers.facebook.com/docs/threads — Threads API docs
- https://blog.hootsuite.com/threads-app/
- https://sproutsocial.com/insights/threads-app/
