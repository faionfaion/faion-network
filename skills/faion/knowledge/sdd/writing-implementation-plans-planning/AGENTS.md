# Writing Implementation Plans

## Summary

**One-sentence:** Generates implementation-plan.md from an Accepted design — WBS, dependency graph, wave shards, per-task token budgets, critical path, risk + test + rollout strategy.

**One-paragraph:** Bridges design.md (AD-X decisions + file table) and executor-ready TASK files. The 11-phase writing process: load SDD context → check prerequisites → WBS → dependency graph → wave analysis → phase definition → task format → critical path → risk assessment → testing strategy → rollout strategy. Output is implementation-plan.md (Accepted). The plan rows become the input to `template-task` for per-task file authoring.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'implementation-plan authoring' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Accepted design.md exists for the feature (status: Accepted).
- The feature has ≥3 interacting components OR sequencing matters.
- Multiple waves of parallel work are possible OR critical-path matters.
- The plan will be consumed by automated agents that need ordered, sharded inputs.

## Skip If (ANY kills it)

- Feature has fewer than 3 tasks — skip the plan, write TASK files directly.
- Spec or design doc is still Draft — writing the plan too early wastes tokens when requirements shift.
- Bug fixes — use a single TASK file.
- Exploratory spikes — plans assume known solutions; spikes discover the solution.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Accepted design.md | markdown | `.aidocs/features/<status>/<feature>/design.md` |
| Accepted spec.md (for FR-X back-trace) | markdown | `.aidocs/features/<status>/<feature>/spec.md` |
| Repo testing convention | markdown | repo testing guide |
| Existing implementation-plan template | shell | `templates/create-tasks.sh` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/workflow-design-phase` | Provides the Accepted design.md this plan consumes. |
| `solo/sdd/sdd-planning/template-task` | Downstream consumer that renders each plan row into a TASK file. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the implementation-plan.md + valid/invalid/forbidden examples | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 11-step procedure: load context → WBS → deps → waves → phases → tasks → critical path → risk → testing → rollout → review | ~1100 |
| `content/05-examples.xml` | medium | Worked example: implementation-plan.md for the JWT refresh feature | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposition` | sonnet | Mechanical mapping of file_table to atomic tasks. |
| `dependency-graph` | opus | Multi-task ordering + critical-path reasoning. |
| `wave-shard` | sonnet | Bin-pack tasks into waves respecting deps + token budgets. |
| `risk-and-rollout` | opus | Cross-task risk synthesis + rollout strategy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-tasks.sh` | Bash helper that stubs empty TASK_*.md files for a wave. |
| `templates/implementation-plan.md.j2` | Canonical implementation-plan.md skeleton with WBS, dep graph, waves, critical path, risk, testing, rollout sections. |
| `templates/implementation-plan.md` | Canonical implementation-plan.md skeleton with WBS, dep graph, waves, critical path, risk, testing, rollout sections. Generated from `templates/implementation-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[workflow-design-phase]]
- [[template-task]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (design Accepted, task count ≥3, sequencing matters) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether to run the full planning phase or shard tasks directly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/create-tasks.sh`

```bash
#
# create-tasks.sh — create empty TASK_*.md stubs for a wave
# Usage: create-tasks.sh FEATURE_DIR TASK_IDS...
# Example: create-tasks.sh .aidocs/features/in-progress/user-auth 001 002 003

FEATURE_DIR="${1:?Usage: create-tasks.sh feature-dir task-id [task-id ...]}"
shift

mkdir -p "$FEATURE_DIR/todo"

for id in "$@"; do
  FILE="$FEATURE_DIR/todo/TASK_${id}.md"
  if [ -f "$FILE" ]; then
    echo "SKIP $FILE (already exists)"
    continue
  fi
  cat > "$FILE" << EOF
# TASK_${id}: {Title in Imperative Voice}

**Phase:** {N}
**Wave:** {N}

**Description:**
{2-3 sentences: what needs to be done}

**Traces to:**
- AD-{N}: {architectural decision text}
- FR-{N}: {requirement text}

**Depends on:** None

**Blocks:** {TASK_NNN or "None"}

**Complexity:** simple | normal | complex
**Context Estimate:** ~{X}k tokens

**Acceptance Criteria:**
- [ ] {Specific observable outcome}
- [ ] {Another specific criterion}

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | \`{path}\` | {purpose} |

**Technical Notes:**
{Fill after Wave N-1 execution}

**Tests:**
- [ ] Unit: {description}
- [ ] Integration: {description}
EOF
  echo "Created $FILE"
done
```
