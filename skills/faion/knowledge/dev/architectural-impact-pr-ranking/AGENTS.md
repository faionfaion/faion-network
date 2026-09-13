# Architectural Impact PR Ranking

## Summary

**One-sentence:** Produces a weekly architectural-impact PR ranking report — top N PRs scored on blast-radius (modules touched, public API delta, dep changes, contract change) — so the architect's 45-minute review session lands on the PRs that actually move the architecture.

**One-paragraph:** Produces a weekly architectural-impact PR ranking report — top N PRs scored on blast-radius (modules touched, public API delta, dep changes, contract change) — so the architect's 45-minute review session lands on the PRs that actually move the architecture. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** tech leads / software architects running the weekly 45-minute architectural review who must pick which PRs to read out of hundreds without missing the ones that quietly bend the architecture.

## Applies If (ALL must hold)

- A time-boxed architecture review session exists with a fixed slot (45 minutes by default) and an architect or tech lead who reads what the ranking selects.
- The PR population is defined: a list of repositories and a window of opened-or-merged timestamps the ranker can query.
- Each repository's diff, file list and dependency manifests are readable by the ranker (git access or the hosting API), so signals can be computed from the change itself.
- Each repository has, or can commit, a version-controlled list of its public API paths (schemas, migrations, exports, event definitions, CLI flags).
- The architect will mark each ranked PR hit or miss after the session, so precision can be recorded.

## Skip If (ANY kills it)

- There is no recurring architecture review session; ranking PRs for a slot that does not exist produces a list nobody reads.
- The week's population is small enough to read in full inside the time-box; rank only when the queue exceeds the session.
- The repositories expose no diff access to the ranker (mirrored read-only snapshots without history), so signals would have to come from PR metadata, which the rules forbid.
- A platform team already publishes an architecture-impact ranking over the same repositories and window; consume that report rather than running a second scorer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| PR population for the window | list of owner/repo#number with opened and merged timestamps | hosting API (GitHub, GitLab) |
| Diff and file list per PR | git diff --name-status and --stat output | git / hosting API |
| Dependency manifests | package.json, go.mod, pyproject.toml, Cargo.toml, pom.xml diffs | repository |
| Public API path list per repository | version-controlled YAML or JSON listing schema, migration, export and event paths | each repository's .arch/ or docs/ directory |
| Session parameters | slot, time-box minutes, review threshold | review owner |
| Previous report with hit / miss marks | last week's report JSON with outcome per ranked PR | .product/architectural-impact-pr-ranking/ |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: published formula, signals from diff, public API list per repo, dependency kinds, top N fits session, window and exclusions, merged-without-review, precision recorded | ~1850 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the report: window over opened-or-merged PRs, repositories with public API path config, session time-box and summed read minutes, five published weights, dependency kind weights with lockfile_only 0 and patch bumps capped, signals_from_diff_only, ranked PRs with signals, lines, read minutes and hit / miss outcome, deferred, reconciling exclusions, merged_without_review, previous precision, weight_change requiring four weeks; valid and invalid examples | ~4600 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~1000 |
| `content/04-procedure.xml` | recommended | 9 steps: session and population, public API path list per repo, publish weights, signals from diff, dependency kinds, rank and cut to the time-box, reconcile exclusions and merged-without-review, record precision, validate and publish | ~1800 |
| `content/05-examples.xml` | recommended | Complete week 37 report over three repositories with notes on every non-obvious value, plus the same week from the first ranker breaking seven rules and what the validator and architect say | ~2350 |
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
| `scripts/validate-architectural-impact-pr-ranking.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
