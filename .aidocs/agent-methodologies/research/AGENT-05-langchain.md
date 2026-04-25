# AGENT-05: LangChain + LangGraph + LlamaIndex Patterns (April 2026)

**Summary L1:** Patterns that survive framework migration: state-machine graph + checkpointer for durability, deterministic-first routing, supervisor with handoff-only tools, Command for fused state+route, Send for map-reduce, subgraph context isolation, file-system offload at 85% context, Generator-Critic, trajectory evals, multi-mode streaming.
**Summary L2:** LangGraph's value is the runtime primitives (checkpointer, Send, Command, interrupt, store), not the agent abstractions. Treat the graph as a durable state machine, push routing to deterministic code wherever ambiguity is low, and reserve LLMs for the irreducibly fuzzy hops. LlamaIndex AgentWorkflow is the same pattern with an event-bus naming convention; ports cleanly to Temporal/Restate when you outgrow LangGraph's runtime.

---

## M1. Checkpoint after every super-step, not every node

**Rule.** Compile every production graph with a persistent checkpointer (Postgres/DynamoDB/Redis), pass `thread_id` on every invoke, and rely on LangGraph's per-super-step write semantics. Never run an agent in production with `MemorySaver` — switch the backend, not the graph code. Set durability to `"sync"` for any graph that touches money, identity, or external side effects; use `"async"` only for read-only research agents.

**Source.** [Durable execution — docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/durable-execution), [Build durable AI agents with LangGraph and DynamoDB — AWS](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).

**Use when:** Long-running agents, anything with HITL, anything that calls a paid external API. The `thread_id` is your conversation primary key.
**Skip when:** Pure stateless one-shots (classification, single-tool RAG) — the checkpoint write is wasted I/O.

**Maps to:** `mem-` (thread state = short-term memory), `pl-` (resume from failure replaces re-planning), `eval-` (replay from any super-step is the debugger), `cost-` (cheaper than re-running half a multi-step trace).

---

## M2. Supervisor must not hold worker tools — only `route_to(name, instructions)`

**Rule.** The supervisor agent gets exactly one tool surface: handoff/route tools that take a target name and a free-text instruction payload. It never holds the workers' tools. This (a) cuts supervisor token bloat 30–50% because tool schemas dominate the system prompt, (b) prevents the supervisor from "helping" by doing the worker's job badly, and (c) makes routing accuracy auditable as a single classification metric. Use `add_handoff_back_messages=True` so the worker can return control with a structured envelope.

