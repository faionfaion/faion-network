# Subagent as Context Firewall

**Category:** `mem-` (memory & context)

## The Rule

Use a subagent NOT primarily for parallelism, but as a **context firewall**: a one-way valve that lets a heavy task happen in an isolated context window and returns ONLY a slim summary + references back to the parent.

The parent's context grows by ~500 tokens regardless of how much the subagent read.

## Why It Works

Every token in your main agent's context is a token paid for on every turn. Reading a 30-file codebase to find a bug "uses up" 100K tokens of main context — and they stay there for the rest of the session, taxing every subsequent turn and triggering early compaction.

A subagent has its own fresh context window. It does the heavy reading, finds the bug, and reports back: "Found bug in src/auth/middleware.py:42; cause is missing await. Files reviewed: 30." 25 tokens. The parent never paid for the 100K.

This is how Claude Code, OpenAI Swarm, and LangGraph subgraphs all achieve "deep work without main-context blowup."

## When To Use

- Heavy reading: scanning many files, summarizing a corpus, exploring a codebase
- Task that needs many tool calls but produces a small answer
- Anywhere the *process* of finding the answer is much heavier than the *answer*
- Speculative branches: send a subagent to try approach A; main keeps approach B alive
- Untrusted content: subagent reads attacker-controlled doc, returns sanitized summary

## When NOT To Use

- When the parent needs the FULL details of what the subagent saw — defeats the firewall
- When the work is small enough that main can do it directly (1-2 file reads)
- When subagent latency matters (subagents add round-trip overhead)
- For TRUE parallelism gains — that's a different pattern (multiple subagents in parallel, each firewalled)

## Subagent Output Contract

Define a strict contract on what the subagent returns:

```
class SubagentReport:
    summary: str                       # 3-5 sentences max
    interesting_refs: list[str]        # paths/URLs/IDs the parent might want
    follow_up_questions: list[str]     # if anything unclear
    confidence: Literal["high", "medium", "low"]
```

Forbid the subagent from returning raw content. The parent re-reads if it cares.

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Subagent returns 50K tokens of "everything I found" | Hard cap output at 500 tokens; force the schema to be summary + refs only |
| Parent re-passes the subagent's output to ANOTHER subagent without slimming | Each subagent boundary should slim, not preserve, the previous content |
| Spawn a subagent for a 1-file question | Diminishing returns; subagent overhead > main reading the file |
| Multiple subagents share state via shared context | Defeats firewall — use shared FILES instead |
| Subagent crashes/timeouts swallow the parent's question | Always return *some* result with `confidence: low` rather than nothing |

## Composition

- + **file-reference-passing**: subagent reports refs, not content — the firewall is *what* you put through it
- + **weak-model-preselection**: subagent itself uses a cheap model first; only escalates to strong model on selected items
- + **schema-field-order**: subagent's report schema follows reasoning-before-answer

## Implementation Notes

- Set `system_prompt` of the subagent EXPLICITLY: "You are an investigation subagent. Return only summary + paths. The parent will re-read what it needs."
- Cap the subagent's max_tokens — subagent budgets should be a fraction of the parent's
- Log subagent invocations centrally — these are your debug breadcrumbs
- For long subagent runs, consider streaming intermediate `<task-notification>` so the parent can monitor

## References

- [Anthropic Engineering — Multi-agent research system](https://www.anthropic.com/research/built-multi-agent-research-system)
- [Claude Code subagents docs](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [LangGraph supervisor + subgraph patterns](https://langchain-ai.github.io/langgraph/how-tos/multi_agent/)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
