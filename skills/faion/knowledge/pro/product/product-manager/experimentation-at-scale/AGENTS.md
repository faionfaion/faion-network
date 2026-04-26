# Experimentation at Scale

## Summary

A maturity model and platform design for running 100+ experiments per year with statistical rigor. Covers four maturity levels (ad-hoc → structured → scaled → culture), the modern 2026 experiment stack (feature flags, A/B tooling, analytics warehouse), and PM-specific practices: pre-registered hypotheses (if-then-because), behavioral predictions, guardrail metrics, and decision rules that prevent HiPPO override.

## Why

Ad-hoc A/B testing does not build organizational learning — results are siloed, hypotheses are solution-shaped, and decisions are overridden by opinion. A scaled experimentation platform converts every product bet into a falsifiable, time-bounded test with a pre-committed verdict rule. Microsoft runs ~100k experiments/year; the competitive gap between ad-hoc and scaled orgs compounds with each roadmap cycle.

## When To Use

- A roadmap bet is reversible, has a clear behavioral prediction, and can be measured within 4 weeks at current traffic.
- Quarterly planning when roadmap candidates outnumber conviction — turn opinions into a ranked experiment slate.
- After discovery rounds where 2-4 candidate solutions exist for one opportunity — experiment to pick, not to launch.
- Stakeholder disputes (design vs. eng vs. growth) where pre-registering a metric and accepting the verdict is faster than politics.
- Planning org experimentation infrastructure: choosing tooling (GrowthBook vs. Statsig vs. Eppo), governance, and statistical standards.

## When NOT To Use

- Strategic, irreversible bets (rebrand, repositioning, contract terms) — A/B under-powers on what matters and over-emphasizes short-term proxies.
- Pre-PMF (&lt;1k WAU): users need problem interviews, not CTA optimization; a null result means "no signal," not "no effect."
- Innovation-tier features where users need &gt;30 days to adopt the new behavior — novelty effects dominate.
- B2B with &lt;50 accounts or one-off launches (regulatory, marketing event) — use cohort or case-study analysis.
- Surfaces under compliance review (HIPAA, PCI) — gating loop is slower than the experiment cadence.

## Content

| File | What's inside |
|------|---------------|
| `content/01-maturity-and-stack.xml` | Four maturity levels, 2026 tool stack, AI-augmented experimentation, scale benchmarks. |
| `content/02-pm-practices.xml` | Hypothesis framing, pre-registration, decision rules, anti-patterns (HiPPO, local maxima). |

## Templates

| File | Purpose |
|------|---------|
| `templates/hypothesis-doc.yaml` | Full hypothesis intake schema: if-then-because, primary metric, guardrails, decision rule, stop conditions. |
| `templates/triage-idea.py` | 30-line Python: scores idea testability (reversible + behavioral + traffic) and routes to tier. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/triage-idea.py` | Scores idea testability and emits tier (A/B, prototype, qual, irreversible-strategic). |
