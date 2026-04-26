# Agent Integration — Viral Loops & Types

## When to use
- You're choosing between WOM, inherent, incentivized, content, or outbreak loops for a new product or vertical.
- You're trying to raise K-factor by 0.1-0.3 and need a structured experiment plan rather than ad-hoc tweaks.
- You're modeling growth in a planning doc and need realistic K, i, c benchmarks per loop type.
- You want an agent to instrument share-moment events and report loop health weekly.

## When NOT to use
- You haven't proven retention — virality on a leaky bucket just speeds churn.
- B2B enterprise with 6-month sales cycles — loops won't compound on that timescale, focus on ABM.
- Heavily regulated products (medical, financial) where outbound viral mechanics breach compliance.
- Pre-launch with no users — modeling K is fine, but optimization must wait until you have invite-event data.

## Where it fails / limitations
- LLMs love to recommend "make it inherent" for non-collaborative products — forced inherent virality kills NPS.
- Outbreak/spam loops still get suggested by older sources; modern email and OS protections kill them and damage brand.
- Wordle-style content virality is survivorship-biased; most copies fail because the share artifact lacks novelty.
- K is volatile early; sample size for K significance is much larger than for typical conversion tests.
- Loop type is rarely pure — most products run 2-3 loops in parallel and attribution between them is messy.

## Agentic workflow
On `opus`, a strategist agent picks 1-2 loop types per product type, drafts share-moment events, and models target K. A `sonnet` agent writes share-flow copy and designs the artifact (image, link preview, OG meta). A `haiku` ops agent computes i, c, K weekly from analytics, splits by loop and segment, and posts a delta vs previous week to a dashboard or Slack channel.

### Recommended subagents
- `faion-growth-agent` (opus) — loop selection, K modeling, growth simulation.
- Copy/sonnet subagent — share copy, artifact design brief, OG metadata.
- Data/haiku subagent — i, c, K computation per loop, anomaly detection.

### Prompt pattern
```
Given product = {description}, user count = {N}, retention curve = {curve},
recommend 1-2 viral loop types. For each: target K, top 3 share moments,
required instrumentation events, expected time to K=0.5. Cite which
benchmark range you used.
```

```
Compute i, c, K for last 14d split by loop_type in {events_table}.
Compare to prior 14d. Flag any loop where K dropped >20%. Return markdown
table + one-line diagnosis per loop.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` SDK | Open-source product analytics, custom K dashboards | `pip install posthog` |
| `mixpanel` SDK | Funnel + cohort for invite → signup conversion | `pip install mixpanel` |
| `amplitude` Data API | i/c/K via JQL or behavioral cohorts | https://amplitude.com/docs/apis |
| `segment` CLI | Route share events to multiple destinations | `npm i -g @segment/cli` |
| `branch` / `appsflyer` | Mobile deep-link attribution for invite flows | dashboards + REST APIs |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Branch | SaaS | Yes (REST) | Deep links, cross-platform invite attribution |
| AppsFlyer | SaaS | Yes (REST) | Same, larger enterprise focus |
| PostHog | OSS | Yes (REST + self-host) | Best for agent-driven analysis on owned infra |
| Mixpanel | SaaS | Yes (REST + JQL) | Mature behavioral cohorts |
| Amplitude | SaaS | Yes (REST) | Strongest funnel/cohort UX |
| Customer.io | SaaS | Yes (REST) | Trigger invite emails on share-moment events |

## Templates & scripts
See `templates.md` for the referral-program design block. Inline simulator:

```python
# viral_sim.py — agent uses to compare loop choices
def simulate(initial: int, k: float, cycle_days: int, days: int) -> int:
    cycles = days // cycle_days
    users = initial
    for _ in range(cycles):
        users = users + int(users * k)
    return users

# Compare 30d for K=0.4 (good WOM) vs K=0.8 (incentivized)
# print(simulate(1000, 0.4, 7, 30))  # ~3,800
# print(simulate(1000, 0.8, 7, 30))  # ~10,500
```

## Best practices
- Pick the loop type that matches the product's natural use, then layer one secondary loop. Don't try to run 4 loops at once.
- Instrument the share moment as a first-class event with `loop_type`, `share_channel`, `recipient_count` properties before launch.
- Treat K below 0.5 as a supplement, not a strategy — pair with paid or content acquisition.
- Optimize cycle time as aggressively as K — halving cycle time roughly equals doubling K in compounding terms.
- Re-baseline K quarterly; product changes silently break loops (a redesigned share button can drop i by 40%).

## AI-agent gotchas
- Models confuse K with conversion rate; force the prompt to specify K = i × c.
- Never let an agent push outbreak (auto-contact-import) loops without explicit human approval — TOS and CAN-SPAM landmine.
- Sample-size warning: weekly K computed on <500 invites is noise; agent should flag low-power computations rather than report them.
- Agents tend to over-fit on Dropbox/PayPal case studies; require it to cite a benchmark range from the README before recommending a target K.
- Mobile attribution agents must use the same client_id across web and app — passing different IDs silently breaks K.

## References
- Andrew Chen, *The Cold Start Problem*
- Adam Penenberg, *Viral Loop*
- Sean Ellis, *Hacking Growth*
- David Skok, "Lessons Learned — Viral Marketing" — https://www.forentrepreneurs.com/lessons-learnt-viral-marketing/
- Reforge, "Growth Loops" course (Brian Balfour)
