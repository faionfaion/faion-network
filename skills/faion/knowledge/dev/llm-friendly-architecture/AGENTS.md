# LLM-Friendly Architecture (Software Developer)

## Summary

**One-sentence:** Produces an LLM-friendly architecture audit — file-size histogram, directory-depth check, naming-clarity score, explicit-import lint — written from a software developer's viewpoint, so AI-driven edits stop bouncing off oversized files and hidden import chains.

**One-paragraph:** Produces an LLM-friendly architecture audit — file-size histogram, directory-depth check, naming-clarity score, explicit-import lint — written from a software developer's viewpoint, so AI-driven edits stop bouncing off oversized files and hidden import chains. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers (typescript / react / python) whose codebase is being edited daily by Claude Code or Cursor and who need a measurable rubric (100-300 LOC per file, ≤3 dir levels, explicit imports) before AI edit errors compound.

## Applies If (ALL must hold)

- A named trigger has fired (release, incident, schedule, scope change) that warrants producing the artefact.
- The owner is a named person (role:handle), not a team alias or channel.
- The required input artefacts in `## Prerequisites` are available and machine-readable.
- The downstream consumer for the produced artefact is known (review board, CI gate, customer, regulator).

## Skip If (ANY kills it)

- Trigger is vague ("when needed", "soon"); rewrite the trigger first.
- No named owner — refuse to produce; assign first.
- Inputs are missing or non-deterministic; fix the upstream observability before applying.
- A different, already-pinned methodology handles this exact decision (avoid duplicate artefacts).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Trigger record | text / ticket link | upstream alerting / planning queue |
| Owner identity | `role:handle` string | RACI / org directory |
| Input artefacts | as listed in `02-output-contract.xml` `required` | upstream methodology output |
| Prior artefact (if exists) | JSON matching the output contract | repo `.product/llm-friendly-architecture/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | recommended | One full worked example end-to-end | ~600 |
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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-friendly-architecture.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "trigger": {
    "kind": "weekly-review",
    "url": "https://example.com/trigger/1"
  },
  "owner": "swe:alice",
  "inputs": [
    {
      "name": "scope",
      "value": "billing"
    }
  ],
  "decision": "Adopt variant A behind feature flag.",
  "evidence": [
    "https://example.com/pr/1"
  ],
  "review": {
    "cadence": "quarterly",
    "next_review_at": "2026-08-22"
  }
}
```

### `templates/llm-arch-audit.sh`

```bash
# llm-arch-audit.sh — Find files violating LLM-friendly architecture limits.
# Usage: bash llm-arch-audit.sh [src-dir] [line-limit]
# Input:  source directory (default: src), line limit (default: 250)
# Output: files exceeding limit (sorted by size desc), barrel re-export files

DIR=${1:-src}
LIMIT=${2:-250}

echo "=== Files exceeding ${LIMIT} lines in ${DIR} ==="
find "$DIR" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) \
  | while read -r f; do
      lines=$(wc -l < "$f")
      if [ "$lines" -gt "$LIMIT" ]; then
        echo "$lines  $f"
      fi
    done \
  | sort -rn

echo ""
echo "=== Barrel re-exports (agent navigation traps) ==="
if command -v rg &>/dev/null; then
  rg --glob "*.ts" "^export \* from" "$DIR" -l
else
  grep -rl "^export \* from" "$DIR" --include="*.ts"
fi
```
