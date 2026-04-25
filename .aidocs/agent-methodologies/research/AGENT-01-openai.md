# AGENT-01 — OpenAI Agents SDK Methodologies

Focus: OpenAI Agents SDK (Python + JS), Swarm legacy patterns, Responses API,
function calling, structured outputs. State as of April 2026.

---

## M-01: schema-field-order-cot-before-answer
**Category:** so-
**Sources:**
- https://openai.com/index/introducing-structured-outputs-in-the-api/
- https://community.openai.com/t/structured-output-and-element-ordering/1291089
- https://platform.openai.com/docs/guides/structured-outputs
**Rule:** In a structured-output schema, place `reasoning` / `steps` / `evidence`
fields BEFORE the `final_answer` / `decision` field — order in the JSON Schema
controls generation order, and the answer must autoregress over the reasoning
tokens to benefit from them.
**When to use:** Any classification / extraction / decision task where you want
the boost from chain-of-thought without separate "thinking" calls. Especially
useful with `gpt-4.1` / `gpt-5` non-reasoning models where you have to bake CoT
into the schema yourself.
**When NOT to use:** With reasoning models (o3, o4-mini, gpt-5 reasoning) — they
already produce internal reasoning tokens; an extra `reasoning` field just
duplicates and inflates output cost. Also skip for trivial extraction (one
field, no judgment).
**Example/snippet:**
```python
class Verdict(BaseModel):
    # ORDER MATTERS — reasoning is generated first, decision sees it
    reasoning: str
    risk_signals: list[str]
    decision: Literal["approve", "reject", "review"]
```
**Why it works:** OpenAI's constrained decoding emits fields in schema order.
The model is autoregressive — tokens for `decision` are conditioned on every
previously emitted token, including the `reasoning` body. Reverse the order and
`decision` is sampled before the model has "thought" anything, giving you
prior-only behavior.

---

## M-02: required-everything-nullable-for-optional
**Category:** so-
**Sources:**
- https://platform.openai.com/docs/guides/structured-outputs
- https://medium.com/@aviadr1/how-to-fix-openai-structured-outputs-breaking-your-pydantic-models-bdcd896d43bd
- https://engineering.fractional.ai/openai-structured-output-fixes
**Rule:** With `strict: true`, every property must appear in `required` and
`additionalProperties` must be `false`. Emulate optional fields with
`Union[T, None]` (nullable), never with default values or Pydantic
`Optional[T]` without explicit `None` default rewriting.
**When to use:** Any time you set `response_format={"type":"json_schema",
"strict": true}` or pass `output_type=PydanticModel` to the Agents SDK.
Mandatory for parallel-safe tool calls (see M-08).
**When NOT to use:** `strict: false` mode tolerates Pydantic defaults but loses
the 100 % schema guarantee — only acceptable for prototypes.
**Example/snippet:**
```python
# WRONG: strict mode rejects this
class Out(BaseModel):
    name: str
    note: str | None = None     # default → schema validation fails

# RIGHT
class Out(BaseModel):
    name: str
    note: str | None            # null when absent, still required
```
**Why it works:** Strict mode compiles the schema into a finite-state machine
for constrained decoding. Default values and unknown properties make the FSM
ambiguous, so OpenAI rejects the schema at registration time. Nullable + always
required keeps the FSM total.

---

## M-03: handoff-vs-agent-as-tool
**Category:** lp-
**Sources:**
- https://openai.github.io/openai-agents-python/handoffs/
- https://cookbook.openai.com/examples/orchestrating_agents
- https://openai.github.io/openai-agents-python/agents/
**Rule:** Use `handoffs=[specialist]` when the specialist should OWN the rest of
the conversation (replaces the active agent, sees full history). Use
`agent.as_tool(tool_name=..., tool_description=...)` when the orchestrator
should keep control and only borrow the specialist's output as a tool result.
**When to use:**
- Handoff: triage → billing/refund/tech-support style routing where the user
  continues talking to the specialist.
- `as_tool`: orchestrator that needs structured input/output from a specialist
  but composes the final reply itself (translator, summarizer, validator).
