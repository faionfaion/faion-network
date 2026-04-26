# Agent Integration — Idea Generation

## When to use
- Solopreneur in "blank page" mode: skills inventory exists, no idea picked.
- Quarterly idea-refresh sprint: generate 20+ candidates, score, pick 1-2 to validate next quarter.
- Combining a known skill (e.g., "Python + scraping") with current pain points to surface SaaS angles.
- Repurposing a portfolio of past services into productized offerings (Framework #4).

## When NOT to use
- You already have a validated idea and paying users — switch to roadmap/discovery, not generation.
- You need market sizing or financial projections — this methodology is generation, not evaluation.
- Highly technical R&D (deep tech, hardware) where the generation frameworks (Reddit pain mining, Upwork gigs) don't apply.
- Burnout / decision-fatigue state — adding more options makes things worse, not better.

## Where it fails / limitations
- The 5-criteria scorecard (Market, Fit, Competition, Monetization, MVP-speed) is an unvalidated rubric; weights drift between agents and humans.
- "Personal Fit = excited daily" is unmeasurable without time. LLMs cannot evaluate it; only the founder can.
- Market Stacking (#6) tends to produce gimmicks ("AI × X") when run by an LLM — pattern-matching beats substance.
- "Speed to MVP" is dramatically miscalibrated for AI-augmented dev; the README's 5 = 2 weeks anchor is now closer to days for many ideas.
- Agents over-index on Pain Point Mining (#2) and ignore Skills Inventory (#1) and Your Own Problems (#7) — the most personal frameworks have the highest hit rate but require non-LLM input.

## Agentic workflow
Generation is human-LLM hybrid. Founder fills Skills Inventory and Own Problems offline (LLM cannot). Agent then runs the other five frameworks in parallel — one agent per framework — and produces 5-10 ideas each. A converger agent dedupes, removes obvious gimmicks, and outputs ≤20 candidates. The founder scores Personal Fit; agent scores the other four columns from market data. Final pick is collaborative.

### Recommended subagents
- `faion-idea-generator-agent` — canonical agent named in the README; orchestrates the 7 frameworks.
- `faion-pain-point-researcher-agent` — feeds Framework #2 with pain points + scores from `pain-point-research/`.
- `faion-brainstorm` (skill) — diverge/converge over the unioned idea list; native multi-agent.
- A custom `unbundling-finder` (sonnet) — scans a target platform's feature list and proposes unbundled niches.
- A custom `gimmick-filter` (sonnet) — flags "X but with AI" / "Uber for X" patterns.

### Prompt pattern
```
Read skills/faion/knowledge/solo/research/researcher/idea-generation/README.md.
Run frameworks 2 (Pain Mining), 3 (Job Substitution), 4 (Productized), 5 (Unbundling), 6
(Stacking) for audience=<X>, founder skills=<list>. Output a JSON list of ideas with
{name, framework, problem, audience, rough_solution, gimmick_risk:0-1}.
```

```
Score these ideas on Market/Competition/Monetization/Speed (5-pt). Leave PersonalFit
column blank — founder will fill. Compute weighted total assuming PersonalFit=3 placeholder.
Sort desc.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `apify` CLI | Scrape Upwork, Fiverr, Indie Hackers for Frameworks #2/#3 | https://docs.apify.com/cli |
| `praw` | Reddit niche subreddit mining | https://praw.readthedocs.io |
| `serpapi` | "People Also Ask" + trends | https://serpapi.com |
| `g2-scraper` (apify actor) | Pull competitor feature lists | https://apify.com/store |
| `notion-cli` | Idea backlog persistence | https://developers.notion.com |
| Anthropic SDK | Batch idea-generation across frameworks | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Indie Hackers | SaaS | Partial | No public API; use Apify actor or RSS. |
| Upwork / Fiverr | SaaS | Partial | ToS-restricted; use Apify actors carefully. |
| Product Hunt | SaaS | Yes | Public API for trending products → unbundling targets. |
| Exploding Topics / Glimpse | SaaS | Yes | Trend feeds; agent-pollable for Stacking framework. |
| Notion / Airtable | SaaS | Yes | Idea backlog + scoring matrix. |
| GummySearch / F5Bot | SaaS | Yes | Reddit listening for ongoing pain capture (Framework #2). |
| LinkedIn (Sales Nav) | SaaS | Partial | Job-post mining for Framework #3; rate-limited. |

## Templates & scripts
See `templates.md` and the README's two templates. Inline scoring helper (Python ≤25 lines):

```python
import json, sys
W = {"market":0.20, "fit":0.25, "competition":0.15, "monetization":0.20, "mvp":0.20}
ideas = json.load(sys.stdin)
for it in ideas:
    s = sum(W[k] * float(it["scores"].get(k, 0)) for k in W)
    it["weighted"] = round(s, 2)
ideas.sort(key=lambda x: x["weighted"], reverse=True)
print(json.dumps(ideas[:10], indent=2))
```

Pair with the README's "Idea Discovery Session" markdown template for human-readable output.

## Best practices
- Run all 7 frameworks even if one feels productive. Different frameworks surface different idea classes; skipping bias-locks the founder.
- Generate at least 20 ideas before scoring. Below that the matrix has no signal — too few comparison points.
- Score Personal Fit first, before any market data. Excitement in market context contaminates the founder's honest answer.
- Time-box generation (≤4 hours per session). Beyond that, agents repeat themselves and ideas converge.
- Persist every idea, even bad ones. The "Weekly Idea Capture" template compounds over months — patterns emerge from the rejected list.
- Pair with `pain-point-research` first — pain-data fuels Framework #2 with concrete inputs instead of LLM speculation.
- Re-evaluate scores quarterly. "Speed to MVP" especially shifts with AI tooling; an idea that scored 2 last year may be 5 today.

## AI-agent gotchas
- LLMs gravitate to "AI agent for X" / "GPT-powered Y" — explicit `gimmick_risk` flag and a filter agent are mandatory.
- Agents inflate Market Size scores by quoting global TAM. Constrain to the actual ICP segment.
- Personal Fit cannot be scored by an LLM. If the agent fills it in anyway, throw the row out and have the founder re-score.
- Agents recycle the same SaaS tropes (CRM-for-X, Notion-for-Y) — diversify by framework explicitly: prompt one agent at a time per framework.
- Date drift: trend-based ideas decay fast. Always include a "valid as of" date in the persisted record.
- Human checkpoint: before any selected idea moves to validation, founder reviews the dedupe step — agents collapse genuinely-different ideas into one.
- Don't let one agent both generate AND score — generators self-rate too high. Use separate agents (or sessions) for the two phases.

## References
- https://www.indiehackers.com/post/how-to-come-up-with-saas-ideas
- https://www.lennysnewsletter.com/p/finding-product-market-fit
- https://stratechery.com/2017/the-product-question/
- https://www.startupschool.org/library
- https://www.ycombinator.com/library/8c-how-to-get-startup-ideas (Paul Graham)
- https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
