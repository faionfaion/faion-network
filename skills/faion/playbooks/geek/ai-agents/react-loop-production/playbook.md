---
name: react-loop-production
description: Build a production-grade ReAct loop with the Anthropic SDK using tool_use/tool_result blocks, halt conditions, exponential-backoff retries, and JSONL trace logging.
tier: geek
group: ai-agents
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python agent that drives a ReAct (Reason → Act → Observe) loop using `claude-sonnet-4-6`, halts deterministically on max iterations / repeated calls / explicit answer, retries flaky tools with exponential backoff, and writes every turn to a JSONL trace file you can replay and diff.

## Prerequisites

- Python 3.11+, `pip install anthropic>=0.51` (Anthropic Python SDK 2026 line).
- An `ANTHROPIC_API_KEY` exported in the environment.
- Familiarity with the `tool_use` / `tool_result` content-block shape — see [Anthropic tool-use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).
- Understanding of why ReAct is the right loop pattern for exploratory goals — see `geek/ai/ai-agents/plan-execute-vs-react` before proceeding.

## Steps

1. **Create the project layout** and install dependencies.

   ```
   mkdir react-agent && cd react-agent
   pip install anthropic>=0.51
   ```

2. **Define two tools** — `search_docs` and `read_file` — with JSON-schema descriptions. Both return structured results the model reads as `tool_result` content blocks.

   ```python
   # tools.py
   import json, pathlib, time, random

   TOOLS = [
       {
           "name": "search_docs",
           "description": (
               "Search the local docs directory for files whose content contains the query. "
               "Returns a list of {path, snippet} objects, at most 5 results."
           ),
           "input_schema": {
               "type": "object",
               "properties": {
                   "query": {"type": "string", "description": "Search term (case-insensitive substring)"}
               },
               "required": ["query"],
           },
       },
       {
           "name": "read_file",
           "description": "Read the full UTF-8 text of a local file by path. Returns {path, content}.",
           "input_schema": {
               "type": "object",
               "properties": {
                   "path": {"type": "string", "description": "Absolute or relative file path"}
               },
               "required": ["path"],
           },
       },
   ]


   def _maybe_fail(fail_prob: float) -> None:
       """Simulate transient failure for retry demonstration."""
       if random.random() < fail_prob:
           raise RuntimeError("transient: upstream timeout")


   def search_docs(query: str, docs_dir: str = "./docs", fail_prob: float = 0.0) -> dict:
       _maybe_fail(fail_prob)
       results = []
       for p in pathlib.Path(docs_dir).rglob("*.md"):
           text = p.read_text(errors="replace")
           idx = text.lower().find(query.lower())
           if idx != -1:
               snippet = text[max(0, idx - 60): idx + 120].replace("\n", " ")
               results.append({"path": str(p), "snippet": snippet})
               if len(results) >= 5:
                   break
       return {"results": results, "total": len(results)}


   def read_file(path: str, fail_prob: float = 0.0) -> dict:
       _maybe_fail(fail_prob)
       content = pathlib.Path(path).read_text(errors="replace")
       return {"path": path, "content": content}
   ```

3. **Implement the retry wrapper** with exponential backoff for transient tool errors.

   ```python
   # retry.py
   import time, logging

   log = logging.getLogger("react.retry")


   def call_with_retry(fn, *args, max_attempts: int = 4, base_delay: float = 1.0, **kwargs):
       """Call fn(*args, **kwargs) with exponential backoff on RuntimeError.

       Raises the last exception after max_attempts exhausted.
       Returns {"error": ..., "recoveryHint": "RETRY_LATER"} if all attempts fail,
       so the model gets a structured error rather than a raw exception.
       """
       delay = base_delay
       for attempt in range(1, max_attempts + 1):
           try:
               return fn(*args, **kwargs)
           except RuntimeError as exc:
               if attempt == max_attempts:
                   log.warning("tool %s failed after %d attempts: %s", fn.__name__, attempt, exc)
                   return {
                       "error": str(exc),
                       "recoveryHint": "RETRY_LATER",
                       "attempts": attempt,
                   }
               log.info("retry %d/%d for %s in %.1fs: %s", attempt, max_attempts, fn.__name__, delay, exc)
               time.sleep(delay)
               delay *= 2
   ```

4. **Implement the JSONL trace logger** — one JSON line per turn.

   ```python
   # trace.py
   import json, pathlib, datetime


   class TraceLogger:
       def __init__(self, path: str = "trace.jsonl"):
           self._path = pathlib.Path(path)
           self._path.parent.mkdir(parents=True, exist_ok=True)
           self._fh = self._path.open("a", encoding="utf-8")

       def log(self, turn: int, role: str, content: object, meta: dict | None = None) -> None:
           entry = {
               "ts": datetime.datetime.utcnow().isoformat() + "Z",
               "turn": turn,
               "role": role,
               "content": content,
           }
           if meta:
               entry.update(meta)
           self._fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
           self._fh.flush()

       def close(self) -> None:
           self._fh.close()
   ```

