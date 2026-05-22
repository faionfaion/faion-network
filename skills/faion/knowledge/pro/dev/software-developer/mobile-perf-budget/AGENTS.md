---
slug: mobile-perf-budget
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Mobile-specific performance budget for iOS / Android — cold-start time, frame-drop ceiling, binary-size cap — with CI enforcement, distinct from web perf.
content_id: "2082e4bfe64332b3"
tags: [mobile,perf,cold-start,frame-drop,binary-size,ios,android,budget]
---
# Mobile Perf Budget

## Summary

**One-sentence:** Mobile-specific performance budget for iOS / Android — cold-start time, frame-drop ceiling, binary-size cap — with CI enforcement, distinct from web perf.

**One-paragraph:** Generic `perf-test-basics` covers web's Core Web Vitals (LCP, INP, CLS), but mobile has different fault lines: cold-start time (P1 launch-to-interactive), frame-drop rate (jank in scroll / animation), and binary size (download + storage cost). This methodology defines numeric budgets per platform, the measurement protocol (real devices in lab + RUM in production), the CI gate that blocks merges exceeding budget, and a regression-attribution workflow. Mechanism: 3 budget axes × 2 platforms, real-device profiling tools (Instruments, Profile GPU Rendering, Bitrise / Firebase Test Lab), CI integration via PR checks, and a runbook for when budgets blow. Primary output: a checked-in `perf-budget.yaml` with current numbers + last regression date.

## Applies If (ALL must hold)

- product has iOS OR Android client (native or React Native / Flutter)
- app has &gt; 5,000 monthly active users (RUM signal threshold)
- team owns the mobile build pipeline OR can wire CI checks
- support for in-app performance instrumentation (Firebase Performance, Datadog RUM, Sentry Mobile)
- ≥ 1 release per month (budget meaningful only with regular cadence)

## Skip If (ANY kills it)

- pure web app (no mobile binary) — use web-perf-budget methodology
- prototype / sandbox app pre-launch — perf is later
- enterprise B2B app with controlled-device deployment — budgets less critical
- single-platform app with platform-default budgets fully sufficient
- regulated app where instrumentation requires legal sign-off — separate workflow

## Prerequisites (must be true before starting)

- baseline measurements on representative devices (low-end + mid-tier per platform)
- access to RUM data for production performance distribution
- CI pipeline that can fail builds based on perf gate
- agreed-upon budget per axis (default values exist; team may adjust)
- on-call team understands the perf rollback procedure

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/perf-test-basics` | Web-perf companion methodology |
| `pro/dev/software-developer/api-monitoring-metrics` | Backend perf budget for mobile API |
| `pro/dev/software-developer/release-management` | Receives budget gate as a release blocker |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 3 budget axes, real-device + RUM, CI gate, regression attribution, low-end device floor | ~1000 |
| `content/02-output-contract.xml` | essential | perf-budget.yaml schema, CI integration, RUM report format | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (synthetic-only, ignored low-end, gate bypassed, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `baseline_collector_outline` | haiku | List devices + test scenarios for baseline |
| `budget_threshold_synth` | sonnet | Recommend budgets per axis given baseline + product |
| `regression_attributor` | sonnet | Correlate perf regression with PRs in the window |
| `release_blocker_message_draft` | sonnet | Compose CI failure message with context |

## Templates

| File | Purpose |
|------|---------|
| `templates/perf-budget.yaml` | Per-platform budget configuration |
| `templates/baseline-device-matrix.md` | Recommended device list for lab + RUM |
| `templates/ci-perf-gate.yaml` | CI check definition (GitHub Actions / Bitrise) |
| `templates/regression-runbook.md` | Steps when budget blows |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/measure-cold-start.sh` | Cold-start measurement on iOS / Android | Each release branch |
| `scripts/frame-drop-analyzer.py` | Parse profiling traces for frame drops | Each release branch |
| `scripts/binary-size-diff.sh` | Diff binary size across PRs | Each PR |
| `scripts/perf-gate.py` | CI script that fails if any budget exceeded | PR check |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodology: `perf-test-basics`, `release-management`
- external: [Apple Instruments docs](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance) · [Android Profile GPU Rendering](https://developer.android.com/topic/performance/rendering/profile-gpu) · [Firebase Performance](https://firebase.google.com/docs/perf-mon)
