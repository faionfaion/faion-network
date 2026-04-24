# Agent Integration — Product-Led Growth (PM angle)

PM-specific cut on PLG: ownership boundaries, the activation/retention metrics PMs are accountable for, and the hand-offs to growth/marketing that go wrong without instrumentation. The product-operations PLG variant covers tooling and ops; this file covers what a PM signs up for and how to drive it with subagents.

## When to use
- New SaaS / API / dev-tool product where the buyer is also the user (founder, dev, designer, marketer).
- Existing sales-led product losing on CAC payback (>18 months) — convert top-of-funnel to self-serve while keeping enterprise sales-assist.
- Bottom-up wedge into an enterprise account: individual signs up free, expansion to team/org is the business model.
- Product has a measurable "aha moment" reachable in <10 minutes (signup → first value-creating action).
- API / developer product where the integration itself is the activation event (first successful call).
- Pricing-page experimentation: PM owns activation funnel and runs PQL → SQL conversion tests with sales.

## When NOT to use
- True top-down enterprise sales (procurement, RFPs, security review take 6+ months) — PLG instrumentation is fine, but PLG-as-strategy will starve.
- Highly regulated B2B (healthcare, banking) where self-serve onboarding is legally blocked.
- One-time-purchase / transactional products (no retention curve to optimize).
- Marketplaces with cold-start liquidity problems — fix supply/demand before PLG funnels.
- Products that genuinely need a human implementation (data migration, custom modeling) — fake-PLG forces ops to do invisible setup.

## Where it fails / limitations
- **Activation metric drift.** "Activation" gets redefined every quarter to make the chart go up. Without a frozen, written definition tied to retention, the number is decorative.
- **Freemium cannibalization.** Free tier eats paid usage when limits are wrong; PMs lack the pricing instrumentation to detect it (need cohort revenue, not signup count).
- **PQL → sales hand-off rot.** PQL definition is owned by PM, scoring lives in product analytics, but acted on by sales in CRM. Three systems out of sync = silent loss of deals.
- **One-size-fits-all onboarding.** PLG playbooks assume one ICP; in reality multiple personas hit signup and a single tour fails all of them.
- **Vanity North Star.** "Weekly active users" without a revenue link rewards engagement hacks (notifications, streaks) that hurt retention long-term.
- **Time-to-value cliff.** TTV <5 min only matters if the second session happens. PMs over-optimize first-run and lose D7 retention.
- **PLG ≠ no marketing.** Without content/SEO funnel, PLG = empty funnel; PMs ship features instead of fixing acquisition and blame product-market fit.
- **Ownership ambiguity.** Activation owned by PM, conversion owned by growth, retention shared with CS — gaps between handoffs are where churn lives.

## Agentic workflow
PLG is a metric-driven loop, not a feature shipping cadence — the PM's job is to run the loop. Drive it with three subagent passes per week: (1) an analytics agent pulls activation/retention/expansion cohorts from Mixpanel/Amplitude/PostHog and diffs vs. last week; (2) a discovery agent runs `continuous-discovery` interview synthesis on activation drop-off users; (3) an SDD planning agent converts the top friction into a `todo/` task. Persist the metric snapshot at `.aidocs/product_docs/plg-metrics.md` and weekly diffs at `.aidocs/product_docs/plg-weekly/<date>.md`. Hand-off to growth marketing happens via shared dashboard + a single PQL definition file the agent reads.

