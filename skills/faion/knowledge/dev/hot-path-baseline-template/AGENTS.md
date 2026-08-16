# Hot Path Baseline Template

## Summary

**One-sentence:** Before-you-optimize baseline spec: the N numbers to capture for any hot path (p50/p95/p99 latency, throughput, allocation rate, cache hit, dep call count) prior to refactor.

**One-paragraph:** Before-you-optimize baseline spec: the N numbers to capture for any hot path (p50/p95/p99 latency, throughput, allocation rate, cache hit, dep call count) prior to refactor. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-hot-path-baseline-template.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Hot Path Baseline Template — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `hot-path-baseline-template` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Hot path is about to be refactored or replaced.
- Optimisation work needs an objective before/after delta.
- Production traffic representative of the hot path is reachable for measurement.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Path is cold (< 1 call/min) — baseline noise dwarfs any signal.
- Refactor is motivated by correctness, not perf — baseline-then-compare is the wrong gate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[library-evaluation-rubric]] | Workflow context: related methodology in the same family |

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
| `fill-hot-path-baseline-template-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-hot-path-baseline-template.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hot-path-baseline-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[library-evaluation-rubric]]
- [[migration-impact-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (traffic level, perf goal, measurement readiness) to capture-baseline / skip-cold-path / defer. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "hot-path-baseline-template-2026-05-23",
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "status": "ready_for_review",
  "evidence": [
    {
      "source": "https://example.com/source-1",
      "citation": "verbatim quote from source"
    }
  ],
  "title": "draft",
  "scope": [
    "draft-item"
  ],
  "decisions": {
    "key": "value"
  }
}
```
