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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[feature-flag-cleanup-discipline]] | Flag cleanup gate after experiment ends. |
| [[deterministic-test-data-pattern]] | Same hashing discipline for offline test data. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules — runtime: deterministic hash, sticky across surfaces, SRM gate, exposure-before-conversion, Wilson CI; design + decision: pre-registered design, locked sample size, full business cycle, guardrails gate the ship, pre-specified segments, practical-significance floor, named human signs off | 2000 |
| `content/02-output-contract.xml` | essential | JSON Schema for experiment-run artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: random.choice, no-SRM, peeking, post-assignment changes, multi-variable variant, ignored guardrail | 950 |
| `content/04-procedure.xml` | essential | 6-step procedure (pre-register design → wire bucket → emit exposure → emit conversion → analyse → decide + sign off) | 950 |
| `content/05-examples.xml` | essential | Worked example: pricing-page A/B run with SRM-clean output | 600 |
| `content/06-decision-tree.xml` | essential | Routes by cycle length, power, SRM, significance, guardrails, practical floor | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ab_testing_implement_bucket` | sonnet | Hash impl + collision checks. |
| `ab_testing_analyse` | sonnet | Stats engine query + Wilson CI computation. |
| `ab_testing_srm_check` | haiku | Mechanical chi-square check. |
| `ab_testing_preregister` | sonnet | Draft the plan: metric choice, guardrail selection, sample-size computation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the experiment-run artefact |
| `templates/sample-size.py` | Sample-size calculator (proportions test, two-sided) |
| `templates/analyzer.py` | Variant analyser with z-test + Wilson CI + SRM check |
| `templates/_smoke-test.json` | Minimum viable filled-in experiment-run for validator round-trip |
| `templates/test-plan.md.j2` | Pre-registration plan frozen before launch: hypothesis, split, metrics, guardrails, sample size, timeline, risks |
| `templates/test-plan.md` | Pre-registration plan frozen before launch: hypothesis, split, metrics, guardrails, sample size, timeline, risks Generated from `templates/test-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/results-report.md.j2` | Human-readable results report: per-metric table, guardrail verdict, statistical detail, pre-specified segments, sign-off |
| `templates/results-report.md` | Human-readable results report: per-metric table, guardrail verdict, statistical detail, pre-specified segments, sign-off Generated from `templates/results-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing.py` | Validate experiment-run artefact against schema + SRM gate + power gate | Pre-commit; CI on each experiment close |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[feature-flag-cleanup-discipline]]
- [[deterministic-test-data-pattern]]
- [[caching-strategy]]
- [[api-rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) power — under-powered experiments never decide, (b) SRM — failing SRM invalidates the result regardless of significance, and (c) significance — only Wilson-CI-clean wins ship. Every leaf references a rule in `01-core-rules.xml`.
