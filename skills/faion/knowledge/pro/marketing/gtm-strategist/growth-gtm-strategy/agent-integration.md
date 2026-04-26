# Agent Integration — Go-to-Market Strategy

## When to use
- Drafting an initial GTM one-pager from product brief + market data: ICP, anti-ICP, positioning, channels, motion, launch timeline.
- Building a competitive positioning map by scraping G2, Capterra, SimilarWeb, and competitor sites, then synthesizing positioning gaps.
- Generating multiple GTM hypotheses (channel × motion × pricing combinations) and stress-testing each against unit economics.
- Maintaining a living GTM doc that reflects monthly metric reviews — agent updates targets, flags off-track KPIs, and proposes pivots.
- Preparing launch-readiness reports across phases (private beta → public beta → GA) with checklist gates.

## When NOT to use
- No product yet, only an idea. GTM without product validation is fiction. Run customer-discovery interviews first; agents are bad interviewers and worse at coding qualitative signal.
- Late-stage pivots driven by founder intuition or emergent insight from a single deep customer call. Agent will optimize on outdated assumptions; humans must own the strategic shift.
- Industries with heavy regulatory gating (medical devices, fintech with licensing, defense). GTM constraints are legal, not market. Agent help is limited to compliance research.

## Where it fails / limitations
- LLM-generated ICPs default to "tech-savvy SMB founders" or similarly generic personas. Without disciplined input data (won-deal interview transcripts, churn-call notes), output is flattering noise.
- Competitive analysis from public web is shallow — pricing pages lie, G2 reviews are gamed, SimilarWeb traffic is noisy at <100k MAU. Agent must triangulate, not single-source.
- Sales-motion choice is sensitive to ACV math the LLM gets wrong (CAC payback, LTV/CAC). Always wire actual financial inputs; do not let the model reason from priors.
- Channel rec ("SEO, content, Product Hunt") becomes uniform across briefs. Agent must constrain channel set per ICP behavior data, not blanket recommendations.
- Phased launch timelines proposed by an LLM ignore real engineering capacity. Plug in the actual roadmap or the plan is fantasy.

## Agentic workflow
A multi-agent GTM workflow: (1) researcher subagent scrapes competitor sites + review platforms + community discussions; (2) brainstorm subagent diverges on ICP/positioning/channel combinations; (3) strategist subagent converges, produces a one-pager with explicit assumptions and unknowns; (4) reviewer subagent critiques against unit-economics constraints and prior failed bets; (5) human approves and locks the doc. Monthly: a metrics agent reads dashboards, flags drift, and queues a strategy review.

### Recommended subagents
- `faion-content-agent` (methodology frontmatter) — drafts positioning copy, GTM one-pager, value prop variations.
- `faion-brainstorm` (skill) — multi-perspective diverge/converge for ICP and channel choice; useful before any single-strategy commitment.
- `faion-sdd-executor-agent` — runs GTM as an SDD feature: spec (vision), design (channel/motion), test-plan (90-day metrics), implementation-plan (phased launch).
- `faion-improver` — quarterly review session that audits prior GTM doc against actuals.

### Prompt pattern
```
Goal: produce GTM one-pager v1 for product P.
Inputs: product brief, 5 won-deal transcripts, 5 lost-deal transcripts, competitor list, current MRR/CAC/LTV.
Constraints: ONE ICP (not three); name the anti-ICP; pick 2-3 channels with explicit reasoning; sales motion must reconcile with CAC payback < 12 months.
Output: filled GTM one-pager template; mark every unverified claim as "ASSUMPTION".
```

