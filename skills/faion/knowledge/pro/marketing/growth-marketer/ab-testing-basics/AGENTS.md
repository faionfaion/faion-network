# A/B Testing Basics

## Summary

A/B testing (split testing) is a controlled experiment that compares two versions of a change by splitting traffic 50/50, measuring which variant performs better on a pre-registered primary metric, and deciding based on statistical significance. The lifecycle is: hypothesis (if/then/because) → sample-size calculation → run to full size → analyze (p-value, SRM check, guardrails) → ship or kill.

## Why

Opinion-driven product decisions fail because individual intuition has no error rate. A/B tests produce a causal estimate of a change's effect with a known false-positive rate (alpha). Without a pre-committed end date and a sample-ratio mismatch check, peeking inflates false positives 5–10x and SRM silently invalidates results.

## When To Use

- Reversible UI/copy/flow changes where the change affects a metric trackable in real time.
- At least 1k weekly events on the primary metric surface.
- One change per experiment — multiple simultaneous changes prevent causal isolation.
- Team has committed to a single primary metric and 3+ guardrail metrics before launch.
- A/B platform available with deterministic-hash bucketing (user_id + experiment_id).

## When NOT To Use

- Strategic choices (pricing model, brand positioning) — blast radius too large, too few decisions.
- Network-effect surfaces (Slack workspaces, marketplaces) — treatment leaks into control; use cluster/switchback designs.
- Traffic below 100 users/day on the test surface — test duration exceeds product-iteration cadence.
- Full redesigns — too many confounders; use phased feature-flag rollout instead.
- Highly personalized products where every user already sees a different variant.

## Content

| File | What's inside |
|------|---------------|
| `content/01-lifecycle.xml` | Hypothesis format, lifecycle steps, decision rules, statistical interpretation table |
| `content/02-checklist.xml` | Pre-launch checklist rules: SRM, guardrails, sample gate, no-peeking |
| `content/03-examples.xml` | Worked examples: button copy win, pricing badge marginal win, failed testimonial test |

## Templates

| File | Purpose |
|------|---------|
| `templates/pretest-check.py` | Python gate function — blocks underpowered or misconfigured tests before launch |
| `templates/prompt-test-card.txt` | LLM prompt to draft a hypothesis card with all required fields |

## Scripts

none
