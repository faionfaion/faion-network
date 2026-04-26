# Agent Integration — Success Metrics Definition

## When to use
- Before sprint planning: defining what "done" looks like for a feature
- At product launch: establishing the AARRR baseline before any optimization
- When a team disagrees on whether a feature worked (no agreed metric = no resolution)
- OKR setup cycles: translating goals into measurable KPIs
- After a pivot: resetting metrics to match new product direction

## When NOT to use
- When you have no baseline data and no way to collect it (define instrumentation first)
- For pure infrastructure tasks where the output is binary (works / doesn't work)
- When the product is pre-revenue and you're still searching for problem-solution fit — metrics framework too early locks in false assumptions
- When stakeholders cannot agree on the North Star — skip to qualitative research first

## Where it fails / limitations
- AARRR framework maps poorly to B2B enterprise products with long sales cycles
- North Star Metric selection is political as much as analytical — agents cannot resolve team alignment issues
- Targets set without baselines are guesses; agents will produce plausible-sounding numbers that may be wildly off
- Metric hierarchies become stale fast; without a review cadence, the framework degrades into orphaned dashboards
- Confounding variables make attribution unreliable — a metric moving does not mean the action caused the move

## Agentic workflow
Claude subagents can draft a metrics framework given a product description and business goals, selecting appropriate North Star candidates from the AARRR taxonomy and generating metric specifications. However, target-setting requires real baseline data — agents must be given current metric values as input context. The framework output should be reviewed by a human before being used to set team OKRs.

### Recommended subagents
- `faion-market-researcher-agent` — generates metrics framework for a described product; suggests North Star candidates with rationale
- `faion-research-agent` (mode: validate) — validates that proposed metrics are actionable and not vanity metrics

### Prompt pattern
```
You are a metrics design agent. Given the product description and business goals below,
output a filled Metrics Framework following AARRR. For each metric include:
- exact definition (formula)
- data source
- whether it is a leading or lagging indicator
- why it is actionable (what decision changes if it moves)

Do NOT set targets — mark target fields as [NEEDS BASELINE].

Product: {description}
Goals: {goals}
```

```
Review this proposed metric list and flag any that are vanity metrics.
For each vanity metric explain why and suggest an actionable replacement.
Apply this test: "If this metric changed by 20%, what would we do differently?"

Metrics: {list}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `metabase` CLI | Query and export dashboards for baseline data | metabase.com/docs |
| `mixpanel-python` | Pull event counts and funnel data for baseline | `pip install mixpanel` |
| `posthog` CLI | OSS analytics: funnel, retention, feature flag data | `pip install posthog`, posthog.com/docs |
| `amplitude-python` | Pull cohort and retention baselines | github.com/amplitude/Amplitude-Python |
| `plausible` API | Lightweight web analytics for traffic metrics | plausible.io/docs/stats-api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS/SaaS | Yes | REST API, Python SDK; funnels, retention, NPS |
| Mixpanel | SaaS | Yes | Events API; good for AARRR activation/retention |
| Amplitude | SaaS | Yes | Cohort API; better for large data volumes |
| Plausible | OSS/SaaS | Yes | Simple stats API; acquisition metrics only |
| Grafana | OSS | Yes | Dashboards from any data source; scriptable |
| Metabase | OSS/SaaS | Yes | SQL-based; good for pulling baseline snapshots |
| Stripe | SaaS | Yes | Revenue metrics (MRR, churn) via API |

## Templates & scripts
See `templates.md` for Metrics Framework and Metric Specification templates.

Inline helper — pull PostHog funnel conversion for baseline:
```python
import requests

POSTHOG_KEY = "..."
PROJECT_ID = "..."

def get_funnel_conversion(steps: list[str], date_from: str, date_to: str) -> dict:
    resp = requests.post(
        f"https://app.posthog.com/api/projects/{PROJECT_ID}/insights/funnel/",
        headers={"Authorization": f"Bearer {POSTHOG_KEY}"},
        json={
            "events": [{"id": s, "type": "events"} for s in steps],
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    resp.raise_for_status()
    result = resp.json()["result"]
    return {s["name"]: s["conversion_rate"] for s in result}

baseline = get_funnel_conversion(["signup", "onboarding_complete", "first_value_action"], "-30d", "today")
print(baseline)
```

## Best practices
- Start with one North Star Metric before adding any secondary metrics; teams that start with 5 KPIs focus on none
- Document metric definitions with edge cases — "weekly active user" must specify what counts as active (specific event, not just login)
- Set targets only after you have at least 4 weeks of baseline data; earlier targets are fiction
- Include guardrail metrics alongside growth metrics — optimizing acquisition while retention collapses is a common trap
- Review the entire metrics framework quarterly; retire metrics that have stopped driving decisions
- Segment every metric by cohort (acquisition channel, plan type, geography) from day one — aggregates hide the signal

## AI-agent gotchas
- Agents will confidently suggest targets without baseline data; always require the agent to mark targets as [NEEDS BASELINE] until real data is provided
- AARRR stage mapping is ambiguous for non-consumer products; give the agent explicit stage definitions for the specific product type
- Metric definitions generated by agents often omit edge cases (what counts as "active"?); require the agent to specify what is excluded, not just what is included
- "North Star" selection by agents defaults to revenue or DAU; push for output metric that actually measures value delivered to the user, not value captured by the business
- Human approval required before metrics are shared with the team — agents lack organizational context about what is politically actionable

## References
- Dave McClure: AARRR Pirate Metrics — https://500hats.typepad.com/500blogs/2007/09/startup-metrics.html
- Lenny Rachitsky: What is a good North Star Metric? — https://www.lennysnewsletter.com/p/north-star-metric
- Sean Ellis: Product-Market Fit survey (40% very disappointed) — https://www.startup-marketing.com/the-startup-pyramid/
- PostHog Docs: Funnel Analysis — https://posthog.com/docs/product-analytics/funnels
- Amplitude: Metrics & KPIs Playbook — https://amplitude.com/blog/product-metrics
