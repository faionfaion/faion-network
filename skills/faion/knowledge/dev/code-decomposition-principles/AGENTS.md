# Code Decomposition Principles

## Summary

**One-sentence:** Audits a file against the three decomposition principles (size, single-responsibility, LLM-context fit) and emits a decision record: split / leave / merge.

**One-paragraph:** A file is decomposable when three signals align: LOC > 300 / tokens > 10k, multiple responsibilities, and frequent churn against unrelated callers. This methodology audits each candidate file, emits a decision record with the triggering signals + the proposed action, and feeds candidates into `code-decomposition-patterns` for the actual move list. Output is a decision record (markdown frontmatter or JSON) — versioned, owner-named, reviewable. Anti-pattern: splitting because it 'feels big'.

**Ефективно для:**

- Аудит monorepo на decomposition candidates: ranking за churn + size — топ-10 кандидатів за один прохід.
- Code-review: рев'юер має детермінований чек 'чи варто розбивати'.
- Onboarding: новий розробник бачить, які файли planned-to-split (decision = split + status=queued).
- LLM-context tuning: файли &gt;10k токенів дражать context-window; рішення = split &lt;5k шматків.

## Applies If (ALL must hold)

- Repo has files ≥300 LOC OR ≥10k tokens (candidate pool exists).
- Working git history (≥3 months) so churn can be measured.
- A reviewer / owner can act on the decision record.

## Skip If (ANY kills it)

- Repo is &lt;500 files total — overhead beats payoff.
- Greenfield prototype where files will be rewritten before they stabilise.
- Files are auto-generated.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| File path list | newline-separated | find . -name '*.py' -size +5k |
| Git churn data | json | git log --pretty=format per file |
| Token counts | integer | tiktoken / tokenizer on file content |
| Responsibility map | tags per file | static analysis or AGENTS.md docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: size-trigger, srp-detector, churn-signal, llm-fit, owner-named | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision record | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: split-by-feeling, ignore-churn, decompose-and-rewrite, no-owner | 700 |
| `content/04-procedure.xml` | essential | 5-step audit procedure | 700 |
| `content/06-decision-tree.xml` | essential | split / leave / merge tree | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan_candidates` | haiku | Static metrics: LOC, tokens, churn — deterministic. |
| `classify_responsibilities` | sonnet | Per-file judgment of which responsibilities exist; needs context. |
| `draft_decision_record` | sonnet | Synthesises signals into a one-page record. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-candidates.sh` | Shell scan that lists files crossing decomposition thresholds |
| `templates/planner-prompt.txt` | LLM prompt that turns scan output into a decision record |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-decomposition-principles.py` | Validate a decision record against the schema | After draft_decision_record, before posting to PR / owner |

## Related

- - [[code-decomposition-patterns]] — once a file is decided 'split', pick the pattern.
- - [[refactoring-patterns]] — low-level transforms inside each split.

## Decision tree

See `content/06-decision-tree.xml`. Tree branches: size threshold met? → responsibilities ≥2? → churn high vs. unrelated? Leaves: split (highest-confidence candidate), leave (one signal only), merge (file is unusually small but always edited with a sibling).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decomp-candidates.sh`

```bash
#!/usr/bin/env bash
# decomp-candidates.sh — surface files that likely need splitting.
# Emits: oversize files, high-complexity functions, high-churn hotspots.
# Usage: decomp-candidates.sh [src-dir] [line-threshold] [complexity-threshold]
set -euo pipefail

ROOT="${1:-.}"
THRESHOLD_LINES="${2:-300}"
THRESHOLD_CCN="${3:-15}"

echo "## Oversize files (> ${THRESHOLD_LINES} lines)"
find "$ROOT" -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' \
  -o -name '*.js' -o -name '*.go' \) \
  | xargs wc -l 2>/dev/null \
  | awk -v t="$THRESHOLD_LINES" '$1 > t && $2 != "total" {printf "%6d  %s\n", $1, $2}' \
  | sort -rn | head -30

echo ""
echo "## High-complexity functions (CCN > ${THRESHOLD_CCN})"
if command -v lizard >/dev/null 2>&1; then
  lizard -C "$THRESHOLD_CCN" "$ROOT" 2>/dev/null | tail -n +3 | head -20
else
  echo "  lizard not installed: pip install lizard"
fi

echo ""
echo "## Hotspots (high churn × large file — last 6 months)"
git -C "$ROOT" log --since='6 months ago' --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|go)$' \
  | sort | uniq -c | sort -rn | head -15
```

### `templates/planner-prompt.txt`

```text
Plan a decomposition of {{FILE_PATH}}.

Steps:
1. List current responsibilities (one bullet per distinct concern).
2. Propose a target file tree. Constraints:
   - Max 200 lines per file.
   - Min 30 lines per file (no micro-files).
   - No export * barrel re-exports.
   - Use git mv semantics (preserve history).
3. Order the moves so tests stay green after each step.
4. List import sites that must be updated per move.

Output JSON only:
{
  "responsibilities": ["<concern 1>", ...],
  "target_tree": [
    {"file": "<path>", "responsibility": "<one sentence>", "est_lines": <int>}
  ],
  "moves": [
    {"step": <int>, "from": "<path>", "to": "<path>",
     "what": "<description>", "import_sites": ["<file:approx-line>"]}
  ]
}

Do not begin executing. Wait for explicit human approval before any file edits.
```
