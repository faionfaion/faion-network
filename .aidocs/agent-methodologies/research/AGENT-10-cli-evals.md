# Agent 10: CLI vs SDK Trade-offs + Agent Evaluation/Observability

**Summary (2 lines):** CLI agents (Claude Code `-p`, Codex CLI, Aider, opencode) win when you need a battle-tested harness with shell+git+filesystem already wired; SDKs win when you need custom domains, custom tools, or programmatic embedding. Production agents need OTel-GenAI traces, trajectory + outcome evals, LLM-as-judge with rubrics, deterministic replay, and chaos-style fault injection — not just unit tests on prompts.

State: April 2026.

---

## CLI VS SDK METHODOLOGIES

### cli-1: Use Claude Code `-p` headless as the default agent runtime; only drop to Agent SDK when CLI hits a wall

**Rule:** Invoke `claude -p "<prompt>" --output-format stream-json --verbose --allowedTools <list>` as a subprocess from your orchestrator. The CLI ships with the full Claude Code harness (filesystem, bash, git, MCP, plan mode, sub-agents, hooks, skills, compaction). Reach for the Claude Agent SDK only when you need: (a) custom non-coding domain, (b) custom tools beyond MCP, (c) programmatic control of the inner loop, or (d) embedding inside another product.

**Cite:**
- https://code.claude.com/docs/en/headless
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://github.com/anthropics/claude-agent-sdk-python

**When to use:** Coding/devops/research tasks, cron jobs, GitHub Actions, internal automation. Anything that benefits from filesystem+git context.
**When NOT:** Non-coding business workflows (sales triage, claims processing) — Agent SDK + custom tools is leaner. Also avoid CLI when you need to embed inside a SaaS product that can't shell out.

**Tiny example:**
```bash
claude -p "Fix failing test in tests/test_auth.py" \
  --output-format stream-json --verbose \
  --allowedTools "Read,Edit,Bash(pytest:*)" \
  --max-turns 20 < /dev/null
```

---

### cli-2: Treat the CLI as a process; pipe stream-json into your own state machine

**Rule:** Don't wrap the CLI as a black-box "give me the answer" call. Read stream-json line-by-line; each line is a discrete event (`system/init`, `assistant`, `tool_use`, `tool_result`, `result`). Drive your orchestrator off these events: cost accounting, budget caps, tool gating, mid-stream interruption, hand-off to a sibling agent. This is what makes "stream chaining" — piping one Claude into another — possible.

**Cite:**
- https://backgroundclaude.com/blog/stream-json
- https://github.com/ruvnet/ruflo/wiki/Stream-Chaining

**When to use:** Multi-agent pipelines, dashboards, budget enforcers, anything that needs to react before the agent finishes.
**When NOT:** Simple one-shot scripts where you just need exit code + final text — `--output-format text` is plenty.

**Tiny example:**
```python
proc = subprocess.Popen(["claude","-p",task,
    "--output-format","stream-json","--verbose"],
    stdout=subprocess.PIPE, text=True)
for line in proc.stdout:
    ev = json.loads(line)
    if ev["type"]=="result" and ev["total_cost_usd"]>1.00:
        proc.terminate()  # budget cap
```

---

### cli-3: Wrap the SDK in a CLI only when you need a stable interface across languages/teams

**Rule:** If your agent will be called from Python, TS, Go, bash, n8n, cron, and humans — wrap the SDK in a thin CLI (`mything agent run --task X --json`). The CLI becomes your stable contract; the SDK can churn underneath. If your agent only ever runs from one Python service, skip the CLI layer — direct SDK calls are simpler and faster.

**Cite:**
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://github.com/bradAGI/awesome-cli-coding-agents (pi-builder pattern)

**When to use:** Multi-language org, ops teams want shell access, n8n/Temporal/Airflow orchestration.
**When NOT:** Single-service embedding — direct SDK has lower overhead and better error propagation.

**Tiny example:**
```bash
# stable CLI surface, SDK churns inside
faion agent run --task "summarize PR" --model sonnet-4.5 --json | jq .summary
```

---

### cli-4: Pin the OpenAI Codex CLI to the Responses API, not Chat Completions

