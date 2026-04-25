# Agent Integration — Competitive Analysis (UX)

## When to use
- Before a new feature spec is written — understand what competitors do before designing something that already exists
- Quarterly product reviews — market and competitor UI patterns shift faster than annual reviews capture
- When a stakeholder asks "what do others do?" — answer with evidence, not opinion
- Before a positioning or pricing decision — understanding competitor UX quality is part of the market landscape
- When user research reveals that users compare your product to specific competitors — study those exact products

## When NOT to use
- As a substitute for user research — competitor analysis tells you what others built, not what users need
- When all target competitors are behind closed paywalls and cannot be legally accessed for analysis
- For internal tooling with no external market — no competitors means no competitive analysis
- When the product is intentionally defying conventions (e.g., a novel interaction paradigm) — conventional competitive analysis will anchor you to patterns you're trying to break

## Where it fails / limitations
- A competitor's feature may exist due to technical debt, not product decision — copying it means inheriting their mistake
- Analysis at a point in time goes stale: a product observed in January may have been redesigned by Q2
- Surface-level UX review misses backend capabilities that drive UX decisions (e.g., a competitor's faster search is why their UX can afford a smaller search input)
- A "best practice" observed in a competitor with 10x your traffic may not be achievable at your scale
- Agents cannot create accounts or complete real purchase flows — the deepest user flows remain inaccessible without human research participation

## Agentic workflow
An agent can structure the analysis framework, synthesize publicly available information (screenshots, product pages, app store reviews, help center content, changelogs), and produce a feature comparison matrix. The core research step — actually using the competitor products — requires human participation. Once a human provides observations (raw notes, screenshots, annotated flows), the agent can synthesize findings, identify patterns, and produce the final report with recommendations. App store reviews are a high-value, agent-accessible data source for competitor pain points.

### Recommended subagents
- `faion-ux-researcher-agent` — structures the analysis framework and synthesizes research inputs into the final report
- general web research agent — scrapes public changelogs, App Store/Play Store review summaries, and product hunt comments for competitor signals

### Prompt pattern
```
You are conducting a UX competitive analysis for [product] in the [category] space.
Competitors to analyze: [list].
For each competitor, analyze the following from the provided notes and screenshots:
1. Onboarding flow: steps, time to value, friction points
2. Core task completion: [specific user goal]
3. Navigation pattern: what structure and labels are used
4. Error handling: quality of error messages and recovery paths
5. Mobile experience: mobile-first or responsive-degraded
Output: feature comparison matrix + 3 opportunities where we can differentiate.
```

```
Given the following App Store reviews for [competitor] (rating ≤ 2 stars),
extract the top 5 recurring UX complaints. Categorize each by Nielsen heuristic violated.
Format: | Complaint | Frequency | Heuristic | Severity (1-4) |
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` CLI | Automate navigation of competitor public pages for screenshot capture | `npm i -D @playwright/test` / playwright.dev |
| `puppeteer` | Headless screenshot of competitor pages at specific viewports (mobile, desktop) | `npm i puppeteer` / pptr.dev |
| `app-store-scraper` | Scrape App Store and Google Play reviews for competitor sentiment analysis | `npm i app-store-scraper` / github.com/facundoolano/app-store-scraper |
| `curl` + `jq` | Query public APIs (Product Hunt, Crunchbase) for competitor product metadata | built-in / jq.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SimilarWeb | SaaS | Yes — REST API (paid) | Traffic estimates, engagement metrics, device split for competitor sites |
| SEMrush | SaaS | Yes — REST API (paid) | Competitor keyword strategy, traffic sources — useful for understanding their positioning |
| Miro / FigJam | SaaS | Partial | Best tool for collaborative competitive analysis boards; agent prepares content, human arranges visually |
| Notion | SaaS | Yes — API | Agent writes structured competitor profiles and comparison matrices to Notion database |
| Airtable | SaaS | Yes — full API | Feature comparison matrix as a database; filterable by competitor and criteria |
| Owler | SaaS | Yes — REST API | Competitor news and alerts; agent can monitor for competitor product launches |
| Product Hunt | SaaS | Yes — GraphQL API | Hunt data, upvotes, comments reveal real user reactions to competitor launches |

## Templates & scripts
See `templates.md` for the full Competitive Analysis Plan, Feature Comparison Matrix, Individual Competitor Profile, and Summary Report templates.

Inline script — scrape App Store reviews for a competitor:
```javascript
// Usage: node scrape-reviews.js <app-id> <num-reviews>
// Example: node scrape-reviews.js 284882215 100
const store = require('app-store-scraper');

const appId = process.argv[2];
const count = parseInt(process.argv[3] || '100');

store.reviews({ id: appId, sort: store.sort.CRITICAL, num: count })
  .then(reviews => {
    const complaints = reviews
      .filter(r => r.score <= 2)
      .map(r => ({
        score: r.score,
        title: r.title,
        text: r.text.slice(0, 200),
        date: r.updated
      }));
    console.log(JSON.stringify(complaints, null, 2));
    console.log(`\nTotal critical reviews: ${complaints.length}`);
  })
  .catch(console.error);
```

## Best practices
- Analyze the same specific user flow across all competitors — comparing checkout of Competitor A to onboarding of Competitor B produces noise, not insight
- Screenshot everything during analysis — competitor UIs change; your documentation is the historical record
- Rate each competitor per criterion on a consistent scale (Excellent/Good/Fair/Poor or 1-4) before writing narrative — prevents post-hoc rationalization
- Seek out negative reviews (App Store 1-2 stars, Reddit complaints, G2/Capterra reviews) to find competitor weaknesses that represent your opportunities
- Include at least one "aspirational" example from outside your direct category — cross-industry patterns often produce the best differentiation ideas
- Prioritize findings into three buckets: table stakes (must match), parity (should match), differentiation (opportunity to exceed) — this maps directly to roadmap prioritization
- Schedule recurring analysis: quarterly lightweight check, annual deep analysis, triggered when a competitor ships a major release

## AI-agent gotchas
- Agents analyzing competitor public pages via screenshots cannot access gated features requiring accounts — the most important flows (checkout, settings, admin) are invisible to the agent
- App Store reviews are biased toward extreme experiences (1-star and 5-star) — agent-extracted patterns may overrepresent edge cases
- Competitor feature presence detected from marketing pages may not reflect actual implementation quality — "AI-powered search" on a landing page means nothing about UX quality
- Feature comparison matrices generated by agents from web content frequently contain outdated information — every cell needs a human spot-check date
- An agent identifying "what most competitors do" as best practice may be identifying a shared bad practice — industry consensus is not the same as user-validated design

## References
- https://www.nngroup.com/articles/competitive-usability-evaluations/
- https://www.interaction-design.org/literature/article/how-to-do-a-competitive-analysis-in-ux-design
- Just Enough Research — Erika Hall (A Book Apart)
- Competitive Strategy — Michael Porter (Harvard Business School Press)
- https://www.smashingmagazine.com/2018/04/competitive-analysis-ux-design/
