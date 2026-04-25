# Agent Integration — Customer Success Metrics

## When to use
- B2B/SaaS product with >50 paying accounts where manual relationship management no longer scales.
- Net Revenue Retention is below 100% and you need to systematize early-warning signals.
- Onboarding a CSM or Success function and need an objective health-score to triage book-of-business.
- Replacing gut-feel quarterly reviews with a measurable monthly cadence (NPS, CSAT, adoption, expansion).

## When NOT to use
- Pre-PMF or fewer than ~20 customers; talking to every customer beats any score.
- Pure self-serve consumer products where 1:1 outreach has negative ROI; rely on lifecycle marketing instead.
- When event tracking isn't instrumented yet; building a health score on top of unreliable data produces false alerts and erodes trust.
- When the team can't act on alerts; a score with nobody to chase at-risk accounts is theater.

## Where it fails / limitations
- Garbage-in: missing or malformed events make health scores meaningless; spend the first cycle fixing telemetry.
- Overweight on usage when the buyer is not the user (e.g., enterprise software): the user is engaged, the buyer churns.
- Static thresholds (80/60/40) become outdated as product matures; without periodic re-calibration the score loses signal.
- NPS is noisy at small N; <50 responses gives ±15-point error; don't move on a quarterly delta of 3 points.
- Survey fatigue: chasing CSAT after every ticket while running NPS quarterly tanks both.

## Agentic workflow
Subagents are well-suited to data plumbing: pulling events, joining them with billing + support data, computing scores, surfacing at-risk lists, drafting outreach. The action — calling the customer, escalating to product, granting credits — stays human. Pipeline: nightly ETL (agent) → score recompute (agent) → at-risk + expansion lists (agent) → CSM playbook draft (agent) → human action → outcome logged (agent updates).

### Recommended subagents
- `general-purpose` — query analytics warehouse, build cohort tables, produce health-score CSVs.
- `faion-content-agent` — draft personalized at-risk outreach and QBR decks from raw account data.
- `password-scrubber-agent` — strip emails/PII before logs/snippets leave local context.
- Custom `cs-ops-agent` (build): owns weekly review packet — health distribution, at-risk MRR, expansion opportunities, leading indicators.

### Prompt pattern
- "Given this account-level CSV (usage, features-adopted, last-ticket-sentiment, payment-status, MRR), compute health 0-100 using this rubric. Output: account_id, score, top-2 risk drivers, recommended next action."
- "Draft a 6-line check-in email to the primary contact at [account]. Reference: usage dropped 40% over 14 days, last positive ticket on [date], MRR $1,200. Tone: helpful, not salesy. End with 15-min call CTA."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Transform raw events → health-score model in SQL | `pip install dbt-core` |
| `duckdb` | Local OLAP for health-score recompute on CSV exports | `brew install duckdb` |
| `pandas` / `polars` | Score calculation in scripts | `pip install pandas` |
| `sqlite3` / `psql` | Query app DB for usage facts | system |
| Mixpanel / Amplitude CLI | Pull cohort exports | https://docs.mixpanel.com/docs/quickstart |
| `streamlit` / `evidence-dev` | Lightweight CS dashboards from CSV | `pip install streamlit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vitally | SaaS | API yes | Dev-friendly CS platform |
| Totango | SaaS | API yes | Health-score originator |
| ChurnZero | SaaS | API yes | Mid-market |
| Gainsight | SaaS | API yes | Enterprise |
| Catalyst | SaaS | API yes | Modern CS w/ Salesforce integration |
| Planhat | SaaS | API yes | EU-heavy CS |
| Mixpanel | SaaS | API yes | Product analytics, cohort retention |
| Amplitude | SaaS | API yes | Product analytics + CDP |
| Heap | SaaS | API yes | Auto-capture analytics |
| Delighted / Wootric | SaaS | API yes | NPS/CSAT distribution + collection |
| Typeform / Tally | SaaS | API yes | Custom surveys |
| HubSpot Service Hub | SaaS | API yes | Light CS w/ ticketing |
| Customer.io / Iterable | SaaS | API yes | Lifecycle messaging on score buckets |

## Templates & scripts
See `templates.md` for health dashboard markdown. Inline weighted score:

```python
# health.py — compute 0-100 health for one account
def health(usage_freq, features_adopted, support_sentiment, engagement, payment):
    # ranges chosen so each score caps at its weight
    u = {"daily": 30, "weekly": 20, "monthly": 10, "inactive": 0}[usage_freq]
    f = min(features_adopted / 5, 1.0) * 25
    s = {"positive": 20, "neutral": 15, "negative": 5, "escalated": 0}[support_sentiment]
    e = {"high": 15, "medium": 10, "low": 5, "none": 0}[engagement]
    p = {"current": 10, "minor": 7, "overdue": 3, "failed": 0}[payment]
    return round(u + f + s + e + p)

# bucket
def bucket(score):
    return ("healthy" if score >= 80 else
            "stable" if score >= 60 else
            "at_risk" if score >= 40 else "critical")
```

## Best practices
- Validate the health score: pick 30 churned accounts, score them as of T-90 days; if >70% weren't flagged "at-risk", recalibrate weights.
- Track NRR cohort-by-cohort, not in aggregate; aggregate NRR hides retention rot inside fast new-logo growth.
- Pair leading-indicator alerts (usage drop, escalations) with playbooks — the alert is worthless without an owned next-step.
- Survey at moments of value-delivery (after first success, after support resolution), not on calendar cadence; response rate doubles.
- Rebuild thresholds quarterly; what was "healthy" pre-launch of a new tier is "stable" post-launch.
- Auto-escalate critical-bucket drops within 24h; manual triage at this segment loses the account.

## AI-agent gotchas
- LLMs over-credit qualitative signals ("user said they love it") and discount usage decay; weight quantitative facts explicitly in the prompt.
- Sentiment analysis on tickets — prompt the agent to score sentiment 1-5 per message and output the chain, not a single verdict; calibration drift otherwise.
- Don't let an agent send customer-facing emails autonomously; one mis-personalized "we noticed you stopped using X" to a power user damages trust.
- Survey response analysis: agents conflate NPS detractors with customer-success problems; some are pricing complaints — segment.
- Beware of survivor bias: health scores trained on currently-active customers under-weight the signals that drive new customers to churn.
- Token bloat: don't pass full event histories — pre-aggregate to weekly buckets before prompting.
- Privacy: scrub emails / company names if outputs are logged or sent to external APIs.

## References
- ChartMogul SaaS Metrics Guide: https://chartmogul.com/blog/saas-metrics-guide/
- Totango Customer Health Score guide: https://www.totango.com/customer-success-resources/customer-health-score/
- ProfitWell Recur — retention metrics: https://www.profitwell.com/recur/all
- Gainsight Pulse Library (recorded talks)
- "Customer Success" by Mehta/Steinman/Murphy (book)
