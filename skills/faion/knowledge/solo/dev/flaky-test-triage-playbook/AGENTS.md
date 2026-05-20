---
slug: flaky-test-triage-playbook
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "fd222b314976290c"
summary: "Process playbook for flaky tests: detect via mechanical signal, quarantine within budget, bucket by responsible owner and severity, fix by class, close the loop with a 'held N runs' confirmation — the lifecycle existing testing-patterns refer to but do not specify."
tags: [dev, solo, qa, flaky-tests, triage, lifecycle, pipeline]
---
# Flaky Test Triage Playbook

## Summary

Existing testing-patterns content mentions flakes but never gives a triage process — only a vague directive to "fix flaky tests". This playbook supplies the missing lifecycle: a five-stage pipeline (detect → quarantine → bucket → fix → close) where each stage has an entry condition, an artefact, and an exit gate. Detection is mechanical, quarantine respects a hard budget, bucketing assigns the right owner before any fix is attempted, fixing follows class-specific patterns, and closing requires N consecutive green runs before the flake leaves the ledger. The playbook is complementary to the test-pyramid rebalance work because misclassified flakes often hint that an E2E test should have been a contract or unit test.

## Applies If

- The team is running a regression suite or E2E suite with at least 100 tests and weekly CI runs.
- A flake-detection signal exists or can be added (CI re-run rate, retry counters, or a daily aggregator).
- The team owns a single flake ledger (file, board, or sheet) that everyone agrees to update.
- A test pyramid rebalance is plausible (some flakes may be hints to move tests down the pyramid).

## Skip If

- Single dev hobby suite where lifecycle overhead is more expensive than ad-hoc fixes.
- The team already has a working triage SOP that maps to the same five stages — keep yours; do not stack.
- The suite is being decommissioned; do not invest in lifecycle process for tests due to disappear.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules defining each lifecycle stage (detect, quarantine, bucket, fix, close-loop) with explicit entry/exit gates |

## Related

- parent skill: `solo/dev/`
- triggering activity: `Regression suite hardening: flaky test elimination`, `Test pyramid rebalance: too-many-e2e to contract + unit`
- neighbouring: `solo/dev/flaky-test-elimination`, `solo/dev/qa-flake-ledger-template`, `pro/dev/test-pyramid-rebalance-playbook`
