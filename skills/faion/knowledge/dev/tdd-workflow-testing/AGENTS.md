# TDD Workflow

## Summary

**One-sentence:** Produces a TDD-workflow config (per-behavior RED-GREEN-REFACTOR cycle, PostToolUse hook, CLAUDE.md snippet) for LLM-assisted development.

**One-paragraph:** LLMs naturally skip the RED step — they write implementation and tests together, producing tests that prove the implementation rather than specify behavior. This methodology emits a per-behavior loop script, a PostToolUse hook that auto-runs pytest after a file write, and a CLAUDE.md snippet that pins the discipline. Result: failing test first, minimal implementation second, refactor third — verifiable in CI.

**Ефективно для:** solopreneur using Claude Code who keeps catching themselves letting the model write tests after the implementation lands.

## Applies If (ALL must hold)

- Starting a new feature or module where behavior is well-defined.
- Writing business logic where correctness is critical.
- Enforcing RED-step discipline when an agent tends to skip it.
- Setting up PostToolUse hooks for TDD enforcement.

## Skip If (ANY kills it)

- Exploratory spikes or prototypes where spec is unknown.
- UI/layout work — visual feedback drives design.
- Performance optimization — benchmark-driven, not test-driven.
- Throwaway scripts with no production use.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `behavior-list.yaml` | list of {behavior, signature, happy_path, edge_cases} | operator |
| `test_command` | string (e.g., `pytest tests/test_x.py -x`) | repo |
| `claude_md_path` | path | repo |
| `settings_json_path` | path (Claude Code settings.json) | user config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[testing-pytest]] | RED-GREEN cycle assumes pytest semantics. |
| [[code-review-basics]] | Refactor step uses review heuristics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: RED before GREEN, one behavior per cycle, minimal GREEN, no behavior change in REFACTOR, commit test+impl together, no TDD on UI/spike. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tdd-workflow-config artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: write tests after, batch behaviors, generalize too early, add behavior in REFACTOR, skip the failing-run step. | ~800 |
| `content/04-procedure.xml` | recommended | 7-step per-behavior loop (write RED → run RED → write GREEN → run all → refactor → run all → commit). | ~700 |
| `content/05-examples.xml` | recommended | One worked behavior end-to-end + sample CLAUDE.md snippet + PostToolUse hook JSON. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks TDD vs spike-first vs benchmark-driven based on behavior_known + visual_feedback_drives. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_behavior_list` | haiku | Mechanical YAML→typed list. |
| `prioritize_behaviors` | sonnet | Sequencing happy path vs edge cases. |
| `audit_for_red_skip` | opus | Detecting silent test-after-implementation in agent transcripts. |
| `emit_workflow_config` | sonnet | Mechanical JSON emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/tdd-cycle.sh` | Shell script: run failing test → implement → run passing test → prompt refactor. |
| `templates/claude-md-snippet.md.j2` | TDD-discipline reminder block to append to CLAUDE.md. |
| `templates/claude-md-snippet.md` | TDD-discipline reminder block to append to CLAUDE.md. Generated from `templates/claude-md-snippet.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/posttool-hook.json` | Settings.json fragment that runs pytest after Write/Edit on test_*.py. |
| `templates/_smoke-test.yaml` | Minimum behavior list (one happy path). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-pytest]]
- [[unit-testing]]
- [[code-review-basics]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `behavior_known` (no → spike-first, then tests; yes → continue), then on `visual_feedback_drives` (yes → screenshot-driven, defer TDD; no → continue), then on `performance_dominant` (yes → benchmark-driven; no → strict RED-GREEN). Each leaf cites a rule id.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tdd-cycle.sh`

```bash
# tdd-cycle.sh — guided TDD cycle for a single behavior
#
# Usage:
#   ./tdd-cycle.sh "test_command" "impl_file"
#
# Example:
#   ./tdd-cycle.sh "pytest tests/test_cart.py::test_discount -x" "src/cart.py"
#
# The script walks you through RED → GREEN → REFACTOR with confirmation prompts.

set -euo pipefail

TEST_CMD="${1:-pytest -x --tb=short}"
IMPL_FILE="${2:-}"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

confirm() {
    local msg="$1"
    echo -e "${YELLOW}${msg}${RESET}"
    read -rp "Press Enter when ready... " _
}

echo "=============================="
echo "  TDD Cycle"
echo "=============================="
echo ""

# ---- RED ----
echo -e "${RED}[RED] Write a failing test for ONE behavior.${RESET}"
echo "     Test file should NOT pass yet — implementation does not exist."
echo ""
confirm "When done writing the test, press Enter to run it."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${RED}WARNING: Test PASSED without implementation.${RESET}"
    echo "This means the test is testing nothing, or the behavior already exists."
    echo "Review your test before proceeding."
    exit 1
else
    echo ""
    echo -e "${GREEN}Good — test is FAILING as expected (RED).${RESET}"
fi

echo ""

# ---- GREEN ----
echo -e "${GREEN}[GREEN] Write minimal implementation to make the test pass.${RESET}"
if [[ -n "$IMPL_FILE" ]]; then
    echo "     Edit: $IMPL_FILE"
fi
echo "     Do NOT add features beyond what the failing test requires."
echo ""
confirm "When done writing implementation, press Enter to run tests."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${GREEN}All tests PASS (GREEN).${RESET}"
else
    echo ""
    echo -e "${RED}Tests still FAILING.${RESET}"
    echo "Fix the implementation until all tests pass, then re-run this script."
    exit 1
fi

echo ""

# ---- REFACTOR ----
echo -e "${YELLOW}[REFACTOR] Improve code quality without changing behavior.${RESET}"
echo "     - Extract functions, rename variables, remove duplication"
echo "     - Do NOT add new behavior here — start a new RED cycle for that"
echo ""
confirm "When done refactoring (or if no refactor needed), press Enter to verify."

echo ""
echo "Running: $TEST_CMD"
echo ""
if $TEST_CMD 2>&1; then
    echo ""
    echo -e "${GREEN}All tests PASS after refactor.${RESET}"
    echo ""
    echo "=============================="
    echo -e "${GREEN}TDD cycle complete.${RESET}"
    echo "Commit test + implementation together, then start next RED cycle."
    echo "=============================="
else
    echo ""
    echo -e "${RED}Tests broke during refactor.${RESET}"
    echo "Revert refactor changes until tests pass again."
    exit 1
fi
```

### `templates/posttool-hook.json`

```json
{
  "_header": {
    "purpose": "Claude Code PostToolUse hook auto-running pytest on test file writes",
    "consumes": "Write/Edit tool events targeting test_*.py paths",
    "produces": "pytest -x --tb=short output appended to the conversation",
    "depends-on": "pytest installed; tests/ dir resolvable",
    "token-budget-impact": "hook adds ~200 tokens per write of a test file"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'p=$(jq -r \".tool_input.file_path // empty\" <<<\"$CLAUDE_TOOL_INPUT\"); case \"$p\" in *test_*.py) pytest \"$p\" -x --tb=short 2>&1 | tail -40 ;; esac'"
          }
        ]
      }
    ]
  }
}
```

### `templates/_smoke-test.yaml`

```yaml
behaviors:
  - behavior: register-issues-token
    signature: "register(email: str) -> str"
    happy_path: "returns 32-hex-char token"
    edge_cases: []

drivers:
  behavior_known: true
  visual_feedback_drives: false
  performance_dominant: false

test_command: "pytest tests -x --tb=short"
claude_md_path: CLAUDE.md
settings_json_path: .claude/settings.json
```
