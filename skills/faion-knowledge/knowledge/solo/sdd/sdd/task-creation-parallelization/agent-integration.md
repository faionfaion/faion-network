# Agent Integration — Task Creation & Parallelization

## When to use
- Decomposing an approved `design.md` into executable `TASK-XXX-*.md` files before execution begins
- Planning wave-based parallel execution to achieve 2-4x throughput on independent tasks
- Checking that each task fits the 100k token context budget before handing it to an execution agent
- Propagating patterns discovered in early waves (Wave 1) into later-wave task context
- Managing dependencies: a task that requires output from two other tasks must wait for both to complete (not just one)

## When NOT to use
- Feature is a single-task implementation (< 30k tokens) — one task, no waves needed
- Design doc is not yet approved — don't decompose into tasks while spec is still changing
- Tasks are unknown until runtime (e.g., data-driven pipelines) — decomposition cannot be done upfront
- Experimental/spike work where implementation approach is undefined — discover first, decompose after

## Where it fails / limitations
- Token estimates (30k/60k/100k buckets) are approximations; actual context usage can exceed estimates by 30-50% when loading dependent code
- Wave dependencies modeled in markdown files are not machine-enforced — an execution agent can pick up a Wave 2 task before Wave 1 is complete if the todo/ directory isn't checked carefully
- Pattern propagation between waves requires explicit "dependency summary" sections in task files; without them, each agent starts fresh and produces inconsistent patterns
- Taskmaster AI / claude-task-master complexity scores (1-10) are heuristic; very thin tasks still require human validation of the decomposition
- Parallel execution in git worktrees creates merge conflicts if tasks touch overlapping files — task boundaries must be defined at the file level, not just feature level

## Agentic workflow
A decomposition agent reads `design.md` and `implementation-plan.md`, then generates `TASK-XXX-*.md` files in `todo/` using the INVEST criteria and 100k token rule. It outputs a wave dependency graph. An orchestrating agent then launches Wave 1 tasks as parallel sub-agents (one per task), waits for all Wave 1 completions, collects their summaries, injects those summaries into Wave 2 task context, and launches Wave 2. The orchestrator, not the execution agents, manages wave sequencing.

### Recommended subagents
- `faion-task-executor-agent` — the decomposition step is part of its impl-plan phase
- `faion-feature-executor` skill — executes tasks sequentially with quality gates (use when parallel orchestration isn't set up)
- Claude Code with `isolation: "worktree"` — runs each task in an isolated git worktree for parallel execution without conflicts

### Prompt pattern
```
You are a task decomposition agent. Input: design.md (attached).
Output: a list of TASK-XXX-*.md files following the template in templates.md.
Rules:
1. Each task must fit in 100k tokens (estimate: code_to_read + code_to_write + context)
2. Mark wave number and dependencies for each task
3. Apply INVEST: each task must be Independent within its wave
4. Never combine "research how" and "implement" in one task
Output the wave dependency graph as a markdown table before generating tasks.
```

```
Wave transition: Wave 1 complete. Collecting summaries.
For each completed TASK in Wave 1: read its execution report, extract:
- Key patterns established
- Files created/modified
- Critical code snippets (10 lines max each)
Inject these summaries into the "Task Dependency Tree" section of each Wave 2 task.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git worktree` | Isolated parallel task execution | `git help worktree` |
| `claude` (Claude Code CLI) | Execute tasks with task file as context | https://docs.anthropic.com/en/docs/claude-code |
| `task-master` (claude-task-master) | PRD → task decomposition, complexity scoring | https://github.com/eyaltoledano/claude-task-master |
| `cursor` | Plan Mode for decomposition research | https://cursor.so |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Taskmaster AI | SaaS | Yes | Automatic PRD-to-task with complexity 1-10 scoring, MCP integration |
| Claude Task Master | OSS | Yes | Open source version; GitHub-based; supports Claude Code, Cline, Cursor |
| Linear | SaaS | Partial | Mirror wave plan to issue tracker via API; no automatic wave enforcement |
| GitHub Projects | SaaS | Partial | Use Kanban columns for todo/in-progress/done per wave |

## Templates & scripts
See `templates.md` for `TASK-XXX-*.md` template with INVEST fields, token estimate, wave number, and dependency tree section.

Wave orchestration script (inline):
```bash
#!/usr/bin/env bash
# run-wave.sh <wave_number> <feature_dir>
# Launches all tasks in a wave as parallel Claude Code sessions
set -euo pipefail
WAVE=$1
FEATURE_DIR=$2
TASKS=$(grep -l "wave: $WAVE" "$FEATURE_DIR/todo/TASK-"*.md 2>/dev/null || true)
if [ -z "$TASKS" ]; then
  echo "No tasks for wave $WAVE in $FEATURE_DIR"
  exit 0
fi
PIDS=()
for TASK in $TASKS; do
  TASK_NAME=$(basename "$TASK" .md)
  BRANCH="task/$TASK_NAME"
  git worktree add "../worktrees/$TASK_NAME" -b "$BRANCH" 2>/dev/null || true
  (
    cd "../worktrees/$TASK_NAME"
    claude --task "$TASK" --non-interactive > "logs/$TASK_NAME.log" 2>&1
  ) &
  PIDS+=($!)
done
for PID in "${PIDS[@]}"; do wait "$PID"; done
echo "Wave $WAVE complete."
```

## Best practices
- Split tasks at file boundaries, not feature boundaries — two tasks editing the same file will conflict in parallel execution
- Include a "Pattern Dependency" section in each task that summarizes what prior tasks established (naming conventions, error handling patterns, shared utilities) — prevents each agent from reinventing them
- The "one focus" rule: planning tasks produce only a documented plan; implementation tasks only execute that plan — never mix in one agent call
- Use `git commit` after each task completion as a save point and rollback boundary
- Cross-model review (write with Claude, review with a separate GPT/Kiro call) catches issues the generation model is blind to

## AI-agent gotchas
- Agents underestimate token usage for tasks that require reading existing code — add 20k tokens to the estimate for any task touching > 3 existing files
- Without explicit dependency summaries, each Wave 2 agent starts fresh and may produce different naming conventions or error handling patterns — breaks consistency
- Agents ignore the "Independent within wave" INVEST rule and create tasks that implicitly depend on Wave 1 side effects; require the decomposition agent to explicitly list what each task assumes is pre-existing
- The `task-master` complexity score is useful for flagging tasks that need splitting (score > 7 → split), but the split point requires human or orchestrator judgment
- Parallel worktree execution requires `git merge` or `git rebase` after each wave — this is a human-in-the-loop checkpoint; don't skip it

## References
- https://www.anthropic.com/engineering/claude-code-best-practices
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://addyosmani.com/blog/ai-coding-workflow/
- https://github.com/eyaltoledano/claude-task-master
- https://mgx.dev/insights/task-decomposition-for-coding-agents-architectures-advancements-and-future-directions/a95f933f2c6541fc9e1fb352b429da15