**Source.** [langgraph-supervisor-py — github.com/langchain-ai](https://github.com/langchain-ai/langgraph-supervisor-py), [Multi-Agent Orchestration: Supervisor vs Swarm](https://dev.to/focused_dot_io/multi-agent-orchestration-in-langgraph-supervisor-vs-swarm-tradeoffs-and-architecture-1b7e).

**Use when:** ≥3 specialized workers, clear domain boundaries, you can describe each worker in one sentence.
**Skip when:** 2 workers (use a conditional edge), or workers overlap heavily (use swarm and let them hand off peer-to-peer).

**Maps to:** `mm-` (clean orchestrator-worker contract), `tu-` (tool surface area discipline), `cost-` (token reduction), `pl-` (supervisor = planner, workers = executors).

---

## M3. Deterministic router first hop, LLM router only above ambiguity threshold

**Rule.** Front every multi-agent graph with a deterministic classifier (regex → keyword → small encoder, in that order of escalation). Send the request to the LLM router only when the cheap layer returns confidence < τ (typically 0.7) or `None`. Wire it as a conditional edge that branches `regex_match → direct_node | semantic_match → direct_node | fallback → llm_router`. Production deployments routinely report 10-33× cost reduction and 95% accuracy retention this way.

**Source.** [How I Cut My AI Agent API Bill 10-33x With Deterministic Routing](https://www.roborhythms.com/cut-ai-agent-api-costs/), [Router — docs.langchain.com](https://docs.langchain.com/oss/python/langchain/multi-agent/router), [Doing More with Less: Routing Strategies survey (arxiv 2502.00409)](https://arxiv.org/html/2502.00409v2).

**Use when:** High-volume traffic with a long tail of simple intents (FAQ, status, lookup). Classifier accuracy ≥90% on the head distribution.
**Skip when:** Truly free-form open-ended queries where the head is <30% of traffic — the classifier will misroute more than it saves.

**Maps to:** `cost-` (the headline win), `lp-` (latency win is bigger than cost win on cached classifiers), `so-` (deterministic-where-possible orthogonality), `eval-` (classifier accuracy is a single trackable metric).

---

## M4. Use `Command` for fused state+goto, conditional edges for everything else

**Rule.** Return a `Command(update=..., goto=...)` from a node only when the routing decision is data-dependent on the same state mutation. Use static `add_edge` for fixed flow, `add_conditional_edges` for routing that depends on state but doesn't mutate it. Mixing the three idioms in one graph is fine; using `Command` everywhere makes the graph topology un-graphable and breaks LangSmith's visualizer. Reserve `Command(graph=Command.PARENT)` exclusively for handoff tools in subgraph-as-agent setups.

**Source.** [Command: A new tool for multi-agent architectures — langchain.com/blog](https://www.langchain.com/blog/command-a-new-tool-for-multi-agent-architectures-in-langgraph), [Handoffs — docs.langchain.com](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs).

**Use when:** Tool nodes that decide the next agent based on tool output (e.g. classifier tool → branch). Handoff tools in swarm.
**Skip when:** The routing predicate is pure (no state write needed) — conditional edge is more readable and statically analyzable.

**Maps to:** `so-` (control-flow primitive), `mm-` (handoff mechanics), `tu-` (tools that route).

---

## M5. Send API for map-reduce; one reducer per parallel branch type

**Rule.** Dynamic fan-out (variable N parallel workers) uses `Send(node, payload)` returned from a router node. Aggregation requires the target state field to be annotated with a reducer (`Annotated[list, operator.add]` or a custom merge). Any failure in any Send branch fails the entire super-step atomically — design Send children to be idempotent and retryable, and never use Send for branches with side effects you can't replay. Cap Send fan-out (≤20 concurrent) to avoid rate-limit cliffs.

**Source.** [Use the graph API — docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/use-graph-api), [Map-Reduce with Send() in LangGraph — Medium](https://medium.com/ai-engineering-bootcamp/map-reduce-with-the-send-api-in-langgraph-29b92078b47d), [Scaling LangGraph Agents: Parallelization, Subgraphs, Map-Reduce](https://aipractitioner.substack.com/p/scaling-langgraph-agents-parallelization).

**Use when:** Per-document scoring, multi-source RAG fan-out, multi-candidate generation+vote, batch tool calls over a list.
**Skip when:** Fixed-N parallel (use static fan-out edges), or branches that mutate shared external state (use a queue + workers, not Send).

**Maps to:** `pl-` (planner emits Sends), `lp-` (parallelism is the latency tool), `cost-` (smaller/cheaper model per branch), `tu-` (parallel tool dispatch).

---

## M6. Subgraph-as-agent with private message history, mapped state at boundary

**Rule.** Each worker agent gets its own subgraph compiled with its own checkpointer. The parent passes only a task brief on entry and receives only a structured result on exit — never share the parent's `messages` list with the worker. Implement explicit `state_in: ParentState -> WorkerState` and `state_out: WorkerState -> ParentState` adapter functions inside the wrapping node. This contains context bloat (workers don't see siblings' transcripts), enables namespace-isolated checkpoints, and makes worker swap-out trivial.

**Source.** [Subgraphs — docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/use-subgraphs), [LangGraph Best Practices — swarnendu.de](https://www.swarnendu.de/blog/langgraph-best-practices/).

**Use when:** Multi-agent systems with ≥2 workers, especially when worker prompts/models differ. Always when a worker is itself iterative.
**Skip when:** Single-agent ReAct loop — subgraphs add ceremony with no isolation benefit.

**Maps to:** `mm-` (worker isolation), `mem-` (per-worker memory namespace), `cost-` (smaller worker context), `eval-` (per-worker trajectory).

---

## M7. Plan-and-Execute for known shape, ReAct for exploration, never hybridize the outer loop

**Rule.** Pick one outer loop per agent: Plan-and-Execute when the task shape is known and >3 steps (research reports, codegen, multi-stage ETL); ReAct when the next step depends on the last observation in unpredictable ways (debugging, exploratory analysis, customer support). You may nest a ReAct loop inside a single Plan-and-Execute step, but never fuse them at the top level — that produces the worst of both: the planner can't commit and the executor can't recover. Plan-and-Execute lets you route sub-tasks to cheaper models (the planner is the only call needing the frontier model), typical 40-60% cost cut versus pure ReAct.

**Source.** [Plan-and-Execute Agents — langchain.com/blog](https://www.langchain.com/blog/planning-agents), [ReAct vs Plan-and-Execute — dev.to](https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9).

**Use when:** Plan-and-Execute for >3 steps with a stable schema; ReAct for ≤5 turns with high environmental noise.
**Skip when:** Single tool, single answer — neither loop, just a structured tool call.

**Maps to:** `pl-` (the planning axis itself), `cost-` (model tiering), `lp-` (Plan-and-Execute parallelizes steps), `eval-` (plan adherence is its own metric).

---

## M8. Generator-Critic loop with hard iteration cap and "improvement delta" exit

**Rule.** Wrap any open-ended generation node (write, code, summarize) in a Generator → Critic → Generator loop. The critic must return both a structured `score` and `should_continue: bool`. Exit when `should_continue=False`, when score plateau (delta < ε for 2 iterations), or at hard cap (default 3). Never let the loop run unbounded — the second iteration captures most of the gain, the fifth wastes tokens. Use a smaller/cheaper model as the critic when the criterion is rubric-shaped (style, format, completeness); use the same-tier model only for correctness critique (code, math).

**Source.** [Reflection Agents — langchain.com/blog](https://blog.langchain.com/reflection-agents/), [LangGraph: self-correcting RAG agent](https://learnopencv.com/langgraph-self-correcting-agent-code-generation/).

**Use when:** Codegen, copywriting, structured extraction with quality bar, RAG answer drafting.
**Skip when:** Latency-critical paths (chat completions) — the second pass doubles wall time. Tool-calling agents where the tool result is the ground truth.

**Maps to:** `eval-` (critic IS an inline evaluator), `pl-` (critic feedback shapes next plan), `cost-` (smaller critic model), `mem-` (store critique for prompt-improvement loop).

---

## M9. Offload context to a virtual filesystem at 85% window; summarize only as last resort

**Rule.** Adopt the Deep Agents pattern: give every long-running agent a `write_file` / `read_file` / `ls` tool surface backed by either real disk, S3, or a state-dict virtual FS. Offload large tool results (search dumps, full documents, raw API responses) immediately and pass back only filenames + short snippets. Trigger LLM-based summarization of the conversation only when context hits ~85% AND there's nothing left to offload — summarization loses information, file offload doesn't. Persist the FS to the same store as the checkpointer so resume-after-failure recovers files too.

**Source.** [Deep Agents overview — docs.langchain.com](https://docs.langchain.com/oss/python/deepagents/overview), [langchain-ai/deepagents — github](https://github.com/langchain-ai/deepagents), [Anatomy of an Agent Harness — Daily Dose of DS](https://blog.dailydoseofds.com/p/the-anatomy-of-an-agent-harness).

**Use when:** Research agents, codegen across many files, any task that touches >5 documents or runs >20 turns.
**Skip when:** Short chat (<10 turns), single-doc QA — the FS abstraction is ceremony.

**Maps to:** `mem-` (FS = working memory), `cost-` (don't pay for re-tokenizing huge tool results), `tu-` (the FS tools), `pl-` (TODO file becomes the plan).

---

## M10. Streaming: use `updates` mode for UI, `messages` for token UX, `debug` only in dev

**Rule.** Default to `stream_mode="updates"` for production frontends — it sends only state diffs, ~5-10× less bandwidth than `values`. Layer `messages` on top when the UI shows token-level streaming (combined: `stream_mode=["updates", "messages"]`). Reserve `debug` mode for local dev / staging traces; never enable it on customer traffic, it logs full state and tool I/O. For HITL, the `interrupt` event surfaces in the `updates` stream — your client must handle pause/resume tokens, not just text deltas.

**Source.** [Streaming — docs.langchain.com](https://docs.langchain.com/oss/javascript/langgraph/streaming), [LangGraph Streaming 101: 5 Modes — dev.to](https://dev.to/sreeni5018/langgraph-streaming-101-5-modes-to-build-responsive-ai-applications-4p3f).

**Use when:** Any user-facing chat or agent UI. Always.
**Skip when:** Server-to-server batch jobs (use `.invoke`).

**Maps to:** `cli-` (streaming UX is the chat protocol), `lp-` (perceived latency), `eval-` (debug mode = trace pipe), `mm-` (cross-agent step visibility).

---

## M11. Trajectory evals over endpoint evals; LangSmith multi-turn for goal completion

**Rule.** End-to-end answer correctness is the lagging indicator. Evaluate trajectories: tool-call sequence match, planning coherence, off-topic step rate, retry count, escalation rate. Use `agentevals` ready-made evaluators against an expected trajectory for golden flows; layer LLM-as-judge for the open-ended majority. For chat agents, trajectory eval per turn is insufficient — run multi-turn evals that score whether the user's underlying goal was met across the whole conversation. Wire CI to fail on regression in (a) tool-call accuracy and (b) average turns-to-resolution.

**Source.** [agentevals — github.com/langchain-ai](https://github.com/langchain-ai/agentevals), [Evaluate a complex agent — docs.langchain.com](https://docs.langchain.com/langsmith/evaluate-complex-agent), [Insights Agent and Multi-turn Evals — blog.langchain.com](https://blog.langchain.com/insights-agent-multiturn-evals-langsmith/), [Evaluating Deep Agents](https://blog.langchain.com/evaluating-deep-agents-our-learnings/).

**Use when:** Always, from day 1. Trajectory eval surfaces routing bugs that endpoint eval hides behind a "good enough" answer.
**Skip when:** Stateless one-shot classifiers — endpoint accuracy is sufficient.

**Maps to:** `eval-` (the spine), `pl-` (plan adherence as a metric), `mm-` (handoff correctness), `cost-` (token-per-resolved-task is the unit cost).

---

## M12. MCP tools wrapped via `langchain-mcp-adapters`; one MultiServerMCPClient per process

**Rule.** Don't hand-write tool wrappers for external services that publish an MCP server — use `langchain-mcp-adapters` to convert MCP tools to LangChain tools at startup. Instantiate a single `MultiServerMCPClient` per process and inject the resulting tool list into agents; do not re-establish stdio connections per request. For LangGraph Platform deployments, the MCP endpoint is automatically exposed — your graph becomes consumable by any MCP client (Claude Desktop, Cursor, IDEs) for free.

**Source.** [langchain-mcp-adapters — github.com/langchain-ai](https://github.com/langchain-ai/langchain-mcp-adapters), [MCP Adapters announcement — changelog.langchain.com](https://changelog.langchain.com/announcements/mcp-adapters-for-langchain-and-langgraph), [MCP endpoint in Agent Server — docs.langchain.com](https://docs.langchain.com/langsmith/server-mcp).

**Use when:** Tools live in third-party systems already exposing MCP (Notion, Slack, GitHub, Figma, Linear). Cross-team tool sharing.
**Skip when:** All tools are first-party Python functions in the same repo — MCP adds a serialization hop with no benefit.

**Maps to:** `mcp-` (the entire purpose), `tu-` (tool surface), `so-` (tool transport orthogonal to agent logic), `cost-` (avoid re-implementing tool clients).

---

## Cross-cutting takeaways (framework-portable)

1. **Graph-as-state-machine** beats agent-as-string-of-prompts — port the topology, not the framework.
2. **Checkpointer + thread_id** is the single most portable abstraction; identical concept in Temporal, Restate, Inngest.
3. **Handoff payloads are a contract** — versioning them like an API survives any orchestrator swap.
4. **Trajectory evals** outlive the framework; persist trajectories as JSON, not framework-specific objects.
5. **Deterministic-first** routing is a meta-rule — applies whether you use LangGraph, Pydantic-AI, OpenAI Agents SDK, or roll your own.
