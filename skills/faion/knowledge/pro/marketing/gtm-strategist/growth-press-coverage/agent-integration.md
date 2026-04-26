# Agent Integration — Press & PR Coverage

## When to use
- Building and maintaining a journalist database scoped to your beats (search recent articles, extract authors, enrich contacts).
- Daily HARO / Qwoted / SourceBottle triage: filter, draft tailored pitches for matching queries, queue for human review.
- Drafting personalized cold pitches at scale (100+/month) where each is anchored to a specific recent piece by the journalist.
- Monitoring outcomes (open, reply, coverage) and feeding that signal back into the journalist database for ranking.
- Maintaining the press kit (founder bio versions, boilerplate, fact sheet, asset URLs) under version control.

## When NOT to use
- Pre-product / pre-traction. Without a real story (data, milestone, launch, novel angle), no agent volume will earn coverage. Fix the news first.
- Embargoed announcements with negotiated exclusives — relationship work, requires human-only contact.
- Crisis comms or legal-sensitive PR. Agent-drafted statements carry legal risk; route to humans + counsel.
- Tier-1 outlets (NYT, WSJ, TechCrunch staff list). Agents should research, never auto-pitch — these journalists will blacklist sender on first templated email.

## Where it fails / limitations
- LLM-drafted pitches default to generic flattery ("Loved your piece"). Journalists screen these instantly. Agent must extract a specific, non-obvious insight from the linked article and reference it.
- HARO replaced by Connectively in 2024 then shut down June 2024. Many outdated guides still reference it. Use Qwoted, SourceBottle, Featured (formerly Terkel), JustReachOut, Help A B2B Writer.
- Email deliverability: cold pitches from a new domain land in Gmail Promotions or spam. Need warmed sending domain, SPF/DKIM/DMARC, low daily volume per inbox.
- Embargo coordination is human work — agent cannot reliably hold back a press release across 10 reporters with different timezones.
- Hallucinated journalist beats are common. Agent must cite recent article URLs as evidence, not infer.

## Agentic workflow
The PR agent runs as a multi-stage pipeline: (1) discovery — scrapes Muck Rack / Twitter / publication pages for journalists matching beat keywords; (2) enrichment — pulls last 5 articles per journalist, extracts beat tags + tone; (3) angle match — given a story brief, ranks journalists by fit; (4) draft — writes a pitch citing one specific article and a tailored hook; (5) human review — every pitch requires sign-off; (6) send + track — opens, replies, mentions logged back into the registry. Daily: triage HARO-alternatives, draft responses, queue for human.

### Recommended subagents
- `faion-content-agent` (named in methodology frontmatter) — owns pitch drafting, founder bio versions, press kit copy.
- `faion-sdd-executor-agent` — wraps each campaign (launch, funding, milestone) as an SDD feature with deliverables: target list, story angle, pitch templates, follow-up cadence.
- `faion-brainstorm` — diverges on possible story angles before convergence on the lead one.

### Prompt pattern
```
Goal: rank 50 candidate journalists for story angle "<X>".
Inputs: journalist db with last 5 articles each, story brief.
Method: score 0-1 on (beat_match, recent_topic_proximity, audience_fit, response_history).
Output: top-15 with one-line justification each, citing article URL.
Rule: do NOT invent articles. If <5 articles available, mark as "insufficient data".
```