### Recommended subagents
- `faion-product-manager` skill (this directory's parent) — orchestrator: routes to activation, retention, or expansion sub-tasks.
- `faion-research-agent` (`pro/research/researcher/`) modes `personas`, `pains`, `validate` — generate ICP-segmented activation hypotheses; required input before tour redesigns.
- `faion-market-researcher-agent` — pull competitor PLG benchmarks (free tier limits, paywall placement, public pricing) for diff vs. own funnel.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — turn the weekly top-friction finding into a spec → design → task chain. Critical: PLG without execution loop = analysis paralysis.
- `faion-product-analytics` skill (in product-operations) — define event taxonomy, frozen activation definition, cohort SQL.
- `faion-growth-marketer` (`pro/marketing/growth-marketer/`) — owns the hand-off; PM agent writes PQL spec, growth agent ingests it.
- `faion-conversion-optimizer` (`pro/marketing/conversion-optimizer/`) — A/B testing infrastructure for paywall, upgrade prompts, signup flow.
- A purpose-built **PQL-scoring agent** (worth creating): reads event stream, applies the PQL definition, writes scored leads to CRM webhook. Replaces brittle SQL views.

### Prompt pattern
Weekly metrics pass:
```
You are a product manager analyst. Pull last 7 days of cohort data from
<analytics-source>. Compute: activation rate (% of signups completing
<frozen-event>), D1/D7/D30 retention, PQL count, expansion MRR. Diff
each metric vs. trailing 4-week median. For any metric -1 stdev or
worse, list the top 3 contributing user segments (plan, persona,
acquisition-channel). Output the table from plg-metrics.md template.
No commentary unless a metric crosses an alarm threshold.
```

Activation drop-off pass:
```
You are a product discovery analyst. Given the cohort that signed up
between <date_a> and <date_b> and did NOT complete <activation_event>,
cluster their last-action events into 5 themes. For each theme: name,
sample event sequence, count, hypothesis (one sentence), proposed
experiment (one sentence). Reference customer-interview transcripts in
<path> if available. Reject hypotheses unsupported by either event
data or an interview quote.
```

PQL hand-off spec:
```
You are a PM writing a PQL definition for the growth team. Output a
single yaml block with: pql_name, frozen_event_sequence, threshold_per_user,
threshold_per_account, cooldown_period, sales_action (book_call|email_drip|
ignore), owner_pm, owner_growth, sla_to_action_hours. No prose.
This file is the contract; sales pipeline is broken if it changes
without both owners signing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` (CLI / API) | Self-host analytics, agent-readable HogQL, free tier with no row cap on self-host | https://posthog.com/docs/api |
| `amplitude-python` | Pull cohorts and behavioral cohorts via Dashboard REST | `pip install amplitude-analytics` |
| `mixpanel` (JQL / Query API) | Cohort exports, funnel reports | https://developer.mixpanel.com |
| `dbt` | Model the activation funnel as versioned SQL — frozen definition lives in git, not a dashboard UI | https://docs.getdbt.com |
| `metabase` / `lightdash` | Self-serve BI on top of dbt models for non-PM stakeholders | https://www.metabase.com |
| `growthbook` | Open-source A/B testing, agent-callable feature flag + experiment API | https://docs.growthbook.io |
| `statsig` | Hosted experimentation with a free tier; SDK + REST | https://docs.statsig.com |
| `gh` CLI | Mirror PQL-spec changes as PRs so PM and growth co-sign | https://cli.github.com |
| `claude` (Anthropic CLI) | Run weekly cohort diff and discovery passes headlessly via cron | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS + SaaS | API yes, HogQL is LLM-friendly | Best agentic fit; self-host removes data-pull rate limits. |
| Amplitude | SaaS | API yes (paid tiers) | Strong cohort syntax; expensive at scale, free tier limited. |
| Mixpanel | SaaS | API yes | Solid funnels; free tier 20M events/month. |
| Heap | SaaS | API limited | Auto-capture is great for early PLG, harder to script. |
| June.so | SaaS | API yes | Built-for-PLG; templated activation/retention reports. |
| Userlist / Customer.io | SaaS | API yes | PQL → email automation hand-off; agents can drive campaigns. |
| HubSpot / Salesforce | SaaS CRM | API yes | PQL destination for sales-assisted PLG; agents push scored leads. |
| Userpilot / Appcues / Pendo | SaaS | API yes | In-app tours; treat tours as code (versioned), not as marketing copy. |
| Chameleon | SaaS | API yes | Survey + tour, NPS — agent can rotate copy from experiment results. |
| LaunchDarkly / GrowthBook / Statsig | SaaS / OSS | API yes | Feature flagging + experimentation; required for PLG iteration speed. |
| Stripe (Billing + Metering) | SaaS | API yes | Usage-based pricing infrastructure; expansion revenue lives here. |
| Orb / Metronome | SaaS | API yes | Modern usage billing for PLG products with metered pricing. |
| Pocus / Endgame / Correlated | SaaS | API yes | PLG-specific PQL platforms — score users for sales hand-off. |
| Notion / Linear | SaaS | API yes | PQL spec + activation-definition lives as a versioned doc; agents read it. |

## Templates & scripts

The methodology README ships principles and a metrics table. Gap: there is no concrete activation-definition contract or weekly-snapshot script. Drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# plg-snapshot.sh — weekly PLG metric snapshot for the PM.
# Usage: plg-snapshot.sh [yyyy-mm-dd]
# Reads .aidocs/product_docs/plg-definitions.yml (frozen activation/PQL spec).
set -euo pipefail
date_arg="${1:-$(date -I)}"
out=".aidocs/product_docs/plg-weekly/${date_arg}.md"
mkdir -p "$(dirname "$out")"
python3 - "$date_arg" "$out" <<'PY'
import os, sys, yaml, datetime, json, urllib.request
date_arg, out = sys.argv[1], sys.argv[2]
spec = yaml.safe_load(open(".aidocs/product_docs/plg-definitions.yml"))
host = os.environ["POSTHOG_HOST"]; key = os.environ["POSTHOG_KEY"]
def hogql(q):
    req = urllib.request.Request(f"{host}/api/projects/@current/query/",
        data=json.dumps({"query":{"kind":"HogQLQuery","query":q}}).encode(),
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req).read())["results"]
end = datetime.date.fromisoformat(date_arg); start = end - datetime.timedelta(days=7)
act_event = spec["activation"]["event"]
signups = hogql(f"select count() from events where event='signed_up' and timestamp>='{start}' and timestamp<'{end}'")[0][0]
activated = hogql(f"select count(distinct distinct_id) from events where event='{act_event}' and timestamp>='{start}' and timestamp<'{end}'")[0][0]
rate = (activated/signups*100) if signups else 0
with open(out, "w") as f:
    f.write(f"# PLG snapshot {date_arg}\n\n")
    f.write(f"| Metric | Value | Target |\n|---|---|---|\n")
    f.write(f"| Signups | {signups} | — |\n")
    f.write(f"| Activated | {activated} | — |\n")
    f.write(f"| Activation rate | {rate:.1f}% | {spec['activation']['target_pct']}% |\n")
    f.write(f"| Frozen activation event | `{act_event}` | (do not edit without ADR) |\n")
