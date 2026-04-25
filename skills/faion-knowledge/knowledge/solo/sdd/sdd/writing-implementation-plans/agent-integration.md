# Agent Integration — Writing Implementation Plans

## When to use
- After `design.md` is approved and ready to translate into executable tasks
- When a feature has multiple logical components that could run in parallel
- When the critical path needs to be explicit to avoid bottlenecks (e.g., schema must exist before handlers)
- When handing a feature to an autonomous agent executor that needs an ordered work queue
- When estimating token budget before committing to a full feature (is the feature too large for one session?)
- When the team (or AI agent) needs to communicate progress in terms of waves, not vague "done / not done"

## When NOT to use
- Single-task changes: one file, no dependencies — write the task directly, skip the plan overhead
- Hotfixes: urgency makes planning overhead counterproductive
- Research/spike work: deliverable is a decision, not code — use an ADR instead
- Features still in spec draft: design must be approved before tasks can be derived

## Where it fails / limitations
- Wave analysis is only as accurate as the dependency graph — hidden code-level dependencies (shared utils, implicit initialization order) cause mid-execution failures that invalidate the plan
- Token estimates are rough; LLM output variance and codebase familiarity gaps can push actual usage 30-50% above estimate
- Plans become stale quickly when design evolves during implementation; re-syncing plan with design is a manual step agents cannot do reliably without re-reading design.md
- Critical path is meaningful only if tasks truly run serially; in solo/single-agent contexts, parallelism is theoretical — one agent still executes sequentially
- INVEST validation applied mechanically produces technically valid but vague tasks ("As a developer I want...") — acceptance criteria quality requires domain knowledge

## Agentic workflow
A Claude subagent reads `spec.md`, `design.md`, and `constitution.md` in sequence, extracts all file-level changes and AD-X decisions, builds a dependency graph, groups tasks into waves, and outputs a draft `implementation-plan.md`. A second review pass (or a human) validates the INVEST criteria and critical path before the plan is promoted to `Approved`. The `faion-sdd-executor-agent` then consumes the plan wave by wave, picking the next unblocked task and executing it.

### Recommended subagents
- `faion-sdd-executor-agent` — consumes implementation plan wave by wave; picks next unblocked task, executes, commits, advances lifecycle
- Inline Claude call for plan drafting — no dedicated plan-writer agent exists; use the main agent with the prompt pattern below

### Prompt pattern
```
You are writing an implementation plan for feature: <feature-name>.
Read these files in order:
1. .aidocs/constitution.md (project standards)
2. <feature-dir>/spec.md (FR-X requirements)
3. <feature-dir>/design.md (AD-X decisions, file changes)

Extract all file-level changes (CREATE / MODIFY) from design.md.
Build a dependency DAG. Identify parallel waves using the wave algorithm:
  Wave N = all tasks whose dependencies are all in Wave 1..N-1.
For each task: estimate tokens using the formula in writing-implementation-plans README.
Apply INVEST validation. Flag any task exceeding 100k tokens for decomposition.
Output: implementation-plan.md following the full template structure.
```

```
Review this implementation plan for TASK-<N>: <paste task>.
Check: INVEST criteria, token estimate plausibility, acceptance criteria testability.
List issues. Do not rewrite the plan — output a critique only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| mermaid-cli (`mmdc`) | Renders DAG dependency graphs from Mermaid syntax to PNG/SVG | `npm install -g @mermaid-js/mermaid-cli` / https://github.com/mermaid-js/mermaid-cli |
| tokencost | Estimates token counts for file sets before plan execution | `pip install tokencost` / https://github.com/AgentOps-AI/tokencost |
| jq | Parses task JSON manifests, filters by wave number | System package / https://jqlang.github.io/jq/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — REST + GraphQL API | Wave-based task import via API; can mirror implementation plan tasks |
| GitHub Issues | SaaS | Yes — REST API | Tasks as issues, dependencies via "blocked by" labels or project fields |
| Notion | SaaS | Partial — REST API | Implementation plan as database; limited dependency modeling |
| Jira | SaaS | Partial — REST API | Story/subtask hierarchy maps to wave structure; complex to automate |

## Templates & scripts
See `templates.md` for the full `implementation-plan.md` template.

Wave-dependency extraction helper (reads a plan, prints task→dependencies as JSON):
```python
#!/usr/bin/env python3
"""Extract wave assignments from implementation-plan.md for agent scheduling."""
import re, sys, json

def parse_plan(path):
    tasks = {}
    current = None
    with open(path) as f:
        for line in f:
            m = re.match(r'### (TASK-\d+):', line)
            if m:
                current = m.group(1)
                tasks[current] = {"depends_on": [], "wave": None}
            if current and re.match(r'\*\*Depends on:\*\*', line):
                deps = re.findall(r'TASK-\d+', line)
                tasks[current]["depends_on"] = deps
            if current and re.match(r'\*\*Wave:\*\*\s*(\d+)', line):
                tasks[current]["wave"] = int(re.search(r'\d+', line).group())
    return tasks

if __name__ == "__main__":
    print(json.dumps(parse_plan(sys.argv[1]), indent=2))
```

## Best practices
- Always derive tasks from design.md file-change table, not from vague feature descriptions — every task should map to one or more named files
- Mark the critical path explicitly in the plan; the executor agent needs to know which delays are blockers
- Apply 20% contingency buffer to all token estimates before flagging a task for decomposition at 80k (not 100k)
- Keep each task's acceptance criteria strictly verifiable — "returns HTTP 201" not "works correctly"
- Validate the dependency graph before running: missing dependency = executor deadlock waiting for a file that was never created
- In solo contexts, parallelism is execution-order guidance, not true concurrency — still valuable for prioritization

## AI-agent gotchas
- Agents confuse "task independence" with "no shared files" — two tasks that both import from a shared utility have an implicit ordering dependency even if not expressed in the plan
- Token estimates are routinely underestimated for "modify existing file" tasks because agents undercount the context needed to understand the existing code before editing
- The 100k rule applies to the agent's context window at execution time, not just the task description size — include buffer for the files the agent must read (2-5k per file)
- Dependency graph cycles: agents can produce circular dependencies when derived from a complex design; validate with a topological sort before starting execution
- Human-in-loop checkpoint: plan should be reviewed by a human (or a review-mode agent) before `faion-sdd-executor-agent` begins — post-hoc plan corrections mid-wave are expensive

## References
- https://mgx.dev/insights/task-decomposition-for-coding-agents-architectures-advancements-and-future-directions/a95f933f2c6541fc9e1fb352b429da15
- https://arxiv.org/abs/2510.25320 (GAP: Graph-based Agent Planning — parallel tool use with dependency awareness)
- https://research.trychroma.com/context-rot (Context Rot: how input token length degrades LLM performance)
- https://arxiv.org/html/2601.14470 (Tokenomics in Agentic Software Engineering)
- https://www.projectmanager.com/guides/critical-path-method (Critical Path Method)
- https://martinfowler.com/bliki/TestPyramid.html (Testing Pyramid — for testing plan section)
