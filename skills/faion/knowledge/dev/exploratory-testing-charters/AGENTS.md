# Exploratory Testing Charters

## Summary

**One-sentence:** Session-based exploratory-testing charter format: a one-page mission with named area, threat hypothesis, time-box, and debrief schema; produces a charter spec the tester executes and a debrief report logged against it.

**One-paragraph:** Session-based exploratory-testing charter format: a one-page mission with named area, threat hypothesis, time-box, and debrief schema; produces a charter spec the tester executes and a debrief report logged against it. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Pre-release smoke on a feature that automated tests cover only happy-path.
- Onboarding a new tester to a legacy module — charters double as guided tour.
- Post-incident exploration of the area around the root cause.
- Solo founders who must test like a tester for a 90-minute window per release.

## Applies If (ALL must hold)

- Feature, area, or release candidate exists where automated tests give incomplete coverage.
- Tester has ≥1 uninterrupted block of 60–120 minutes for the session.
- Charter has a single named author + tester (same person allowed for solo).
- A log location (markdown, ticket) exists for the debrief.

## Skip If (ANY kills it)

- Pure regression check — automated tests are the right tool.
- No tester time available — un-executed charters are noise.
- Area is too broad (whole product) — narrow the charter first or it becomes wandering.

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
| [[qa-bug-bash-runbook]] | upstream context this methodology builds on |
| [[qa-session-based-test-management]] | sibling discipline cited in decision tree |

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
| `fill-exploratory-testing-charters-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-exploratory-testing-charters.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-exploratory-testing-charters.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[qa-bug-bash-runbook]]
- [[qa-session-based-test-management]]
- [[qa-prioritization-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
