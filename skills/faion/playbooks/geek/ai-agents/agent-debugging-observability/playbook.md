---
name: agent-debugging-observability
description: Instrument an AI agent loop with structured JSONL trace logging and inspect traces via Langfuse, Helicone, or self-hosted Postgres + Grafana.
tier: geek
group: ai-agents
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a Python decorator that writes one structured JSON line per agent-loop iteration — capturing iter index, prompt, response, tool_calls, tool_results, latency_ms, and token counts — and you will have at least one observability backend (Langfuse, Helicone, or self-hosted Postgres + Grafana) wired up so you can query, filter, and dashboard every iteration in production.

## Prerequisites

- Python 3.11+, `pip install anthropic>=0.51 pydantic>=2.7`.
- An `ANTHROPIC_API_KEY` exported in the environment.
- Familiarity with the `tool_use`/`tool_result` content-block flow — see the `react-loop-production` playbook before proceeding.
- One of:
  - A Langfuse project (cloud at langfuse.com or self-hosted via Docker).
  - A Helicone account (helicone.ai) with an API key.
  - A running Postgres 15+ instance with write access and Grafana connected to it.
- (Optional) `pip install langfuse>=2.30` for the Langfuse path.

## Steps

1. **Define the per-iteration trace schema** using Pydantic so every path produces the same shape.

   ```python
   # agent_trace.py
   import time
   from typing import Any
   from pydantic import BaseModel, Field


   class ToolCallRecord(BaseModel):
       id: str
       name: str
       inputs: dict[str, Any]


   class ToolResultRecord(BaseModel):
       tool_use_id: str
       name: str
       output: str                # JSON-serialised result string


   class IterTrace(BaseModel):
       iter: int
       prompt_messages: list[dict[str, Any]]   # snapshot of messages sent
       response_content: list[dict[str, Any]]  # assistant content blocks
       tool_calls: list[ToolCallRecord] = Field(default_factory=list)
       tool_results: list[ToolResultRecord] = Field(default_factory=list)
       stop_reason: str
       latency_ms: int
       input_tokens: int
       output_tokens: int
       model: str
   ```

2. **Implement the `@trace_iter` decorator** that wraps each loop body, measures latency, and emits one JSONL line to a local file.

   ```python
   # agent_trace.py (continued)
   import functools, json, pathlib, datetime, logging

   log = logging.getLogger("agent.trace")


   class JsonlTracer:
       """Append-only JSONL sink. One IterTrace per line."""

       def __init__(self, path: str = "agent-traces.jsonl"):
           self._path = pathlib.Path(path)
           self._path.parent.mkdir(parents=True, exist_ok=True)
           self._fh = self._path.open("a", encoding="utf-8")

       def emit(self, trace: IterTrace) -> None:
           record = {
               "ts": datetime.datetime.utcnow().isoformat() + "Z",
               **trace.model_dump(),
           }
           self._fh.write(json.dumps(record, ensure_ascii=False) + "\n")
           self._fh.flush()

       def close(self) -> None:
           self._fh.close()


   def trace_iter(tracer: JsonlTracer):
       """Decorator factory. Wrap a one-iter agent function that returns IterTrace."""
       def decorator(fn):
           @functools.wraps(fn)
           def wrapper(*args, **kwargs):
               t0 = time.monotonic()
               result: IterTrace = fn(*args, **kwargs)
               result.latency_ms = int((time.monotonic() - t0) * 1000)
               tracer.emit(result)
               log.info(
                   "iter=%d stop=%s tokens_in=%d tokens_out=%d latency_ms=%d",
                   result.iter, result.stop_reason,
                   result.input_tokens, result.output_tokens, result.latency_ms,
               )
               return result
           return wrapper
       return decorator
   ```

3. **Wire the decorator into the agent loop**. The decorated function calls the Anthropic API once and returns an `IterTrace`.

   ```python
   # agent_loop.py
   import json
   import anthropic
   from agent_trace import IterTrace, ToolCallRecord, ToolResultRecord, JsonlTracer, trace_iter

   MODEL = "claude-sonnet-4-6"
   client = anthropic.Anthropic()
   tracer = JsonlTracer("runs/agent-traces.jsonl")


   def build_iter_fn(tracer: JsonlTracer):
       @trace_iter(tracer)
       def run_iter(iter_idx: int, messages: list[dict], tools: list[dict]) -> IterTrace:
           import time
           response = client.messages.create(
               model=MODEL,
               max_tokens=4096,
               tools=tools,
               messages=messages,
           )
           tool_calls = [
               ToolCallRecord(id=b.id, name=b.name, inputs=b.input)
               for b in response.content if b.type == "tool_use"
           ]
           return IterTrace(
               iter=iter_idx,
               prompt_messages=messages,
               response_content=[b.model_dump() for b in response.content],
               tool_calls=tool_calls,
               tool_results=[],          # filled after dispatch, see Step 4
               stop_reason=response.stop_reason,
               latency_ms=0,             # overwritten by decorator
               input_tokens=response.usage.input_tokens,
               output_tokens=response.usage.output_tokens,
               model=MODEL,
           )
       return run_iter
   ```

