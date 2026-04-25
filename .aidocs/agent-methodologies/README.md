# Agent Methodologies — Research & Curation

**Goal:** Collect 50 most relevant, high-leverage methodologies for building AI agents.
Output: methodologies in `geek/ai/ai-agents/` + matching articles in `faion-net-fe/content/knowledge/{agents,llm-integration,prompting}/`.

## Files

| File | Purpose |
|------|---------|
| `state.json` | Counter, target, last-updated, current cycle |
| `methodologies.jsonl` | One line per accepted methodology (id, slug, category, source) |
| `candidates.md` | Queue of brainstormed candidates (not yet accepted) |
| `sources.md` | Bibliography (URLs cited by research subagents) |
| `progress.md` | Append-only log of every loop tick |
| `loop-prompt.md` | The /loop 5m prompt — read by each tick |
| `research/AGENT-NN.md` | Output from each research subagent (1..10) |
| `brainstorm/CYCLE-NN.md` | Each loop-tick brainstorm output |
| `project-mining/` | Tricks extracted from neromedia/pashtelka/etc. |
| `articles-published/MAP.md` | methodology-id → article-id mapping |

## Categories (target distribution)

| Category | Target | Slug prefix |
|----------|--------|-------------|
| Structured-output tricks | 10 | `so-` |
| Multi-model orchestration | 6 | `mm-` |
| Tool-use & function calling | 6 | `tu-` |
| Pipeline & sub-task delegation | 6 | `pl-` |
| Agentic loops & control flow | 5 | `lp-` |
| Memory & context management | 4 | `mem-` |
| CLI vs SDK trade-offs | 3 | `cli-` |
| Evaluation & guardrails | 4 | `eval-` |
| Cost optimization | 3 | `cost-` |
| MCP / external tools | 3 | `mcp-` |
| **Total** | **50** | |

## Acceptance criteria for a methodology

1. Concrete, testable rule (not "use good prompts")
2. Has at least one cited source OR a real example from our projects
3. Identifies *when to use* and *when NOT to*
4. Distinct from already-accepted methodologies (no near-duplicates)
5. Maps to one of the 10 categories
