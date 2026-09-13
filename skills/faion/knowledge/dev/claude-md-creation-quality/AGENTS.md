# CLAUDE.md Creation

## Summary

**One-sentence:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — that fits a Claude Code session's loading budget without leaking secrets or wasting tokens on stale prose.

**One-paragraph:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — that fits a Claude Code session's loading budget without leaking secrets or wasting tokens on stale prose. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers and tech leads opening a new repo for Claude Code who need a token-efficient, secrets-safe project brief their team can amend in PRs.

## Applies If (ALL must hold)

- A root CLAUDE.md is being created for a repository that has none, or an existing one fails a check: secret scan, line budget, path existence or a command that does not run.
- The build, test, lint and run commands exist in a machine-readable place (Makefile, package.json scripts, pyproject, CI workflow) or can be written as verbatim invocations and run on a fresh clone.
- CI and pre-commit can host gitleaks or trufflehog, a wc -l line-budget check and a referenced-path existence check.
- In a multi-package repository each package directory can carry its own CLAUDE.md that Claude Code loads on demand.
- A named reviewer will approve the PR after the three checks are green.

## Skip If (ANY kills it)

- The root file exists, fits its declared budget, scans clean, and every path and command resolves; amend it in the PR that renames a referenced file, not on a schedule.
- The directory is not a repository root or a deployable package (a docs folder, a data set); there is nothing for a session to run.
- Personal or machine-specific instructions are the only content wanted; those belong in CLAUDE.local.md or ~/.claude/CLAUDE.md, not in a committed project file.
- A platform-generated CLAUDE.md owns the commands section and its checks already run in the organisation's CI; contribute prohibitions and imports there instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Command source | Makefile, package.json scripts, pyproject tooling or CI workflow | repository |
| Fresh clone | clean checkout at the commit being briefed, with the toolchain installed | local machine or CI |
| Secret scanner in CI and pre-commit | gitleaks or trufflehog configuration | .pre-commit-config.yaml and CI workflow |
| Repository docs to import | README, CONTRIBUTING, ADR index, style guide with their paths | repository |
| Package layout | list of deployable packages and their directories | repository / architecture doc |
| Named reviewer | role:handle of the person who approves CLAUDE.md changes | CODEOWNERS or team lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: no secrets, verbatim commands, line budget, import-not-paste, local scope, subdir scoping, argued prohibitions, refs exist | ~2000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the record: root_file with declared line budget, within_budget and CI line check, secrets scanner in CI and pre-commit and clean, verbatim commands with exit 0, imports within five hops and no pasted content, local scope, subdir_files required for multi-package with no per-package commands in the root, prohibitions with consequence stated and emphasis_ratio at most 0.25, refs check, named reviewer; valid and invalid examples | ~3550 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 9 steps: bootstrap and declare budget, verbatim commands run on a fresh clone, import not paste, personal content local, per-package scoping, argued prohibitions and rationed emphasis, secret / line / path checks in CI and pre-commit, reviewer approval, validate and merge | ~1700 |
| `content/05-examples.xml` | recommended | Complete multi-package platform record at 84 of 100 lines with notes on every non-obvious value, plus the 480-line first draft breaking all eight rules and what the validator and reviewer say | ~1900 |
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
| `scripts/validate-claude-md-creation-quality.py` | Validate the CLAUDE.md quality record JSON against the output-contract schema. | Pre-merge of the CLAUDE.md PR, after the secret scan, line check and path check are green. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
