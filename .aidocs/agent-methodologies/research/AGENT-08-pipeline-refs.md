# AGENT-08 — Pipeline & Sub-task Delegation: References Over Content

**Subagent:** 8 of 10 — Brainstorm research
**Focus:** Pipeline tricks where each step passes REFERENCES (paths/IDs/URLs/doc-ids) instead of full content. Subagent isolation, map-reduce, lazy-loading, file-system-as-memory, manifest-then-fetch, plan-as-state, pointer trees.
**Date:** 2026-04-25
**State of the art:** April 2026.

---

## Summary

In April 2026 the dominant paradigm is **"effective context > raw context"**: subagents return small structured answers (paths, IDs, deltas) and the orchestrator passes those references — never raw payloads — into the next pipeline step. The filesystem (or a content store keyed by ID) acts as infinite, restorable memory; the LLM context holds only what is needed *right now* to make the next decision.

---

## Methodologies

### M-PL-01 — Subagent Isolation: Final-Answer-Only Channel

**Rule.** Spawn each delegated task as a fresh subagent with its own context window. The parent receives **only the subagent's final message**; intermediate tool calls, file reads, scratch reasoning never enter the parent context. The single channel from parent → subagent is the prompt string; the single channel back is the final answer (which should be a list of references, not content).

**Cite.** Anthropic Claude Code "Subagents" docs and Agent SDK docs (https://code.claude.com/docs/en/sub-agents, https://platform.claude.com/docs/en/agent-sdk/subagents). Anthropic multi-agent research system writeup (https://www.anthropic.com/engineering/multi-agent-research-system) reports 90.2% improvement over single-agent baseline.

**When to use.** Any time a sub-task involves browsing/reading large amounts of material the parent does not need to see (codebase grep, multi-file analysis, doc skim).
**When NOT.** Tightly coupled iterative reasoning where parent and child must share intermediate state — use a "fork" (shared context) instead.

**Example.**
```
Parent prompt to subagent: "Find all Django models that override save(). Return ONLY a JSON list of {file_path, line, model_name}. Do NOT include code."
Subagent burns 80k tokens grepping/reading → returns 600 bytes of references.
Parent context grows by 600 bytes, not 80k.
```

---

### M-PL-02 — Manifest-Then-Fetch (Two-Phase Tool Result)

**Rule.** Tools return a **ToolResult** object: `{execution_id, preview (first ~200 chars or metadata), size_tokens}`. The full payload is stored externally. The agent decides — based on the preview alone — whether to call `get_full_result(execution_id)` to load the body. Default behavior is "preview-only".

**Cite.** Agno feature request (https://github.com/agno-agi/agno/issues/5534) and Databricks agent system design patterns (https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns).

**When to use.** Tools with high payload variance (web fetch, SQL, log search). Median call doesn't need the full body, but ~10% do.
**When NOT.** When every call result is small (<1k tokens) — overhead of the manifest dance isn't worth it.

**Example.**
```
sql_query("SELECT * FROM events WHERE...") →
  {id: "tr_a3f", preview: "12,847 rows; cols: id, ts, user_id, payload", size: 1.8M}
Agent decides: "I only need count" → never fetches body.
```

---

### M-PL-03 — Filesystem-as-Memory (Reversible Compression)

**Rule.** Instead of keeping tool outputs in the message history, write them to disk and replace the message with `{file_path, summary}`. The agent can `read_file(path)` to restore the content if needed later. Compression must be **reversible**: drop the body but always preserve enough of an identifier (URL, path, doc-id) to re-fetch.

**Cite.** Manus blog "Context Engineering for AI Agents" (https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus); LangChain "How agents can use filesystems for context engineering" (https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering); rlancemartin agent design patterns (https://rlancemartin.github.io/2026/01/09/agent_design/).

**When to use.** Long-running agents (50+ tool calls), web research, codebase exploration. Tasks that produce large artifacts the agent re-touches sporadically.
**When NOT.** Single-shot Q&A, stateless API. Don't introduce a filesystem for a 3-step task.

**Example.**
```
fetch("https://faion.net/article/x") → writes /tmp/agent_cache/article_x.md (40k tokens)
Message becomes: "Fetched article_x → /tmp/agent_cache/article_x.md (40k tokens, about model training)"
Agent later: read_file(/tmp/agent_cache/article_x.md, lines=200-260) — only the slice it needs.
```

---

### M-PL-04 — Auto-Eviction at Token Threshold (Deep Agents Pattern)

**Rule.** Wrap the tool runtime so any single tool result exceeding **N tokens (e.g. 20,000)** is auto-written to disk and substituted with `{path, first_10_lines_preview}` before the LLM ever sees it. This is M-PL-03 enforced by middleware, not by the LLM's discretion.

**Cite.** LangChain Deep Agents Filesystem Middleware (https://deepwiki.com/langchain-ai/deepagentsjs/5.2-filesystem-middleware); LangChain "Context Management for Deep Agents" (https://www.langchain.com/blog/context-management-for-deepagents). Knob is `toolTokenLimitBeforeEvict`.

**When to use.** When you can't trust the LLM to self-restrain (and you can't — small models leak large payloads into context all the time). Default-on for any tool that can hit a remote service.
**When NOT.** Streaming/realtime tools where the agent acts on each chunk immediately and won't re-read.

**Example.** `npm install` log → 35k tokens → middleware writes `.agent/logs/npm_3491.log`, returns `{path: ".agent/logs/npm_3491.log", preview: "added 1247 packages...", evicted: true}`.

---

### M-PL-05 — Map-Reduce Over Documents (Parallel Path-Returning Workers)

**Rule.** Split N docs across N parallel subagents. Each subagent processes one doc and returns ONLY `{doc_id, verdict, evidence_path[]}`. The reducer agent reads only the verdicts (and selectively pulls evidence by path when needed). Recurse if the combined verdict list still exceeds the reducer's effective context.

**Cite.** Google Cloud "Long document summarization with workflows and Gemini" (https://cloud.google.com/blog/products/ai-machine-learning/long-document-summarization-with-workflows-and-gemini-models); LangChain summarization tutorial (https://python.langchain.com/docs/tutorials/summarization/); LLM×MapReduce paper (https://arxiv.org/html/2410.09342v1).

**When to use.** N independent items (docs, files, PRs, support tickets) where work fans out cleanly.
**When NOT.** When items have cross-references and a worker must see siblings to reason — use M-PL-08 (pointer tree) instead.

**Example.**
```
Parent: "Classify these 200 PRs as bug/feat/chore. Return JSON list of {pr_number, label}."
20 workers × 10 PRs each → returns 200 lines × ~40 bytes = 8KB.
Parent never loads PR diffs. Reducer prints summary table.
```

---

### M-PL-06 — Recursive Summarization (Tree-Reduce)

**Rule.** When a flat reduce step still exceeds context, recurse: group K summaries → re-summarize → group K of those → re-summarize. Build a **summary tree** bottom-up. At query time, the agent can drill from root → leaves through pointers.

**Cite.** RAPTOR paper (https://arxiv.org/abs/2401.18059, https://github.com/parthsarthi03/raptor) — recursive abstractive processing for tree-organized retrieval; LangChain map-reduce summarization recursion docs (https://python.langchain.com/docs/tutorials/summarization/).

**When to use.** Document corpus too large for any single map-reduce pass; QA over books, codebases, research libraries. Improves QuALITY benchmark by +20% absolute when paired with GPT-4 (RAPTOR paper).
**When NOT.** Small corpora (<50k tokens total) — flat summarization is fine.

**Example.** 800-page book → 800 leaf summaries (1 per page) → 80 mid summaries (10:1) → 8 high summaries → 1 root. Agent answers a thematic question by reading root + drilling 2 levels.

---

### M-PL-07 — Pointer Tree / Vectorless Tree-Search Retrieval (PageIndex)

**Rule.** Build a hierarchical **table-of-contents tree** of a long document where each node carries a title/summary and a pointer (page-range, section-id) to its children. The LLM **navigates** the tree like a human reading a TOC — never embeds, never searches by similarity. It returns leaf-pointers; downstream code fetches the leaf bodies.

**Cite.** PageIndex by VectifyAI (https://github.com/VectifyAI/PageIndex); VentureBeat "tree search framework hits 98.7% on documents where vector search fails" (https://venturebeat.com/infrastructure/this-tree-search-framework-hits-98-7-on-documents-where-vector-search-fails).

**When to use.** Single very-long document with structure (legal contracts, technical manuals, books) where chunk-and-embed misses cross-section reasoning.
**When NOT.** Many short heterogeneous docs — vector RAG or BM25 still wins.

**Example.** 600-page regulation → tree of 12 chapters × 8 sections × 6 subsections. Agent for query "what about cross-border data transfer?" navigates: root → Ch.4 (Data) → §4.3 (Transfers) → returns `{section_id: "4.3.2", pages: 187-194}`. Downstream loads only those 8 pages.

---

### M-PL-08 — Tools That Return Tool-IDs (Recursive Tool Discovery)

**Rule.** For agents with hundreds of tools, don't dump them all into the system prompt. Use a **tool-search tool** that returns *handles* (names + JSON schemas) on demand. The agent first asks "what tools exist for X?" → receives 3 handles → calls one of them. Schemas only enter context when fetched.

**Cite.** LlamaIndex ObjectIndex (https://docs.llamaindex.ai/en/stable/examples/objects/object_index/, https://docs.llamaindex.ai/en/v0.10.19/examples/objects/object_index.html); Anthropic Skills system uses progressive disclosure of tools/skills (https://docs.anthropic.com/en/docs/claude-code/skills).

**When to use.** Tool count > ~30. Agents spanning many MCP servers. Plugin ecosystems where new tools appear at runtime.
**When NOT.** Fixed small tool set (≤10) — eager registration is simpler and faster.

**Example.** Claude Code's `ToolSearch` returns deferred tool schemas: agent asks `select:WebSearch,Read` → schemas are injected into the assistant's tool list mid-conversation. (This very file uses that pattern; ~70 tools never loaded.)

---

### M-PL-09 — Plan-Document-as-State (.aidocs / TODO.md / plan.md)

**Rule.** The pipeline's *plan* lives on disk as a markdown file the agent reads-and-writes. Each task transition (`todo → in-progress → done`) is a file edit. The plan is **the source of truth** across sessions; the LLM context is a temporary view of the current task. New conversation? Just `read_file(plan.md)` and resume.

**Cite.** Nick Tune "Minimalist Claude Code Task Management Workflow" (https://medium.com/nick-tune-tech-strategy-blog/minimalist-claude-code-task-management-workflow-7b7bdcbc4cc1); Arthur Clune "Claude Code — The Missing Manual" (https://clune.org/posts/claude-code-manual/); PAACE plan-aware framework (https://arxiv.org/pdf/2512.16970); Agent Factory Tasks System (https://agentfactory.panaversity.org/docs/General-Agents-Foundations/context-engineering/tasks-system).

**When to use.** Multi-session work, refactors, SDD-style feature delivery. Anything where context will be cleared at least once before completion.
**When NOT.** One-shot tasks completing in a single context window.

**Example.** NERO uses `.aidocs/features/in-progress/F012-podcast/implementation-plan.md`. `/continue-feature F012` re-loads the plan, picks the first `in-progress` task, executes. Plan is updated as the only side-effect on terminate.

---

### M-PL-10 — Compaction Templates That Preserve References, Drop Reasoning

**Rule.** When the agent loop must compact a long conversation, the compaction prompt MUST instruct: *always preserve* file paths, function names, error messages, decisions, URLs, IDs; *always drop* intermediate reasoning and verbatim tool output. The compacted summary is itself a manifest of references.

**Cite.** Anthropic Claude Cookbook "Context engineering: memory, compaction, and tool clearing" (https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools); lethain "Building an internal agent: context window compaction" (https://lethain.com/agents-context-compaction/); opencode context compaction docs (https://deepwiki.com/sst/opencode/2.4-context-management-and-compaction).

**When to use.** Always, in any agent that survives more than ~30 turns. Hard-code the schema; do not let the LLM invent compaction format.
**When NOT.** Stateless single-turn agents.

**Example.** Compact-template output:
```yaml
goal: refactor auth module
files_touched: [src/auth/login.py:42, src/auth/jwt.py:88-110]
decisions: [chose RS256 over HS256, see ADR-007]
open_errors: [test_login_invalid_pw fails — see /tmp/pytest_4882.log]
next: implement refresh token rotation
```
No code. No reasoning. Just pointers.

---

### M-PL-11 — Handoff Payload = ID + Minimal Metadata (Multi-Agent Routing)

**Rule.** When agent A hands off to agent B, the payload is `{task_id, target_agent, minimal_decision_metadata}`, not the full conversation. B reads task state from the shared store using `task_id`. Routing supervisors return structured `SupervisorDecision` objects, not message histories.

**Cite.** OpenAI Agents SDK Handoffs (https://openai.github.io/openai-agents-python/handoffs/); LangChain handoffs docs (https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs); Towards Data Science "How Agent Handoffs Work" (https://towardsdatascience.com/how-agent-handoffs-work-in-multi-agent-systems/).

**When to use.** Multi-agent meshes, supervisor/worker topologies, role-specialized agents (researcher → writer → editor).
**When NOT.** Monolithic single-agent loops — adds infrastructure for no gain.

**Example.** NERO mesh: classifier returns `{route: "neromedia", task_id: "t_8821"}`. The neromedia worker pulls full input from `/srv/nero/queue/t_8821.json`. The classifier's context never carries the article body.

---

### M-PL-12 — Effective Context Discipline (the meta-principle)

**Rule.** Treat the *advertised* context window as a hardware spec, not a usable resource. The **Maximum Effective Context Window (MECW)** — where the model still maintains accuracy — is often **10×–100× smaller** than advertised. Pipeline design must minimize *effective* context per step, not raw context. Every M-PL-01 through M-PL-11 is in service of this rule.

**Cite.** "Context Is What You Need: The Maximum Effective Context Window for Real World Limits of LLMs" (https://arxiv.org/abs/2509.21361); JetBrains research "Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents" (https://blog.jetbrains.com/research/2025/12/efficient-context-management/); "lost in the middle" effect documented across all major models.

**When to use.** Always. This is the lens through which all other methodologies are evaluated.
**When NOT.** Never; even a 1M-token model degrades fast past ~100k of relevant content.

**Example.** Two pipelines for the same task:
- **Bad:** dump 800k tokens of code → ask Sonnet 4.7 to find all bugs. Accuracy: ~40%, latency: 90s.
- **Good:** map-reduce (M-PL-05) over 200 files in parallel subagents (M-PL-01) returning paths only, reducer reads ~12k tokens of references and drills (M-PL-02) into the 6 suspicious files. Accuracy: ~85%, latency: 25s, cost: 1/3.
The 1M-context model is not the answer; the architecture is.

---

## Mapping

| ID | Family | Mnemonic |
|----|--------|----------|
| M-PL-01 | pipeline | subagent-isolation |
| M-PL-02 | pipeline | manifest-fetch |
| M-MEM-03 | memory | filesystem-as-memory |
| M-PL-04 | pipeline | auto-evict-threshold |
| M-PL-05 | pipeline | map-reduce-paths |
| M-PL-06 | pipeline | recursive-summarize |
| M-PL-07 | pipeline | pointer-tree |
| M-PL-08 | pipeline | tools-return-tool-ids |
| M-MEM-09 | memory | plan-as-state |
| M-PL-10 | pipeline | compaction-references |
| M-PL-11 | pipeline | handoff-id-only |
| M-PL-12 | meta | effective-context |

---

## Sources

- [Anthropic Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Agent SDK Subagents](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic Cookbook orchestrator-workers](https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/orchestrator_workers.ipynb)
- [Anthropic context engineering cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [LangChain filesystems for context engineering](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering)
- [LangChain Deep Agents context management](https://www.langchain.com/blog/context-management-for-deepagents)
- [Deep Agents Filesystem Middleware](https://deepwiki.com/langchain-ai/deepagentsjs/5.2-filesystem-middleware)
- [LangChain summarization tutorial (map-reduce)](https://python.langchain.com/docs/tutorials/summarization/)
- [Google Cloud long document summarization](https://cloud.google.com/blog/products/ai-machine-learning/long-document-summarization-with-workflows-and-gemini-models)
- [LLM×MapReduce paper](https://arxiv.org/html/2410.09342v1)
- [RAPTOR paper](https://arxiv.org/abs/2401.18059)
- [RAPTOR implementation](https://github.com/parthsarthi03/raptor)
- [PageIndex repository](https://github.com/VectifyAI/PageIndex)
- [VentureBeat tree-search retrieval](https://venturebeat.com/infrastructure/this-tree-search-framework-hits-98-7-on-documents-where-vector-search-fails)
- [LlamaIndex ObjectIndex](https://docs.llamaindex.ai/en/stable/examples/objects/object_index/)
- [Agno lazy tool result feature request](https://github.com/agno-agi/agno/issues/5534)
- [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [LangChain handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)
- [Towards Data Science agent handoffs](https://towardsdatascience.com/how-agent-handoffs-work-in-multi-agent-systems/)
- [rlancemartin agent design patterns 2026](https://rlancemartin.github.io/2026/01/09/agent_design/)
- [PAACE plan-aware automated context engineering](https://arxiv.org/pdf/2512.16970)
- [Agent Factory Tasks System](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/context-engineering/tasks-system)
- [Nick Tune Claude Code task management](https://medium.com/nick-tune-tech-strategy-blog/minimalist-claude-code-task-management-workflow-7b7bdcbc4cc1)
- [Arthur Clune Claude Code Missing Manual](https://clune.org/posts/claude-code-manual/)
- [lethain context window compaction](https://lethain.com/agents-context-compaction/)
- [opencode context management](https://deepwiki.com/sst/opencode/2.4-context-management-and-compaction)
- [Maximum Effective Context Window paper](https://arxiv.org/abs/2509.21361)
- [JetBrains efficient context management](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)
- [Databricks agent system design patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns)
- [FlowHunt context offloading and state management](https://www.flowhunt.io/blog/advanced-ai-agents-with-file-access-mastering-context-offloading-and-state-management/)
