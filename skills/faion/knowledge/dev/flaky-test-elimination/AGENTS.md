# Flaky Test Elimination

## Summary

**One-sentence:** End-to-end recipe to eliminate a flaky test: classify, isolate, fix, verify by repeated runs; produces a report pinning root cause to one of seven canonical buckets and recording the verification N-run pass count.

**One-paragraph:** End-to-end recipe to eliminate a flaky test: classify, isolate, fix, verify by repeated runs; produces a report pinning root cause to one of seven canonical buckets and recording the verification N-run pass count. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Specific Cypress / Playwright tests that flake on a CI shard.
- Backend integration tests that fail on month boundaries.
- Snapshot tests that drift after locale or fixture changes.
- Solo founders who cannot afford to keep re-running CI.

## Applies If (ALL must hold)

- A specific test (or small set) flakes ≥1x/week in CI.
- The test can be re-run locally with the same inputs.
- Operator has authority to modify test code, production code, or test infra.
- Suite history (CI logs / re-run records) is queryable for the past month.

## Skip If (ANY kills it)

- Flake rate is unmeasured ('feels flaky') — start with the triage playbook first.
- The whole suite is flaky — start with the suite-health canon first.
- Test is for a deprecated feature about to be removed — kill the test instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[flaky-test-triage-playbook]] | upstream context this methodology builds on |
| [[deterministic-test-data-pattern]] | sibling discipline cited in decision tree |

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
| `fill-flaky-test-elimination-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-flaky-test-elimination.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-flaky-test-elimination.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[flaky-test-triage-playbook]]
- [[deterministic-test-data-pattern]]
- [[qa-flaky-test-root-cause-taxonomy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "flaky-test-elimination-2026-05-23",
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "status": "ready_for_review",
  "test_id": "draft",
  "classification": "draft",
  "root_cause": "draft",
  "fix_summary": "draft",
  "verification_runs": 50,
  "verification_pass_count": 50,
  "regression_test": "draft"
}
```
