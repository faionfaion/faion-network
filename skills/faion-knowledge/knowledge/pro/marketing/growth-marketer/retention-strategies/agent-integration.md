# Agent Integration — Retention Strategies

## When to use
- D1/D7/D30 retention is below target and you've established product-market fit (paying users exist, but they don't return).
- Designing a new product surface where you can choose retention loop type (content / social / progress / stored value / workflow / network).
- Refactoring lifecycle messaging when re-engagement campaigns have decayed (open rates dropping, dormant cohort widening).
- Adding gamification (streaks, achievements, leagues) to consumer SaaS or learning products and need a pattern reference.

## When NOT to use
- Pre-PMF: improving retention curves on a non-resonating product is rearranging deck chairs; fix activation/value-prop first.
- B2B-enterprise multi-stakeholder products where the user is not the buyer; "streaks" and gamification feel out of place.
- One-shot transactional products (single-purchase courses, e-commerce) — repeat-purchase strategies and lifecycle email work better than retention loops.
- Products without a stable event-tracking foundation; designing loops on top of unreliable data produces phantom wins.

## Where it fails / limitations
- Notification fatigue: aggressive push/email cadence drives opt-outs and OS-level mute; permanent loss of trigger surface.
- Gamification pasted on top of weak core value: streaks fail if the lesson/feature itself has no inherent reward.
- Survivor bias: studying current cohorts misses the signals that drove churned users out; need cohort-level analysis.
- Variable-reward systems can drift toward dark-pattern manipulation; brand and trust risk.
- Stored-value loops only work if export/portability friction stays subtle; obvious lock-in triggers backlash and regulatory scrutiny.

## Agentic workflow
Subagents help discover which loop is operative, design candidate loop variants, draft notification/email copy, score user lifecycle states, and propose A/B tests. The product/UX decisions, ethical guardrails on dark patterns, and threshold-tuning sit with humans. Pipeline: cohort retention curve analysis (agent) → loop diagnosis (agent) → candidate loop redesign (agent) → A/B test plan (agent) → human approval → instrumentation (agent) → measurement (agent).

### Recommended subagents
- `general-purpose` — pull cohort retention data, segment by behavior, build hook-model breakdown of current product.
- `faion-content-agent` — draft re-engagement email sequences, push-notification variants, in-app prompts.
- Custom `lifecycle-agent` (build): owns daily user-state classification (active / slipping / dormant / churned) and per-state action recommendations.

### Prompt pattern
- "Given this 12-week cohort retention CSV, identify the curve shape (smile/decay/flat) and the cliff (which week loses most users). Hypothesize 3 retention-loop interventions and rank by expected lift × effort."
- "Draft a 5-email re-engagement sequence for users dormant 14-60 days. Each email: subject + 80-word body + CTA. Tone: helpful, not pleading. Avoid superlatives. End with 'is everything okay?' last touch only."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Build cohort + retention models in warehouse | `pip install dbt-core` |
| `duckdb` | Local cohort analysis on event CSV exports | `brew install duckdb` |
| `pandas` / `polars` | Cohort + retention curve scripting | `pip install pandas` |
| `streamlit` / `evidence-dev` | Lightweight retention dashboards | `pip install streamlit` |
| Mixpanel / Amplitude CLI | Pull cohort retention reports | platform docs |
| OneSignal / Firebase CLI | Push notification dispatch | https://documentation.onesignal.com |
| Customer.io / Iterable APIs | Lifecycle email orchestration | platform docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mixpanel | SaaS | API yes | Cohort retention curves |
| Amplitude | SaaS | API yes | Behavioral cohorts + retention |
| PostHog | SaaS / OSS | API yes | Self-host, retention reports |
| Heap | SaaS | API yes | Auto-capture, retention |
| Customer.io | SaaS | API yes | Trigger-based lifecycle |
| Iterable | SaaS | API yes | Cross-channel orchestration |
| Braze | SaaS | API yes | Mobile + push focus |
| OneSignal | SaaS | API yes | Push notifications |
| Firebase Cloud Messaging | SaaS | API yes | Free push |
| Pendo / Appcues | SaaS | API yes | In-app prompts + tours |
| Intercom | SaaS | API yes | In-app messages |
| Iterable Catalyst / Reforge | content | n/a | Retention pattern libraries |
| Hopscotch / Userpilot | SaaS | API yes | In-app onboarding hooks |

## Templates & scripts
The README inlines a streak helper. Inline cohort-curve helper:

```python
# cohort_retention.py — D-N retention by signup week
import pandas as pd

def cohort_retention(events, action_event="active", windows=(1, 7, 14, 30)):
    df = events.copy()
    df["signup_week"] = df.groupby("user_id")["timestamp"].transform("min").dt.to_period("W")
    df["days_since_signup"] = (
        df["timestamp"] - df.groupby("user_id")["timestamp"].transform("min")
    ).dt.days
    out = []
    for w, g in df[df.event == action_event].groupby("signup_week"):
        size = g["user_id"].nunique()
        row = {"cohort": str(w), "size": size}
        for n in windows:
            row[f"D{n}"] = g[g.days_since_signup <= n]["user_id"].nunique() / size
        out.append(row)
    return pd.DataFrame(out)
```

## Best practices
- Diagnose loop type before redesigning: TikTok-style content loops fail if pasted onto a workflow tool, and vice versa.
- Pair every external trigger (push/email) with an internal trigger (habit, time-of-day, emotional cue) to avoid notification dependence.
- Set notification budgets per user; aggressive cadence destroys the surface long-term, modest cadence compounds.
- Re-engagement: respect quiet hours, rate-limit per channel (max 1/day), kill any user who marks emails as spam.
- Test variability of rewards; static rewards saturate users in 30-60 days, variable rewards keep engagement curves elevated longer.
- Streak design must include a "freeze" mechanic; otherwise vacations / sickness break streaks and trigger churn from frustration.
- Measure leading indicator (D7/D14 active days, sessions/week) per cohort, not aggregate DAU/MAU which masks new-user growth covering churn.

## AI-agent gotchas
- LLMs over-prescribe gamification — every problem looks like a streak. Force the agent to justify pattern choice via product context.
- Re-engagement copy drifts to guilt-trips ("we miss you"); set a tone constraint and ban specific phrases.
- Don't let agents send push notifications autonomously — wrong-time-zone or wrong-segment fires are unrecoverable.
- Cohort math errors: agents conflate "users active in week N" with "users retained at week N"; force them to define the metric in plain English first.
- Dark-pattern risk: agents copy attention-economy patterns (FOMO, false scarcity, infinite scroll) without ethical review; require explicit user-benefit articulation.
- Variable-reward implementations: agents propose RNG without seeding, leading to non-reproducible bug reports; require deterministic seeding for testability.
- Survey selection bias: agent recommends decisions based on "engaged users said X" — that's the surviving cohort, not the truth.
- Privacy: behavioral models can produce PII-adjacent data (location pattern, sleep schedule); require explicit data-classification check.

## References
- "Hooked" by Nir Eyal (hook model basis)
- "Indistractable" by Nir Eyal (ethical engagement counterpoint)
- Reforge "Retention + Engagement" course
- Andrew Chen "The Cold Start Problem" (network effects + retention)
- Mixpanel cohort retention guide: https://mixpanel.com/blog/cohort-analysis/
- Amplitude retention playbook: https://amplitude.com/blog/retention-rate
- PostHog retention docs: https://posthog.com/docs/product-analytics/retention
- Casey Winters notes on retention loops
