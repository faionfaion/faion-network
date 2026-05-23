---
slug: behavior-parity-verification
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a per-stage parity report comparing legacy vs new code-path outputs over shadow traffic, gating ramp progression on diff rate and cluster review.
content_id: "581d8e59ff07ba59"
complexity: medium
produces: report
est_tokens: 4200
tags: [migration, parity, shadow-traffic, dark-launch, refactor]
---
# Behavior Parity Verification (Solo Tier)

## Summary

**One-sentence:** Validates that a rewritten code path produces the same observable behavior as the legacy path by shadowing real traffic and diffing outputs, with a lightweight setup a solo developer can stand up in a day.

**One-paragraph:** Major rewrites or framework migrations face a single hard question: did we break anything? Golden-master testing answers it via captured fixtures, but a solo developer often cannot afford the harness. Behavior parity verification offers the lighter alternative: route a small percentage of production traffic to both the old and new implementation, compare results in real time, and surface diffs. The methodology pins three things — what counts as observable, how to compare without leaking PII, and how to ramp safely from 1% to 100%. Output: a parity report per ramp stage that closes only when diff rate drops below a defined threshold for a defined window.

**Ефективно для:**

- Соло-розробник переписує сервіс на новий фреймворк/мові і боїться upgrade-regressions.
- Команда хоче безпечно вирізати legacy-шар без повного golden-master harness.
- AI-агент згенерував новий код-шлях і потрібен empirical gate перед видаленням старого.
- Міграція з monolith → service-extract, де хочеться dark-launch перед cutover.

## Applies If (ALL must hold)

- An existing code path is being replaced (new language, new framework, new algorithm) — not greenfield.
- The path is observable: defined input contract and a comparable output (HTTP response, file write, DB row, returned object).
- Production traffic is non-zero and reproducible (deterministic given inputs OR diffs can be tolerated probabilistically).
- The developer can deploy the new path behind a feature flag or routing layer.

## Skip If (ANY kills it)

- Pure UI changes — visual diffs need screenshot diffing, not behavioral parity.
- The legacy path is being removed in the same release — no shadow possible.
- Outputs include side-effects with no replay (sends real emails, charges real cards) — must be sandboxed first.
- Single-user dev tools without production traffic — replay captured logs instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Legacy implementation handle | code path / endpoint | repo |
| New implementation handle | code path / endpoint | repo |
| Feature flag / router | code | flag service or proxy layer |
| Diff store schema | SQL / KV definition | DBA / infra |
| Observable field list | Markdown | author of the rewrite |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-feature-flags` | Routing traffic between implementations is flag-gated. |
| `solo/dev/changelog-automation-conventional-commits` | Each ramp-stage promotion is a release event; the changelog records it. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: observable list, normalize-before-diff, staged ramp gates, freeze-on-regression | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for parity-report artefact + valid/invalid examples + forbidden patterns | 700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: PII leak, timestamp false-positives, ramp-jump, async observables missed, permissive normalizer, skipped cluster analysis | 800 |
| `content/04-procedure.xml` | medium | 6-step procedure: define observables → write normalizer → deploy diff sampler → ramp 1%→100% with gates → cluster analysis → sign-off | 700 |
| `content/05-examples.xml` | reference | One worked example: pricing endpoint migration from legacy Python service to new Go service | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree: traffic-non-zero? observables-defined? normalizer-deterministic? gate-met? → ramp/freeze/revert | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-observable-fields` | sonnet | Bounded judgment on which response fields are observable vs incidental. |
| `write-diff-normalizer` | sonnet | Coding task: deterministic transforms (timestamp quantization, UUID canonicalization, list ordering). |
| `analyze-diff-clusters` | opus | Synthesis: cluster surviving diffs into root causes; cross-input pattern matching. |
| `score-parity-report` | haiku | Mechanical schema validation; pass/block computation against thresholds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/parity-report.md` | Markdown skeleton for the per-stage parity report (scope, observables, ramp window, diff metrics, sign-off). |
| `templates/parity-report.json` | JSON Schema for the parity-report artefact (canonical contract). |
| `templates/diff-store-schema.sql` | Postgres DDL for the `parity_diffs` table the sampler writes to. |
| `templates/normalizer-skeleton.py` | Python skeleton of a deterministic diff normalizer (timestamp/UUID/list rules). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-behavior-parity-verification.py` | Validate a parity-report JSON against the schema and threshold rules. | After each ramp stage closes; before promoting to next stage. |

## Related

- [[trunk-based-feature-flags]] — flag plumbing that gates the shadow router.
- [[ci-quality-gate-design]] — same artefact-gate pattern at the CI layer.
- [[characterization-test-recipes]] — orthogonal: pre-rewrite test capture.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks whether production traffic is non-zero and whether the observable list has been written — these are hard prerequisites. It then branches on diff-rate vs threshold at each ramp stage, routing to one of `promote-next-stage`, `freeze-investigate`, or `revert-previous-stage`. Each leaf references a rule id in `01-core-rules.xml`. Use it before every ramp-promotion decision.
