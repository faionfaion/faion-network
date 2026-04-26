# Agent Integration — Competitive Analysis

## When to use
- Before designing a new product or major feature to establish baseline expectations
- When a stakeholder asks "what do competitors do?" and you need a structured answer
- After discovering that users expect a feature that doesn't exist yet — to verify if competitors have it
- When differentiating positioning: find gaps no one fills
- During quarterly design reviews to catch competitor product updates

## When NOT to use
- As a substitute for user research — competitor patterns reflect competitor assumptions, not your users
- When your product targets a problem with no direct competitors (use analogous domain research instead)
- When the competitive landscape changes faster than you can act (e.g., fast-moving AI tooling) — snapshot analysis becomes stale within weeks
- For validating exact user flows with real users — use usability testing

## Where it fails / limitations
- Survivorship bias: you only see what competitors shipped, not what they tried and killed
- You cannot know why competitor made specific decisions — copying without understanding propagates mistakes
- Publicly accessible flows differ from authenticated/paid flows; agent scraping hits walls at login
- Accessibility gaps in competitor products are hard to surface without assistive technology testing
- Pattern convergence risk: analyzing the same 5 competitors as everyone else leads to industry-wide design homogeneity

## Agentic workflow
An agent can systematically capture public-facing competitor flows by navigating URLs, extracting page structure, and comparing feature presence against a predefined criterion matrix. The agent handles the mechanical data collection phase — screenshot capture, feature matrix population, and pattern counting — while a human reviews annotated findings, validates severity of gaps, and decides what to adopt.

The most effective split: agent does structured scanning across 5-10 competitor URLs and fills a comparison table; human does one deep qualitative pass on the 2-3 most relevant results.

### Recommended subagents
- `faion-sdd-executor-agent` — execute structured competitive research tasks from a spec, populate feature matrices
- General Claude subagent with browser tool — navigate competitor sites, extract navigation structures, document flow steps

### Prompt pattern
```
You are doing competitive analysis for [product]. For each competitor URL below, document:
1. Navigation structure (top-level items)
2. Onboarding flow steps (count and describe each)
3. Presence/absence of these features: [list]
4. Any notable UX patterns in [specific area]

Competitors: [URL list]
Output: markdown table with one row per competitor.
```

```
Given this competitor comparison matrix: [matrix]
Identify: (a) features present in 4+ competitors (table stakes), (b) features present in 1-2 (differentiators), (c) features absent everywhere (opportunities).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `puppeteer` / `playwright` | Headless browser for capturing competitor flows | `npm i playwright` / playwright.dev |
| `shot-scraper` | CLI screenshot tool for web pages | `pip install shot-scraper` / github.com/simonw/shot-scraper |
| `curl` + `pup` | Lightweight HTML extraction from public pages | `brew install pup` / github.com/ericchiang/pup |
| `wappalyzer-cli` | Detect tech stack of competitor sites | `npm i -g wappalyzer` / wappalyzer.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Similarweb | SaaS | Partial (API tier) | Traffic estimates, top pages; API is expensive |
| BuiltWith | SaaS | Yes (REST API) | Tech stack detection per domain |
| Owler | SaaS | No | Competitor monitoring; no programmatic API |
| Wayback Machine (archive.org) | OSS/public | Yes (CDX API) | Historical snapshots of competitor flows |
| Mobbin | SaaS | No | Mobile UI screenshot library; browse-only |
| Screenlane | SaaS | No | Desktop UI screenshot library; browse-only |

## Templates & scripts
See `templates.md` for full competitive analysis plan, feature comparison matrix, individual competitor profile, and summary report templates.

Inline helper — generate feature matrix skeleton from a competitor list:
```bash
#!/usr/bin/env bash
# Usage: ./gen-matrix.sh "Competitor A" "Competitor B" "Competitor C"
FEATURES=("Guest checkout" "Mobile app" "SSO login" "API access" "Free tier")
echo "| Feature | Our Product | $(echo "$@" | tr ' ' '\n' | paste -sd ' | ') |"
echo "|---------|-------------|$(echo "$@" | tr ' ' '\n' | sed 's/.*/-------------|/' | paste -sd '')"
for f in "${FEATURES[@]}"; do
  echo "| $f | ? | $(echo "$@" | tr ' ' '\n' | sed 's/.*/? |/' | paste -sd '') "
done
```

## Best practices
- Conduct the analysis yourself (use the product, create accounts, complete full flows) — do not delegate deep qualitative pass to an agent
- Score each criterion consistently using the same rubric (Excellent/Good/Fair/Poor) rather than yes/no to capture degree of implementation
- Include one aspirational non-competitor (different industry, best-in-class UX) to break pattern lock
- Annotate screenshots immediately; memory of observations degrades fast
- Re-run analysis after major competitor launches, not on a fixed calendar schedule
- Separate "what they do" observations from "what we should do" recommendations — keep them in distinct sections until synthesis

## AI-agent gotchas
- Agents cannot complete authenticated flows (checkout with payment, dashboard post-login) — these require human walkthroughs
- Dynamically rendered React/Vue apps may return empty HTML to a basic curl fetch; must use headless browser
- Competitors frequently A/B test their own UIs — agent capturing on one day may see a variant that disappears next week; note the date and take screenshots
- Do not let an agent generate "insights" from competitor data without a human review step; LLMs tend to over-interpret surface patterns
- Pattern extraction is reliable for structured data (feature presence, step counts); qualitative judgments (tone, visual hierarchy) require human review

## References
- Nielsen Norman Group: https://www.nngroup.com/articles/competitive-usability-evaluations/
- Interaction Design Foundation competitive analysis guide: https://www.interaction-design.org/literature/article/how-to-do-a-competitive-analysis-in-ux-design
- Erika Hall, "Just Enough Research" (Rosenfeld Media, 2013)
- Michael Porter, "Competitive Strategy" (Free Press, 1980)
- Smashing Magazine deep dive: https://www.smashingmagazine.com/2018/04/competitive-analysis-ux-design/