**Rule:** Codex CLI is a Rust binary that runs the agent loop locally and talks to OpenAI's Responses API (not Chat Completions). Chat Completions support is deprecated in Codex. Use `gpt-5.3-codex` (or current `*-codex` variant) and let the Responses API's tool-search defer large tool surfaces until runtime. Pair with `codex exec` for headless one-shot mode in CI.

**Cite:**
- https://developers.openai.com/codex/cli
- https://developers.openai.com/codex/changelog
- https://openai.com/index/unrolling-the-codex-agent-loop/

**When to use:** OpenAI-stack teams; CI tasks where the cached responses API + reasoning summaries matter; cross-provider via `--config model_provider=...` for OSS models.
**When NOT:** When you need MCP-rich harness — Claude Code's MCP integration is more mature. Also when you need the Assistants API's persistent threads (deprecated 2026 anyway).

**Tiny example:**
```bash
codex exec --model gpt-5.3-codex \
  --sandbox workspace-write \
  "refactor src/db.py to use async sqlalchemy"
```

---

### cli-5: Pick the harness by job: Aider for git-first edits, opencode for fully terminal-native, Cline for IDE-coupled

**Rule:** Don't use one CLI for everything. Match harness to ergonomics:
- **Aider** — git-first, autocommits with descriptive messages, scriptable from bash/Python; best when the unit of work is "a coordinated multi-file change with a commit."
- **opencode** — pure terminal, no IDE, ~140k stars in 2026; best when you SSH into remote dev boxes.
- **Cline** — IDE extension; best when the dev wants inline diffs and the agent in the same window as the code.
- **Cursor CLI** — for Cursor users who want a headless variant of their IDE workflow.

**Cite:**
- https://github.com/Aider-AI/aider
- https://dev.to/ji_ai/opencode-hit-140k-stars-why-terminal-agents-won-2026-aci
- https://thoughts.jock.pl/p/ai-coding-harness-agents-2026

**When to use:** Pick per-task; CI = Aider/Codex, dev box = opencode/Claude Code, local IDE = Cline/Cursor.
**When NOT:** Don't standardize org-wide on one — different jobs have different ergonomics.

**Tiny example:**
```bash
# Aider: git-first refactor
aider --yes --message "extract auth middleware" src/auth/*.py
# opencode: terminal-only on remote
ssh prod-dev "cd /app && opencode 'add retry to webhook handler'"
```

---

### cli-6: Headless = `-p` + `--allowedTools` + `--max-turns` + non-TTY stdin; never let an agent run interactively in CI

**Rule:** A stable headless agent has four guards: (1) `-p`/`--print` to disable TUI, (2) explicit `--allowedTools` allowlist (NOT `--dangerously-skip-permissions` in prod), (3) `--max-turns` cap, (4) closed stdin (`< /dev/null`) so the agent can't accidentally block on input. Same applies to Codex (`codex exec`), Aider (`--yes`), opencode (headless mode). Anything missing → mystery hangs in prod.

**Cite:**
- https://code.claude.com/docs/en/headless
- https://www.mindstudio.ai/blog/claude-code-headless-mode-autonomous-agents-2

**When to use:** All non-interactive runs (cron, CI, queues, scheduled agents).
**When NOT:** Interactive dev sessions (you want the TUI then).

**Tiny example:**
```bash
timeout 600 claude -p "$TASK" \
  --allowedTools "Read,Edit,Bash(pytest:*)" \
  --max-turns 15 --output-format json \
  < /dev/null > result.json 2> err.log
```

---

## EVAL & OBSERVABILITY METHODOLOGIES

### eval-1: Score every agent run on three axes — task success, token cost, step count — never just one

**Rule:** A single eval that only checks "did it work?" misleads. For every task in your eval set, record (task_success: bool/score, token_cost: $/tokens, steps: int turns/tool-calls, latency_p50/p95). Track all four over time. An agent that goes from 60% → 80% success but 3× cost is sometimes a regression. Anthropic's official guidance and Stanford's AI Index 2026 both anchor on goal-achievement-rate (>85%), tokens-per-task (<5k typical target), and policy-violation-rate (0%).

