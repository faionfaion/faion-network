# Agent Integration — Template: Task File

## When to use
- Generating TASK_*.md files from an approved implementation plan
- Converting implementation plan row stubs into standalone, self-contained task files
- Ensuring the executing agent has all required context within a single file (no external lookups needed at runtime)
- Verifying completed tasks before marking them done — template defines the done state

## When NOT to use
- Before implementation plan is approved — task scope will change and the file is wasted effort
- For research spikes where the deliverable is a decision, not code — use a lighter note format
- When a task takes fewer than 5k tokens to execute — overhead of full template is not worth it
- When writing tasks for manual human execution — human tasks need narrative description, not Given-When-Then AC

## Where it fails / limitations
- `Estimated Tokens` field is advisory; executors often exceed it without enforcement
- `Implementation` and `Summary` sections are filled after execution — they're empty when task is dispatched, defeating their purpose as context for the executor
- Token estimation guide in template is Django/React-centric; other stacks have different baselines
- Task states (todo → in-progress → done) are file-system directory states, not fields — template section is ambiguous
- No field for "rollback" — when a task must be undone, there is no documented reversal procedure

## Agentic workflow
A task-creator subagent receives one row from the implementation plan and the full SDD context (constitution, spec, design). It reads dependency task summaries from `done/TASK_*.md` files, then instantiates the template. The critical sections are: SDD References, Task Dependency Tree, Objective, AC, Technical Approach, and Files. The Implementation and Summary sections are left for the executor to fill. After creation, the task file is placed in `todo/` and reviewed by `faion-sdd-reviewer-agent (mode: tasks)` before execution begins.

### Recommended subagents
- `faion-sdd-executor-agent` — primary consumer; reads TASK_*.md and executes it
- `faion-sdd-reviewer-agent (mode: tasks)` — 4-pass review of generated task file completeness

### Prompt pattern
```
Create TASK_{NNN}.md for feature {feature_name}.

Task from plan: {task_row_from_implementation_plan}
SDD docs: constitution.md, spec.md, design.md at {sdd_path}
Completed dependencies: {list_of_done_task_paths}

Required sections (fill all):
- SDD References (table of doc paths)
- Task Dependency Tree (read done/ task summaries)
- Requirements Coverage (paste FR-X and AD-X text from spec/design)
- Objective (single-agent executable goal, 2-3 sentences)
- Acceptance Criteria (Given-When-Then, link to FR-X)
- Technical Approach (numbered steps)
- Files (CREATE/MODIFY table)
- Estimated Tokens (breakdown: research + task + impl + tests, must be <100k)

Do not fill Implementation or Summary sections.
Save to: {task_dir}/todo/TASK_{NNN}.md
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ls todo/ in-progress/ done/` | Monitor task lifecycle state | built-in |
| `grep -l "Status: COMPLETED"` | Find completed tasks by executor report | built-in |
| `grep "Estimated Tokens"` | Audit token estimates across all tasks | built-in |
| `wc -l TASK_*.md` | Check task file lengths (good: 80-200 lines) | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Issues | SaaS | Yes | Mirror tasks as issues: `gh issue create --label task` |
| Linear | SaaS | Yes | Each TASK_*.md maps to a Linear issue with custom fields |
| Notion | SaaS | Partial | Database rows per task; API write supported but format lossy |
| Obsidian | OSS | No | No write API; file sync only via filesystem |

## Templates & scripts
The canonical template is in `README.md`. Key sections and their fill-order:

```
Creation order (task-creator agent):
1. SDD References → links to constitution/spec/design
2. Task Dependency Tree → read done/ summaries
3. Requirements Coverage → paste FR/AD text
4. Objective → 2-3 sentence goal
5. Dependencies → explicit FS dependencies
6. Acceptance Criteria → Given-When-Then
7. Technical Approach → numbered implementation steps
8. Files → CREATE/MODIFY table
9. Estimated Tokens → breakdown per phase

Execution order (executor agent fills these):
10. Implementation → changes made, tests added
11. Summary → completion status, issues, lessons
```

Task lifecycle script:
```bash
#!/usr/bin/env bash
# Move task through lifecycle; verifies section headers before state change
TASK_FILE="$1"
TARGET_STATE="$2"  # in-progress | done

if [ "$TARGET_STATE" = "done" ]; then
  if ! grep -q "## Summary" "$TASK_FILE"; then
    echo "BLOCKED: Summary section missing — task not done"
    exit 1
  fi
  if ! grep -q "Status: COMPLETED\|Status: BLOCKED" "$TASK_FILE"; then
    echo "BLOCKED: Execution Report missing — task not done"
    exit 1
  fi
fi

mkdir -p "$(dirname "$TASK_FILE")/../$TARGET_STATE"
mv "$TASK_FILE" "$(dirname "$TASK_FILE")/../$TARGET_STATE/$(basename "$TASK_FILE")"
echo "Moved to $TARGET_STATE"
```

## Best practices
- Write the Dependency Tree section by actually reading done task files, not from memory — patterns drift between tasks
- Acceptance Criteria should be self-verifiable: the executor must be able to run a test or command to confirm each AC
- Technical Approach steps should be ordered to match file change order — avoids import errors during execution
- Set Estimated Tokens conservatively; better to split tasks than to have an executor run out of context mid-implementation
- Mark "Out of Scope" with explicit items the executor might attempt based on the task description — prevents over-engineering
- One task = one objective; if the title has "and", the task should probably be split
- Tag AC items with FR-X references — this makes the reviewer's traceability check automated

## AI-agent gotchas
- Executors frequently skip reading the Dependency Tree section — make it the first section after metadata so it cannot be skipped
- Given-When-Then format breaks for background jobs (no "when" actor) — use "Given / Triggered by / Then" variant
- Estimated Tokens for test files is consistently underestimated by 50%; test files for Django viewsets can be 40k+ tokens
- Task files marked "todo" but placed in wrong directory confuse the lifecycle — executor checks directory, not status field
- Agents fill Summary section with optimistic language even when tests fail — reviewer must check git log against claimed completions
- "Lessons Learned" is valuable for `.aidocs/memory/` population but is almost never filled under execution pressure

## References
- [INVEST criteria for task quality — Bill Wake](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/)
- [Acceptance criteria best practices — Adzic](https://gojko.net/books/specification-by-example/)
- [Context window management for LLMs](https://platform.openai.com/docs/guides/prompt-engineering)
- [Task decomposition patterns — XP](https://www.extremeprogramming.org/rules/userstories.html)
