# Spec-Driven Debugging

## Summary

**One-sentence:** Bug-scale SDD: write a failing spec naming the symptom, minimize the repro to <=20 lines, fix while spec is red→green, attach the spec to the codebase as a regression test.

**One-paragraph:** Feature-scale SDD does not cover bugs. Devs spend ~30% of their time debugging, often via guess-and-check that produces fixes without regression tests. This methodology applies SDD at bug scope: (1) write a failing spec naming the symptom + expected behaviour, (2) minimize the repro to <=20 lines, (3) bisect to the offending commit, (4) fix while the spec turns green, (5) attach the spec to the codebase as a permanent regression test. Output is a bug-spec document + the test commit.

**Ефективно для:**

- Bug repro >100 рядків - звузити до <=20.
- Fix без regression test - впровадити failing-spec-first.
- Бубну схожу на попередній - перевірити стару spec, не переписувати.
- Невідтворюваний bug - bisect + minimal repro для відтворення.
- AI generates fix - спочатку failing test, потім код.

## Applies If (ALL must hold)

- Bug reported with reproducible symptom OR strongly suspected reproducer.
- Test infrastructure exists where a failing test can be added.
- Developer has authority to add tests + commit fixes.
- Bug touches a code path (not pure config / infra).

## Skip If (ANY kills it)

- Infrastructure / config bug with no code path involved.
- Bug takes longer to write a test for than to fix (typo, copy edit).
- Research / spike investigation - different mode.
- Non-reproducible bug from logs only - use observability methodology first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test framework | pytest / jest / cargo test / etc. | engineering |
| Stack trace or log | captured failure | incident report |
| Git SHA of reproducing state | commit hash + env | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-self-code-review-protocol]] | fix PR runs through the self-review protocol. |
| [[xp-extreme-programming]] | red-green-refactor cycle this methodology specialises. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: failing spec first, minimize repro <=20 lines, bisect on regression, fix while red→green, spec stays as regression test, name symptom precisely, link to incident | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: spec, minimise, bisect, fix, keep regression | ~900 |
| `content/05-examples.xml` | essential | Worked example for an orders-validation regression | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-bug-spec` | sonnet | Per-bug judgement on symptom + expected. |
| `minimize-repro` | sonnet | Delta-debugging requires per-step judgement. |
| `run-bisect` | haiku | Mechanical git bisect with spec oracle. |
| `design-fix` | opus | Stakes high; minimum-code-change discipline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bug-spec.md` | Markdown bug-spec template (symptom + expected + repro + fix link). |
| `templates/bisect.sh` | Wrapper running git bisect with the failing spec as oracle. |
| `templates/_smoke-test.json` | Minimum viable bug-spec record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-driven-debugging.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[solo-self-code-review-protocol]]
- [[xp-extreme-programming]]
- [[performance-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - repro reproducibility, regression-shape, test-cost ratio - onto a rule from `content/01-core-rules.xml`. Use it before fixing: it catches no-regression-test and guess-instead-of-bisect upstream.
