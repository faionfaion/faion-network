# Refactoring Patterns

## Summary

**One-sentence:** Maps a code smell to one of eight canonical refactor transforms and emits an atomic-move plan executed with green tests between every move.

**One-paragraph:** Refactoring without a named transform is editing; one-name-per-move forces discipline. This methodology recognises eight transforms (Extract Function, Inline Function, Extract Variable, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Number with Constant, Decompose Conditional, Rename) and routes each code smell to its canonical transform. Output is an atomic-move plan: one transform per commit, tests green between, no behaviour change. Behaviour change rides a separate PR.

**Ефективно для:**

- Local refactor (function-scale): від smell до плану за один прогон.
- AI-driven refactor: агент має детермінований enum 'що саме робити', не 'just refactor this'.
- Code-review: рев'юер ловить 'wrong transform picked'.
- Учбовий контекст: каталог 8 трансформів — карта Fowler-канона без 400-сторінкової книги.

## Applies If (ALL must hold)

- Code smell is local (one function / one file / one class).
- Test suite is green at the start.
- Behaviour change is NOT planned in the same PR.

## Skip If (ANY kills it)

- Smell is architectural — different methodology (decomposition-patterns).
- Tests are red — fix tests first.
- Behaviour change is intended — refactor + change in one PR is the classic anti-pattern.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source file + line range | absolute path + lines | smell location |
| Code-smell description | Markdown | reviewer comment or static analysis |
| Test command | shell | repo CI config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: one-transform-per-commit, tests-green-between, no-behaviour-change, named-transform, atomic-rename-via-tool | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for atomic-move plan | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: refactor-and-fix, multi-transform-commit, manual-rename, untested-extract | 700 |
| `content/04-procedure.xml` | essential | 5-step refactor loop procedure | 800 |
| `content/06-decision-tree.xml` | essential | Smell → transform picker tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_smell` | sonnet | Per-file judgement; picks transform from catalog. |
| `draft_plan` | sonnet | Sequences transforms; checks dependencies. |
| `execute_loop` | haiku | Per-step apply + test; deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/planner-prompt.txt` | Prompt that turns a smell into a transform plan |
| `templates/refactor-loop.sh` | Shell loop: apply transform → run tests → commit |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- - [[code-decomposition-patterns]] — file-scale; this methodology is function-scale.
- - [[code-coverage]] — coverage data identifies smells with low-coverage cliffs.

## Decision tree

See `content/06-decision-tree.xml`. Branches: smell category (long function / complex conditional / magic value / duplicated code / inappropriate name / large parameter list) → canonical transform.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/planner-prompt.txt`

```text
Pick exactly ONE refactoring pattern from this closed catalog:
[extract-method, extract-class, replace-conditional-with-polymorphism,
 introduce-parameter-object, replace-magic-numbers, decompose-conditional,
 rename-for-clarity, move-method].

Apply it to:
<code>
{{CODE}}
</code>

Constraints:
- Behavior preservation is mandatory. Cite which test(s) verify the affected code.
- Do not apply replace-conditional-with-polymorphism for fewer than 4 distinct branches.
- Do not rename exported public API symbols without adding a deprecation alias.
- Output JSON only:
  {
    "pattern": "<pattern-name>",
    "justification": "<one sentence why this pattern, not another>",
    "unified_diff": "<git diff format>",
    "test_command": "<command to verify>"
  }
- If no catalog pattern fits cleanly, return:
  {"pattern": null, "reason": "<why no pattern applies>"}
```

### `templates/refactor-loop.sh`

```bash
#!/usr/bin/env bash
# refactor-loop.sh — apply one refactoring pattern, test, commit, repeat.
# Usage: refactor-loop.sh <target-file> <test-command> [max-iterations]
# Example: refactor-loop.sh src/payments.py "pytest tests/test_payments.py" 5
set -euo pipefail

TARGET="${1:?path required}"
TESTS="${2:?test command required}"
MAX="${3:-5}"

for i in $(seq 1 "$MAX"); do
  echo "=== Iteration $i ==="
  PLAN=$(claude -p "Pick exactly ONE refactoring pattern from this catalog: \
[extract-method, extract-class, replace-conditional-with-polymorphism, \
introduce-parameter-object, replace-magic-numbers, decompose-conditional, \
rename-for-clarity, move-method]. \
Apply it to: $(cat "$TARGET") \
Constraints: \
- Behavior preservation is mandatory. Cite which test(s) verify the affected code. \
- Output JSON: {\"pattern\": \"...\", \"justification\": \"...\", \"unified_diff\": \"...\", \"test_command\": \"...\"}. \
- If no catalog pattern fits cleanly, return {\"pattern\": null, \"reason\": \"...\"}.")

  PATTERN=$(echo "$PLAN" | jq -r '.pattern')
  [ "$PATTERN" = "null" ] && { echo "No more refactors available."; break; }

  echo "Applying: $PATTERN"
  echo "$PLAN" | jq -r '.unified_diff' | git apply --3way

  if eval "$TESTS"; then
    git add -A
    git commit -m "refactor: $PATTERN in $(basename "$TARGET")"
    echo "Committed: $PATTERN"
  else
    git checkout -- .
    echo "Reverted: $PATTERN broke tests"
    break
  fi
done
```