print(out)
PY
git add "$out" && git diff --cached --stat
```

Wire to cron weekly; commit the snapshot — diffing the file across weeks is the PM's primary signal, not a Looker chart that nobody opens.

## Best practices
- **Freeze the activation definition in YAML, not in a dashboard.** A frozen `activation: {event, threshold, window}` in `.aidocs/product_docs/plg-definitions.yml` survives PM turnover; a Mixpanel chart does not.
- **One PQL, one owner-pair.** Every PQL has exactly one PM and one growth/sales owner. Two PMs splitting a PQL = nobody acts.
- **Activation event must predict D30 retention.** If activated users don't retain materially better than non-activated, your activation definition is wrong, not your funnel.
- **Run a weekly 30-min PLG review with growth.** PM + growth + analytics + 1 engineer. No slides; read the snapshot file. Decide one experiment to ship.
- **Pricing page is a product surface, not marketing.** PM owns it; instrument every CTA; treat copy changes as A/B tests with min sample size.
- **Expansion revenue beats new logos.** NRR >120% covers a multitude of acquisition sins; track per-cohort expansion, not aggregate MRR.
- **Time-to-second-value matters more than time-to-first-value.** D1 to D7 conversion is the real growth lever once TTV is sub-10-min.
- **Limit free tier on the dimension that scales with value, not signup count.** Throttling new users hurts top-of-funnel; throttle on usage that correlates with willingness-to-pay.
- **Hand-off to sales-assist via webhook, not Slack message.** A PQL fires → CRM enrichment → SDR queue. Slack pings rot.
- **Keep an "activation graveyard"** — past activation definitions and why they were retired. Prevents reverting to a metric that broke the team last year.

## AI-agent gotchas
- **LLM "activation rate is great" hallucination.** Agents will confidently restate a number without checking the time window. Force the agent to print the SQL/HogQL it ran and the row count it received before any commentary.
- **Drift between PQL spec and SQL.** Agent edits the YAML but not the dbt model, or vice versa — funnel silently changes. CI must verify spec-yaml hash matches model annotation.
- **Funnel-drop hypothesis collapse.** Single-agent runs converge on "improve onboarding copy." Use 3 agents with separate roles (data, customer voice, competitor) and force divergent hypotheses before merging.
- **Survivorship bias on retention cohorts.** Agent reports "D30 retention is 60%" but excludes cohorts that haven't aged 30 days. Force explicit cohort-age filter in every retention query.
- **PQL inflation.** Agent loosens PQL thresholds because count is too low. Threshold changes are governance events; require a `git diff` review on `plg-definitions.yml`, never accept inline tweaks.
- **Expansion attribution.** Agent credits expansion to the last feature shipped; usage growth has multi-week lag. Use a fixed attribution window per the spec, not "what feels recent."
- **Persona collapse.** Agent treats all signups as one persona; PLG funnels are persona-specific (developer vs. designer vs. PM signing up). Segment before reporting; reject single-cohort outputs.
- **Hand-off prompt-injection risk.** PQL spec lives in a YAML the sales agent reads; if untrusted user content lands there (e.g., from a survey free-text), it can hijack the sales action. Treat the file as a contract, validate schema before any agent ingest.
- **No human checkpoint on pricing/paywall changes.** Agents must NOT autonomously change paywall placement, free-tier limits, or pricing — those are revenue-impacting governance decisions. Human-in-the-loop gate required.
- **Confidentiality leak in cohort exports.** Cohort dumps include emails, plan tier, sometimes free-form survey text. Run `password-scrubber-agent` before sharing analytics output externally or with broad-access bots.

## Hand-off contracts (PM ↔ growth/marketing)
| Artifact | Owner | Reader | Format | Cadence |
|----------|-------|--------|--------|---------|
| `plg-definitions.yml` (activation, PQL, frozen events) | PM | growth, sales, analytics | YAML in repo | Edit only via PR, both owners sign |
| `plg-weekly/<date>.md` snapshot | PM (auto via agent) | all | Markdown in repo | Weekly Monday 09:00 |
| Funnel experiment brief | PM | growth + design | `.aidocs/product_docs/experiments/<id>.md` | Per experiment |
| Onboarding tour copy | growth | PM (review) | Userpilot/Appcues + git-tracked export | Per release |
| PQL → CRM payload schema | PM + growth | sales | JSON schema in repo | Versioned, semver |
| ICP segment list | growth | PM (input to discovery) | YAML | Quarterly |
| Pricing-page A/B results | PM | growth, finance | `.aidocs/product_docs/pricing-tests/<id>.md` | Per test |

## References
- Wes Bush (2019). *Product-Led Growth*. ProductLed Press. (Origin of the modern PLG playbook.)
- OpenView — Product-Led Growth Index. https://openviewpartners.com/product-led-growth/
- Reforge — *Mastering Product-Led Growth* curriculum. https://www.reforge.com
- Lenny Rachitsky — *PLG metrics, activation, retention* essays. https://www.lennysnewsletter.com
- Amplitude — *North Star Playbook*. https://amplitude.com/north-star
- Andrew Chen — *The Cold Start Problem* (network-effect side of PLG). https://andrewchen.com
- Sequoia — *PLG benchmarks 2024–2025*. https://www.sequoiacap.com
- Sibling methodologies in this repo: `pro/product/product-operations/product-led-growth/`, `pro/marketing/growth-marketer/`, `pro/marketing/conversion-optimizer/`, `pro/product/product-manager/product-analytics/`.