**Cite:**
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks
- https://www.beri.net/article/stanford-ai-index-2026-agents-66-percent-success

**When to use:** Every agent that ships to prod. Build the dashboard before the agent.
**When NOT:** Throwaway prototypes — but even then, log so you can graduate later.

**Tiny example:**
```python
@dataclass
class EvalResult:
    task_id: str
    success: bool       # outcome
    cost_usd: float     # efficiency
    steps: int          # trajectory length
    p95_latency_s: float
# fail CI if any of: success<0.85, cost>budget, steps>2x baseline
```

---

### eval-2: Trajectory eval (was the path optimal?) is separate from outcome eval (did it work?)

**Rule:** Outcome eval = "final answer correct." Trajectory eval = "did the agent take the most efficient path, or did it loop, retry, or pick the wrong tool first?" Both matter. Phoenix in 2026 introduced ATIF (Agent Trajectory Interchange Format) so you can upload offline runs as span trees and grade trajectories. Score: tool-selection accuracy, redundant calls, plan-vs-execution divergence. An agent with 90% outcome success but 5× the optimal trajectory length will drift, get expensive, and confuse users.

**Cite:**
- https://arize.com/docs/phoenix/release-notes/04-2026/04-03-2026-atif-trajectory-upload
- https://phoenix.arize.com/
- https://github.com/Arize-ai/phoenix

**When to use:** Multi-step / multi-tool agents (basically all real agents).
**When NOT:** Single-call generators (RAG retrieve+answer) — outcome alone is fine.

**Tiny example:**
```python
def trajectory_score(trace):
    optimal_tools = {"search", "read_file", "edit_file"}  # ground truth
    actual = [s.tool for s in trace.tool_spans]
    return {
        "redundant_calls": len(actual) - len(set(actual)),
        "tool_overlap": len(set(actual) & optimal_tools)/len(optimal_tools),
        "step_efficiency": len(optimal_tools)/max(len(actual),1),
    }
```

---

### eval-3: LLM-as-judge with structured rubric, JSON output, evidence-before-score, and bias mitigation

