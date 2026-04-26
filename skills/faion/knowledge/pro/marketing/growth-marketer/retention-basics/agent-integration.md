# Agent Integration — Retention Basics

## When to use
- Post-acquisition users drop off and you cannot identify a single dominant cause; a structured retention-loop / Hook-model audit is the right first step.
- New product feature that needs to be evaluated as a retention driver (does it create a trigger / variable reward / investment?).
- Onboarding redesign or "habit formation" workstream — needs explicit framing of which loop type the product depends on.
- Companion to `cohort-basics` (measurement) and `retention-strategies` (tactics) — `retention-basics` is the framing layer.

## When NOT to use
- Pre-PMF: there is no habitual user yet; chase value, not loops.
- One-off / transactional products (tax filing, event ticketing) where "retention" means repeat-purchase next cycle, not daily return — different model.
- Enterprise contracts where engagement is not user-driven (compliance tools, audit software) — retention is decided by procurement, not Hook loops.
- B2B tools with a small DAU but high economic value per session — DAU/MAU is misleading; measure feature-completion or workflow retention instead.

## Where it fails / limitations
- The Hook model is a design lens, not a causal theory — applying it does not guarantee retention; PMF still dominates.
- "Variable reward" can drift into addictive or manipulative design (slot-machine notifications). Ethical and regulatory risk in EU/UK/AU.
- Streak mechanics work for some categories (learning, habit) and backfire in others (work tools, finance) where users want predictability.
- DAU/MAU is a vanity metric for many products; a lot of "retained" users may be passive.
- Trigger fatigue: too many push/email triggers degrade open rates and produce uninstall waves.

## Agentic workflow
Use subagents to (1) classify your product into a retention-loop type, (2) walk the Hook model on each core flow and find missing components, (3) propose triggers / rewards / investments mapped to user lifecycle, and (4) draft messaging copy and schedule policy. Keep the agent off the live messaging tool — it produces drafts and trigger-rule specs; humans review for fatigue, ethics, regional compliance.

### Recommended subagents
- `growth-marketer` (sonnet) — retention-loop classification, Hook walkthrough, copy.
- `product-designer` (opus) — investment mechanics that survive long term.
- `lifecycle-marketer` (sonnet) — trigger schedule, channel mix, fatigue caps.
- `data-analyst` (sonnet) — define retention metric (DAU/MAU vs feature-completion) per product type.

### Prompt pattern
```
Input: product type + 5 core user flows + current trigger/reward inventory
Task: 1) pick primary retention-loop type with rationale
      2) for each flow: list trigger -> action -> variable_reward -> investment
      3) mark missing components and propose ONE concrete fix per gap
      4) propose a fatigue cap (max triggers/day, suppression windows)
Output: markdown table per flow + JSON of trigger schedule (channel, timing, condition)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `customer.io` CLI | Manage lifecycle campaigns from CI | `npm i -g customerio-cli` |
| `braze-cli` | Push canvas / campaign config | https://www.braze.com/docs |
| `posthog` CLI | Cohort + funnel definitions for retention | `npm i -g posthog-node` |
| `dbt-core` | Materialize retention curves and trigger eligibility | `pip install dbt-core` |
| `iterable-cli` (community) | Templated campaign edits | https://api.iterable.com/api/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Customer.io | SaaS | Yes — Track + App API | Behavioral lifecycle, segments, journeys |
| Braze | SaaS | Yes — REST | Multi-channel; rich Canvas API |
| Iterable | SaaS | Yes — REST | Email + push + in-app |
| OneSignal | SaaS / OSS SDKs | Yes — REST | Push + web push |
| Klaviyo | SaaS | Yes — REST | Ecommerce retention flows |
| MoEngage | SaaS | Yes — REST | App engagement, journey orchestration |
| Mixpanel / Amplitude | SaaS | Yes — REST | Retention metrics + cohorts feeding triggers |
| PostHog | OSS + SaaS | Yes — REST | Cohort triggers + feature flags + experiments |

## Templates & scripts
See the README "Hook Model" mapping template and the "When user [TRIGGER], they [ACTION] to get [REWARD], which causes them to [INVEST]" sentence template. For a quick DAU/MAU + WAU rolling computation feeding the retention review:

```python
# retention_curves.py — DAU/MAU + 8-week curve
import pandas as pd
ev = pd.read_csv("events.csv", parse_dates=["event_date"])
ev = ev[ev.event_type == "core_action"]

dau = ev.groupby(ev.event_date.dt.date).user_id.nunique()
mau = ev.set_index("event_date").user_id.resample("D").apply(
    lambda s: ev[(ev.event_date >= s.name - pd.Timedelta("30D")) & (ev.event_date <= s.name)].user_id.nunique()
)
print("DAU/MAU last 7d:", (dau / mau).tail(7).round(2).to_dict())

# Weekly retention curve (week 0..7)
ev["week"] = ev.event_date.dt.to_period("W")
first = ev.groupby("user_id").event_date.min().dt.to_period("W").rename("cohort")
df = ev.merge(first, on="user_id")
df["week_offset"] = (df.week - df.cohort).apply(lambda x: x.n)
curve = df[df.week_offset.between(0, 7)].groupby(["cohort", "week_offset"]).user_id.nunique().unstack()
print(curve.div(curve[0], axis=0).round(2).tail(8))
```

## Best practices
- Pick the right metric per product: DAU/MAU for habit products, weekly active for tools, monthly active for utilities — using the wrong one chases ghosts.
- Move from external triggers (email/push) to internal triggers (user thinks of you when stimulus X) — the lifecycle plan should taper external triggers as internal triggers form.
- Rewards must be variable and earned; rigged-feeling rewards (bots posting fake "likes") destroy trust quickly.
- Investment compounds value: every onboarding step should add data, customization, or social ties that make returning more valuable.
- Cap notification frequency per user per day and per category; track unsubscribe + uninstall as primary fatigue signals.
- Streaks are powerful but high-risk — provide streak-freeze / forgiveness or you punish your power users for taking a vacation.

## AI-agent gotchas
- LLMs love to recommend "gamification" as a fix; in B2B and finance categories this is wrong and erodes trust. Constrain by product category.
- The Hook model can be misapplied to dark-pattern designs (infinite scroll, anxiety triggers); require ethical constraints in the prompt and have a human reviewer.
- Trigger drafts often miss fatigue rules — have the agent emit a fatigue policy alongside any new trigger.
- Retention metric ambiguity: "active" must be defined operationally; agents that say "improve retention" without a definition are useless.
- Variable-reward generators tend toward unpredictability for unpredictability's sake; the reward must still be net-positive in expectation, or users feel cheated.
- Causal claims ("streaks caused +5pp D30") need an experiment, not a Hook walkthrough; redirect to `ab-testing-basics`.

## References
- Nir Eyal, "Hooked: How to Build Habit-Forming Products" (book)
- Nir Eyal, "Indistractable" (counterpoint on ethical use)
- Andrew Chen, "DAU/MAU is an important metric" — https://andrewchen.com
- Brian Balfour, "Retention is the King of SaaS metrics" — https://brianbalfour.com
- Casey Winters, "Retention deep dive" — https://caseyaccidental.com
- Reforge "Retention + Engagement" — https://www.reforge.com
- BJ Fogg, "Tiny Habits" (book) — behavior model complementary to Hook
