# CLAUDE.md Creation (Software Developer)

## Summary

**One-sentence:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — tuned for a software developer opening a new repo in Claude Code, with bounded token budget and zero secrets.

**One-paragraph:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — tuned for a software developer opening a new repo in Claude Code, with bounded token budget and zero secrets. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers opening a new repo in Claude Code who need a fast, token-efficient project brief their team can amend in PRs without rewriting it every Monday.

## Applies If (ALL must hold)

- A repository or app directory has no CLAUDE.md, or its existing one names a command that no longer exists in package.json, the Makefile or pyproject.toml.
- The repository's commands live in a manifest (package.json scripts, Makefile targets, pyproject.toml tooling, justfile) that templates/extract-commands.sh or a manual read can list.
- A clean checkout is available (locally or in CI) on which every listed command can be run once before the file is committed.
- A secret scanner (gitleaks, trufflehog or the host's built-in) can run on the file in CI or pre-commit.
- CI or pre-commit can host the manifest-resync check.

## Skip If (ANY kills it)

- A CLAUDE.md exists, its commands match the manifests and the resync check is green; amend it in the PR that changes the code, not on a schedule.
- The directory is not a repository root or an app with its own manifests (a docs folder, a data directory); there are no commands to brief.
- The organisation mandates a generated CLAUDE.md from a platform tool that owns the commands section; contribute gotchas there rather than hand-writing a competing file.
- The repository is archived or read-only; a brief for a repo nobody works in is tokens paid for nothing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Manifest command list | output of templates/extract-commands.sh or the manifests themselves | repository root |
| Clean checkout | fresh clone at the commit being briefed | local machine or CI |
| Secret scanner | gitleaks / trufflehog / host scanner run over CLAUDE.md | CI or pre-commit |
| Directory tree and key files | paths a developer needs in the first hour, verified to exist | repository |
| .env.example | env var names with placeholders, no values | repository root |
| Per-app manifests (monorepo) | one manifest per app directory | apps/*/ |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: commands extracted and executed, zero secrets, token budget held, load-bearing structure, monorepo delegates via imports, repo-specific gotchas, personal settings local, manifest resync check | ~2050 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the record: layout and template with token_count capped at 250 / 500 / 700, commands with manifest source and ran_ok true, secret scan clean with env vars by name, structure of at most 20 purposed paths excluding generated dirs, key files that exist, gotchas naming a file / env var / command / pin / lint rule, personal paths clean, resync check that fails on drift, monorepo delegation block; valid and invalid examples | ~3700 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~1050 |
| `content/04-procedure.xml` | recommended | 8 steps: template by layout, extract and run commands, structure and key files, gotchas and env by name, per-app delegation, personal content local, secret scan and budget, resync check then validate and commit | ~1750 |
| `content/05-examples.xml` | recommended | Complete FastAPI service record from the standard template with notes on every non-obvious value, plus the first draft breaking six rules and what the validator and reviewer say | ~1900 |
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
| `templates/claude-md-minimal.md.j2` | Minimal CLAUDE.md skeleton for single-language repos. |
| `templates/claude-md-minimal.md` | Minimal CLAUDE.md skeleton for single-language repos. Generated from `templates/claude-md-minimal.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/claude-md-standard.md.j2` | Standard CLAUDE.md skeleton for product repos. |
| `templates/claude-md-standard.md` | Standard CLAUDE.md skeleton for product repos. Generated from `templates/claude-md-standard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/claude-md-monorepo.md.j2` | Monorepo CLAUDE.md skeleton — root brief + per-app addenda. |
| `templates/claude-md-monorepo.md` | Monorepo CLAUDE.md skeleton — root brief + per-app addenda. Generated from `templates/claude-md-monorepo.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/extract-commands.sh` | Shell helper dumping repo commands into CLAUDE.md-ready format. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-md-creation.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
