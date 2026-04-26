# Agent Integration — Task Creation Principles

## When to use
- Converting an approved design document into executable TASK_*.md files
- Splitting large undefined work into bounded units before assigning to a subagent
- Auditing an existing implementation plan where tasks are vague or oversized
- When `faion-sdd-executor-agent` will run unattended and needs unambiguous inputs

## When NOT to use
- Prototyping or exploratory spikes — INVEST/SMART overhead not worth it
- Single-file hot-fixes with obvious scope — task structure adds ceremony with no return
- Early brainstorming phases before a spec exists (no FR-X to trace to yet)

## Where it fails / limitations
- INVEST "Independent" criterion is often violated in sequential migration chains — accept partial dependency and document it rather than forcing artificial splits
- Token estimates are rough; large config files or generated types can spike context unexpectedly
- Given-When-Then ACs work poorly for performance NFRs — supplement with measurable thresholds rather than scenario language

## Agentic workflow
A planning agent reads the approved `design.md` and `spec.md`, then produces one TASK_*.md file per unit. Each file is validated against the INVEST/SMART checklist before being written. The executor agent (`faion-sdd-executor-agent`) later picks tasks from `todo/` and runs them sequentially in dependency order, writing an execution report back into the same file.

Keep task creation and task execution in separate agent turns: a planning agent that also executes tends to cut corners on AC definition.

### Recommended subagents
- `faion-sdd-executor-agent` — executes tasks from `todo/`, moves through lifecycle, writes execution reports
- General Claude subagent (Sonnet) — sufficient for task decomposition from a well-structured design doc

### Prompt pattern
```
Given this design.md and spec.md, produce TASK_*.md files.
Each task: <100k tokens, INVEST-valid, Given-When-Then ACs, FR/AD links.
Output one markdown block per task. Do not implement anything.
```

```
Review these TASK_*.md files. Flag any that violate INVEST (not independent,
not estimable, not testable). For each violation, suggest a split or rewrite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tokencounter` / `ttok` | Estimate token count of a file before assigning | `pip install ttok` / https://github.com/simonw/ttok |
| `jq` | Parse and validate JSON task metadata if stored in frontmatter | system package |
| `grep` / `ripgrep` | Trace FR-X and AD-X references across docs | `apt install ripgrep` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (REST + GraphQL API) | Can create issues from TASK_*.md; maps to INVEST story format |
| GitHub Issues | SaaS | Yes (gh CLI + REST) | Cheapest integration; label by complexity; milestone = wave |
| Jira | SaaS | Partial (REST API, complex auth) | Overkill for solo workflow; use only if client requires |
| Notion | SaaS | Partial (REST API) | Good for stakeholder visibility; not ideal for agent writes |

## Templates & scripts
See `templates.md` → TASK_*.md template (full task file format). The implementation-plan template in `templates/README.md` shows the wave/checkpoint structure.

Inline helper — count tokens in a task file before committing:
```bash
#!/usr/bin/env bash
# token-check.sh — warn if task file exceeds 80k-token warning threshold
FILE=${1:?usage: token-check.sh TASK_001.md}
COUNT=$(ttok < "$FILE" 2>/dev/null || wc -w < "$FILE")
if [ "$COUNT" -gt 60000 ]; then
  echo "WARNING: $FILE is large (~${COUNT} tokens). Consider splitting."
fi
```

## Best practices
- Write task files in waves: create Wave 1 tasks in detail, execute, then write Wave 2 with patterns learned from Wave 1 output
- Always include the full text of referenced FR-X and AD-X inline in the task file — the executor agent should not need to re-read the entire spec
- Keep "Technical Notes" specific: name the exact pattern file, line range, or prior task that establishes the pattern to follow
- One task = one commit; never combine multiple TASK-IDs in a single commit
- Assign `complexity: complex` tasks their own wave rather than parallelizing them — complex tasks have higher abort/rework rates

## AI-agent gotchas
- Executor agents ignore vague AC like "works correctly" — every criterion must have an observable, code-verifiable outcome
- If a task file is a stub ("See implementation-plan.md"), `faion-sdd-executor-agent` extracts from the plan table — this loses context; always prefer full task files
- Circular dependency detection is not automatic — validate the dependency graph manually before handing to an executor
- Agents tend to overestimate independence: "no code dependency" does not mean "no data dependency" (e.g., task B needs the DB rows created by task A)
- Human checkpoint required before executing any `complex`-rated task that touches auth, payments, or public APIs — flag these in the task file

## References
- https://agileforall.com/new-to-agile-invest-in-good-user-stories/ — INVEST criteria (Bill Wake)
- https://cucumber.io/docs/bdd/ — BDD / Given-When-Then
- https://www.pmi.org/pmbok-guide-standards/framework/practice-standard-wbs — PMI WBS
- https://martinfowler.com/bliki/GivenWhenThen.html — Martin Fowler on GWT
