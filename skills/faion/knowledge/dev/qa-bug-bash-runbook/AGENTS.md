# QA Bug Bash Runbook

## Summary

**One-sentence:** Runs a 60-minute pre-release bug bash with charters per persona, time-boxed sessions, dedup pipeline, and a severity-classified bug ledger ready for triage.

**One-paragraph:** Runs a 60-minute pre-release bug bash with charters per persona, time-boxed sessions, dedup pipeline, and a severity-classified bug ledger ready for triage. Charter + persona + timebox + observers. Each tester gets one charter; observers triage live; dedup pass at the end; output is a triaged bug ledger with sev/owner. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Pre-release stage with feature complete but no recent broad exploratory pass.
- Team has 4+ humans available for a 60-minute focused session.
- Release scope spans multiple personas (admin, end user, integrator) and only narrow tests have run.
- Output produces `playbook-step` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Pre-release stage with feature complete but no recent broad exploratory pass.
- Team has 4+ humans available for a 60-minute focused session.
- Release scope spans multiple personas (admin, end user, integrator) and only narrow tests have run.

## Skip If (ANY kills it)

- Solo developer release — exploratory pass is one person's job, no facilitation needed.
- Continuous deploy with feature flags and < 1% blast radius per change.
- Compliance-driven release where the test plan is fixed and bug-bashing creates audit noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release notes | Markdown | release-qa-cycle output |
| Persona list | list | product spec |
| Bug tracker URL | URL | Jira/Linear |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-test-strategy-template]] | Test strategy this complements with exploratory coverage. |
| [[qa-prioritization-rubric]] | Severity rubric used to triage findings. |

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
| `draft-charters` | sonnet | One charter per persona from release notes. |
| `dedup-findings` | haiku | Mechanical dedup of bug titles by similarity. |
| `classify-severity` | sonnet | Apply rubric to each finding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/charters.md` | Markdown skeleton for the artefact. |
| `templates/bug-bash-ledger.csv` | CSV template for tabular artefacts. |
| `templates/_smoke-test.csv` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-bug-bash-runbook.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-test-strategy-template]]
- [[qa-prioritization-rubric]]
- [[release-qa-cycle-template]]
- [[qa-session-based-test-management]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the release scope broad enough to warrant a multi-persona exploratory pass?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