5. **Implement halt conditions** — max iterations (10), repeated tool call detection, and explicit `FINAL_ANSWER` signal.

   The agent halts when any of these is true:
   - Turn count reaches `MAX_TURNS` (10).
   - The same `(tool_name, frozen_inputs)` pair appears twice — indicates stuck loop.
   - The model emits a `text` block containing `FINAL_ANSWER:` followed by its answer.

   ```python
   # halt.py
   import json


   MAX_TURNS = 10


   def freeze_inputs(inputs: dict) -> str:
       return json.dumps(inputs, sort_keys=True)


   class HaltChecker:
       def __init__(self, max_turns: int = MAX_TURNS):
           self.max_turns = max_turns
           self._seen_calls: set[tuple[str, str]] = set()

       def check(self, turn: int, response_blocks: list) -> tuple[bool, str]:
           """Return (should_halt, reason). Call before dispatching tool results."""
           if turn >= self.max_turns:
               return True, f"max_turns={self.max_turns} reached"
           for block in response_blocks:
               if block.type == "tool_use":
                   key = (block.name, freeze_inputs(block.input))
                   if key in self._seen_calls:
                       return True, f"repeated_tool_call: {block.name}({block.input})"
                   self._seen_calls.add(key)
               if block.type == "text" and "FINAL_ANSWER:" in block.text:
                   return True, "explicit_answer"
           return False, ""
   ```

6. **Implement the main ReAct loop** that wires everything together.

   ```python
   # agent.py
   import json, logging
   import anthropic
   from tools import TOOLS, search_docs, read_file
   from retry import call_with_retry
   from trace import TraceLogger
   from halt import HaltChecker

   logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
   log = logging.getLogger("react.agent")

   MODEL = "claude-sonnet-4-6"
   SYSTEM = (
       "You are a research assistant with access to a local docs directory. "
       "Use search_docs to locate relevant files, then read_file to read them. "
       "Reason step-by-step. When you have a complete answer, write exactly:\n"
       "FINAL_ANSWER: <your answer here>\n"
       "Do not write FINAL_ANSWER until you are confident."
   )


   def dispatch_tool(name: str, inputs: dict, fail_prob: float = 0.3) -> str:
       if name == "search_docs":
           result = call_with_retry(search_docs, inputs["query"], fail_prob=fail_prob)
       elif name == "read_file":
           result = call_with_retry(read_file, inputs["path"], fail_prob=fail_prob)
       else:
           result = {"error": f"unknown tool: {name}", "recoveryHint": "REPORT_TO_USER"}
       return json.dumps(result, ensure_ascii=False)


   def run(question: str, trace_path: str = "trace.jsonl") -> str:
       client = anthropic.Anthropic()
       tracer = TraceLogger(trace_path)
       halter = HaltChecker()

       messages: list[dict] = [{"role": "user", "content": question}]
       tracer.log(0, "user", question)

       answer = "(no answer — loop halted without FINAL_ANSWER)"

       for turn in range(1, HaltChecker().max_turns + 1):
           response = client.messages.create(
               model=MODEL,
               max_tokens=4096,
               system=SYSTEM,
               tools=TOOLS,
               messages=messages,
           )
           tracer.log(
               turn, "assistant",
               [b.model_dump() for b in response.content],
               {"stop_reason": response.stop_reason, "usage": response.usage.model_dump()},
           )

           should_halt, reason = halter.check(turn, response.content)

           # Collect FINAL_ANSWER text before halting
           for block in response.content:
               if block.type == "text" and "FINAL_ANSWER:" in block.text:
                   answer = block.text.split("FINAL_ANSWER:", 1)[1].strip()

           if should_halt:
               log.info("HALT turn=%d reason=%s", turn, reason)
               tracer.log(turn, "halt", {"reason": reason})
               break

           if response.stop_reason == "end_turn":
               log.info("STOP end_turn at turn=%d", turn)
               tracer.log(turn, "halt", {"reason": "end_turn"})
               break

           # Build tool_result blocks
           tool_results = []
           for block in response.content:
               if block.type == "tool_use":
                   log.info("TOOL turn=%d name=%s inputs=%s", turn, block.name, block.input)
                   result_content = dispatch_tool(block.name, block.input)
                   tool_results.append({
                       "type": "tool_result",
                       "tool_use_id": block.id,
                       "content": result_content,
                   })
                   tracer.log(turn, "tool_result", {
                       "tool_use_id": block.id,
                       "name": block.name,
                       "result": result_content,
                   })

           # Append assistant turn + tool results to messages
           messages.append({"role": "assistant", "content": response.content})
           if tool_results:
               messages.append({"role": "user", "content": tool_results})

       tracer.close()
       return answer


   if __name__ == "__main__":
       import sys
       q = sys.argv[1] if len(sys.argv) > 1 else "What does the deployment guide say about rollback?"
       print(run(q))
   ```

