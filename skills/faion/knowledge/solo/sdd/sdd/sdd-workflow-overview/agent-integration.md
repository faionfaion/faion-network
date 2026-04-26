# Agent Integration — SDD Workflow Overview

## When to use
- Onboarding a new agent or session to the SDD methodology before any phase work begins
- An agent needs the philosophical framing of "intent is source of truth" to avoid drifting into ad-hoc coding
- Deciding whether a task warrants full SDD vs the "15-minute waterfall" vs direct implementation
- Configuring agent model selection per phase (haiku for templates, sonnet for review, opus for architecture)
- Teaching an agent the complete phase sequence: CONSTITUTION → SPEC → DESIGN → TEST-PLAN → IMPL-PLAN → TASKS → EXECUTE → REVIEW → DONE

## When NOT to use
- The agent already has SDD context loaded from a previous session — re-reading the overview wastes tokens
- Task is < 2 hours with a clear implementation path — skip to direct execution
- The project has no `.aidocs/` structure and no time to set it up — use the 15-minute waterfall variant
- Pure research or exploratory work with no deliverable code

## Where it fails / limitations
- Phase 2.5 (Test Plan) is often skipped under time pressure; agents don't enforce it without explicit tooling
- "Spec-as-Source" (Level 3) requires human-only spec edits and generated code — agents frequently blur this boundary
- The confidence threshold table (70% → 90% → 95%) is not enforced by any tool; agents self-report and often round up
- Constitution.md is one-time setup that agents skip for new projects; this causes downstream standard violations
- "15-minute waterfall" is described but not templated — agents improvise and produce inconsistent quick-specs

## Agentic workflow
Load this overview at the start of any SDD session to calibrate the agent's operating mode. An orchestrating Claude agent uses the phase diagram (CONSTITUTION → ... → DONE) as its state machine, delegating each phase to a specialized sub-agent that reads only the artifacts relevant to that phase. The key orchestrator responsibility is enforcing transition gates — blocking forward progress until confidence thresholds are met.

### Recommended subagents
- `faion-task-executor-agent` — the primary SDD orchestrator; routes to all downstream phases
- `faion-feature-executor` skill — sequential task runner for the EXECUTE phase
- `faion-sdd-execution` skill — validation and reflexion for the REVIEW phase
- `faion-brainstorm` skill — used during BRAINSTORM → SPEC transition for diverge-converge

### Prompt pattern
```
You are an SDD orchestrator. The project uses .aidocs/ for lifecycle artifacts.
Current phase: [phase]. Read .aidocs/memory/session.md for state.
Your job: complete the current phase, run the transition gate, then hand off to the next phase agent.
Do not code during SPEC or DESIGN phases. Do not spec during EXECUTE phase.
```

```
Decide SDD level for this task:
- Task description: [description]
- Estimated complexity: [Low/Medium/High]
Output one of: FULL_SDD | WATERFALL_15MIN | DIRECT_IMPLEMENTATION
Justify in one sentence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Drive SDD phases interactively with CLAUDE.md context | https://docs.anthropic.com/en/docs/claude-code |
| `kiro` | Continuous spec-implementation drift detection | https://kiro.dev |
| `git` | Feature lifecycle via branches + worktrees | Built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kiro | SaaS | Yes | Validates implementation against spec automatically |
| OpenSpec | OSS | Yes | Hosts living specs with delta tracking |
| GitHub Spec-Kit | OSS | Partial | GitHub-integrated spec workflows |
| Cursor | SaaS/IDE | Yes | Spec-aware context via rules files |

## Templates & scripts
See `templates.md` in parent directory for constitution.md, spec.md, design.md, test-plan.md, implementation-plan.md skeletons.

Quick SDD level decision script:
```bash
#!/usr/bin/env bash
# sdd-level.sh — print recommended SDD level based on task size estimate
# Usage: sdd-level.sh <token_estimate>
TOKENS=${1:-0}
if [ "$TOKENS" -lt 10000 ]; then
  echo "DIRECT_IMPLEMENTATION"
elif [ "$TOKENS" -lt 40000 ]; then
  echo "WATERFALL_15MIN"
else
  echo "FULL_SDD"
fi
```

## Best practices
- Load constitution.md into agent context before any spec work — it anchors tech stack, standards, and quality thresholds
- Use Level 1 (Spec-First) for new features, Level 2 (Spec-Anchored) for maintenance, Level 3 (Spec-as-Source) only for fully automated pipelines where humans never write code directly
- The test-plan phase (2.5) must come before implementation-plan — writing tests first shapes the task breakdown and makes "done" objective
- Prepend every agent prompt with "If unsure or context is missing, ask for clarification rather than guessing" — directly reduces hallucinations
- Break large specs into phases (backend section, frontend section) to avoid context overflow during spec reading

## AI-agent gotchas
- Agents conflate "spec" and "design": spec answers WHAT, design answers HOW — enforce separation via separate prompts and files
- LLMs hallucinate when context is insufficient; the spec is the anti-hallucination anchor — feed it as system context, not just user message
- The "curse of instructions" applies: loading the full spec (150+ requirements) degrades adherence; prioritize the 20 most critical FRs per task
- Without explicit SDD level selection, agents default to ad-hoc coding — always decide FULL_SDD vs WATERFALL_15MIN vs DIRECT upfront
- Phase completion is not verifiable from outside; require agents to output an explicit "PHASE COMPLETE" signal with artifact paths before proceeding

## References
- https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices
- https://addyosmani.com/blog/ai-coding-workflow/
- https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- https://addyosmani.com/blog/good-spec/
- https://intent-driven.dev/
