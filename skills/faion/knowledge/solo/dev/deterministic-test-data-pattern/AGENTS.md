---
slug: deterministic-test-data-pattern
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pattern for generating test data that is reproducible across runs, machines, and CI shards; produces a fixtures module with seeded factories, time-frozen clocks, and stable id generators replacing ad-hoc faker calls."
content_id: "92eecb97d9f865f6"
complexity: medium
produces: code
est_tokens: 4900
tags: ["dev", "solo", "testing", "fixtures", "determinism"]
---
# Deterministic Test Data Pattern

## Summary

**One-sentence:** Pattern for generating test data that is reproducible across runs, machines, and CI shards; produces a fixtures module with seeded factories, time-frozen clocks, and stable id generators replacing ad-hoc faker calls.

**One-paragraph:** Pattern for generating test data that is reproducible across runs, machines, and CI shards; produces a fixtures module with seeded factories, time-frozen clocks, and stable id generators replacing ad-hoc faker calls. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Snapshot diffs that change every run because of timestamps or uuids.
- CI shards where order-of-execution affects test outcome.
- Cross-OS test runs where locale or timezone shifts dates.
- Solo devs who cannot afford an afternoon chasing a flake.

## Applies If (ALL must hold)

- Test suite has ≥1 flaky test traceable to non-deterministic inputs (random seeds, wall-clock time, uuid4 in assertions).
- Tests run in CI on multiple shards or against multiple OS / Node / Python versions.
- The codebase uses a faker / factory_boy / fishery / similar library.
- Snapshot tests exist or are about to be added.

## Skip If (ANY kills it)

- All test data is hand-written constants — pattern adds no value.
- Only e2e tests against live services — determinism is achieved upstream, not in fixtures.
- Tests intentionally exercise randomness (fuzzers, property tests) — those use different discipline.

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
| [[flaky-test-triage-playbook]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-deterministic-test-data-pattern-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-deterministic-test-data-pattern.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deterministic-test-data-pattern.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[flaky-test-elimination]]
- [[flaky-test-triage-playbook]]
- [[characterization-test-recipes]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
