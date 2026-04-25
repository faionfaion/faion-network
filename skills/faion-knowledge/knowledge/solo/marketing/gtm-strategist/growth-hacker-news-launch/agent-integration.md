# Agent Integration — Hacker News Launch

## When to use
- Launching a developer tool, CLI, library, or OSS project to a technical audience
- Product has genuine technical novelty or an interesting engineering story to tell
- Author has existing HN karma and comment history (or plans to build it)
- Writing a technical deep-dive blog post that belongs on HN as an article, not just a Show HN
- Drafting the first comment for a Show HN post to maximize engagement quality

## When NOT to use
- Consumer app targeting non-technical users — HN audience is not representative and feedback will be skewed
- Product has no demo, requires signup to evaluate, or is not production-ready — HN commenters will try it immediately and harshly judge gaps
- Author has no HN account or < 2 weeks of comment history — a new account with only a self-promotional post will be flagged
- The product is primarily a no-code or AI wrapper with no novel engineering — HN values technical depth; shallow products receive hostile reception
- Marketing-led content (press releases, "exciting news" posts) — the community actively flags and downvotes promotional framing

## Where it fails / limitations
- HN traffic is typically a one-day spike; it does not convert to sustained organic search traffic the way a strong SEO article does
- Post ranking is a black box; timing, initial upvote velocity, and community mood all interact in ways agents cannot predict or simulate
- Agents cannot build HN karma or post history for you — participation must be done by a real person over weeks
- The HN audience is vocal about product flaws; an agent-drafted first comment cannot anticipate every technical critique in real-time
- HN's spam detection flags posts from new accounts, posts with identical IPs across multiple submissions, and coordinated upvoting — agents must not attempt to automate any of these

## Agentic workflow
Agents add value in two phases for HN launches: (1) pre-launch content preparation — given the product's technical stack, problem statement, and key design decisions, draft the Show HN title, first comment, and a supporting technical blog post following HN's preferred structure (problem → approaches considered → what was built → deep-dive → results → learnings); (2) post-launch comment response drafting — given incoming HN comments, draft factual, non-defensive responses that acknowledge critique and provide technical depth. Human must post all responses and should do a final tone review before any public comment.

### Recommended subagents
- `faion-content-agent` (referenced in README) — Show HN title variants, first comment, technical blog post structure
- A `hn-comment-responder-agent` could ingest a batch of HN comments and draft response options for each, flagged by type (bug, critique, question, feature request)

### Prompt pattern
```
You are preparing a Hacker News Show HN launch for [Product].

Technical context:
- What it does: [one sentence]
- Stack: [languages, frameworks, key libraries]
- Novel approach or interesting engineering decision: [description]
- Known limitations: [list]
- Demo URL (no signup required): [url]

Task:
1. Generate 5 Show HN title variants. Rules: descriptive, no marketing language, no superlatives, no "revolutionary/AI-powered/best". Format: "Show HN: [What it does] – [How/differentiator]"
2. Write the first comment (300-500 words) covering: why I built this, technical approach, current status, known limitations, specific feedback questions.
Rules: first-person, honest, technical, inviting critique.
Output: numbered titles + first comment in separate sections.
```

