---
slug: behavior-parity-verification
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "581d8e59ff07ba59"
summary: Shadow-run new code paths against the legacy system in production traffic and diff observable behavior — without a full golden-master setup or test harness rewrite.
tags: [migration, parity, shadow-traffic, dark-launch, refactor]
---
# Behavior Parity Verification (Solo Tier)

## Summary

**One-sentence:** Validates that a rewritten code path produces the same observable behavior as the legacy path by shadowing real traffic and diffing outputs, with a lightweight setup a solo developer can stand up in a day.

**One-paragraph:** Major rewrites or framework migrations face a single hard question: did we break anything? Golden-master testing (see `geek/sdlc-ai/test-golden-master-legacy-rewrite`) answers it via captured fixtures, but a solo developer often cannot afford the harness. Behavior parity verification offers the lighter alternative: route a small percentage of production traffic to both the old and new implementation, compare results in real time, and surface diffs. The methodology pins three things — what counts as "observable," how to compare without leaking PII, and how to ramp safely from 1% to 100%. Output: a parity report per release that closes only when diff rate drops below a defined threshold for a defined window.

## Applies If (ALL must hold)

- An existing code path is being replaced (new language, new framework, new algorithm) — not greenfield.
- The path is observable: it has a defined input contract and a comparable output (HTTP response, file write, database row, returned object).
- Production traffic is non-zero and reproducible (deterministic given inputs OR diffs can be tolerated probabilistically).
- The developer can deploy the new path behind a feature flag or routing layer.

## Skip If (ANY kills it)

- Pure UI changes — visual diffs need screenshot diffing, not behavioral parity.
- The legacy path is being removed in the same release — no shadow possible.
- Outputs include side-effects with no replay (sends real emails, charges real cards) — must be sandboxed first.
- Single-user dev tools without production traffic — replay captured logs instead.

## Prerequisites

- Both implementations runnable side-by-side (feature flag, dual deployment, or shadow worker).
- A diff comparator: structural-equal for JSON, tolerance-aware for floats, normalization rules for IDs/timestamps.
- Storage for at least 24h of diff samples (Postgres table, S3 bucket, or log aggregator).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/feature-flags` | Routing traffic between implementations is flag-gated; this methodology assumes the flag plumbing is in place. |
| `solo/dev/code-quality/observability-basics` | The diff sampler is an observability sink; the basics of structured logs / metrics are assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: define observable, normalize before diff, ramp gates, freeze on regression | ~800 |
| `content/02-output-contract.xml` | essential | Parity report shape; required fields; required diff sample storage | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: PII leak, timestamp false-positives, ramping too fast, missed async paths, others | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-observable-fields` | sonnet | Bounded judgment on which fields are observable vs incidental |
| `write-diff-normalizer` | sonnet | Coding task: deterministic transforms (timestamps, UUIDs, ordering) |
| `analyze-diff-clusters` | opus | Synthesis: cluster surviving diffs into root causes |

## Templates

| File | Purpose |
|------|---------|
| `templates/parity-report.md` | Report skeleton: scope, ramp schedule, diff metrics, sign-off |
| `templates/diff-store-schema.sql` | Postgres schema for `parity_diffs` table |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/parity-summarize.py` | Aggregate `parity_diffs` into per-cluster counts and surface top-10 | Daily during ramp |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodology: `feature-flags`, `dark-launch`, `golden-master-testing` (geek tier)
- external: [GitHub Scientist](https://github.com/github/scientist) · [Twitter Diffy](https://github.com/opendiffy/diffy)
