# Documentation

## Summary

**One-sentence:** Defines the AGENTS.md + CLAUDE.md per-dir doc convention so agents can navigate any code dir under ~80 lines of context.

**One-paragraph:** Agents that lack a routing doc fall back to guessing file paths; the guesses go stale and the agent edits the wrong place. This methodology mandates one AGENTS.md per code directory (20-80 lines, structured: purpose + key files + commands + gotchas) and one CLAUDE.md that just contains `@AGENTS.md`. The pair fits in any agent's auto-load budget and answers four questions: what is this dir, what files matter, how do I build/test, what are the pitfalls. Output is a spec artefact listing every dir + its required headers + a smoke-test that verifies the pair exists.

**Ефективно для:**

- Repos з 50+ subdirs: agent-navigation collapse без routing-doc.
- Multi-agent workflows (faion/poll-agents): кожен субагент стартує в незнайомому dir — потрібен 20-line context.
- Onboarding new dev: AGENTS.md = живий orientation tour без 50-page handbook.
- Migration: old README.md → AGENTS.md як частина refactor PR.

## Applies If (ALL must hold)

- Repo has ≥10 code directories (below that, root AGENTS.md suffices).
- Agents are routinely launched in subdirectories (cwd-scoped sessions).
- Team treats docs as code (PR-reviewed, versioned).

## Skip If (ANY kills it)

- Single-file repo or one-shot script.
- Pure data repo (no code modules).
- Vendored / generated subdirs — exempted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo root | path | git rev-parse --show-toplevel |
| Existing AGENTS.md inventory | list | find . -name AGENTS.md |
| Code-dir inventory | list | find . -type d with source files |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pair-required, 20-80-lines, structured-sections, no-readme-shadowing, refresh-on-edit | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for doc-spec artefact | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: drift-from-code, stretch-past-80, readme-shadow | 600 |
| `content/04-procedure.xml` | essential | 5-step rollout procedure | 700 |
| `content/05-examples.xml` | reference | Example AGENTS.md for a python module | 500 |
| `content/06-decision-tree.xml` | essential | Dir-shape tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_dirs` | haiku | find + filter; deterministic. |
| `draft_agents_md` | sonnet | Per-dir custom content; needs source skim. |
| `verify_pair` | haiku | File-exists checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agents-md-universal.md.j2` | Universal AGENTS.md skeleton with placeholders |
| `templates/agents-md-universal.md` | Universal AGENTS.md skeleton with placeholders Generated from `templates/agents-md-universal.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/doc-outline.sh` | Shell that scans a dir and prints draft AGENTS.md sections |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- - [[code-review-process]] — docs PRs use the same review template.
- - [[code-decomposition-patterns]] — decomposition PRs MUST update / create AGENTS.md per moved dir.

## Decision tree

See `content/06-decision-tree.xml`. Branches: dir has source code? → pair required. Dir is tests-only / generated / vendored? → exempt. Repo-root vs sub-dir → root carries top-level map, sub-dir carries local map.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/doc-outline.sh`

```bash
#!/usr/bin/env bash
# doc-outline.sh — emit a JSON outline for a directory the writer agent will fill.
# Usage: doc-outline.sh path/to/dir
# Output: JSON with dir, type, files (from git ls-files), languages (from tokei)
set -euo pipefail
DIR="$1"

jq -n \
  --arg dir "$DIR" \
  --argjson files "$(git ls-files "$DIR" | jq -Rsc 'split("\n")|map(select(length>0))')" \
  --argjson lang "$(tokei -o json "$DIR" 2>/dev/null | jq '.. | objects | select(.language) | {(.language): .code}' 2>/dev/null || echo '{}')" \
  --arg type "$(test -f "$DIR/package.json" && echo frontend \
                || test -f "$DIR/manage.py" && echo backend-django \
                || test -f "$DIR/pyproject.toml" && echo backend-python \
                || test -d "$DIR/terraform" && echo infra \
                || echo library)" \
  '{dir:$dir, type:$type, files:$files, languages:$lang}'
```
