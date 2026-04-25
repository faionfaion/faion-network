# Agent Integration — Content Marketing

## When to use
- Generating keyword research lists and content briefs for a defined topic cluster
- Drafting long-form blog posts from a structured brief (keyword, intent, outline, competitors)
- Building a 3-month content calendar with topics mapped to funnel stages
- Repurposing a single long-form piece into 5-7 derivative formats (tweet thread, newsletter, LinkedIn post, social carousel)
- Writing distribution checklists and outreach messages for newly published content

## When NOT to use
- Defining content pillars — these require ICP interviews and product positioning work, not synthesis
- Content that depends on original data, proprietary research, or lived experience — agents produce generic content without unique inputs
- Publishing directly to any CMS without human review
- Predicting SEO performance — agents cannot query live search engine data
- Replacing a content strategist's judgment on what topics to pursue for a specific brand

## Where it fails / limitations
- Content brief quality determines output quality — vague briefs produce vague content
- Generated blog posts without unique data or specific examples are indistinguishable from commodity content and will not rank
- Distribution tactics require platform-specific accounts and existing audiences; agents cannot build reach from zero
- Content ROI calculation requires actual analytics data; agents work from benchmarks, not real conversion rates
- Agent-written content requires significant editing to pass E-E-A-T requirements (experience, expertise, authoritativeness, trustworthiness) for competitive SERPs

## Agentic workflow
The most productive pattern is assembly-line content production: (1) agent generates 20-40 keyword + intent pairs from seed topics, (2) human selects and prioritizes 5-10, (3) agent expands each into a structured content brief, (4) human approves briefs, (5) agent drafts each article from the brief, (6) human edits for voice, adds original data/examples, (7) agent produces the repurposed formats. Each handoff requires human review. Fully automated publishing without review produces content that damages SEO and brand credibility.

### Recommended subagents
- `faion-sdd-executor-agent` — execute structured content production tasks from a task file
- No dedicated content marketing agent exists; use a general content subagent role for drafting

### Prompt pattern
```
You are a content strategist. Given the seed topic "[TOPIC]" for a [PRODUCT TYPE]
targeting [ICP], generate 20 keyword opportunities.

For each keyword, provide:
- keyword phrase
- estimated search intent (informational/commercial/transactional)
- content type best fit (blog post / comparison / landing page / guide)
- difficulty estimate (low/medium/high) based on SERP competitiveness signals

Output as JSON array: [{"keyword": "...", "intent": "...", "content_type": "...", "difficulty": "..."}]
```

```
Write a 1200-word blog post draft from the following brief.

Primary keyword: [KEYWORD]
Search intent: [INTENT]
Target audience: [ICP]
Unique angle: [DIFFERENTIATOR]
Competitors to beat: [URL1], [URL2]
Outline:
  H2: [SECTION1]
  H2: [SECTION2] with H3s: [SUBSECTION A], [SUBSECTION B]
  H2: [SECTION3]
  H2: Conclusion + CTA

Requirements: include one data point per H2, avoid passive voice,
end with CTA to [FREE TRIAL / NEWSLETTER / RESOURCE].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ahrefs` API | Keyword data, backlink analysis, content gap | ahrefs.com/api |
| `semrush` API | Keyword research, rank tracking, site audit | developer.semrush.com |
| `google-search-console` API | Real impressions/clicks/ranking data for owned domains | developers.google.com/webmaster-tools |
| `clearscope` API | Content optimization scoring against top SERP results | clearscope.io (API on enterprise plan) |
| `buffer` CLI / API | Schedule social distribution of published content | buffer.com/developers/api |
| `hypefury` | Twitter/X thread scheduler with content repurposing | No public CLI; web app only |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ahrefs | SaaS | Yes — REST API (paid) | Gold standard for keyword + backlink data |
| Semrush | SaaS | Yes — REST API (paid) | Broader marketing suite; strong keyword API |
| Google Search Console | SaaS (free) | Yes — REST API | Real ranking data for your domain; essential |
| Clearscope | SaaS | Partial — Enterprise API | Content scoring; most useful via web UI |
| Surfer SEO | SaaS | Partial | SERP analysis; API available on higher plans |
| Frase | SaaS | Partial | Brief generation + content scoring; limited API |
| ConvertKit | SaaS | Yes — REST API | Email distribution of content to subscribers |
| Buffer | SaaS | Yes — REST API | Social scheduling across channels |
| Plausible | OSS/SaaS | Yes — REST API | Privacy-friendly analytics; useful for content tracking |
| WordPress REST API | OSS | Yes — REST | CMS publishing; agents can draft but not publish |

## Templates & scripts
See `templates.md` for content calendar, content brief template, and distribution checklist.

Minimal Google Search Console API call to pull top-performing content pages:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SERVICE_ACCOUNT_FILE = "gsc-credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("searchconsole", "v1", credentials=credentials)

response = service.searchanalytics().query(
    siteUrl="https://yourdomain.com",
    body={
        "startDate": "2026-01-01",
        "endDate": "2026-03-31",
        "dimensions": ["page"],
        "rowLimit": 20,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    }
).execute()

for row in response.get("rows", []):
    print(f"{row['keys'][0]} | clicks: {row['clicks']} | impressions: {row['impressions']}")
```

## Best practices
- Provide the agent with 3-5 real examples of content that converts in your niche as format references before asking for drafts
- Always include a unique angle in the brief — "how [your product]'s data shows X" or "based on our customer interviews" — and then inject the actual data/quotes during editing
- Distribution should consume 50% of total content production time; agents can help automate the social posts and email version but not relationship-based distribution
- Internal linking is often omitted from agent drafts; add a step to the editorial workflow where the agent is given a list of existing published URLs and asked to suggest anchor text links
- Update old content quarterly using Search Console data — improving existing rankings is higher ROI than always publishing new content

## AI-agent gotchas
- Agents default to a "how to X" structure regardless of search intent; specify content type explicitly in the brief
- Generated content passes plagiarism checks but reads similarly to other AI content on the same keyword — unique data is the primary differentiator
- Agents will pad word count to hit targets with redundant sentences; constrain with "no filler, cut anything that doesn't add information"
- CTAs generated by agents are usually weak ("Learn more about X"); specify the exact offer and action you want
- Never let an agent publish to WordPress or any CMS directly — a misformatted post or wrong category can hurt crawlability and indexation
- Content briefs that include competitor URLs improve agent output quality significantly; always provide at least 2 competitor examples

## References
- https://ahrefs.com/blog/content-marketing/ (Ahrefs content marketing guide)
- https://contentmarketinginstitute.com/research/ (annual CMI research reports)
- https://developers.google.com/webmaster-tools (Search Console API)
- https://moz.com/beginners-guide-to-content-marketing
- Google Search Quality Rater Guidelines: developers.google.com/search/docs/fundamentals/creating-helpful-content
