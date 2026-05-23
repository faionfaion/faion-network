---
slug: flaky-test-triage-playbook
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Triage step that runs BEFORE flake-elimination: detect, score, route, and decide which flakes to fix vs quarantine vs delete; produces a triage report ranking flakes by cost-of-flake and routing each to the right next step."
content_id: "4c40a18787f15e4d"
complexity: medium
produces: report
est_tokens: 4900
tags: ["dev", "solo", "testing", "triage", "flake"]
---
# Flaky Test Triage Playbook

## Summary

**One-sentence:** Triage step that runs BEFORE flake-elimination: detect, score, route, and decide which flakes to fix vs quarantine vs delete; produces a triage report ranking flakes by cost-of-flake and routing each to the right next step.

**One-paragraph:** Triage step that runs BEFORE flake-elimination: detect, score, route, and decide which flakes to fix vs quarantine vs delete; produces a triage report ranking flakes by cost-of-flake and routing each to the right next step. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Multi-tenant codebases inheriting flaky tests from acquisitions or rewrites.
- Pre-release stabilisation when the flake tail blocks releases.
- Solo founders who must triage before they fix because they cannot fix all.
- Audit prep where 'we have no flakes' must be measured, not asserted.

## Applies If (ALL must hold)

- Suite has ≥3 known-flaky tests (mute markers, retry decorators, or ≥1 flake/week).
- CI history is queryable (job logs, retry counts) for the past 30 days.
- Operator can mute / quarantine tests without blocking releases.
- A weekly triage cadence is committed.

## Skip If (ANY kills it)

- Only one flaky test exists — skip to elimination directly.
- No CI history available — install measurement first.
- Suite is being rewritten — triaging the old suite wastes effort.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[flaky-test-elimination]] | upstream context this methodology builds on |
| [[qa-flaky-test-root-cause-taxonomy]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-flaky-test-triage-playbook-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-flaky-test-triage-playbook.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-flaky-test-triage-playbook.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[flaky-test-elimination]]
- [[qa-flaky-test-root-cause-taxonomy]]
- [[qa-flake-ledger-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
