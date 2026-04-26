# Agent Integration — Implementation Plan Examples

## When to use
- Bootstrapping a new implementation plan when an agent needs a concrete format reference
- Validating a generated plan against known-good examples (3-task simple, 7-task medium, 12-task complex)
- Teaching wave analysis and critical path calculation by example before an agent attempts it on a real feature
- Identifying the split point for tasks that exceed the 100k token budget (the refactoring split example)

## When NOT to use
- Copying example task names and file paths directly into a new plan — examples are structural references, not content templates
- Referencing effort estimates from examples (hours) — per project conventions, no time estimates are allowed; use token estimates instead
- Using the wave diagram ASCII art format — project rules prohibit ASCII art; use tables or text descriptions instead
- For plans with >20 tasks — examples top out at 12; very large features need a custom approach beyond these examples

## Where it fails / limitations
- Examples use hour-based effort estimates throughout (3h, 5h) which directly violates the "no time estimates" rule; agents copy this format
- Wave diagrams in Example 3 use ASCII box-and-arrow art — prohibited in this project; examples must be adapted before use
- Critical path calculation assumes all tasks have accurate token estimates, which is rarely true in practice
- Example 2 (payment) references Stripe-specific implementation details that are inappropriate for non-Stripe projects
- Rollback strategy is missing from all examples — a significant gap for production deployment planning

## Agentic workflow
A planning subagent reads the relevant example (simple/medium/complex based on feature scope) as a structural reference, then generates the real implementation plan with actual feature content. The subagent fills in wave analysis, dependency graph, and task details. An Opus subagent reviews the critical path calculation and wave grouping for logical consistency. The finished plan goes to `faion-sdd-reviewer-agent (mode: plan)` for a 100k compliance check before it is saved and tasks are created.

### Recommended subagents
- `faion-sdd-reviewer-agent (mode: plan)` — 100k compliance per task, dependency acyclicity, FR/AD coverage check
- Opus agent for critical path analysis on complex (10+ task) features — Sonnet makes arithmetic errors in dependency chains

### Prompt pattern
```
Generate implementation-plan.md for feature: {feature_name}
Design doc: {design_path} (approved)
Feature complexity: {simple|medium|complex} ({N} tasks estimated)

Use the {simple|medium|complex} example as structural reference only.
Do NOT copy task names or effort estimates from the example.
Token estimates replace time estimates (no hours, no days).
Wave analysis: table format (no ASCII diagrams).
Critical path: list format (TASK-X → TASK-Y → TASK-Z).
```

```
Review implementation-plan.md for 100k compliance:
- Every task has Estimated Tokens?
- Every task total < 100k?
- Tasks >100k: propose split (like the refactoring example)?
- Dependency graph: no cycles?
- All AD-X from design assigned to at least one task?
- All FR-X from spec assigned to at least one task?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `grep "Context:" impl-plan*.md` | Extract token estimates per task | built-in |
| `grep -c "TASK-"` | Count total tasks in plan | built-in |
| `graphviz dot` | Render dependency graph from DOT notation | `apt install graphviz` |
| `toposort` (Python) | Validate dependency graph is acyclic | `pip install toposort` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Projects | SaaS | Yes | Implementation plan tasks → project board issues; `gh project` CLI |
| Linear | SaaS | Yes | Wave → Cycle; tasks → issues with dependencies |
| Mermaid | OSS | Yes | Dependency graph as Mermaid Gantt or flowchart; renders in GitHub |
| Jira | SaaS | Yes | Epic breakdown with story linking; REST API for programmatic creation |

## Templates & scripts
Examples in `README.md` are the structural references. Adapt format, not content.

Dependency graph validator:
```python
from collections import defaultdict, deque

def validate_no_cycles(tasks: dict[str, list[str]]) -> list[str]:
    """
    Topological sort to detect cycles in task dependency graph.
    tasks = {"TASK-003": ["TASK-001", "TASK-002"], ...}
    Returns list of tasks in valid execution order, or raises if cycle found.
    """
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    all_tasks = set(tasks.keys())
    for task, deps in tasks.items():
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1
            all_tasks.add(dep)
    queue = deque(t for t in all_tasks if in_degree[t] == 0)
    order = []
    while queue:
        task = queue.popleft()
        order.append(task)
        for dependent in graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    if len(order) != len(all_tasks):
        remaining = all_tasks - set(order)
        raise ValueError(f"Cycle detected involving: {remaining}")
    return order
```

## Best practices
- Choose example scale before generating — simple (1-4 tasks), medium (5-8), complex (9-15); this sets expectations for wave count and checkpoint frequency
- Adapt the refactoring split example whenever a task estimate exceeds 100k — split at natural boundaries (interface → implementation → API layer)
- Write wave analysis as a table (Wave, Tasks, Parallel, Dependencies) rather than as a diagram — text tables are machine-parseable
- Critical path must be explicit as a task chain with arrows, not inferred — agents need it to prioritize under time pressure
- Rollback plan is missing from all examples but required in production — add a "Rollback" section per phase for DB migrations and API changes
- Prerequisites section should reference infrastructure items by version (SendGrid API v3, not just "SendGrid") — avoids compatibility surprises

## AI-agent gotchas
- Agents copy the hour-based effort estimates from examples verbatim — explicitly forbid it in the prompt: "no hours, token estimates only"
- Wave analysis speedup calculations (1.8x - 3.5x) get copied from examples even when actual dependency structure yields different speedup
- ASCII wave diagrams in Example 3 are interpreted as valid format by agents — they will reproduce them; specify "table format only"
- Agents generate 3 waves because examples have 3; complex features may need 5+ waves — do not let the example count constrain the real plan
- "Prerequisites" section is skipped for non-auth features because examples focus on auth/email/payment — prompt to add infra prerequisites explicitly
- Test tasks (TASK-003, TASK-005 in examples) are frequently parallelized with implementation tasks; this is wrong — tests depend on implementation

## References
- [Scrum task board and story sizing — Atlassian](https://www.atlassian.com/agile/scrum/boards)
- [Feature slicing patterns — Agile for All](https://agileforall.com/vertical-slices-and-scale/)
- [Dependency graph analysis — toposort](https://pypi.org/project/toposort/)
- [Critical path method — PMI](https://www.pmi.org/learning/library/critical-path-analysis-project-management-4126)
