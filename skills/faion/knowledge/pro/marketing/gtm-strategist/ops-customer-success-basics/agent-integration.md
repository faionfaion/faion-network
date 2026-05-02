# Agent Integration — Customer Success Basics

## When to use
- Defining "what success looks like" for the first time on a SaaS, course, membership, or service product.
- Building lifecycle email sequences (Day 1 / 3 / 7 / 14 / 30) with triggers tied to product events.
- Computing customer health scores from usage + sentiment + support data and routing at-risk accounts to outreach.
- Designing self-serve enablement (knowledge base structure, onboarding guides, video library taxonomy).
- Constructing expansion playbooks: detect upgrade signals (limits hit, seats added, advanced features used) and trigger relevant offers.

## When NOT to use
- Reactive customer support tickets — use `ops-customer-support` knowledge instead.
- Detailed health-score modeling and CS metrics — use sibling `ops-customer-success-metrics`.
- Churn-prevention forensics on already-churning customers — different methodology (deeper diagnostic, not playbook).
- Enterprise-tier CSM with named-account QBRs — methodology covers framework but agents shouldn't drive strategic conversations.
- Pre-sales / SDR motion — different domain (gtm-strategy, growth-cold-outreach).

## Where it fails / limitations
- Source README is high-touch/low-touch agnostic; doesn't deeply address tech-touch (fully-automated) flows where most solo SaaS lives.
- Health scoring suggested but framework not specified — treat as a starting outline only; needs real data + iteration.
- Engagement cadence ("Day 1, 3, 7, 14, 30") is a default that erodes for B2B with long evaluation cycles.
- "Define success" is product-specific; the four buckets (SaaS / course / service / membership) miss hybrid models (community + tool, hardware + subscription).
- Doesn't address negative-churn dynamics, expansion-MRR economics, or net-revenue retention math.

## Agentic workflow
Run a continuous CS agent: ingests product-event stream (Mixpanel/Amplitude/Segment), Stripe billing, support tickets, NPS responses; computes per-account health weekly; emits a list of at-risk accounts with suggested outreach drafts and a list of expansion-ripe accounts with upgrade prompts. Hand off all customer-facing communication to a human reviewer for personal touchpoints; let automation handle the templated lifecycle drips. Pair with `ops-customer-success-metrics` (KPIs), `ops-customer-support` (tickets), `ops-upselling-cross-selling` (expansion).

### Recommended subagents
- `faion-growth-agent` (source README) — owns CS playbook construction and at-risk triage.
- `faion-content-agent` — drafts the lifecycle emails, success guides, knowledge-base entries.
- `improver` — quarterly: review which playbook actions actually moved retention and prune ineffective touchpoints.
- General-purpose Claude subagent — converts raw event logs to per-customer narrative summaries for human CSM review.

### Prompt pattern
```
For each account in <list>, compute:
- adoption_score: % of core features used in last 30 days,
- engagement_score: weekly logins,
- sentiment_score: from latest NPS + support sentiment,
- billing_signal: usage approaching plan limit?
Output ranked list with reason + suggested next action (email | call | upsell offer | wait).
```

