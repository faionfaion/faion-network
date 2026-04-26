# Agent Integration — Task Creation Template Guide

## When to use
- Generating TASK_*.md files from an approved implementation plan
- Ensuring each task contains enough context for a single-agent execution without re-reading the whole codebase
- When implementation plans exist but tasks are stubs ("See plan for details")
- Before handing off feature execution to `faion-sdd-executor-agent`

## When NOT to use
- Before `spec.md` and `design.md` are both approved — templates will be incomplete
- For spike/research tasks with unknown scope (token budget cannot be estimated)
- When codebase has no patterns to reference (new greenfield project with no prior tasks)

## Where it fails / limitations
- Token estimates in templates are rough approximations; complex tasks often run 40% over
- Dependency tree becomes stale if completed tasks are refactored after their summary was written
- Given-When-Then AC format breaks down for infrastructure tasks (no user-observable "then")
- Template fields marked "filled by executor" are frequently skipped under time pressure

## Agentic workflow
A planning subagent reads the approved `implementation-plan.md` and iterates over each task row, calling a task-creator subagent per task. The creator reads the dependency summaries from completed `done/TASK_*.md` files, extracts FR/AD references from `spec.md` and `design.md`, then instantiates the full template. A reviewer subagent runs a 4-pass check (completeness, consistency, coverage, executability) before the task is moved to `todo/`.

### Recommended subagents
- `faion-sdd-executor-agent` — picks up completed TASK files and executes them sequentially
- `faion-task-creator-agent` (invoked inline via Task() call) — instantiates one TASK file per plan row
- `faion-sdd-reviewer-agent` — 4-pass quality review of generated tasks

### Prompt pattern
```
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task row from implementation-plan.md}
SDD_PATH: .aidocs/features/in-progress/{feature}/

Read dependency task summaries. Create TASK_{NNN}.md following the v2.0 template.
Token estimate must be <100k. AC in Given-When-Then. Include full dependency tree.
```

```
MODE: tasks
Review all TASK_*.md files for feature {feature}.
Pass 1: completeness — all plan rows covered?
Pass 2: consistency — no contradictions between tasks?
Pass 3: coverage — every FR and AD referenced?
Pass 4: executability — can each task run standalone within 100k tokens?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `wc -w` / `tiktoken` | Quick token count check before committing task file | `pip install tiktoken` |
| `grep -r "FR-"` | Verify FR references exist across task files | built-in |
| `jq` | Parse implementation plan JSON/YAML metadata if structured | built-in on most systems |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Partial | API for syncing tasks but no native SDD format |
| GitHub Issues | SaaS | Yes | Tasks can be mirrored as issues via `gh issue create` |
| Notion | SaaS | Partial | Database API works but template fidelity is lossy |
| Obsidian | OSS | No | No programmatic write API; file-based only |

## Templates & scripts
See `templates.md` and `template-task.md` for the canonical TASK_{NNN}.md template.

Inline helper — count token estimate before writing task file:
```python
import tiktoken

def estimate_tokens(text: str, model: str = "claude-3-5-sonnet-20241022") -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def check_task_budget(sdd_docs: str, research: str, implementation: str, tests: str) -> dict:
    budget = {
        "sdd_docs": estimate_tokens(sdd_docs),
        "research": estimate_tokens(research),
        "implementation": estimate_tokens(implementation),
        "tests": estimate_tokens(tests),
    }
    budget["total"] = sum(budget.values())
    budget["ok"] = budget["total"] < 100_000
    return budget
```

## Best practices
- Write the dependency tree before any other section — it sets the vocabulary for all subsequent fields
- Keep each task's "Files to Change" table to ≤8 files; if more, split the task
- Include at least one code snippet from a completed dependency task to anchor the executor's style
- Mark AC items with the FR-X they cover so reviewers can trace without re-reading spec
- Always write "Out of Scope" before "Goals" — prevents scope creep during execution
- Token estimate should be conservative: add 20% buffer on top of component-level sums
- Store completed task summaries in a machine-readable format (fixed section header) so future tasks can extract them programmatically

## AI-agent gotchas
- Agents tend to skip the "Lessons Learned" section — enforce via reviewer pass or it loses memory value
- Dependency tree snippets go stale: if TASK_001 is refactored, TASK_005's snippet reference is wrong; add a "last verified" date
- Haiku generates template shells quickly but leaves placeholder text; always run a Sonnet review pass
- The 100k budget assumes fresh context; if the executor's session already has prior tasks loaded, effective budget is lower
- "Potential Blockers" checkboxes are rarely cleared — agents treat them as decorative; make them actual exit conditions
- Given-When-Then AC works poorly for async tasks (email sends, webhooks) — add explicit "wait for" clauses

## References
- [Extreme Programming: User Story Rules](https://www.extremeprogramming.org/rules/userstories.html)
- [Specification by Example — Gojko Adzic](https://gojko.net/books/specification-by-example/)
- [tiktoken token counter](https://github.com/openai/tiktoken)
- [INVEST criteria for task quality](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/)
