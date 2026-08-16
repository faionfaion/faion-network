# Documentation

## Summary

**One-sentence:** Produces the CLAUDE.md (@AGENTS.md) + AGENTS.md (20-80 lines) pair in every source-bearing directory: purpose, file table, key types, commands, gotchas. Required at every source-bearing dir.

**One-paragraph:** Produces the CLAUDE.md (@AGENTS.md) + AGENTS.md (20-80 lines) pair in every source-bearing directory: purpose, file table, key types, commands, gotchas. Required at every source-bearing dir. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project contains directories with source code that lack `CLAUDE.md` / `AGENTS.md`.
- The team has agreed to the convention `CLAUDE.md = @AGENTS.md`.
- AI agents (Claude Code, Codex, Cursor) read these files during sessions.

## Skip If (ANY kills it)

- Single-file scripts with no surrounding directory.
- Vendored / generated code directories where edits would be overwritten.
- Empty `__init__.py`-only dirs with no logic.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | Repo-wide convention surface this implements. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to documentation | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold the output skeleton | sonnet | Mechanical, deterministic. |
| Refine domain-specific content | opus | Needs judgement. |
| Validate against output contract | sonnet | Schema check, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/AGENTS-universal.md.j2` | Canonical AGENTS.md skeleton (20-80 lines, file table, key types, commands, gotchas). |
| `templates/AGENTS-universal.md` | Canonical AGENTS.md skeleton (20-80 lines, file table, key types, commands, gotchas). Generated from `templates/AGENTS-universal.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/audit-agents-md.sh` | Sweep the repo and report directories missing CLAUDE.md / AGENTS.md. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-documentation.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-review]] — see methodology AGENTS.md for context.
- [[django-coding-standards]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/audit-agents-md.sh`

```bash
# audit-agents-md.sh — flag dirs where source files are newer than AGENTS.md by >14 days.
# Usage: bash audit-agents-md.sh [repo-root]
set -e
THRESH=$((14*24*60*60))
fail=0
while IFS= read -r dir; do
  agents="$dir/AGENTS.md"
  [ -f "$agents" ] || continue
  agents_ts=$(stat -c %Y "$agents")
  newest_src=$(find "$dir" -maxdepth 1 -type f \
      \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.go' \) \
      -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1)
  [ -z "$newest_src" ] && continue
  if [ $((newest_src - agents_ts)) -gt $THRESH ]; then
    echo "DRIFT: $agents (source newer by >14 days)"
    fail=1
  fi
done < <(find "${1:-.}" -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*')
exit $fail
```
