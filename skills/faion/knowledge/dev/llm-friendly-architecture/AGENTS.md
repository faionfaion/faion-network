# LLM-Friendly Architecture (Software Developer)

## Summary

**One-sentence:** Produces an LLM-friendly architecture audit — file-size histogram, directory-depth check, naming-clarity score, explicit-import lint — written from a software developer's viewpoint, so AI-driven edits stop bouncing off oversized files and hidden import chains.

**One-paragraph:** Produces an LLM-friendly architecture audit — file-size histogram, directory-depth check, naming-clarity score, explicit-import lint — written from a software developer's viewpoint, so AI-driven edits stop bouncing off oversized files and hidden import chains. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers (typescript / react / python) whose codebase is being edited daily by Claude Code or Cursor and who need a measurable rubric (100-300 LOC per file, ≤3 dir levels, explicit imports) before AI edit errors compound.

## Applies If (ALL must hold)

- The codebase is edited by an AI coding agent (Claude Code, Cursor or similar) on a recurring basis, not only by people.
- The language is TypeScript / JavaScript or Python, so `templates/llm-arch-audit.sh` and the import lint (Ruff F403/F405, eslint-plugin-import no-namespace) apply.
- The repo can be audited at a pinned commit by a committed script, and the command can later run in CI on pull requests.
- A `CLAUDE.md` exists at the repo root or can be generated from `templates/claude-md-project.md.j2` and committed.
- One developer will own the splits, deletions and renames the decision names, as `role:handle`.

## Skip If (ANY kills it)

- No AI agent edits the codebase; a human-only repo gets a normal architecture review, not this rubric.
- The tree is generated or vendored code (protobuf stubs, ORM migrations, node_modules-style bundles) where file size and naming are not the team's to change.
- The language has no wildcard-import or barrel construct and a monolithic file layout is imposed by the framework (a single Arduino sketch, a Jupyter notebook).
- An audit at the same commit already exists with the same line limit; rerun only after the named splits have merged.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Repo at a pinned commit | clone plus `git rev-parse HEAD` | the project repo |
| Audit script | `templates/llm-arch-audit.sh` or the project's committed equivalent | this methodology / `scripts/` in the repo |
| Line limit | integer 100 to 300 (default 250) | team convention, written into CLAUDE.md |
| Import lint output | Ruff `F403`/`F405` or `eslint-plugin-import` `import/no-namespace` report | the project's linter |
| CLAUDE.md | Markdown at the repo root with commands, structure, conventions and the max file size | `templates/claude-md-project.md.j2` |
| Namespace import allow-list | list of module names (e.g. react, three) | team convention |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: file-size histogram with threshold, directory depth cap, no barrels, explicit imports, naming score lists offenders, static data extracted, CLAUDE.md matches audit, reproducible audit command | ~1750 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the audit record: repo and SHA, line_limit (100 to 300), audit block with histogram and ranked oversized files each with a named split, depth violations, barrels, wildcard-import hits, naming rubric with score and offenders, inline data, CLAUDE.md line limit, CI wiring; decision that names files; evidence with command and SHA; valid and invalid records; 8 forbidden patterns | ~4150 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 8 steps: pin limit and SHA, run the audit script, rank oversized files with splits, list depth / barrels / wildcards, score naming with offenders, find inline data, reconcile CLAUDE.md, decide and wire CI | ~1500 |
| `content/05-examples.xml` | recommended | Complete storefront audit record (1,412-line CheckoutPage split, one barrel, one namespace import, depth-5 path, naming 84 with offenders, CLAUDE.md at 250) with a note per value, plus the usual 400-line 'split later' audit and what the validator prints | ~1900 |
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
| `templates/claude-md-project.md.j2` | CLAUDE.md skeleton tuned for LLM-friendly architecture rules. |
| `templates/claude-md-project.md` | CLAUDE.md skeleton tuned for LLM-friendly architecture rules. Generated from `templates/claude-md-project.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/llm-arch-audit.sh` | Shell audit: file size, directory depth, naming-clarity rules. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-friendly-architecture.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
