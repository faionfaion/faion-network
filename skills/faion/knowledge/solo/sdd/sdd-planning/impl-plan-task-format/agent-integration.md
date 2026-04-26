# Agent Integration — Implementation Plan Task Format

## When to use
- Converting design.md architecture decisions into executor-ready TASK_*.md files
- Defining the exact structure that `faion-sdd-executor-agent` will parse and execute
- When building an implementation plan that supports parallel waves (multiple agents or sequential single-agent runs)
- Auditing existing task files for INVEST compliance and AC quality before executor assignment

## When NOT to use
- One-off scripts or changes that do not follow the SDD lifecycle
- Research spikes where the output is a document, not code
- When the feature is simple enough for a single undivided task — overhead of the format exceeds benefit under ~15k token tasks

## Where it fails / limitations
- Dependency type notation (FS/SS/FF/SF) is rarely used correctly; in practice almost all dependencies are FS — document the exceptions explicitly
- "Technical Notes" sections written too early become stale when implementation patterns differ from design assumptions; write them after Wave 1 is complete for later waves
- Context estimates are underspecified for tasks that require reading large generated files (Prisma client, GraphQL schema, migrations) — add a separate "Generated files" line in the estimate breakdown
- INVEST "Valuable" criterion is hardest to enforce for pure infrastructure tasks; accept "Enables FR-X" as sufficient value statement

## Agentic workflow
A planning agent reads `design.md` → extracts each AD and maps it to one or more tasks → fills the TASK format template for each → outputs a complete `implementation-plan.md` with embedded task stubs. The `faion-sdd-executor-agent` then processes the stubs in wave order: it picks the first uncomplete task in `todo/`, moves it to `in-progress/`, executes, writes an execution report, and moves to `done/`.

Wave-based task creation is the key pattern: the planning agent generates only Wave 1 task files in full detail; after Wave 1 execution, it generates Wave 2 files using patterns learned from Wave 1 output.

### Recommended subagents
- `faion-sdd-executor-agent` — primary consumer; executes tasks one at a time per the format
- General Claude subagent (Sonnet) — task format generation from design.md AD table
- General Claude subagent (Haiku) — INVEST validation pass (structured output, low token cost)

### Prompt pattern
```
Given this design.md and spec.md, generate TASK_*.md files for Wave 1 only.
Use the implementation plan task format v2.0.
For each task:
- Fill all metadata fields (Phase, Wave, Complexity, Context Estimate).
- Write 3+ testable AC items (observable outcomes, not vague).
- Include full FR-X and AD-X reference text inline (do not require reader to open other files).
- Estimate context in tokens: agent prompt (5k) + project context + task file + files to read + buffer.
Output one markdown block per task.
```

```
Review these TASK_*.md files for INVEST compliance.
For each task, output a table: Task ID | I | N | V | E | S | T | Issues.
Mark each criterion PASS or FAIL with one-line reason.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ttok` | Count tokens in a task file to validate context estimate | `pip install ttok` / https://github.com/simonw/ttok |
| `jq` | Parse task metadata if stored as YAML/JSON frontmatter | system package |
| `ripgrep` | Verify FR-X and AD-X references exist in linked docs | `apt install ripgrep` |
| `dot` (graphviz) | Render dependency graph from task dependency declarations | `apt install graphviz` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Issues + Projects | SaaS | Yes (gh CLI) | Map each TASK_*.md to an issue; labels = wave; milestones = phase |
| Linear | SaaS | Yes (REST API) | Cycles = waves; sub-issues = tasks; native dependency graph |
| Plane (OSS) | OSS | Yes (REST API) | Self-hosted Linear alternative; full API surface |
| Notion | SaaS | Partial | Good for human review of task lists; not ideal for executor agent reads |

## Templates & scripts
See `impl-plan-task-format/README.md` for three complete task examples (simple/normal/complex). The format template is embedded in that README.

Dependency graph generator from task files:
```bash
#!/usr/bin/env bash
# gen-dep-graph.sh FEATURE_DIR
# Outputs DOT format for graphviz
DIR=${1:?usage: gen-dep-graph.sh feature-dir}
echo "digraph tasks {"
for f in "$DIR"/todo/*.md "$DIR"/in-progress/*.md "$DIR"/done/*.md; do
  [ -f "$f" ] || continue
  TASK=$(grep -oP 'TASK-\d+' "$f" | head -1)
  DEPS=$(grep "Depends on:" "$f" | grep -oP 'TASK-\d+')
  for dep in $DEPS; do
    echo "  \"$dep\" -> \"$TASK\";"
  done
done
echo "}"
```

## Best practices
- Always include the full FR-X and AD-X text inline in the task file; the executor agent should not need to load spec.md or design.md during execution
- Use `complexity: complex` only for tasks that genuinely require architecture judgment — most coding tasks are `normal`
- "Technical Notes" should cite the exact file path and pattern (e.g., "Follow error handling in `src/handlers/user.ts` lines 45-67") not generic advice
- Write test acceptance criteria separately from functional AC — use `Tests:` checklist for unit/integration/E2E to ensure test coverage is explicit
- Never assign two complex tasks to the same wave; execution failures on complex tasks create blocking situations for dependent waves

## AI-agent gotchas
- Agents generating task files tend to write "Depends on: None" even when implicit data dependencies exist — validate that database migration tasks precede handler tasks
- Context estimates frequently omit "dependencies" files (files read for pattern matching) — add 10–15k for each dependency task summary the executor needs to read
- AC items written as "passes all tests" or "no errors" are not observable outcomes — require specific HTTP status codes, database state assertions, or measurable values
- `faion-sdd-executor-agent` stops at BLOCKED status; any task requiring an external API key, secret, or manual approval should note this in Technical Notes as a potential blocker
- Human checkpoint before `complexity: complex` tasks that touch auth, payments, or data migrations is not enforced by the executor — must be embedded as an AC item or pre-condition

## References
- https://agileforall.com/new-to-agile-invest-in-good-user-stories/ — INVEST criteria (Bill Wake)
- https://martinfowler.com/bliki/GivenWhenThen.html — Given-When-Then by Martin Fowler
- https://www.mountaingoatsoftware.com/blog/how-to-split-a-user-story — Story splitting patterns
- https://graphviz.org — Graphviz DOT language for dependency graph rendering
- https://github.com/simonw/ttok — Token counting CLI
