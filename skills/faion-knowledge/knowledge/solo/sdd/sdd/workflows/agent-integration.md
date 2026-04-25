# Agent Integration — SDD Workflows

## When to use
- Starting a new multi-day feature that needs structured progression from idea to deployed code
- An agent needs to orchestrate multiple sub-agents across spec → design → implementation → review phases
- The codebase already has `.aidocs/` structure and the team follows SDD lifecycle
- Resuming mid-session work: agent reads `session.md` to restore state and continue from last checkpoint
- Producing auditable artifacts: regulated domains, client deliverables, or systems requiring traceability

## When NOT to use
- Task estimated at under 2 hours — direct implementation is faster
- Pure bug fix with a known root cause — fix + test is sufficient
- Exploratory spike/prototype — throwaway code doesn't benefit from full SDD overhead
- Configuration-only change — editing a config file needs no spec or design phase

## Where it fails / limitations
- Workflow state stored in markdown files (`session.md`) can diverge if multiple agents write concurrently without locking
- Confidence thresholds (70%-95%) are self-reported by the agent — no objective external validator enforces them
- Context budget rules (100k tokens per task) are estimates; actual token counts depend on model and encoding
- The state machine has no recovery from partial phase completion when a session crashes mid-phase
- Transition gates require human approval in regulated contexts but the workflow documentation leaves approval mechanics undefined

## Agentic workflow
An orchestrating agent reads `session.md` to find the current phase, then delegates each phase to a specialized sub-agent (spec writer, design reviewer, task executor, code reviewer). Between phases the orchestrator runs the transition gate checklist and records confidence scores in `session.md`. The workflow is inherently sequential per feature but multiple features can run in parallel worktrees.

### Recommended subagents
- `faion-task-executor-agent` — drives the full SDD pipeline; invoked with "Start SDD workflow for [idea]"
- `faion-feature-executor` skill — executes individual tasks from the todo queue with quality gates
- `faion-sdd-execution` skill — handles quality gate validation and reflexion learning after each phase

### Prompt pattern
```
You are resuming an SDD workflow. Current state is in .aidocs/memory/session.md.
Read it, identify the current phase, load the relevant artifacts, and continue.
Do not skip transition gates. Report confidence score before moving to the next phase.
```

```
Phase: DESIGN → IMPL-PLAN transition check.
Read spec.md and design.md. Verify: all FR-X have AD-X decisions, file structure defined,
API contracts specified. Report confidence (0-100%). If >= 90%, output "PROCEED".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git worktree` | Isolated parallel feature branches | `git help worktree` |
| `claude` (Claude Code CLI) | Drive each phase interactively | https://docs.anthropic.com/en/docs/claude-code |
| `kiro` (if installed) | Spec-implementation validation during review phase | https://kiro.dev |
| `codex` (OpenAI CLI) | Cross-model review in review phase | https://github.com/openai/codex |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Automate quality gate CI per phase |
| Linear / Jira | SaaS | Partial | Mirror SDD task lifecycle to issue tracker via API |
| Kiro | SaaS | Yes | Continuous spec-implementation drift detection |
| OpenSpec | OSS | Yes | Source-of-truth spec hosting with delta tracking |

## Templates & scripts
See `templates.md` for phase-specific document templates (spec.md, design.md, implementation-plan.md, TASK-XXX.md).

Phase transition gate check script (inline):
```bash
#!/usr/bin/env bash
# check-transition.sh <from-phase> <to-phase>
# Reads .aidocs and reports blocking items
set -euo pipefail
FROM=${1:-spec}
TO=${2:-design}
echo "=== Transition gate: $FROM -> $TO ==="
case "$FROM-$TO" in
  spec-design)
    grep -c "FR-" .aidocs/*/spec.md 2>/dev/null || echo "WARN: No FR-X requirements found"
    grep -q "Acceptance Criteria" .aidocs/*/spec.md && echo "OK: ACs present" || echo "FAIL: Missing ACs"
    ;;
  design-plan)
    grep -c "AD-" .aidocs/*/design.md 2>/dev/null || echo "WARN: No AD-X decisions found"
    grep -q "File Structure" .aidocs/*/design.md && echo "OK: File structure defined" || echo "FAIL: Missing file structure"
    ;;
  plan-execute)
    ls .aidocs/*/todo/TASK-*.md 2>/dev/null | wc -l | xargs -I{} echo "Tasks in queue: {}"
    ;;
  *)
    echo "Unknown transition: $FROM -> $TO"
    exit 1
    ;;
esac
```

## Best practices
- Use the wave-based parallelization pattern for large features: Wave 1 tasks run concurrently, their summaries propagate to Wave 2
- Always include "do nothing" as a baseline alternative in design docs — mirrors Google's practice
- Record confidence scores numerically in `session.md`; vague "feels ready" is not a gate
- Keep one commit per task completion; git history doubles as workflow audit log
- When using multi-model review (Claude + GPT/Kiro), run reviewers in parallel and merge findings before the fix step — this is the SDD Phase 5 pattern

## AI-agent gotchas
- Agents drift into implementation during spec phase — enforce "WHAT not HOW" strictly in the spec prompt
- Context window exhaustion mid-phase causes the agent to silently drop requirements; break large features into sub-specs before execution
- The "one task, one focus" rule: never combine research ("figure out how") with implementation ("build it") in a single agent call — two separate tasks
- Phase transition confidence scores are self-assessed; an overconfident agent will move to design with an incomplete spec — add a reviewer sub-agent as a check
- `session.md` must be written atomically at phase boundaries; if a crash occurs between phases, the next agent run will find inconsistent state — always re-read session.md at session start

## References
- https://addyosmani.com/blog/ai-coding-workflow/ — Addy Osmani LLM coding workflow 2026
- https://www.webuild-ai.com/insights/five-workflow-patterns-to-multiply-your-development-capacity-with-ai-coding-assistants
- https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