```
Here are HN comments on our Show HN post: [list of comments].
For each comment:
- Classify: bug_report / technical_critique / question / feature_request / praise / troll
- Draft a response (max 100 words): factual, non-defensive, first-person.
- Flag any comment that requires a code fix or factual correction before responding.
Output: structured list with classification + draft response per comment.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| HN Algolia API | Search past Show HN posts by keyword; research successful titles | https://hn.algolia.com/api |
| `hn-cli` (community) | Browse HN, check post status from terminal | https://github.com/rafaelrinaldi/hn |
| `curl` + HN Firebase API | Poll post score and comment count in real-time | https://github.com/HackerNews/API |
| Cloudflare Pages / Vercel CLI | Deploy fast-loading demo site before launch | https://developers.cloudflare.com/pages/framework-guides/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HN Algolia Search | OSS/Free | Yes — REST API | Research past Show HN patterns; no auth required |
| HN Firebase API | OSS/Free | Yes — REST API | Real-time post score polling; no write access |
| Cloudflare Pages | SaaS | Yes — CLI | Fast static hosting; essential for HN (page speed matters) |
| Vercel | SaaS | Yes — CLI | Alternative fast deployment for demo pages |
| Buttondown / Ghost | SaaS | Yes — API | Capture email subscribers from HN traffic spike |
| Plausible / Fathom | SaaS | Yes — API | Privacy-first analytics; HN audience blocks GA |

## Templates & scripts
See templates.md for: Show HN first comment template, technical blog post structure.

Inline script — research past successful Show HN posts for a keyword:

```python
import urllib.request, json

def search_show_hn(keyword: str, top_n: int = 10) -> list[dict]:
    """Search Algolia HN API for Show HN posts matching keyword, sorted by points."""
    query = urllib.parse.quote(f"Show HN {keyword}")
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=show_hn&hitsPerPage={top_n}"
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    return [
        {"title": h["title"], "points": h.get("points", 0), "url": f"https://news.ycombinator.com/item?id={h['objectID']}"}
        for h in sorted(data["hits"], key=lambda x: x.get("points", 0), reverse=True)
    ]

import urllib.parse
for post in search_show_hn("terminal", top_n=5):
    print(f"{post['points']:>5} pts  {post['title']}")
    print(f"       {post['url']}")
```

## Best practices
- Research the top 20 Show HN posts in your product category using the Algolia API before writing your title — pattern-match on what the community rewarded
- The first 90 minutes after posting are critical for ranking; have 5-10 genuine community members (not paid or incentivized) ready to engage with the post organically on launch morning
- "Demo without signup" is a hard requirement from the HN community; use a read-only demo account with preloaded data if your product requires auth
- Technical blog posts that tell a genuine story (what failed, what we tried, why we chose this approach) perform better than polished marketing narratives — agents tend to make copy too clean; instruct them to preserve the messy decision-making details
- Disable any marketing pop-ups, cookie consent banners, or interstitial CTAs for the 24-hour launch window — they cause immediate bounces and negative comments
- If your post gets flagged or doesn't gain traction, do not repost the same day — wait at least 2 weeks and reframe with a different angle

## AI-agent gotchas
- Agents default to polished, enthusiastic copy — HN commenters immediately recognize and downvote "marketing voice"; instruct agent to write in builder voice (plain, honest, technical)
- Show HN title character limits: HN does not enforce a strict limit but titles over 80 characters get truncated in feeds — validate length after generation
- Agents may suggest "guerrilla" tactics (asking friends to upvote, posting in Slack communities simultaneously) that HN flags as vote manipulation — explicitly prohibit these in the system prompt
- First comment drafts by agents often lack real technical depth because agents summarize rather than explain; provide the agent with actual architecture details, code snippets, or benchmark data to include
- Human-in-loop checkpoint: post the Show HN submission and first comment manually — never automate submission; HN's systems detect automated submissions
- Response drafts for hostile comments need human review before posting — a factually correct but poorly toned response can escalate a thread and damage the post's reception

## References
- https://news.ycombinator.com/newsguidelines.html — Official HN submission guidelines (mandatory reading)
- https://news.ycombinator.com/newsfaq.html — HN FAQ on Show HN format and culture
- https://hn.algolia.com/api — Algolia HN API for researching past launches
- https://github.com/HackerNews/API — Official HN Firebase API for real-time monitoring
- https://builtbywords.substack.com/p/how-to-launch-on-hacker-news — Practical launch walkthrough with examples
- https://www.ycombinator.com/library/6g-how-to-launch-again-and-again — YC's advice on repeated launches