```
Goal: draft pitch to journalist J for story brief B.
Constraints: <150 words; subject <8 words; cite ONE specific article by URL; one personalized opener (not "loved your piece"); one explicit value-to-reader sentence; offer 3 specific assets; one CTA.
Output: subject + body. Mark for human review. Never auto-send.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `muckrack` API (paid) | Journalist search, beat data, contact info | https://muckrack.com/api |
| `prowly` / `prezly` API | Newsroom + press distribution | https://docs.prowly.com |
| `instantly.ai` / `smartlead` | Email warmup + deliverability | https://developer.instantly.ai |
| `playwright` | Scrape publication mastheads + author archives | `pip install playwright` |
| `feedparser` | RSS-driven journalist tracking | `pip install feedparser` |
| `sendgrid` / `postmark` | Transactional email with tracking | https://docs.sendgrid.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qwoted | SaaS (HARO replacement) | Partial | Web UI; agent-scrapeable but no API. |
| Featured (Terkel) | SaaS | Partial | API for queries; good for B2B. |
| SourceBottle | SaaS | Partial | RSS of queries; agent-friendly via feed. |
| JustReachOut | SaaS | Yes | API + journalist DB. |
| Muck Rack | SaaS | Yes (paid API) | Best journalist DB; expensive. |
| Prezly / Prowly | SaaS | Yes | Press release distribution + newsroom hosting. |
| Press Kit Hero / Notion press page | SaaS / static | Yes | Host press kit; agent updates content. |
| Mention / Brand24 / Google Alerts | SaaS / free | Yes | Monitor coverage post-pitch. |

## Templates & scripts
Inline: HARO/Qwoted-style query triage. Filter feed, score relevance via embedding similarity, output top-N for human draft.

```python
import feedparser
from openai import OpenAI  # or anthropic; use embeddings
import numpy as np

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def triage_queries(feed_url: str, beats: list[str], client, top_n: int = 10) -> list[dict]:
    feed = feedparser.parse(feed_url)
    beat_emb = [client.embeddings.create(model="text-embedding-3-small", input=b).data[0].embedding for b in beats]
    results = []
    for entry in feed.entries:
        text = f"{entry.title}. {entry.get('summary', '')}"
        emb = client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding
        score = max(cosine(emb, b) for b in beat_emb)
        results.append({"title": entry.title, "link": entry.link, "score": score})
    return sorted(results, key=lambda r: -r["score"])[:top_n]
```

See `templates.md` for pitch + bio + HARO-response templates.

## Best practices
- Quality over volume: 10 well-researched pitches beat 100 templated ones. Agent should refuse to send if it cannot cite a specific article.
- Maintain a "do-not-pitch" list (journalists who said no, no-longer-at-publication, opted out). Update on every bounce/reply.
- Pitch Tuesday-Thursday 09:00-11:00 local to journalist. Agent must compute local time, not just send queue order.
- Always offer assets (founder access, exclusive data, customer story). Agent must match assets to article history.
- Track domain authority of placements (Ahrefs/Moz) — agent reports backlink + DA, not just mention count.
- Maintain founder bio versions (50w, 200w, 500w) and update annually. Stale bios undermine pitches.

## Best practices for human-in-loop
- Tier-1 pitches: human writes, agent researches.
- Tier-2/3 pitches: agent drafts, human approves.
- HARO-alt responses: agent drafts, human approves first 20, then approves only flagged.

## AI-agent gotchas
- LLMs hallucinate journalist names, beats, and quotes. Always ground in scraped + cached data; fail closed when no source URL.
- Sending domain reputation: agent batching 50 cold pitches/day from a new domain will get the domain blacklisted within a week. Stagger across multiple warmed inboxes; cap volume per inbox.
- GDPR: EU journalists' contact info needs lawful basis. Public masthead = legitimate interest, but unsubscribe still required.
- Embargo handling needs explicit state — agent must not auto-send any embargoed story without a hard date check + human ack.
- Reply detection is hard — out-of-office replies look like positive responses to naive parsers. Use a classifier or keyword filter before flagging "interested".
- Avoid agent-generated press releases on the wire. PR Newswire / BusinessWire have plagiarism + AI-detection checks; bland LLM prose triggers low pickup.
- Don't let the agent post on social on behalf of the company without approval — coverage celebration tweets misattribute or misquote often.

## References
- https://muckrack.com/blog/2024/01/17/how-to-pitch-journalists
- https://www.qwoted.com/
- https://featured.com/ (Terkel)
- https://justreachout.io/
- Ryan Holiday — *Trust Me, I'm Lying* + *Perennial Seller*
- https://www.poynter.org/ (journalism context for tone)