**Rule:** Don't ask "rate this 1–10." Build a rubric with named criteria (correctness, completeness, safety, style), require the judge to (1) emit JSON, (2) cite evidence from the output before scoring, (3) score per-criterion. Validate judges with Cronbach's alpha across multiple runs. Mitigate the four canonical biases — position, verbosity, self-preference, authority — with randomized order, length-normalized prompts, and cross-model judging (don't let GPT-4 grade GPT-4 alone).

**Cite:**
- https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80
- https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge
- https://arize.com/llm-as-a-judge/

**When to use:** Open-ended outputs where exact-match doesn't work (code review, summaries, plans).
**When NOT:** Verifiable outputs (compiles?, tests pass?, JSON schema valid?) — use deterministic checks first, judges second.

**Tiny example:**
```json
{
  "rubric": {
    "correctness": {"weight": 0.5, "criteria": "..."},
    "completeness": {"weight": 0.3, "criteria": "..."},
    "safety": {"weight": 0.2, "criteria": "..."}
  },
  "output_schema": {
    "evidence": "string (quote from response)",
    "scores": {"correctness": "int 1-5", ...},
    "rationale": "string"
  }
}
```

---

### eval-4: Run a regression eval suite on every prompt/model/tool change — block merges on regression

**Rule:** Treat the eval set like a unit-test suite: it runs in CI on every PR that touches prompts, models, tools, or system instructions. Pipeline order: (1) fast deterministic checks (schema, exact-match, exit codes) — fail fast; (2) semantic checks (LLM-as-judge); (3) full eval set against a baseline. Block merges on regression of any tracked metric. Graduate "capability evals" with high pass rates into the regression suite to catch drift from upstream model updates.

**Cite:**
- https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
- https://blog.langchain.com/agent-evaluation-readiness-checklist/
- https://arxiv.org/html/2603.02601v1 (AgentAssay)

**When to use:** Any agent past prototype. Cost is small once eval set exists.
**When NOT:** Pure exploration phase — but start the suite as soon as you pick a candidate.

**Tiny example:**
```yaml
# .github/workflows/agent-eval.yml
- run: pytest evals/deterministic/ -x      # schema, exit codes
- run: python evals/llm_judge.py --baseline main
- run: python evals/check_regression.py --threshold 0.05
```

---

### eval-5: Instrument with OpenTelemetry GenAI semantic conventions; backend is interchangeable

**Rule:** Use the OTel GenAI spec for spans/attributes — `gen_ai.operation.name = invoke_agent`, `gen_ai.agent.name`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`. Span kind = CLIENT for remote agents, INTERNAL for in-process. Tool calls become sibling TOOL spans under the AGENT root; multi-turn = nested per-turn AGENT spans. Once instrumented, you can ship the same OTLP traces to Langfuse, Phoenix, Datadog, Grafana, or self-hosted ClickHouse — no vendor lock-in. Conventions are still experimental in 2026 but already supported by major vendors.

**Cite:**
- https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
- https://langfuse.com/integrations/native/opentelemetry
- https://www.datadoghq.com/blog/llm-otel-semantic-convention/

**When to use:** All production agents. Pick OTel before picking a vendor.
**When NOT:** Local prototyping — vendor SDK is faster to wire up. Migrate once you ship.

**Tiny example:**
```python
with tracer.start_as_current_span("invoke_agent neromedia",
    attributes={"gen_ai.operation.name":"invoke_agent",
                "gen_ai.agent.name":"neromedia",
                "gen_ai.request.model":"claude-opus-4.7"}) as span:
    result = agent.run(task)
    span.set_attribute("gen_ai.usage.input_tokens", result.in_tokens)
    span.set_attribute("gen_ai.usage.output_tokens", result.out_tokens)
```

---

### eval-6: Build a deterministic replay harness — record-mode captures everything, replay-mode stubs all nondeterminism

**Rule:** Logs/traces tell you what happened, not why. To debug a 1-in-200 production failure, you need to re-execute the exact decision path. Architect the agent with two modes: **record** (real LLM, real tools, capture every input/output as a trace) and **replay** (LLM + tool calls served from the recorded trace, zero external IO). Replay-mode reproduces the bug deterministically; you can then mutate the prompt or tool stub and verify the fix. LangGraph time-travel checkpoints, Phoenix replay, and AgentOps replay sessions all implement this.

**Cite:**
- https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/
- https://debugg.ai/resources/deterministic-replay-meets-debug-ai-time-travel-debugging-llm-reproduce
- https://dev.to/sreeni5018/debugging-non-deterministic-llm-agents-implementing-checkpoint-based-state-replay-with-langgraph-5171

**When to use:** Production debugging, post-mortems, eval set construction (record once, replay many).
**When NOT:** Pure stateless one-shot calls — replay overhead isn't justified.

**Tiny example:**
```python
agent = Agent(mode="record", trace_path="trace.json")
result = agent.run(task)  # captures all LLM/tool IO
# Later, deterministic reproduce:
agent = Agent(mode="replay", trace_path="trace.json")
agent.run(task)  # identical decisions, no API calls
```

---

### eval-7: Chaos-eval — inject tool failures, rate limits, timeouts, and corrupt data; measure recovery

**Rule:** Production tools fail. Your agent must handle (a) tool returns error, (b) tool times out, (c) LLM rate-limit/5xx, (d) tool returns corrupted/wrong data, (e) MCP server disconnects. Build a chaos-eval suite that injects each failure mode at random points and grades the agent on: did it recover? did it retry intelligently? did it escalate when it couldn't? did it produce a wrong-but-confident answer? Frameworks: ReliabilityBench, agent-chaos. Without chaos eval, your "99% success rate" is on a sunny-day distribution.

**Cite:**
- https://arxiv.org/pdf/2601.06112 (ReliabilityBench)
- https://github.com/deepankarm/agent-chaos
- https://arxiv.org/abs/2505.03096

**When to use:** Any agent with external tool dependencies that ships to prod.
**When NOT:** Air-gapped agents with only deterministic local tools (rare).

**Tiny example:**
```python
chaos = ChaosInjector(faults=[
    "tool_timeout(p=0.1)",
    "tool_error(p=0.05, code=500)",
    "llm_rate_limit(p=0.02)",
    "tool_mutate(p=0.03)",  # corrupt return data
])
for task in eval_set:
    result = agent.run(task, middleware=chaos)
    assert result.recovered or result.escalated_correctly
```

---

### eval-8: Ship a proxy-based fallback for cost/usage even if you also use OTel

**Rule:** OTel is great for traces; a proxy (Helicone, LiteLLM, OpenRouter) is better for cost. Reasons: (1) catches calls from libraries you don't instrument, (2) zero code changes — just `base_url`, (3) graduated cost alerts (50/80/95% of budget), (4) per-environment limits (dev vs prod). Run both: OTel for trajectory/debug, proxy for hard budget caps and cost dashboards. Helicone in 2026 reports ~50–80ms added latency, well within tolerance.

**Cite:**
- https://docs.helicone.ai/guides/cookbooks/cost-tracking
- https://github.com/Helicone/helicone
- https://www.helicone.ai/blog/the-complete-guide-to-LLM-observability-platforms

**When to use:** Any team running multi-agent workloads where cost can spike (autonomous loops, batch jobs).
**When NOT:** Single-call SaaS endpoints with rigid token caps already in place.

**Tiny example:**
```python
client = Anthropic(
    base_url="https://anthropic.helicone.ai",
    default_headers={"Helicone-Auth": f"Bearer {key}",
                     "Helicone-User-Id": "agent-neromedia",
                     "Helicone-Property-Env": "prod"}
)
# Helicone enforces: 95% budget alert, hard cap at 100% in prod
```

---

### eval-9: Persist eval results as a versioned dataset, not a one-off run

**Rule:** Your eval set is a product artifact. Version it (git or dataset-store), grow it whenever a real prod failure surfaces (every incident → new test case), and tag each run with `(agent_version, model_version, prompt_hash, tool_versions, eval_set_version)`. Dashboards plot success/cost/steps over time across the joint version axis. Without versioning, you can't tell whether last week's regression came from a model update, a prompt edit, or eval-set drift.

**Cite:**
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://blog.langchain.com/agent-evaluation-readiness-checklist/

**When to use:** Always. Smallest possible version: a JSONL file in git.
**When NOT:** Never; even prototypes benefit.

**Tiny example:**
```jsonl
// evals/dataset.v3.jsonl
{"id":"E001","task":"...","expected":"...","added":"2026-04-01","origin":"incident-#247"}
{"id":"E002","task":"...","expected":"...","added":"2026-04-12","origin":"new-feature"}
```

---

## Sources

- https://code.claude.com/docs/en/headless
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://github.com/anthropics/claude-agent-sdk-python
- https://backgroundclaude.com/blog/stream-json
- https://developers.openai.com/codex/cli
- https://developers.openai.com/codex/changelog
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://github.com/Aider-AI/aider
- https://dev.to/ji_ai/opencode-hit-140k-stars-why-terminal-agents-won-2026-aci
- https://thoughts.jock.pl/p/ai-coding-harness-agents-2026
- https://github.com/bradAGI/awesome-cli-coding-agents
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks
- https://arize.com/docs/phoenix/release-notes/04-2026/04-03-2026-atif-trajectory-upload
- https://github.com/Arize-ai/phoenix
- https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80
- https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge
- https://arize.com/llm-as-a-judge/
- https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
- https://blog.langchain.com/agent-evaluation-readiness-checklist/
- https://arxiv.org/html/2603.02601v1
- https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
- https://langfuse.com/integrations/native/opentelemetry
- https://www.datadoghq.com/blog/llm-otel-semantic-convention/
- https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/
- https://debugg.ai/resources/deterministic-replay-meets-debug-ai-time-travel-debugging-llm-reproduce
- https://arxiv.org/pdf/2601.06112
- https://github.com/deepankarm/agent-chaos
- https://arxiv.org/abs/2505.03096
- https://docs.helicone.ai/guides/cookbooks/cost-tracking
- https://github.com/Helicone/helicone