```
Goal: red-team GTM doc D.
Method: list 5 ways this strategy fails in 6 months. For each, state the leading indicator and a kill-switch.
Output: risk register; do not rewrite the doc.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Scrape competitor pricing, feature, review pages | `pip install playwright` |
| `similarweb-api` | Traffic + audience data per competitor domain | https://www.similarweb.com/corp/developer/ |
| `serpapi` / `searxng` | Search competitor mentions, reviews | https://serpapi.com or self-hosted SearXNG |
| `dbt` + warehouse | CAC/LTV/payback modeling on first-party data | https://docs.getdbt.com |
| `streamlit` / `evidence` | Internal dashboard for monthly GTM review | https://docs.streamlit.io, https://evidence.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| G2 / Capterra | SaaS review | Read-only | Scrape with care; both have ToS. |
| SimilarWeb | SaaS | Yes (API, paid) | Traffic + audience overlap. Noisy <100k MAU. |
| Crunchbase / PitchBook | SaaS | Yes (API, paid) | Funding + competitive intel. |
| Tally / Typeform | SaaS forms | Yes (API) | Customer-discovery interview scheduling + survey capture. |
| Notion / Coda | SaaS doc | Yes (API) | Host the GTM one-pager; agent edits via API. |
| Mixpanel / Amplitude | SaaS analytics | Yes (API) | Funnel + cohort metrics for GTM KPIs. |
| Plausible / PostHog | OSS / SaaS | Yes | Privacy-friendly analytics with API. |

## Templates & scripts
Inline: feasibility check on a proposed GTM motion against unit economics. Returns pass/fail with reasons.

```python
def gtm_motion_feasibility(
    motion: str, acv_usd: float, gross_margin: float,
    estimated_cac: float, churn_monthly: float,
) -> dict:
    ltv = (acv_usd / 12) * gross_margin / max(churn_monthly, 1e-6)
    payback_months = estimated_cac / max((acv_usd / 12) * gross_margin, 1e-6)
    rules = {
        "self-serve":   {"max_payback": 6,  "min_acv": 60,    "max_acv": 5_000},
        "sales-assist": {"max_payback": 12, "min_acv": 1_200, "max_acv": 30_000},
        "enterprise":   {"max_payback": 18, "min_acv": 25_000, "max_acv": 1e9},
    }
    r = rules.get(motion)
    if not r:
        return {"ok": False, "reason": f"unknown motion {motion}"}
    fail = []
    if payback_months > r["max_payback"]:
        fail.append(f"payback {payback_months:.1f}mo > {r['max_payback']}mo")
    if not (r["min_acv"] <= acv_usd <= r["max_acv"]):
        fail.append(f"ACV ${acv_usd} outside [{r['min_acv']}, {r['max_acv']}]")
    return {"ok": not fail, "ltv": ltv, "payback_months": payback_months, "issues": fail}
```

See `templates.md` for the full GTM one-pager and competitive-positioning map.

## Best practices
- Lock the ICP to ONE segment for the first 6 months. Splitting effort across "SMB and Enterprise" is the #1 GTM failure mode.
- Define anti-ICP explicitly — without it, sales chases bad-fit deals that look like revenue but kill retention.
- Channels: start with two, master both, then add a third. Agents will happily list 7; reject anything over 3.
- Metric reviews are monthly (not weekly — too noisy, not quarterly — too late). Codify the cadence so the agent triggers reviews automatically.
- Treat the GTM doc as a living artifact: every monthly review writes a delta entry, not a rewrite. History preserves learnings.
- Anchor pricing to value not cost; agent should generate 3 pricing scenarios and force a pricing conversation, not auto-pick.

## AI-agent gotchas
- The model will always produce a confident GTM doc, even with terrible inputs. Require explicit "I don't know" tags and assumption flags; reject docs without them.
- "Channels" in LLM-land conflate awareness with acquisition. Agent must separate the funnel (awareness → consideration → conversion → retention) and assign each channel a role.
- Competitive analysis tends to plagiarize one source. Force triangulation: at least 3 independent sources per claim.
- Strategy and tactics blur. Agent often returns tactical to-do lists ("write 10 blog posts") when asked for strategy. Reject; require category-level decisions, not task lists.
- Pricing experiments require legal sign-off (price discrimination, regional pricing law). Agent must surface this gate, not auto-implement.
- ICP from won-deal data only ≠ ICP from market data — survivorship bias. Force the agent to also examine lost deals and never-tried segments.
- A "vision" written by an LLM is forgettable by design (regression to mean). Have humans rewrite the vision sentence — agents draft, humans choose.

## References
- Steve Blank — *The Four Steps to the Epiphany*
- Geoffrey Moore — *Crossing the Chasm*
- April Dunford — *Obviously Awesome* (positioning)
- a16z GTM Workbook: https://a16z.com/go-to-market-workbook/
- OpenView SaaS Benchmarks: https://openviewpartners.com/saas-benchmarks/
- Forget The Funnel: https://www.forgetthefunnel.com/
- *Lean Analytics* — Croll & Yoskovitz (metric selection by stage)