4. **Capture tool results** by mutating the returned `IterTrace` before the next iteration.

   ```python
   # agent_loop.py (continued)

   def dispatch_and_record(trace: IterTrace, dispatch_fn) -> list[dict]:
       """Call dispatch_fn for each tool_use block; populate trace.tool_results."""
       tool_result_blocks = []
       for tc in trace.tool_calls:
           output = dispatch_fn(tc.name, tc.inputs)          # your tool router
           serialised = json.dumps(output, ensure_ascii=False)
           trace.tool_results.append(
               ToolResultRecord(tool_use_id=tc.id, name=tc.name, output=serialised)
           )
           tool_result_blocks.append({
               "type": "tool_result",
               "tool_use_id": tc.id,
               "content": serialised,
           })
       # Persist updated trace with tool_results populated
       tracer.emit(trace)    # second emit overwrites: use run_id in production
       return tool_result_blocks
   ```

5. **Forward traces to Langfuse** (cloud or self-hosted). Use the `langfuse` SDK to create one `generation` span per iteration.

   ```python
   # backends/langfuse_sink.py
   import os
   from langfuse import Langfuse
   from agent_trace import IterTrace

   lf = Langfuse(
       public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
       secret_key=os.environ["LANGFUSE_SECRET_KEY"],
       host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
   )


   def send_to_langfuse(run_id: str, trace: IterTrace) -> None:
       lf_trace = lf.trace(id=run_id, name="agent-loop")
       lf_trace.generation(
           name=f"iter-{trace.iter}",
           model=trace.model,
           input=trace.prompt_messages,
           output=trace.response_content,
           usage={
               "input": trace.input_tokens,
               "output": trace.output_tokens,
           },
           metadata={
               "iter": trace.iter,
               "stop_reason": trace.stop_reason,
               "latency_ms": trace.latency_ms,
               "tool_calls": [tc.model_dump() for tc in trace.tool_calls],
               "tool_results": [tr.model_dump() for tr in trace.tool_results],
           },
       )
       lf.flush()
   ```

6. **Forward traces to Helicone** by routing the Anthropic client through the Helicone proxy. No SDK required — set `base_url` and add headers.

   ```python
   # backends/helicone_sink.py
   import os
   import anthropic

   def helicone_client(session_id: str) -> anthropic.Anthropic:
       """Return an Anthropic client that logs every call to Helicone."""
       return anthropic.Anthropic(
           api_key=os.environ["ANTHROPIC_API_KEY"],
           base_url="https://anthropic.helicone.ai",
           default_headers={
               "Helicone-Auth": f"Bearer {os.environ['HELICONE_API_KEY']}",
               "Helicone-Session-Id": session_id,
               "Helicone-Property-Iter": "0",   # update per iter via per-request headers
           },
       )
   ```

   Each request through this client is automatically captured in the Helicone dashboard at helicone.ai/requests with token counts, latency, and the full prompt/response.

7. **Insert traces into Postgres** for a self-hosted observability stack with Grafana.

   ```python
   # backends/postgres_sink.py
   import json, os, psycopg2
   from agent_trace import IterTrace

   DDL = """
   CREATE TABLE IF NOT EXISTS agent_traces (
       id          BIGSERIAL PRIMARY KEY,
       run_id      TEXT        NOT NULL,
       ts          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       iter        INT         NOT NULL,
       model       TEXT        NOT NULL,
       stop_reason TEXT        NOT NULL,
       latency_ms  INT         NOT NULL,
       input_tokens  INT       NOT NULL,
       output_tokens INT       NOT NULL,
       tool_calls  JSONB,
       tool_results JSONB
   );
   CREATE INDEX IF NOT EXISTS idx_agent_traces_run_id ON agent_traces(run_id);
   CREATE INDEX IF NOT EXISTS idx_agent_traces_ts     ON agent_traces(ts);
   """


   def get_conn():
       return psycopg2.connect(os.environ["AGENT_TRACES_DSN"])


   def ensure_schema(conn) -> None:
       with conn.cursor() as cur:
           cur.execute(DDL)
       conn.commit()


   def insert_trace(conn, run_id: str, trace: IterTrace) -> None:
       with conn.cursor() as cur:
           cur.execute(
               """
               INSERT INTO agent_traces
                   (run_id, iter, model, stop_reason, latency_ms,
                    input_tokens, output_tokens, tool_calls, tool_results)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               """,
               (
                   run_id, trace.iter, trace.model, trace.stop_reason,
                   trace.latency_ms, trace.input_tokens, trace.output_tokens,
                   json.dumps([tc.model_dump() for tc in trace.tool_calls]),
                   json.dumps([tr.model_dump() for tr in trace.tool_results]),
               ),
           )
       conn.commit()
   ```

   In Grafana, connect the data source to your Postgres instance and create panels using queries like:

   ```sql
   SELECT date_trunc('minute', ts) AS time,
          avg(latency_ms)          AS avg_latency_ms,
          sum(input_tokens + output_tokens) AS total_tokens
   FROM agent_traces
   WHERE run_id = '$run_id'
   GROUP BY 1 ORDER BY 1;
   ```

