# QA Session-Based Test Management

## Summary

**One-sentence:** Runs uncharted exploratory testing in time-boxed 90-min sessions with a charter, observers' notes, bug/issue/task split, and a session report committed to repo.

**One-paragraph:** Runs uncharted exploratory testing in time-boxed 90-min sessions with a charter, observers' notes, bug/issue/task split, and a session report committed to repo. Charter-driven session with task/bug/issue ledger, time split (setup/test/bug-investigation/report), and dedicated debrief. Output: machine-readable session report. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Feature is complete but specs are sparse; need exploratory coverage.
- Team is moving away from rigid script-based testing toward charter-driven exploration.
- Need reviewable artefacts from each exploratory pass for audit and trend analysis.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Feature is complete but specs are sparse; need exploratory coverage.
- Team is moving away from rigid script-based testing toward charter-driven exploration.
- Need reviewable artefacts from each exploratory pass for audit and trend analysis.

## Skip If (ANY kills it)

- Regulated context where scripted testing is mandatory — adopt the regulator's framework.
- Team < 2 testers and no time-box discipline — overhead > benefit.
- Pre-product with no UI to explore.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter | 1-paragraph mission | tester or lead |
| Build under test | deployed RC URL | ops |
| Session report template | template path | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-bug-bash-runbook]] | Bug-bash is the multi-person variant of SBTM. |
| [[qa-prioritization-rubric]] | Severities of findings come from the rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-charter` | sonnet | Pull mission scope from a feature spec. |
| `write-report` | sonnet | Synthesise notes into the canonical report shape. |

## Templates

| File | Purpose |
|------|---------|
| `templates/session_report.json` | JSON template scaffolding the artefact contract. |
| `templates/charter.md` | Markdown skeleton for the artefact. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-session-based-test-management.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-bug-bash-runbook]]
- [[qa-prioritization-rubric]]
- [[qa-test-strategy-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are we running uncharted exploratory testing on a non-trivial UI feature?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
