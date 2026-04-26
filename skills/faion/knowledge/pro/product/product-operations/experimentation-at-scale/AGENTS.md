# Experimentation at Scale

## Summary

Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined
hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction
step. Maturity runs from Level 1 (ad-hoc, no standards) to Level 4 (every decision backed by
an experiment). The full agentic loop covers: hypothesis authoring → sample-size math → flag
deployment → hourly SRM watch → daily metric watch → readout → cross-cutting learnings memo.

## Why

Ad-hoc A/B testing does not build organizational learning. Without statistical rigor (pre-registered
primary metrics, guardrails, SRM checks, multiple-comparison correction) teams ship false winners
at high rates: peeking inflates false-positive rate from 5% to 30%+; SRM breaks ~6% of experiments
silently. Scale benchmarks: Microsoft 100k/yr, enterprise avg 500-1k/yr. Agents can operate the
mechanical layers (collection, flag ops, SRM watch) cheaply, freeing humans for decision sign-off.

## When To Use

- Product orgs running 50+ live A/B tests per quarter where coordination has outgrown spreadsheets
- Maturity-level transitions: when formalizing hypothesis intake, sample-size math, and guardrails
- Feature-flag rollouts tied to experiment readouts requiring automated SRM checks
- Warehouse-native shops (Snowflake/BigQuery) driving Eppo/Statsig from dbt models
- Solopreneur / small team needing an agent to generate hypotheses, monitor results, and emit readouts
- Post-launch "what did we learn?" synthesis across an experiment registry

## When NOT To Use

- Pre-PMF with <1k weekly active users — sample-size math demands months per test; use qualitative
  discovery instead
- Single-shot launches where a holdout is impossible or unethical
- High-stakes irreversible decisions (pricing rebrand, contract terms, safety-critical UX) — use
  multi-method evidence, not a single A/B
- Enterprise B2B with <50 accounts — sample size makes A/B impractical; use cohort analysis
- Teams without a metrics governance owner (single source of truth for metric definitions)
- Compliance-bound surfaces (HIPAA, payment flows, KYC) where variants must clear legal before ship

## Content

| File | What's inside |
|------|---------------|
| `content/01-platform.xml` | Maturity levels, modern stack (flags/A-B/analytics/warehouse), best practices |
| `content/02-agent-usage.xml` | Full agentic loop, subagent table, prompt pattern, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-doc.yaml` | Per-experiment spec: hypothesis, primary metric, guardrails, MDE, traffic split |
| `templates/sample_size.py` | Two-proportion z-test sample size + runtime calculator |
| `templates/srm_check.py` | Chi-square SRM check (pass if p > 0.001) |
