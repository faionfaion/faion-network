# Fitness-Function Suite Bootstrap

## Summary

**One-sentence:** Produces a starter fitness-function suite — 5–8 functions covering perf, deploy, dep, complexity, contract — wired into CI with thresholds, owners, and weekly review cadence, so the architecture-fitness practice goes live in a week instead of a quarter.

**One-paragraph:** Produces a starter fitness-function suite — 5–8 functions covering perf, deploy, dep, complexity, contract — wired into CI with thresholds, owners, and weekly review cadence, so the architecture-fitness practice goes live in a week instead of a quarter. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** platform engineers and architects who agreed on evolutionary architecture last quarter and are now stuck on which 5–8 fitness functions to ship first, with what thresholds, and who owns each.

## Applies If (ALL must hold)

- The team has agreed to run fitness functions but has none in CI yet, and wants the first 5 to 8 live within a week.
- One critical endpoint is known and a load tool (k6, Gatling, Locust) can hit it from a dedicated runner or environment.
- The CI system exposes pipeline timestamps (GitHub Actions, GitLab CI, Jenkins) so lead time can be computed by a script.
- The service has a declared layering and a published API definition (OpenAPI, GraphQL, protobuf) or Pact consumers to gate against.
- One person per function will own it as `role:handle` and four weekly reviews can be scheduled from launch.

## Skip If (ANY kills it)

- A fitness-function suite already runs in CI with owners and a review history; use the ongoing suite review, not a bootstrap.
- No CI runs on pull requests or on a schedule, so nothing can be triggered or continual; set up CI first.
- The service has no published API and no consumers, so the contract category cannot be filled and the five-category minimum cannot be met.
- The team wants twelve or more functions in week one; cut to 5 to 8 before applying, or the launch drowns in unexplained reds.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Critical endpoint and a versioned load profile | `METHOD /path` plus a committed k6 / Gatling / Locust config | product owner + `perf/profiles/` in the repo |
| Dependency graph (layers and allowed edges) | package layout, C4 component view or ADR | architecture docs / repo |
| Pipeline run history | last 20 runs on main via `gh run list` or the GitLab pipelines API | CI system |
| Last released API definition or consumer contracts | OpenAPI / GraphQL / protobuf at a released tag, or Pact broker URL | API repo / Pact broker |
| Current complexity violators | tool output at the per-function limit, committed as a baseline file | `radon` / `lizard` / ESLint / SonarQube run on main |
| Owner per function and a reviewer | `role:handle` | org directory |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: 5 to 8 functions, p95 under fixed load, deploy lead time from CI, dependency direction tool, complexity baseline ratchet, contract breaking-change gate, ratchet before block, owner and weekly review | ~2000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the starter suite: 5 to 8 functions with all five categories present, per-function tool, command, threshold, dated baseline, mode, run stage, owner, category-specific fields (endpoint and load profile, minutes from CI, dependency graph, baseline file, consumers or released schema), promotion record for blocking, four weekly reviews; valid and invalid suites; 8 forbidden patterns | ~4450 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 9 steps: one function per category, write the dependency graph, wire performance / deployability / complexity / contract with their tools, baseline and launch non-blocking, four weekly reviews, promote to blocking on five green runs | ~1750 |
| `content/05-examples.xml` | recommended | Complete five-function orders-api suite (k6 nightly, pipeline duration script, import-linter, lizard ratchet with baseline file, oasdiff) with reviews filled and a note per value, plus a three-function blocking launch the validator rejects | ~2300 |
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
| `scripts/validate-fitness-function-suite-bootstrap.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
