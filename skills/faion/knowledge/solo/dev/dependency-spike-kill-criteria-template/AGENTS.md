---
slug: dependency-spike-kill-criteria-template
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pre-commits the disqualifiers that will end a dependency spike before time is sunk; produces a spec with named criteria, measurable thresholds, and a kill-or-continue verdict captured at spike end."
content_id: "d0d48dc05f347b88"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["dev", "solo", "spikes", "kill-criteria", "dependency-evaluation"]
---
# Dependency Spike Kill-Criteria Template

## Summary

**One-sentence:** Pre-commits the disqualifiers that will end a dependency spike before time is sunk; produces a spec with named criteria, measurable thresholds, and a kill-or-continue verdict captured at spike end.

**One-paragraph:** Pre-commits the disqualifiers that will end a dependency spike before time is sunk; produces a spec with named criteria, measurable thresholds, and a kill-or-continue verdict captured at spike end. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Replacing a build-it-yourself component with an off-the-shelf library.
- Adopting an emerging framework where community signals are still mixed.
- Vendor-bundle decisions (auth provider, payments, queue) where lock-in is high.
- Pre-empting yak-shave spirals where 'just one more day' eats a week.

## Applies If (ALL must hold)

- A new third-party dependency is being evaluated for adoption (not an upgrade of an existing one).
- Spike has a planned time-box (≤2 days) the operator commits to before starting.
- The dependency would touch at least one critical path (auth, payments, data integrity, runtime perf).
- A named operator can run and judge the spike.

## Skip If (ANY kills it)

- Dependency is trivial (logging helper, type shim) — kill criteria add more weight than they save.
- Decision is already made for non-technical reasons (vendor mandate, customer requirement) — spike is theatre.
- No time-box committed — without a box the spike runs forever regardless of criteria.

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
| [[library-evaluation-rubric]] | upstream context this methodology builds on |
| [[blast-radius-scoring-rubric]] | sibling discipline cited in decision tree |

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
| `fill-dependency-spike-kill-criteria-template-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-dependency-spike-kill-criteria-template.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dependency-spike-kill-criteria-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[library-evaluation-rubric]]
- [[blast-radius-scoring-rubric]]
- [[hidden-tech-debt-trace]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