7. **Create a minimal `docs/` directory** with at least one Markdown file so the tools have something to search.

   ```bash
   mkdir -p docs
   printf '# Deployment Guide\n\n## Rollback\n\nTo rollback, run `kubectl rollout undo deployment/myapp`.\n' > docs/deployment.md
   ```

8. **Run the agent** with a question that requires both tools.

   ```bash
   ANTHROPIC_API_KEY=sk-ant-... python agent.py "What does the deployment guide say about rollback?"
   ```

   Expected output ends with `FINAL_ANSWER: ...` followed by rollback instructions from `docs/deployment.md`.

## Verify

Run the agent and inspect the trace:

```bash
python agent.py "What does the deployment guide say about rollback?" && \
  python -c "
import json, pathlib
lines = [json.loads(l) for l in pathlib.Path('trace.jsonl').read_text().splitlines()]
print('turns:', max(l['turn'] for l in lines))
print('halt reason:', next(l['content']['reason'] for l in lines if l['role'] == 'halt'))
print('tool calls:', [l['content']['name'] for l in lines if l['role'] == 'tool_result'])
"
```

Expected output:

```
turns: 2
halt reason: explicit_answer
tool calls: ['search_docs', 'read_file']
```

If `turns` exceeds 5 for this query, the loop is not converging — check that `FINAL_ANSWER:` appears verbatim in the system prompt and model output.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `anthropic.BadRequestError: messages: tool_result blocks must come after tool_use` | Tool result appended to wrong message role | Ensure `tool_result` blocks are in a `user` role message, immediately after the `assistant` message containing `tool_use` |
| Loop hits `max_turns=10` on a simple query | Model never writes `FINAL_ANSWER:` | Confirm the system prompt contains the exact string `FINAL_ANSWER:` with colon; check for encoding issues in the SYSTEM constant |
| `repeated_tool_call` halt on first iteration | `HaltChecker._seen_calls` not reset between runs | Instantiate a new `HaltChecker()` per `run()` call — do not share state across requests |
| `call_with_retry` returns `{"error": ..., "recoveryHint": "RETRY_LATER"}` on every call | `fail_prob=0.3` in `dispatch_tool` is too high for your test | Set `fail_prob=0.0` in `dispatch_tool` for production; `0.3` is only for demonstrating retry behaviour |
| `trace.jsonl` grows unbounded in long-running service | TraceLogger appends to the same file forever | Rotate by date or run-id: `TraceLogger(f"traces/{run_id}.jsonl")` |
| `RuntimeError: transient: upstream timeout` escapes retry | `max_attempts=4` exhausted before service recovered | Increase `max_attempts` or add circuit-breaker at the service level; structured error is returned so the agent can report to user |

## Next

- Add `trajectory-eval-otel` span instrumentation around each turn so traces flow to Langfuse or Phoenix — see `geek/ai/ai-agents/trajectory-eval-otel`.
- Replace `search_docs` and `read_file` with MCP server tools using `mcp-transport-stdio-vs-http` to decouple tool implementations from the agent process.
- Graduate from ReAct to a hybrid loop using `plan-execute-vs-react` when the task space becomes predictable enough to pre-plan steps.

## References

- [knowledge/geek/ai/ai-agents/plan-execute-vs-react](../../../knowledge/geek/ai/ai-agents/plan-execute-vs-react) — establishes when ReAct outperforms Plan-Execute for exploratory goals; this playbook's loop design follows the ReAct branch of that decision tree
- [knowledge/geek/ai/ai-agents/max-turns-circuit-breaker](../../../knowledge/geek/ai/ai-agents/max-turns-circuit-breaker) — the `HaltChecker.max_turns=10` cap and structured fallback in Step 5 directly implement the circuit-breaker pattern defined here
- [knowledge/geek/ai/ai-agents/structured-tool-errors](../../../knowledge/geek/ai/ai-agents/structured-tool-errors) — the `recoveryHint` enum in `call_with_retry` follows the structured-error contract so the agent loop can branch on RETRY_LATER vs REPORT_TO_USER deterministically
- [knowledge/geek/ai/ai-agents/trajectory-eval-otel](../../../knowledge/geek/ai/ai-agents/trajectory-eval-otel) — the JSONL trace schema in `TraceLogger` is designed to be forward-compatible with OTel GenAI span attributes for export to Langfuse or Phoenix