```
Draft a Day-7 check-in email for a customer of <product>. Their usage shows
<events>. Tone: helpful, not salesy. Include one specific tip tied to a feature
they haven't tried. <120 words. Subject line under 50 chars.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `segment-cli` | Pull/replay events into the CS pipeline | segment.com/docs |
| `mixpanel-export` | Pull behavioral events for health scoring | developer.mixpanel.com |
| `amplitude-cli` | Same for Amplitude | amplitude.com/docs/apis |
| `intercom-cli` | Drive Intercom messages, tags, segments | developers.intercom.com |
| `customerio-cli` | Lifecycle email sequences via API | customer.io/docs/api |
| `stripe` | Billing signals (limits, downgrades, failed payments) | stripe.com/docs/cli |
| `gh` | If support is GitHub Issues-based, sync ticket state | cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vitally | SaaS | Yes | API-rich CS platform; good agent fit. |
| Totango | SaaS | Yes | Health scoring, playbooks; API surfaced. |
| Gainsight | SaaS | Partial | Enterprise; API exists but heavy. |
| ChurnZero | SaaS | Yes | Lifecycle automation; integrates with Stripe/Salesforce. |
| Customer.io | SaaS | Yes | Best-in-class transactional + lifecycle email API. |
| Intercom | SaaS | Yes | Messaging + product tours; Fin AI available. |
| Front | SaaS | Yes | Shared inbox; API for routing + tagging. |
| Help Scout | SaaS | Yes | Lighter CS/support hybrid; good API. |
| Mixpanel / Amplitude / PostHog | SaaS / OSS | Yes | Source of truth for usage signals. |
| Notion / GitBook / Document360 | SaaS | Yes | Knowledge base; auto-publish docs from agent output. |
| Delighted / Wootric | SaaS | Yes | NPS / CSAT; API for sentiment ingestion. |
| Discourse / Circle / Discord | SaaS / OSS | Yes | Community surfaces — peer success signal. |

## Templates & scripts
See `templates.md` for CS playbook, customer review, and at-risk intervention sheets. Inline health-score skeleton:

```python
# Minimal customer health score
def health_score(account):
    usage = min(account["weekly_logins"] / 5.0, 1.0) * 40        # max 40
    adoption = min(account["features_used"] / 8.0, 1.0) * 30      # max 30
    sentiment = (account.get("nps", 5) + 100) / 200 * 20          # max 20
    billing_ok = 10 if not account.get("payment_failed") else 0   # max 10
    score = usage + adoption + sentiment + billing_ok
    band = "green" if score >= 75 else "yellow" if score >= 50 else "red"
    return {"score": round(score, 1), "band": band}
```

## Best practices
- Define one north-star success metric per product, not five. "Active projects per team >= 3" beats "engagement composite."
- Trigger touchpoints on behavior (event-based), not on calendar dates. Day-7 email when nobody logged in yet is noise.
- Personalize the variable that matters (their use case, their last action), not the cosmetic ones (first name).
- Make every touchpoint optional to reply to but easy to escalate; one-way drips train customers to ignore you.
- Build the knowledge base before the lifecycle emails; emails should link into existing content, not introduce new content per send.
- Celebrate customer wins publicly (with permission) — case studies double as expansion fuel.
- Set "do not contact" cooldowns; an at-risk account should not get three automated re-engagements in seven days.
- Measure NPS, but treat it as a relative trend, not an absolute. Cohorted NPS over time beats company-wide NPS snapshot.

## AI-agent gotchas
- Agents will draft generic empathy; force grounding in the specific customer's events ("you created project X 3 days ago and haven't returned").
- LLM-summarized sentiment is brittle — sarcasm, code-switching, and short replies confuse it. Always require a confidence score and route low-confidence to humans.
- Health-score thresholds drift with product changes; agents will keep firing old rules. Re-calibrate every product release.
- Auto-generated case studies leak customer details. Mandatory human + customer approval before publication.
- Re-engagement spam is the #1 way agents damage trust; cap automated outreaches at 1 per week per account.
- Agent-written upsell prompts that ignore plan boundaries will offer plans the customer is already on; pull current plan into context every time.
- Do not let an agent issue refunds, plan downgrades, or comp credits autonomously. Human approval required at every billing touchpoint.
- Privacy: customer event logs include PII. Use field-level redaction before sending to external LLM APIs.

## References
- Gainsight CS Resource Hub — https://www.gainsight.com/resources/
- ChurnZero playbooks — https://churnzero.net/resources/
- "Customer Success" by Mehta/Steinman/Murphy — https://www.amazon.com/dp/1119167965
- "The Customer Success Professional's Handbook" — https://www.amazon.com/dp/1119624576
- ChartMogul net-revenue-retention metric — https://chartmogul.com/blog/net-revenue-retention/
- Sibling methodology: `ops-customer-success-metrics/README.md`
- Sibling methodology: `ops-customer-support/README.md`
- Sibling methodology: `ops-upselling-cross-selling/README.md`
