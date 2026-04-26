# Agent Integration — Reddit Marketing

## When to use
- Researching which subreddits your ICP actively participates in, before any posting
- Drafting long-form value posts (guides, breakdowns, case studies) for human review and posting
- Analyzing top-performing posts in target subreddits to identify format and tone patterns
- Writing AMA answers in bulk when a live AMA is scheduled and common questions are known in advance
- Monitoring brand/product mentions across subreddits via API polling

## When NOT to use
- Posting directly to Reddit — agents must not post autonomously; Reddit's anti-spam systems flag non-human posting patterns
- Building karma on a real account — agents cannot simulate genuine community participation
- Responding to live comments during an AMA — latency and context sensitivity require a human
- Any situation requiring multiple Reddit accounts — violates Reddit's terms of service
- Subreddits with "no self-promotion at all" rules — there is no compliant agent workflow

## Where it fails / limitations
- Reddit's API (after 2023 changes) has rate limits and requires OAuth; free tier is restricted
- Subreddit rules vary wildly and change without notice; agents cannot track rule changes in real time
- Cultural tone is hyper-local to each subreddit; generated posts sound generic without genuine community immersion
- Upvote/downvote outcomes are unpredictable; agents cannot optimize for virality on Reddit
- Reputation damage from a single spammy post is permanent and searchable — risk is asymmetric

## Agentic workflow
The safe agent workflow for Reddit marketing is research-and-draft only. An agent can analyze the top 50 posts in a target subreddit via the Reddit API, extract format patterns (title structure, content length, list vs. prose ratio), and produce a post draft for human review. A separate agent pass can check the draft against subreddit rules (scraped from the sidebar/wiki). The human then posts manually, responds to comments, and reports back on engagement for the next iteration.

### Recommended subagents
- No dedicated Reddit agent exists in the current agents/ directory
- Use a research subagent role: pull subreddit post data via Reddit API, summarize patterns, output structured brief
- Use a content subagent role: given the brief, draft a long-form guide or case study post

### Prompt pattern
```
Analyze the following 20 Reddit post titles and scores from r/[SUBREDDIT].
Identify:
1. Top 3 title formats that correlate with high scores
2. Average post length (word count) of top 10 posts
3. Whether lists, prose, or mixed format dominates
4. Topics that recur across high-scoring posts

Posts (title | score | comments):
{{POST_DATA}}

Output as JSON: {"title_formats": [...], "avg_length": N, "dominant_format": "...", "top_topics": [...]}
```

```
Write a Reddit guide post for r/[SUBREDDIT] on the topic "[TOPIC]".
Rules: no self-promotion, no links in body, include TL;DR.
Style: conversational, first-person, specific examples with numbers.
Target length: 600-900 words.
The author runs [product] but does not mention it.
End with: "Happy to answer questions in the comments."
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `praw` (Python) | Reddit API wrapper — read posts/comments, OAuth | `pip install praw` / praw.readthedocs.io |
| `pushshift` (archive) | Historical Reddit data access (limited post-2023) | pushshift.io (check current status) |
| `redditdl` | Download post content for offline analysis | `pip install redditdl` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit API (official) | SaaS | Yes — OAuth REST | Rate-limited; requires app registration; read is reliable |
| GummySearch | SaaS | Partial — no API | Best subreddit audience research UI; manual only |
| Subreddit Stats | OSS web | No API | Useful for size/growth data; scrape only |
| Later for Reddit | SaaS | Partial | Scheduling only; karma requirements still human-managed |
| Brand24 | SaaS | Partial — webhooks | Monitors brand mentions including Reddit; alerting API |
| Mention.com | SaaS | Partial — REST API | Similar to Brand24; Reddit mention alerts |

## Templates & scripts
See `templates.md` for AMA post, guide post, and milestone post templates.

Minimal PRAW script to pull top posts from a subreddit for analysis:

```python
import praw, os

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_SECRET"],
    user_agent="research-bot/1.0",
)

subreddit = reddit.subreddit("SaaS")
posts = []
for post in subreddit.top(time_filter="month", limit=50):
    posts.append({
        "title": post.title,
        "score": post.score,
        "comments": post.num_comments,
        "url": post.url,
        "flair": post.link_flair_text,
    })

import json
print(json.dumps(posts, indent=2))
```

## Best practices
- Always read the subreddit's sidebar rules AND wiki before drafting any post; agents should be given this text as context
- Draft posts at least 48 hours in advance to allow a human to review tone and fact-check numbers
- Milestone posts ("I hit $10K MRR") perform better without a product link in the body — only mention it if directly asked in comments
- One subreddit per post; cross-posting the same content is detectable and damages reputation permanently
- The 10:1 ratio (10 value contributions per 1 self-promotional mention) is a minimum floor, not a target
- Monitor the post for the first 2 hours after publishing — early engagement velocity determines algorithmic reach

## AI-agent gotchas
- PRAW returns deleted posts and removed comments as `[deleted]` / `[removed]` — filter these before feeding data to an LLM
- Agents will sometimes include subtle product mentions that violate subreddit rules; always explicitly instruct "zero product mentions" and verify manually
- Reddit post tone is distinct from blog tone — generated posts that read like blog articles get downvoted for sounding corporate
- Do not use agents to generate comments — comment-level personalization requires reading the full thread context, which is too variable
- LLM-generated AMA answers tend to be comprehensive but impersonal; inject specific anecdotes manually before posting

## References
- https://www.reddit.com/wiki/selfpromotion/ (official self-promotion guidelines)
- https://praw.readthedocs.io/en/stable/
- https://gummysearch.com/ (subreddit audience research)
- https://subredditstats.com/ (subreddit size and growth data)
