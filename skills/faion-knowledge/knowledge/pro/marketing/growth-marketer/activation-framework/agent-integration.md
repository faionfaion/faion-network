# Agent Integration — Activation Framework & Path Optimization

## When to use
- You have signups but mediocre week-1 retention and need to find the bottleneck.
- You're choosing/validating an activation event ("aha moment") that should correlate with long-term retention.
- You need to map a funnel, instrument missing events, and prioritize which drop-off to attack first.
- You want an agent to maintain a living activation dashboard and propose weekly experiments.

## When NOT to use
- You haven't shipped product yet — design activation into onboarding from day one, no need for a remediation framework.
- Pre-PMF: low activation might be a wrong-product/wrong-audience signal, not a friction problem. Solve PMF first.
- Sales-led B2B: "activation" happens in human-led implementation; CSM playbooks beat self-serve frameworks.
- Single-session products (utility / one-off purchase) where retention is irrelevant.

## Where it fails / limitations
- Wrong activation metric: optimizing "completed onboarding" when the real predictor is "shared a doc" leads to fake wins.
- Survivorship bias: comparing activated vs non-activated users finds correlations that aren't causal.
- Friction-only thinking misses motivation gaps; sometimes users CAN activate but don't WANT to yet.
- Agents over-trust funnel drop-offs without checking session recordings or qualitative input.
- Cross-device/cross-session activation is invisible to most analytics; agents miss it without identity stitching.

## Agentic workflow
On `opus`, a strategist defines/audits the activation event and reviews retention correlation. A `sonnet` analyst maps the funnel from event data, identifies top 3 drop-offs, and writes hypothesis cards (ICE-scored). A `haiku` ops agent computes weekly activation rate, segments by source/persona, and posts deltas. A `sonnet` copy agent drafts onboarding microcopy, tooltip text, and email-sequence variants for top experiments.

### Recommended subagents
- `faion-growth-agent` (opus) — activation event definition, retention correlation analysis.
- `faion-conversion-optimizer` agent — funnel drop-off prioritization, ICE scoring.
- Data/haiku subagent — weekly activation rate, segment cuts.
- Copy/sonnet subagent — onboarding microcopy, email sequences.

### Prompt pattern
```
Given retention curves for users who did vs did not perform {candidate_event}
within {window} of signup, score the event as a candidate activation
metric. Output: lift in D7/D30 retention, % of signups achieving event,
recommendation (use / replace with X).
```

```
Analyze the funnel {step_1 → step_2 → ... → activation} for last 30d.
Return drop-off table, top 3 fixes ranked by ICE (Impact, Confidence,
Ease 1-10), and a hypothesis card per fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `amplitude` Behavioral Cohorts | Funnel + retention correlation in one place | https://amplitude.com/docs |
| `posthog` (OSS) | Self-host funnels + session recordings | `pip install posthog` |
| `mixpanel` Insights API | Funnel + retention via JQL | `pip install mixpanel` |
| `metabase` / `superset` | SQL dashboards for activation tracking | OSS, self-host |
| FullStory / LogRocket / Hotjar | Session recordings to diagnose drop-offs | dashboards (limited API) |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Amplitude | SaaS | Yes (REST + JQL) | Best behavioral cohort UX |
| Mixpanel | SaaS | Yes (REST) | Mature funnel API |
| PostHog | OSS | Yes (REST) | Self-host, agents can query directly |
| Appcues | SaaS | Yes (REST) | Programmatic onboarding flows, target segments |
| Pendo | SaaS | Partial | Strong UI; API exists but heavier |
| Userflow | SaaS | Yes (REST) | Lightweight onboarding, dev-friendly |
| Customer.io | SaaS | Yes (REST) | Trigger emails on activation events |
| Hotjar / FullStory | SaaS | Partial | Recordings; agent can list, can't auto-watch |

## Templates & scripts
See `templates.md` for funnel and friction-mapping blocks. Inline ICE-score helper:

```python
# ice.py — agent prioritizes activation experiments
def ice_score(impact: int, confidence: int, ease: int) -> float:
    """Each 1-10. Returns 0-10 averaged score."""
    return round((impact + confidence + ease) / 3, 2)

experiments = [
    {"name": "Magic-link signup", "i": 8, "c": 7, "e": 9},
    {"name": "Sample data on first login", "i": 7, "c": 8, "e": 8},
    {"name": "Segment-based onboarding", "i": 9, "c": 5, "e": 4},
]
ranked = sorted(
    [{**x, "ice": ice_score(x["i"], x["c"], x["e"])} for x in experiments],
    key=lambda r: r["ice"], reverse=True,
)
```

## Best practices
- Define activation as a behavior that correlates strongly with D30+ retention, not as an internal milestone (e.g. "completed onboarding").
- Target retained-user behavior in week 1: "added 3 contacts within 24h", "shared 1 doc within 48h", "ran 2 reports within 7d".
- Map the funnel exhaustively before optimizing; agents tend to attack the biggest visible drop-off without confirming it's causal.
- Always run an A/B test for friction reductions; "obvious wins" sometimes regress against guardrail metrics.
- Reduce signup friction last, not first — easy signups inflate top-of-funnel and hide downstream issues.
- Watch 20+ session recordings before forming hypotheses; LLMs can't replace qualitative pattern recognition here.

## AI-agent gotchas
- The agent will pick a high-completion event as "activation" because it looks healthy — force it to score against retention lift, not absolute frequency.
- Funnel events with the same name across web/app but different definitions cause silent drop-offs; agent must list event-name + platform pairs.
- "Time-to-activation" needs a fixed window (e.g. 7d); leaving it open inflates rate and breaks comparisons week-over-week.
- Onboarding-flow tools (Appcues/Pendo) cache content; the agent must invalidate or version-tag flows when shipping copy changes.
- Don't let the agent ship microcopy variants directly to production — route through a feature-flag and an A/B test.
- Cross-device users get attributed twice; require the agent to use a stable user-id, not anonymous distinct_id.

## References
- Wes Bush, *Product-Led Growth* (activation chapters)
- Samuel Hulick, *The Elements of User Onboarding*
- Reforge, "Activation & Retention" course (Casey Winters)
- Andrew Chen, "New data shows up to 77% of your DAUs disappear after 3 days" — https://andrewchen.com/
- Sean Ellis, *Hacking Growth* (North Star + activation)
