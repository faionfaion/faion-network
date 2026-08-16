# Unit Testing (FIRST + AAA)

## Summary

**One-sentence:** Produces a unit-test rubric: FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), AAA structure, method-scenario-expected naming, line-and-branch coverage targets.

**One-paragraph:** Covers the FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), Arrange-Act-Assert structure, test naming conventions (method-scenario-expected, should-when, given-when-then), coverage strategies (line vs branch vs mutation), test categories, and the most damaging anti-patterns (testing implementation, not behavior). Unit tests are the foundation of every test pyramid. Without consistent structure and naming, suites become maintenance burdens.

**Ефективно для:** any new pure-logic test, code-review of test PRs, onboarding new engineers to a codebase, judging if a 'unit' test is actually an integration test in disguise.

## Applies If (ALL must hold)

- Writing the first unit tests for a function, method, or class
- Reviewing a PR with new tests
- Diagnosing why a 'unit' suite takes 30 seconds (clearly not isolated)
- Selecting a naming convention for a fresh codebase

## Skip If (ANY kills it)

- Cross-component or system tests — use integration / E2E layers
- Language-runner setup — use `[[testing-pytest]]`, `[[testing-go]]`, `[[testing-javascript]]`
- UI tests — use `[[e2e-testing]]`

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Code under test | function/method/class | source repo |
| Test runner choice | decision | language-specific methodology |
| Naming convention preference | enum | team policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[testing-patterns]]` | AAA / pyramid / data patterns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick naming convention | sonnet | Policy choice. |
| Author AAA test | sonnet | Template application. |
| Audit suite for FIRST violations | opus | Pattern recognition + remediation strategy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/aaa-skeleton.py.tmpl` | AAA template in Python. |
| `templates/_smoke-test.md.j2` | Minimal filled rubric. |
| `templates/_smoke-test.md` | Minimal filled rubric. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `free/dev/testing-developer/`
- `[[testing-patterns]]`
- `[[testing-pytest]]`
- `[[testing-javascript]]`
- `[[testing-go]]`
- `[[mocking-strategies]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether unit-testing applies: root question — "Is the code under test a pure function or method (no I/O)?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/aaa-skeleton.py.tmpl`

```python
Python AAA skeleton
"""
from __future__ import annotations


def main() -> None:
    """Entry point. Fill per methodology procedure."""
    # TODO: implement per 04-procedure.xml
    raise NotImplementedError


if __name__ == "__main__":
    main()
```