**When NOT to use:** Don't use handoff when the orchestrator must aggregate
results from multiple specialists in one turn — handoff transfers control
permanently within the run, you can't "come back". Don't use `as_tool` when the
specialist needs the full conversation history (it only sees the structured
input you pass).
**Example/snippet:**
```python
translator = Agent(name="Translator", instructions="...")
summarizer = Agent(name="Summarizer", instructions="...")

# Orchestrator stays in charge, calls both, composes
orchestrator = Agent(
    name="Lead",
    tools=[
        translator.as_tool(tool_name="translate", tool_description="..."),
        summarizer.as_tool(tool_name="summarize", tool_description="..."),
    ],
)

# vs. permanent handoff
triage = Agent(name="Triage", handoffs=[billing_agent, tech_agent])
```
**Why it works:** Handoff is implemented internally as a tool call named
`transfer_to_<agent>` that swaps the run's current agent — the LLM stops being
"itself" mid-conversation. `as_tool` runs the sub-agent in an isolated nested
Runner.run with its own input, returning a string that the parent uses as a
tool observation. Same primitives, opposite control-flow semantics.

---

## M-04: cheap-guardrail-tripwire-before-expensive-agent
**Category:** cost-
**Sources:**
- https://openai.github.io/openai-agents-python/guardrails/
- https://github.com/openai/openai-guardrails-python
- https://openai.github.io/openai-agents-python/ref/exceptions/
**Rule:** Run `input_guardrails` with a small/fast model (gpt-4.1-mini /
gpt-4o-mini) BEFORE the main agent ever sees the request. If the guardrail
returns `tripwire_triggered=True`, the SDK raises
`InputGuardrailTripwireTriggered` and the expensive agent is never invoked.
**When to use:** Public-facing endpoints (PII screening, jailbreak detection,
off-topic filtering, abuse classification). Anywhere your main loop is on
gpt-5/o3/Opus and 90 %+ of bad requests can be filtered cheaply.
**When NOT to use:** Internal pipelines with trusted callers — guardrails add
latency. Don't put output guardrails on streaming responses unless you're
willing to buffer (output guardrails see the full final output, breaking
true token streaming — open issue #495).
**Example/snippet:**
```python
@input_guardrail
async def offtopic(ctx, agent, msg) -> GuardrailFunctionOutput:
    res = await Runner.run(triage_screener, msg)  # gpt-4.1-mini
    return GuardrailFunctionOutput(
        output_info=res.final_output,
        tripwire_triggered=res.final_output.is_offtopic,
    )

main = Agent(model="gpt-5", input_guardrails=[offtopic], ...)
```
**Why it works:** Guardrails run in parallel to (or before) the main LLM call.
A tripwire short-circuits via exception — zero tokens consumed on the
expensive model, zero tool side-effects. Effectively a 10-100× cost reducer
for adversarial / spammy traffic.

---

## M-05: previous-response-id-for-reasoning-reuse
**Category:** mem-
**Sources:**
- https://cookbook.openai.com/examples/responses_api/reasoning_items
- https://platform.openai.com/docs/guides/conversation-state
- https://developers.openai.com/api/docs/guides/migrate-to-responses
**Rule:** With reasoning models on the Responses API, chain turns via
`previous_response_id` (or pass back full output items including reasoning)
rather than re-sending an OpenAI-format message array. This preserves
reasoning items adjacent to function calls and dramatically cuts thinking
tokens on subsequent turns.
**When to use:** Any multi-turn agent loop on o3 / o4-mini / gpt-5 reasoning
where the model calls tools and you feed results back. Reasoning-item reuse
boosts intelligence, raises cache-hit rate, and reduces cost.
**When NOT to use:** ZDR / store=false enterprise constraints — instead
include `["reasoning.encrypted_content"]` in `include` and pass the encrypted
blob back stateless (see M-12). Don't use with non-reasoning models — there's
nothing to reuse.
**Example/snippet:**
```python
r1 = client.responses.create(model="o4-mini", input=user_msg, tools=tools)
# tool call(s) handled...
r2 = client.responses.create(
    model="o4-mini",
    previous_response_id=r1.id,        # carries reasoning items forward
    input=[{"type":"function_call_output", "call_id":..., "output":...}],
)
```
**Why it works:** o3/o4-mini/gpt-5 produce reasoning items that the SDK
silently drops if you reconstruct messages manually (Chat Completions style).
The Responses API keeps them server-side keyed by id; passing
`previous_response_id` reattaches them. Without this, every turn starts
"thinking from scratch" — measurable 20-40 % regression on agentic benchmarks.

---

## M-06: cache-mcp-tools-list-with-invalidate
**Category:** mcp-
**Sources:**
- https://openai.github.io/openai-agents-python/mcp/
- https://deepwiki.com/openai/openai-agents-python/11.3-mcp-tool-discovery-and-filtering
- https://codesignal.com/learn/courses/efficient-mcp-agent-integration-in-typescript/lessons/tool-caching-for-agents
**Rule:** When attaching an MCP server to an Agent, set `cache_tools_list=True`
and tear down the cache only via `server.invalidate_tools_cache()` on a
known-change signal (deploy hook, version bump, file watch). Never leave it
False in production.
**When to use:** Any remote MCP server, especially HTTP-based or
network-mounted. Default is False because the SDK can't know if your tool
inventory is stable; you do know.
**When NOT to use:** Local development where you're actively editing tool
definitions, OR servers that legitimately advertise dynamic tools (e.g. a
data-source connector that exposes a different tool per dataset). For those,
cache for the duration of one Runner.run by setting it True at run start and
invalidating after.
**Example/snippet:**
```python
mcp = MCPServerStdio(params={...}, cache_tools_list=True)
agent = Agent(name="X", mcp_servers=[mcp])
# on deploy webhook:
mcp.invalidate_tools_cache()
```
**Why it works:** Each Runner.run otherwise calls `list_tools` over MCP at the
start of every turn. Round-trip cost is 50-300 ms per server per turn — for
multi-MCP agents with 10-turn loops that's 5-30 seconds of pure protocol
chatter, none of it billable as model latency but all of it user-visible.

---

## M-07: max-turns-as-circuit-breaker-not-error
**Category:** lp-
**Sources:**
- https://openai.github.io/openai-agents-python/running_agents/
- https://openai.github.io/openai-agents-python/ref/exceptions/
- https://github.com/openai/openai-agents-python/issues/844
**Rule:** Set `max_turns` aggressively (5-10 for retrieval, 15-20 for coding
agents) and CATCH `MaxTurnsExceeded`. On catch, drop into a fallback handler
that summarizes the partial trajectory with a cheaper model and asks the user
to clarify, instead of letting the SDK crash.
**When to use:** Every production Runner.run call. Default of `max_turns=10`
in Python / 25 in JS is a footgun for tool-calling agents that get stuck in
"call search → no results → call search with same query" loops.
**When NOT to use:** Long-running async agents you're explicitly architecting
to run for hundreds of turns (e.g. a coding agent in a sandbox). For those,
use a checkpoint scheme + human approval rather than a single max_turns.
**Example/snippet:**
```python
try:
    res = await Runner.run(agent, user_msg, max_turns=8)
except MaxTurnsExceeded as e:
    summary = await Runner.run(
        recovery_agent,             # cheap model, "summarize what was tried"
        e.run_data.to_input_list(),
        max_turns=1,
    )
    return f"I got stuck. Here's what I tried: {summary.final_output}"
```
**Why it works:** Tool-calling loops fail by silently consuming budget — the
LLM keeps proposing actions because each tool result still looks like
"progress" to it. A hard cap is the only deterministic stop. Catching the
exception (instead of letting it bubble) preserves the partial trace for
debugging AND gives the user a graceful answer instead of a 500.

---

## M-08: disable-parallel-tool-calls-when-strict-matters
**Category:** tu-
**Sources:**
- https://platform.openai.com/docs/guides/function-calling
- https://github.com/openai/openai-agents-python/issues/791
- https://community.openai.com/t/what-models-support-parallel-tool-calls-and-when-to-use-it/1310788
**Rule:** Set `parallel_tool_calls=False` on `ModelSettings` whenever you
depend on `strict: true` schemas for tool args. OpenAI explicitly documents
that strict-mode guarantees do NOT hold across parallel calls in the same
turn.
**When to use:** Tools with side effects (DB writes, payments, file mutations)
where a malformed arg = corrupted state. Also when using `gpt-4.1-nano` or
fine-tuned models that frequently emit duplicate parallel calls.
**When NOT to use:** Read-only retrieval fan-out (web search + vector search
+ memory lookup, all in one turn) where parallelism cuts latency 3-5×. For
those, accept that one of N calls might have a slightly malformed arg and
validate inside the tool function.
**Example/snippet:**
```python
agent = Agent(
    name="Writer",
    tools=[write_db, send_email],     # destructive
    model_settings=ModelSettings(parallel_tool_calls=False),
)
```
**Why it works:** Parallel calls share one logits stream that is multiplexed
across N tool-call branches. The constrained-decoding FSM was designed for one
sequential output, so when the model splits attention across branches the
strict guarantees degrade. With parallel off, the model emits exactly 0 or 1
call per turn, and constrained decoding holds 100 %.

---

## M-09: dynamic-instructions-over-prompt-templating
**Category:** mem-
**Sources:**
- https://openai.github.io/openai-agents-python/agents/
- https://openai.github.io/openai-agents-python/context/
- https://cookbook.openai.com/examples/agents_sdk/context_personalization
**Rule:** Pass `instructions=callable` (a function of `context, agent`) instead
of building a string prompt and re-creating the Agent per request. The callable
is evaluated each turn with current `RunContextWrapper`, so user_id / locale /
tenant config flow in without rebuilding the agent or busting prompt cache.
**When to use:** Multi-tenant SaaS, per-user personalization, time-sensitive
context (current date, market state). The callable should put the VARIABLE
parts at the END of the system prompt and STATIC parts at the start to
preserve OpenAI's automatic 1024-token prefix cache.
**When NOT to use:** Single-tenant agents with truly static prompts — adding a
callable just adds indirection. Also avoid for content that is the SAME for
every user but changes daily — that should be in a tool, not the prompt
(otherwise you bust cache for everyone every midnight).
**Example/snippet:**
```python
def instructions(ctx: RunContextWrapper[UserCtx], agent: Agent) -> str:
    static = "You are SupportBot. Tools: ... Rules: ..."  # cached prefix
    dynamic = f"\n\nCurrent user: {ctx.context.name} (tier={ctx.context.tier})"
    return static + dynamic

agent = Agent(name="Support", instructions=instructions)
```
**Why it works:** OpenAI prompt cache hashes the longest common prefix in
1024-token + 128-token increments. Static-first / dynamic-last layout lets
every user share the prefix cache (typically 90 %+ hit rate, 50 % cost cut on
input). Rebuilding a string per user with the username sprinkled in front of
"You are..." destroys this entirely.

---

## M-10: agent-output-type-as-implicit-final-state
**Category:** lp-
**Sources:**
- https://openai.github.io/openai-agents-python/ref/agent/
- https://openai.github.io/openai-agents-python/results/
- https://github.com/openai/openai-agents-python/issues/474
**Rule:** Setting `output_type=SomeModel` changes the run-loop termination
condition: the loop ends when the LLM emits a tool call to the synthetic
`final_output` tool with valid `SomeModel`. Use this to FORCE a structured
finish state instead of relying on "the model stopped calling tools".
**When to use:** Any agent that must return data to downstream code (REST API,
queue, next pipeline stage). Combine with M-01 ordering. Pairs perfectly with
output_guardrails — the guardrail receives the typed object, not a string.
**When NOT to use:** Conversational chatbots where the user wants prose. Also
avoid output_type with discriminated unions or Pydantic Optional defaults —
known issue #474 produces invalid JSON Schema. Flatten unions to a tagged
literal field manually.
**Example/snippet:**
```python
class TaskResult(BaseModel):
    status: Literal["done", "blocked"]
    artifacts: list[str]            # required, M-02
    blocker_reason: str | None      # nullable, not Optional[str] = None

agent = Agent(name="Worker", tools=[...], output_type=TaskResult)
res = await Runner.run(agent, ...)
typed: TaskResult = res.final_output  # guaranteed by SDK
```
**Why it works:** Without `output_type` the SDK treats "first LLM response with
no tool calls" as final, which is fragile — a chatty model may keep narrating.
With `output_type` the SDK exposes a synthetic terminal tool to the model and
loops until that specific tool is called validly. Schema-guided termination is
strictly stronger than text-guided.

---

## M-11: trace-grading-for-eval-not-final-output-grading
**Category:** eval-
**Sources:**
- https://developers.openai.com/api/docs/guides/trace-grading
- https://developers.openai.com/api/docs/guides/agent-evals
- https://platform.openai.com/docs/guides/graders
**Rule:** Grade the full TRACE (LLM calls + tool calls + handoffs) with an o3
rubric grader, not just the final assistant message. Final-output graders miss
"right answer for wrong reason" — agent that hallucinated a search result then
got lucky on the conclusion looks identical to one that searched correctly.
**When to use:** Regression suites for tool-calling agents, multi-step
workflows, anything with handoffs. Especially when you have a ground-truth
"correct trajectory" not just a "correct answer".
**When NOT to use:** Pure Q&A or single-step extraction — there's no
trajectory worth grading, the final output IS the trace. Don't trace-grade
without first establishing reference traces from a known-good run; otherwise
your rubric is unanchored.
**Example/snippet:**
```yaml
# eval rubric
- name: tool_calls_correct
  type: model_grader
  model: o3
  rubric: |
    Score 1 if the agent called {{ expected_tool }} with semantically equivalent args
    to {{ expected_args }}. Score 0 otherwise. Ignore the final text.
- name: handoff_appropriate
  rubric: "Score 1 if handoff target matches user intent class {{ intent }}."
```
**Why it works:** Agent failures cluster in the trajectory, not the conclusion
— wrong tool, wrong arguments, premature termination, unnecessary handoff.
Trace grading captures these as separate signals you can debug. OpenAI's
own guidance: use o3 as the grader because rubric-following on multi-step
traces is a reasoning task itself.

---

## M-12: encrypted-reasoning-for-zdr-stateless
**Category:** mem-
**Sources:**
- https://community.openai.com/t/how-to-use-reasoning-encrypted-content-with-store-false-stateless/1286934
- https://cookbook.openai.com/examples/responses_api/reasoning_items
- https://github.com/openai/openai-agents-python/issues/2063
**Rule:** When `store=false` (ZDR enterprise) and using a reasoning model, set
`include=["reasoning.encrypted_content"]` and round-trip the encrypted blob
yourself in the next turn's `input` items. Do NOT use `previous_response_id`
— it is silently ignored under store=false.
**When to use:** Healthcare / finance / legal deployments under contractual
ZDR. Any tenant whose data cannot be retained on OpenAI side but who still
needs o3/o4-mini reasoning continuity.
**When NOT to use:** Default deployments — encrypted content adds ~5-15 % to
input tokens (the encrypted blob is bigger than the raw reasoning items it
replaces). If you don't have a ZDR requirement, just use stateful chaining.
**Example/snippet:**
```python
r1 = client.responses.create(
    model="o4-mini", input=msg, store=False,
    include=["reasoning.encrypted_content"],
)
encrypted_items = [i for i in r1.output if i.type == "reasoning"]
r2 = client.responses.create(
    model="o4-mini", store=False,
    include=["reasoning.encrypted_content"],
    input=encrypted_items + [tool_result_item],   # pass blob back
)
```
**Why it works:** The encrypted content is decrypted in OpenAI's serving
process in-memory only, never persisted. From the model's perspective the
reasoning items are restored; from the compliance perspective nothing was
stored at rest. Without this, ZDR + reasoning model = each turn re-thinks
from scratch (15-40 % quality regression on multi-step tasks).

---

Total: 12 methodologies.
