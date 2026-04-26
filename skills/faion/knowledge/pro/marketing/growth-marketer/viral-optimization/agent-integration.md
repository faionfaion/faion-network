# Agent Integration — Viral Loop Optimization

## When to use
- Product already has a working invite/share path and a measured baseline K-factor (even K = 0.05 is fine — you can iterate).
- Event tracking captures the full chain: `invite_shown → invite_sent → invite_clicked → invitee_signup → invitee_active`.
- A live A/B-test framework is wired (LaunchDarkly / Optimizely / Statsig / GrowthBook) so variants can be split without code redeploys.
- You have ≥5,000 weekly users entering the loop, otherwise sample size kills experiments.

## When NOT to use
- Pre-PMF: optimizing K of a product nobody loves yields K = 0.0X × any-multiplier = still nothing.
- B2B enterprise where sharing is gated by procurement/security — viral mechanics do not translate.
- Markets with strict anti-spam rules (regulated finance, medical, EU consumer) where contact-import is non-compliant.
- Products whose value to the inviter requires the invitee to sign up but the invitee has zero standalone reason to — that is "forced virality" and it churns invitees fast.

## Where it fails / limitations
- K is fragile to fraud: incentivized loops attract self-referrers and bot signups; "raw K" looks great while real LTV plummets.
- Cycle time matters as much as K. K = 0.4 with 3-day cycle beats K = 0.7 with 60-day cycle in compounding.
- Holdouts are hard to design — the network effect of one variant can leak into the control via shared social graphs.
- "Personalized invite" wins early then plateaus; users learn the pattern. Expect decay.
- One-click contact import is dead in iOS / Android post-2021 privacy changes; Hotmail-import strategies of 2008 do not work today.

## Agentic workflow
Drive viral optimization with subagents in a tight loop: agent reads K-funnel data, proposes 1–3 hypotheses ranked by Impact × Confidence × Ease, writes A/B-test specs from `templates.md`, drafts variant copy, then waits for human green-light before any code or live-channel change. After test maturity, agent runs significance check (against `statistics-application`), summarizes lift, and proposes the next experiment.

### Recommended subagents
- `growth-marketer` (sonnet) — funnel analysis, hypothesis generation, copy drafts.
- `data-analyst` (sonnet) — K-factor decomposition (i, c, cycle time), invitee-LTV check.
- `experiment-designer` (sonnet) — sample-size math, randomization unit, MDE calc.
- `fraud-checker` (sonnet) — referrer-IP / device-graph anomaly review on referral incentives.

### Prompt pattern
```
Input: viral_funnel_30d.csv (impressions, sends, clicks, signups, activations by variant, by cohort)
Task: 1) compute i, c, K, cycle_time per cohort
      2) rank top 3 drop-offs by absolute user loss
      3) propose ONE A/B test per drop-off using ab-testing-setup template
Output: yaml with hypothesis, variant_spec, primary_metric, mde, sample_size, days_required
Forbidden: claiming a winner before n >= sample_size AND days >= 14
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `growthbook` CLI | Define experiments, push variant configs | `npm i -g @growthbook/cli` |
| `statsig` CLI | Experiment scaffolding, power calc | https://docs.statsig.com/cli |
| `posthog` CLI | Funnel + cohort export, feature flags | `npm i -g posthog-node` |
| `branch.io` CLI | Deferred-deeplink referral attribution | https://help.branch.io |
| `mixpanel-utils` | Bulk export of invite/conversion events | `pip install mixpanel-utils` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Viral Loops | SaaS | Yes — REST + JS SDK | Templated referral campaigns; agent can draft/clone via API |
| ReferralCandy | SaaS | Yes — REST API | Ecommerce referral, Shopify-native |
| Friendbuy | SaaS | Yes — REST API | Two-sided referral with anti-fraud built in |
| GrowSurf | SaaS | Yes — REST API | Waitlist + referral, lightweight |
| Branch | SaaS | Yes — REST + SDKs | Cross-platform deferred deeplinks for invite attribution |
| AppsFlyer / Adjust | SaaS | Yes — REST | Mobile attribution; needed for K on iOS/Android |
| GrowthBook | OSS + SaaS | Yes — REST + GitOps | A/B framework, agent can author experiments |
| Statsig | SaaS | Yes — REST + SDKs | Experimentation; CUPED variance reduction |
| Optimizely | SaaS | Partial — heavy console | Not ideal for agent-driven creation |

## Templates & scripts
See `templates.md` and the README's "A/B Test Template" for the canonical experiment doc. For K decomposition, this 25-line script unpacks the funnel:

```python
# k_factor.py — compute K and cycle time from event stream
import pandas as pd

ev = pd.read_csv("events.csv", parse_dates=["ts"])
inv = ev[ev.type == "invite_sent"]
sig = ev[ev.type == "invitee_signup"]

i = inv.groupby("inviter_id").size().mean()
matched = sig.merge(inv, left_on="ref_token", right_on="ref_token", suffixes=("_s", "_i"))
c = len(matched) / max(len(inv), 1)

cycle = (matched.ts_s - matched.ts_i).dt.days
K = i * c
print(f"i={i:.2f}  c={c:.2%}  K={K:.3f}  cycle_p50={cycle.median():.1f}d")

# Decay check: K by inviter cohort week
inv["cohort"] = inv.ts.dt.to_period("W")
print(inv.groupby("cohort").size().describe())
```

## Best practices
- Optimize `c` (invitee conversion) before `i` (invites sent) — improving the landing page lifts every future loop turn.
- Personal invites ("Anna invited you") beat brand invites by 20–40% on click and signup; cost is one DB join.
- Reward at value-realization, not at signup — cuts incentive fraud massively.
- Track invitee D30 retention separately; if it's <50% of organic, your loop is poisoning the cohort.
- Cap one-time rewards but tier multi-referral (5 → bigger reward, 25 → premium tier) to capture power-referrers.
- Move share moments to peak emotion (just-completed-a-thing), not to settings menus.

## AI-agent gotchas
- Agents will quote the README's "+125x improvement" case as if it is achievable — anchor expectations to your category's K (consumer apps live at 0.1–0.3, B2B SaaS at 0.05–0.2).
- LLMs invent invite-copy claims ("join 50,000 people") that are factually wrong; require numeric claims to be passed in as inputs, not produced.
- Significance: the agent must check sample size and runtime against MDE before declaring a winner; otherwise it will ship noise.
- Two-sided incentives change unit economics — let a `pricing-reviewer` opus pass approve any new reward structure.
- Contact-import "ideas" generated by LLMs often violate platform TOS or privacy law (CASL, GDPR, CCPA). Filter at template stage.
- Fraud detection is adversarial; an agent that "optimizes" without fraud feedback will recommend mechanics that maximize gameable referrals.

## References
- Andrew Chen, "What's your viral loop?" — https://andrewchen.com/whats-your-viral-loop
- Adam Penenberg, "Viral Loop" (book, 2009)
- Reforge, "Growth Models" — https://www.reforge.com/blog/growth-loops
- Lenny Rachitsky, "How the biggest consumer apps got their first 1000 users" — https://www.lennysnewsletter.com
- Jonah Berger, "Contagious: Why Things Catch On" (book)
- Branch, "Mobile attribution for viral loops" — https://branch.io/blog
