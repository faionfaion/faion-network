# Agent Integration — Implementation Plan: 100k Token Rule

## When to use
- Before assigning any task to `faion-sdd-executor-agent` — validate the context budget will fit
- When decomposing a large design into tasks and unsure whether to split or combine
- Auditing an existing implementation plan where tasks seem to exceed the context window
- Estimating total project token cost before committing to an implementation approach

## When NOT to use
- Micro-tasks under 5k tokens — budget calculation overhead is not worth it
- Research and analysis passes where the agent is reading-only (no writes) — context budget still applies but failure mode is less severe
- When using Claude with 200k context — the 100k rule still applies because focus degrades at high context utilization, even within window limits

## Where it fails / limitations
- Token estimates for files that include auto-generated content (Prisma types, OpenAPI clients, migration snapshots) can be 5–10x the estimate for hand-written files
- Wave-based task creation assumes stable patterns after Wave 1; if Wave 1 reveals the architecture was wrong, Wave 2 task files must be rewritten
- "Buffer: 10-20k" is too small for tasks that involve debugging existing code — debugging passes read many files iteratively; add 30k buffer for bug-fix tasks
- The 100% WBS rule is hard to enforce when design is incomplete; accept estimated totals ±30% and refine after Wave 1

## Agentic workflow
Before writing any TASK_*.md, a planning agent estimates context for each proposed task using the breakdown table (agent prompt + project context + task file + design docs + codebase reading + buffer). Tasks over 80k tokens are split immediately; tasks between 60–80k get a "watch" label and are reviewed after Wave 1. The planning agent outputs a token budget table alongside the implementation plan.

`faion-sdd-executor-agent` does not enforce the 100k rule itself — it will attempt any task assigned to it. Budget enforcement is entirely a planning-phase responsibility.

### Recommended subagents
- General Claude subagent (Sonnet) — context estimation from design.md and file list (comparative assessment task)
- General Claude subagent (Haiku) — WBS task table generation (structured output, known format)
- `faion-sdd-executor-agent` — execution after budget is validated

### Prompt pattern
```
For each proposed task below, estimate context budget using this breakdown:
- Agent prompt: 8k
- Project context (constitution + contracts): Xk (read these files and count)
- Task file: 3k
- Design docs (relevant AD-X sections): Xk
- Codebase reading (list files to read + their sizes): Xk
- Buffer: 15k
Flag any task where total > 80k. Suggest a split strategy.
```

```
This task estimates 120k tokens. Split it using Option 1 (By Component):
Original: <task description>
Produce 3-4 sub-tasks, each < 60k tokens, with explicit dependency chain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ttok` | Count tokens in files before including in context estimate | `pip install ttok` / https://github.com/simonw/ttok |
| `wc -c` | Byte count as rough proxy when ttok unavailable (1 token ≈ 4 bytes) | system |
| `find + wc` | Estimate total token cost of a file group before task assignment | system |
| `tokei` | Count lines of code per language to identify large files early | https://github.com/XAMPPRocky/tokei |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Console | SaaS | No API for usage | Useful for manually checking token consumption of test prompts |
| OpenAI Tokenizer | SaaS (web) | No API | Cross-check token count for large files; same BPE tokenization |
| LangSmith | SaaS | Yes (SDK) | Track actual token usage per task execution; identify over-budget tasks |
| Helicone | SaaS | Yes (proxy) | Token usage logging per request; useful for calibrating estimates |

## Templates & scripts
See `impl-plan-100k-rule/README.md` for the WBS example and wave-based task creation pattern. The Implementation Plan template in `templates/README.md` has the full task table format with Est. Tokens column.

Context budget estimator for a task file list:
```bash
#!/usr/bin/env bash
# estimate-context.sh — sum token estimates for a task's file list
# Usage: estimate-context.sh file1 file2 file3 ...
TOTAL=0
AGENT_PROMPT=8000
PROJECT_CTX=12000
TASK_FILE=3000
BUFFER=15000

echo "Fixed costs:"
echo "  Agent prompt:    $AGENT_PROMPT"
echo "  Project context: $PROJECT_CTX"
echo "  Task file:       $TASK_FILE"
echo "  Buffer:          $BUFFER"
echo "Variable costs (files to read):"

for f in "$@"; do
  if [ -f "$f" ]; then
    BYTES=$(wc -c < "$f")
    TOKENS=$((BYTES / 4))
    echo "  $f: ~${TOKENS}k tokens"
    TOTAL=$((TOTAL + TOKENS))
  fi
done

GRAND=$((TOTAL + AGENT_PROMPT + PROJECT_CTX + TASK_FILE + BUFFER))
echo "Total estimate: ~${GRAND} tokens"
if [ "$GRAND" -gt 100000 ]; then
  echo "WARNING: exceeds 100k limit — split this task"
fi
```

## Best practices
- Calculate context budget before writing the TASK_*.md, not after — estimates that reveal a 120k task should trigger a split before any task file is created
- When splitting by component (Option 1), ensure the first sub-task has zero dependencies so Wave 1 can start immediately
- Wave-based creation is the default for features over 5 tasks: create and execute Wave 1, then create Wave 2 with patterns learned from execution reports
- Include "Generated files" explicitly in context estimates — ORM clients, schema snapshots, and type exports are large and agents forget to account for them
- Track actual vs estimated token usage after each task execution; update future estimates based on observed ratios

## AI-agent gotchas
- Agents consistently underestimate codebase reading tokens — they estimate files listed in the task but forget files read for pattern discovery during execution
- The "100% Rule" from WBS means every piece of work must appear in some task; planning agents frequently omit test-writing tasks and CHANGELOG updates
- `faion-sdd-executor-agent` will not abort a task mid-execution when context fills up — it will produce incomplete output and mark the task done; the only prevention is correct upfront estimation
- Wave creation laziness: agents asked to "create all tasks now" will create Wave 2 and 3 stubs with placeholder content; enforce wave-gated creation in the planning prompt
- Context estimate for "Complex" tasks that require debugging or exploration should add a 30k exploration buffer on top of the standard formula — debugging reads are non-deterministic

## References
- https://docs.anthropic.com/claude/docs/models-overview — Claude context window documentation
- https://github.com/simonw/ttok — Token counting CLI by Simon Willison
- https://www.pmi.org/learning/library/applying-work-breakdown-structure-project-lifecycle-6979 — PMI WBS practices
- https://www.atlassian.com/agile/project-management/epics-stories-themes — Atlassian story splitting
- https://github.com/XAMPPRocky/tokei — Fast code line counter
