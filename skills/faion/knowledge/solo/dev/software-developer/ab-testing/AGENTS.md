---
slug: ab-testing
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Implements a deterministic A/B testing runtime — sticky bucketing via hash(user_id|experiment_id), exposure+conversion events, z-test for proportions with Wilson CI, and SRM detection.
content_id: "e0e292beaa1a3139"
complexity: deep
produces: code
est_tokens: 4400
tags: [a-b-testing, experimentation, statistics, feature-flags, srm]
---
# A/B Testing Implementation

## Summary

**One-sentence:** Implements a deterministic A/B testing runtime — sticky bucketing via hash(user_id|experiment_id), exposure+conversion events, z-test for proportions with Wilson CI, and SRM detection.

**One-paragraph:** A/B testing runtime that survives device, session, and process changes. Core rule: assignment uses a 64-bit hash of (user_id || experiment_id) mod 100, never random.choice — this keeps the same user in the same arm across web, iOS, app, and email surfaces. The runtime emits typed exposure + conversion events to a stats engine and a periodic SRM (Sample Ratio Mismatch) check that fails the experiment if traffic split drifts more than the configured chi-square p-value.

**Ефективно для:**

- Solo dev wiring a feature flag into a real experiment instead of a kill switch.
- Multi-platform consistency — same user must get the same variant on web + iOS + email.
- Pricing or onboarding flow tests where mis-bucketing breaks trust + skews data.
- Adding statistical rigor (Wilson CI, z-test, SRM) instead of eyeballing event counts.

## Applies If (ALL must hold)

- Experiment design is complete (hypothesis + primary metric + MDE + sample size).
- Traffic is high enough to reach statistical power (>=1k weekly users on the surface).
- A stats engine (Snowflake / ClickHouse / BigQuery) is wired to receive events.
- Variants are independent (no network effects between users).

## Skip If (ANY kills it)

- Traffic too low for power — use qualitative methods.
- Change affects every user irreversibly (DB migrations, schema rewrites).
- Marketplace / pricing with strong network effects — use switchback or geo split.
- Compliance-bound flow (KYC / payments) where variant differences create audit problems.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment design | hypothesis + primary metric + MDE + sample size | PM / analyst |
| Feature flag | flag key + targeting rule | LaunchDarkly / Unleash / homegrown |
| Stats engine connection | event stream sink | data team |
| Salt / hash seed | per-experiment string | architect (do not reuse across experiments) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flag-cleanup-discipline]] | Flag cleanup gate after experiment ends. |
| [[deterministic-test-data-pattern]] | Same hashing discipline for offline test data. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (deterministic hash, sticky across surfaces, SRM gate, exposure-before-conversion, Wilson CI) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for experiment-run artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: random.choice, no-SRM, peeking, post-assignment-changes | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (wire bucket → emit exposure → emit conversion → analyse → ship/kill) | 700 |
| `content/05-examples.xml` | essential | Worked example: pricing-page A/B run with SRM-clean output | 600 |
| `content/06-decision-tree.xml` | essential | Routes by power + SRM + significance | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ab_testing_implement_bucket` | sonnet | Hash impl + collision checks. |
| `ab_testing_analyse` | sonnet | Stats engine query + Wilson CI computation. |
| `ab_testing_srm_check` | haiku | Mechanical chi-square check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the experiment-run artefact |
| `templates/sample-size.py` | Sample-size calculator (proportions test, two-sided) |
| `templates/analyzer.py` | Variant analyser with z-test + Wilson CI + SRM check |
| `templates/_smoke-test.json` | Minimum viable filled-in experiment-run for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing.py` | Validate experiment-run artefact against schema + SRM gate + power gate | Pre-commit; CI on each experiment close |

## Related

- [[feature-flag-cleanup-discipline]]
- [[deterministic-test-data-pattern]]
- [[caching-strategy]]
- [[api-rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) power — under-powered experiments never decide, (b) SRM — failing SRM invalidates the result regardless of significance, and (c) significance — only Wilson-CI-clean wins ship. Every leaf references a rule in `01-core-rules.xml`.
