# PLG Optimization Tactics

## Summary

**One-sentence:** ICE-scored PLG tactics catalog for activation, free-to-paid, expansion conversion — upgrade prompts at 80% of limit, never first session, named customer + quantified value in copy.

**One-paragraph:** Post-PMF PLG products plateau because teams lack a structured tactic backlog tied to measurable funnel steps. This methodology delivers an ICE-scored tactic index covering activation friction reduction, free-tier balance, self-serve checkout design, and expansion signal detection. Core rules: pair every tactic with the metric it moves and a current baseline; show upgrade prompts at 80% of limit (not 100%); cap prompts to one per session and zero during the first session; name a comparable customer and quantify value in all upgrade copy; reject "Upgrade Now" and "Premium Plan" as CTA text. Output: a ranked test backlog (report) with hypotheses, ICE scores, and instrumentation.

**Ефективно для:**

- Post-PMF PLG product з плато на activation / free-to-paid / expansion conversion.
- Дизайн free tier або self-serve checkout з нуля — pre-curated friction-point list.
- Generation in-product upgrade copy + feature-gate messaging + pricing-page variants.
- Quarterly A/B test backlog scored проти onboarding/upgrade/pricing test ideas.

## Applies If (ALL must hold)

- Running an existing PLG product where activation, free-to-paid, or expansion conversion has plateaued and you need a backlog of tested tactics rather than a strategy rewrite.
- Designing a free tier or self-serve checkout from scratch and want a pre-curated list of friction points to instrument before launch.
- Generating in-product upgrade copy, feature-gate messaging, and pricing-page variants that follow the methodology good vs bad patterns.
- Producing a quarterly A/B test backlog scored against the included onboarding/upgrade/pricing test idea bank.

## Skip If (ANY kills it)

- Pre-PMF teams without measurable activation data — generic tactics distract from PMF discovery.
- Pure sales-led ACVs above ~$50K where self-serve patterns do not survive procurement; route to sales-led playbooks instead.
- Single-event transactions (one-shot ecommerce, ticketing) where there is no expansion or seat-growth surface to optimize.
- Hard-regulated products (healthcare, banking) where "instant access, no approval" recommendations conflict with compliance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Funnel metrics (activation, free-to-paid, expansion) | dashboard / CSV | analytics tool (PostHog / Amplitude / Mixpanel) |
| Current free-tier limits + plan matrix | spec / JSON | billing system (Stripe Pricing Tables) |
| Existing upgrade copy + feature-gate strings | source / Markdown | product repo |
| Baseline cohort retention (Day-7 / Day-30 / Day-90) | CSV / dashboard | analytics tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[plg-basics]] | Activation / Aha-moment terminology |
| [[plg-metrics]] | PQL signals + cohort retention model |
| [[experiment-hypothesis-scoring]] | ICE scoring template for backlog ranking |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: baseline-required, prompt-at-80-percent, no-first-session-prompt, named-customer-copy, banned-cta-text, balanced-free-tier | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ranked tactic backlog + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: pull metrics → map weak step → ICE-score → write copy → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: free-to-paid plateau → ranked 5-tactic backlog | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree: funnel stage → tactic family → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-funnel-baseline` | haiku | Mechanical metric extraction from analytics. |
| `map-tactics-to-weak-step` | sonnet | Catalog lookup + bounded judgment. |
| `score-with-ice` | haiku | Numeric scoring against template. |
| `write-upgrade-copy-variants` | sonnet | Light judgment; must respect bad-CTA filter. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ice-scorer.py` | Dataclass for ICE-scoring tactic backlog; bucket() returns test_now / this_quarter / if_capacity / backlog |
| `templates/tactic-backlog.md` | Ranked report skeleton with one row per tactic + columns for hypothesis, ICE, instrumentation |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-plg-optimization-tactics.py` | Validate ranked-backlog JSON against the schema in `content/02-output-contract.xml` | After subagent returns; pre-commit |

## Related

- [[plg-basics]]
- [[plg-metrics]]
- [[plg-implementation-guide]]
- [[experiment-hypothesis-scoring]]
- [[onboarding-flows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps the observable funnel-drop step (activation / free-to-paid / expansion) to the tactic family the agent must sample from, each leaf pinning a rule from `01-core-rules.xml`. Use it before ranking — choosing the wrong family wastes ICE-scoring effort.