## Verify

Run the agent for one question and confirm the trace file contains well-formed JSON lines with all required fields:

```bash
python agent_loop.py "Summarise the deployment guide." && \
python - <<'PY'
import json, pathlib, sys

lines = [json.loads(l) for l in pathlib.Path("runs/agent-traces.jsonl").read_text().splitlines() if l.strip()]
required = {"ts","iter","prompt_messages","response_content","tool_calls","tool_results",
            "stop_reason","latency_ms","input_tokens","output_tokens","model"}
for i, rec in enumerate(lines):
    missing = required - set(rec)
    if missing:
        print(f"line {i}: missing fields {missing}", file=sys.stderr)
        sys.exit(1)
print(f"OK — {len(lines)} trace line(s), all fields present")
print(f"iters: {[r['iter'] for r in lines]}")
print(f"latencies ms: {[r['latency_ms'] for r in lines]}")
PY
```

Expected output ends with `OK — N trace line(s), all fields present` and `latencies ms: [...]` showing non-zero values.

For Langfuse: open your project at `cloud.langfuse.com` → Traces; you should see an `agent-loop` trace with one generation per iteration within 30 seconds of the run completing.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `latency_ms: 0` in every trace line | `IterTrace` built with placeholder `latency_ms=0` and decorator emit fires before mutation | Confirm `trace_iter` decorator overwrites `result.latency_ms` after `fn()` returns; `IterTrace` must be a Pydantic model (not frozen) |
| JSONL file empty after run | `JsonlTracer._fh.flush()` not called, or `close()` not called | Call `tracer.close()` at the end of the agent run; wrap in `try/finally` |
| Langfuse shows traces but no generations | `lf_trace.generation()` called on a closed trace object | Call `lf.flush()` inside `send_to_langfuse` before the function returns; check for background-flush config |
| Helicone returns 401 | `HELICONE_API_KEY` missing or wrong header name | Header must be `Helicone-Auth: Bearer <key>` — note the `Bearer` prefix |
| `psycopg2.OperationalError: relation "agent_traces" does not exist` | `ensure_schema()` not called before first insert | Call `ensure_schema(conn)` once at startup before the first `insert_trace()` call |
| Postgres insert hangs under load | Single connection used concurrently | Use a connection pool (`psycopg2.pool.ThreadedConnectionPool`) or switch to `psycopg[async]` |
| `prompt_messages` in trace is empty | Messages list captured before user message appended | Snapshot `messages` _after_ appending the current user turn but _before_ the API call |

## Next

- Add OpenTelemetry span export around each iteration so traces flow into Langfuse's native OTel ingestion or Phoenix — see `geek/ai/ai-agents/trajectory-eval-otel` for the span attribute contract.
- Use `geek/ai/ai-agents/record-replay-debugging` to build a deterministic replay harness on top of the JSONL traces produced here, enabling offline regression tests.
- Extend the Postgres schema with a `score` column and run an LLM-as-judge evaluation pass after each agent session — see `geek/ai/ai-agents/llm-judge-rubric-evidence-first`.

## References

- [knowledge/geek/ai/ai-agents/trajectory-eval-otel](../../../knowledge/geek/ai/ai-agents/trajectory-eval-otel) — defines the OTel GenAI span attribute contract that the `IterTrace` schema in Step 1 is designed to be forward-compatible with, enabling zero-rework export to Langfuse or Phoenix
- [knowledge/geek/ai/ai-agents/record-replay-debugging](../../../knowledge/geek/ai/ai-agents/record-replay-debugging) — the JSONL format emitted by `JsonlTracer` follows the record-side contract of this methodology so that replay harnesses can consume the same files without transformation
- [knowledge/geek/ai/ai-agents/langchain-observability](../../../knowledge/geek/ai/ai-agents/langchain-observability) — covers Langfuse callback integration patterns that inform the `send_to_langfuse` sink in Step 5, specifically the trace/generation nesting model
