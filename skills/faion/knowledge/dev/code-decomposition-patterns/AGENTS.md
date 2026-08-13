# Code Decomposition Patterns

## Summary

**One-sentence:** Pattern-matches a source file's bloat against five canonical decomposition shapes and emits the move list a refactor agent executes.

**One-paragraph:** When a file crosses ~300 lines or ~10k tokens, the question is not 'should we split' but 'which pattern fits the shape of the bloat'. This methodology recognises five canonical patterns: Extract Service (stateful + I/O), Extract Component (UI), Extract Module (pure logic), Extract Configuration (constants tables), Extract Types (type-only declarations). For each it gives the trigger, the cut points, and a language-specific layout (Python / TypeScript / Go). Output is a concrete move list — source paths + line ranges + destination paths — that a refactor agent or developer applies one move at a time with green tests between.

**Ефективно для:**

- Файли &gt;300 рядків з очевидною мікс-логікою: декомпозиція по патерну дешевша за повний rewrite.
- Команди, що мігрують monorepo з 'one big module' на доменно-розрізаний код.
- AI-агенти, що мають детермінований перелік 'що в що рухаємо' замість 'reorganize this file'.
- Code-review гейт: рев'юер ловить 'wrong pattern picked' до того, як refactor мерджиться.

## Applies If (ALL must hold)

- A source file exceeds 300 lines OR ~10k tokens.
- The file mixes responsibilities (≥2 of: I/O, pure logic, UI, types, constants).
- The repo has a working test suite that can run between moves.

## Skip If (ANY kills it)

- File is generated / vendored — splitting fights upstream regenerate.
- File is a deliberate facade (re-exports) — splitting breaks the public API.
- Test suite is broken — moves without green tests turn one refactor into a debugging marathon.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source file path | absolute | repo working tree |
| LOC + token count | integer | wc -l + tokenizer |
| Test command | shell | repo README / CI |
| Public API surface | list of exports | static analysis or grep |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pattern-match-first, move-with-tests, preserve-history, atomic-moves, public-api-stable | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for move-list artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: wrong-pattern, bulk-move, broken-imports, lost-history | 700 |
| `content/04-procedure.xml` | essential | 5-step pattern-pick → move-list → execute → verify procedure | 800 |
| `content/06-decision-tree.xml` | essential | Routing on file shape → one of five patterns | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_pattern` | haiku | Pattern match on imports + symbol kinds; deterministic. |
| `draft_move_list` | sonnet | Per-symbol judgement of destination; bounded by detected pattern. |
| `verify_moves` | haiku | Run test command; deterministic pass/fail. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-guard.sh` | Shell guard that checks file size + symbol mix before allowing a decomposition refactor |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-decomposition-patterns.py` | Validate a move-list artefact against the schema | After draft_move_list, before execute |

## Related

- - [[code-decomposition-principles]] — the size + SRP principles this methodology encodes as patterns.
- - [[refactoring-patterns]] — the catalog of low-level moves each pattern compiles to.

## Decision tree

See `content/06-decision-tree.xml`. The tree asks first 'does this file have I/O?' → if yes, Extract Service. Otherwise it asks 'is it UI?' → Extract Component. 'Pure logic?' → Extract Module. 'Constants table?' → Extract Configuration. 'Types only?' → Extract Types. Each leaf references a rule from `01-core-rules.xml` and points at the procedure for that pattern.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pattern-guard.sh`

```bash
#!/usr/bin/env bash
# pattern-guard.sh — enforce decomposition pattern invariants post-refactor.
# Usage: ./pattern-guard.sh [path]
# Checks: view line counts (Extract Service), component line counts (Extract Component),
#         settings file size (Extract Configuration), circular imports.
set -euo pipefail
ROOT="${1:-.}"
MAX_VIEW=120
MAX_COMPONENT=200
MAX_SERVICE=300
MAX_CONFIG=150

FAIL=0

# Views must be thin (Extract Service)
while IFS= read -r f; do
  n=$(wc -l < "$f")
  if [ "$n" -gt "$MAX_VIEW" ]; then
    echo "FAIL: $f: $n lines (> $MAX_VIEW) — apply Extract Service"
    FAIL=$((FAIL + 1))
  fi
done < <(find "$ROOT" -path '*/views/*' -name '*.py' 2>/dev/null)

# React components capped (Extract Component)
while IFS= read -r f; do
  n=$(wc -l < "$f")
  if [ "$n" -gt "$MAX_COMPONENT" ]; then
    echo "FAIL: $f: $n lines (> $MAX_COMPONENT) — apply Extract Component"
    FAIL=$((FAIL + 1))
  fi
done < <(find "$ROOT/src/components" -name '*.tsx' 2>/dev/null)

# Settings split (Extract Configuration)
if [ -f "$ROOT/settings.py" ]; then
  n=$(wc -l < "$ROOT/settings.py")
  if [ "$n" -gt "$MAX_CONFIG" ]; then
    echo "FAIL: settings.py: $n lines (> $MAX_CONFIG) — extract per-env"
    FAIL=$((FAIL + 1))
  fi
fi

# Circular imports
if command -v madge >/dev/null 2>&1; then
  madge --circular "$ROOT/src" 2>/dev/null || true
fi
if command -v pydeps >/dev/null 2>&1; then
  pydeps --show-cycles "$ROOT" 2>/dev/null || true
fi

if [ "$FAIL" -gt 0 ]; then
  echo "$FAIL invariant(s) violated"
  exit 1
fi
echo "OK"
```
