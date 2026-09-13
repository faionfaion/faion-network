# Evolutionary Architecture Fitness Functions

## Summary

**One-sentence:** Produces an evolutionary-architecture fitness-function suite spec — quality attribute, threshold, sensor, owner, cadence — that turns 'maintainability/scalability' aspirations into CI-checkable constraints.

**One-paragraph:** Produces an evolutionary-architecture fitness-function suite spec — quality attribute, threshold, sensor, owner, cadence — that turns 'maintainability/scalability' aspirations into CI-checkable constraints. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software architects translating Ford/Parsons-style evolutionary architecture from a book into a CI gate: every quality attribute carries a measurable sensor + threshold + owner.

## Applies If (ALL must hold)

- The codebase has a declared layering or module boundary (C4 view, package layout, ADR) that a structural test can enforce.
- A CI pipeline exists that can run a test or linter on every pull request and on a schedule.
- At least one architectural characteristic can be measured by a tool with a number and a unit (ArchUnit, NetArchTest, dependency-cruiser, import-linter, lizard, k6).
- One person per function will own it as `role:handle` and the team will review the suite monthly or quarterly.
- A metrics backend, CI artifact store or committed CSV can keep a per-run value series for at least the review horizon.

## Skip If (ANY kills it)

- The system is a prototype or throwaway with no architecture to protect; write the first ADR instead.
- No CI runs on pull requests, so every function would be `manual` and the one-fifth cap cannot be met.
- The characteristics on the table are only -ilities with no agreed metric; hold a quality-attribute workshop first.
- Every measurable check is already a blocking CI gate with a trended series and an owner; run the cadence review, not this methodology.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Intended dependency graph (layers and allowed edges) | C4 component view, package layout or ADR | architecture docs / repo |
| Candidate characteristics with metric and unit | list of noun phrases with a number and unit | architecture review, last two incident reviews |
| One baseline measurement per function | command output on current main, dated | the tool run once locally or in CI |
| CI pipeline definition | `.github/workflows/*.yml`, `.gitlab-ci.yml` or equivalent | repo |
| Results store location | metrics series name, artifact path or CSV path | SRE / platform team |
| Owner per function | `role:handle` | org directory |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: one attribute one metric, executable in CI, baseline ratchet, blocking vs informational, structural dependency guard, trended results, owner and cadence | ~1800 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the suite spec: per-function characteristic, metric, unit, tool, command, threshold, dated baseline, ratchet mode, blocking/triggered, owner; suite-level dependency graph, results store, review; valid and invalid suites; 8 forbidden patterns | ~3450 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 8 steps: name characteristics, write the dependency graph and structural function, pick tool and command, measure baselines, set thresholds (absolute or ratchet), classify and wire CI, wire the results store, assign owners and review | ~1600 |
| `content/05-examples.xml` | recommended | Complete billing-service suite (ArchUnit layer guard, lizard complexity ratchet, nightly k6 latency) with a note per non-obvious value, plus a rejected manual quality-score entry and what the validator prints | ~1450 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-evolutionary-architecture-fitness-functions.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
