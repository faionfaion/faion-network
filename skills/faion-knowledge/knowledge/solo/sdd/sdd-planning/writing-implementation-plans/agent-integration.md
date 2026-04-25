# Agent Integration — Writing Implementation Plans

## When to use
- Design doc is finalized (Accepted status) and the feature is promoted to `todo/` or `in-progress/`
- Feature has 3+ components that interact; sequencing matters
- Multiple waves of parallel tasks are possible (API before frontend, schema before service layer)
- Handoff is needed between agents or sessions — impl-plan is the coordination artifact
- Task scope is large enough to exceed 100k tokens in one pass

## When NOT to use
- Feature has fewer than 3 tasks — skip the plan, write TASK files directly
- Spec or design doc is still in draft; writing impl-plan too early wastes tokens when requirements shift
- Bug fixes: use a single TASK file, not a full implementation plan
- Exploratory spikes: impl-plans assume known solutions; spikes discover the solution

## Where it fails / limitations
- Wave sequencing breaks if dependency graph has cycles — agent may miss circular deps without explicit prompting
- 100k token rule applies per agent session, not per file; large codebases can exceed this even for "small" tasks
- Critical path analysis requires accurate effort estimates; agents produce estimates that need human review
- Rollout strategy section is often generated as generic; must be customized for the actual deployment topology

## Agentic workflow
The `faion-sdd-executor-agent` uses the implementation plan as its primary coordination document: it reads the wave list, executes tasks in Wave 1 (parallel-safe), confirms success criteria, then proceeds to Wave 2. Each TASK_*.md file is created before execution begins for that wave. Token budget per task is declared in the impl-plan and enforced at task creation time. Human review is required between waves when wave N has a "human checkpoint" marker.

### Recommended subagents
- `faion-sdd-executor-agent` — primary consumer; reads impl-plan to drive sequential/parallel task execution
- Planning subagent (claude-opus-4-7) — writes the impl-plan from spec.md + design.md; requires full SDD context

### Prompt pattern
```
Read {feature}/spec.md and {feature}/design.md.
Extract all AD-X decisions and FR-X requirements.
Write implementation-plan.md following the structure in impl-plan-components.md:
- prerequisites
- dependency graph (text-based, no ASCII art)
- waves (parallel-safe groupings)
- per-task token budget (must not exceed 100k each)
- risk assessment
- rollout strategy
Do NOT write TASK files yet — output the plan only.
```

```
Given implementation-plan.md Wave 1, create TASK_001.md and TASK_002.md.
Each task must include: objective, files to modify (CREATE/MODIFY), acceptance criteria, token budget.
INVEST validation: each task must be Independent, Small (fits 100k), Testable.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `make` | Orchestrate wave-based task execution via Makefile targets | system / https://www.gnu.org/software/make/ |
| `gh` (GitHub CLI) | Create GitHub Issues per task from impl-plan programmatically | `brew install gh` / https://cli.github.com |
| `jq` | Parse impl-plan JSON exports for dependency graph processing | `apt install jq` / https://stedolan.github.io/jq/ |
| `dot` (Graphviz) | Render dependency graph from DOT notation for review | `brew install graphviz` / https://graphviz.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Projects | SaaS | Yes — GraphQL API | Tasks become Issues; impl-plan waves map to milestones |
| Linear | SaaS | Yes — REST + GraphQL | Best for wave tracking via cycle/sprint fields |
| Notion | SaaS | Yes — REST API | Can host impl-plan as linked database with task pages |
| Shortcut (Clubhouse) | SaaS | Yes — REST API | Stories per task; epics per wave |

## Templates & scripts
See `impl-plan-components.md` for the full template and `impl-plan-examples.md` for real examples (3, 7, 12 task features).

Inline — create stub TASK files from an impl-plan task list:
```bash
#!/usr/bin/env bash
# create-tasks.sh — create empty TASK_*.md stubs from a list
# Usage: echo "001 002 003" | bash create-tasks.sh {feature_dir}
FEATURE_DIR="${1:?Usage: $0 feature_dir}"
for id in $2; do
  FILE="$FEATURE_DIR/todo/TASK_$id.md"
  if [ ! -f "$FILE" ]; then
    cat > "$FILE" <<EOF
# TASK_$id: [Title]

## Objective
[What this task accomplishes]

## Files
- MODIFY: []
- CREATE: []

## Acceptance Criteria
- [ ] 

## Token Budget
Est. tokens: ~
EOF
    echo "Created $FILE"
  fi
done
```

## Best practices
- Write impl-plan only after design.md is reviewed and at `Accepted` status
- Declare token budget per task in the impl-plan before creating TASK files — prevents scope creep mid-execution
- Use "Finish-to-Start" dependency notation explicitly (e.g., "TASK-003 depends on TASK-001 complete")
- Wave 1 should always contain only tasks with no dependencies — agents can run them in parallel
- Include a "rollback trigger" in the rollout strategy: which metric or error rate causes a rollback
- Reference `features/done/` for completed impl-plans as patterns before writing a new one
- Mark the critical path explicitly — agents will optimize for parallelism but may miss the longest chain

## AI-agent gotchas
- Agents conflate "design phase" and "implementation planning"; keep prompts scoped to one phase at a time
- 100k token rule applies to the agent session context, not just the task file — include codebase file reads in the budget
- Agents will skip risk assessment unless the prompt explicitly requires it with "list at least 3 risks"
- Wave boundaries are a human-in-loop checkpoint in multi-agent pipelines; one agent's output becomes the next agent's input
- If impl-plan and design.md contradict each other, agents will silently follow impl-plan — always reconcile before execution
- Token estimates in impl-plans are order-of-magnitude only; actual sessions can run 2-3x over

## References
- https://www.pmi.org/learning/library/critical-path-method-schedule-control-6879 — PMI Critical Path Method
- https://www.workbreakdownstructure.com/ — WBS methodology
- https://www.scaledagileframework.com/pi-planning/ — PI Planning for wave-based release planning
- https://www.atlassian.com/agile/project-management/estimation — Agile estimation practices
- impl-plan-100k-rule.md — 100k token rule and WBS (local reference)
- impl-plan-components.md — full document structure (local reference)
