---
name: function-calling-tool-use
description: Define Anthropic tools with JSON Schema draft 2020-12, dispatch parallel tool calls, and validate arguments with Pydantic v2 before execution.
tier: geek
group: llm-integration
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python agent that defines three typed tools (`get_weather`, `book_flight`, `query_db`), dispatches them in a single Claude turn, executes them in parallel with `ThreadPoolExecutor`, validates every incoming argument set with Pydantic v2 before calling the real implementation, and feeds structured error messages back to the model so it can self-correct.

## Prerequisites

- Python 3.11+.
- `pip install anthropic>=0.51 pydantic>=2.7`.
- `ANTHROPIC_API_KEY` exported in the environment.
- Basic familiarity with the Anthropic Messages API and the `tool_use` / `tool_result` block format.
- Read [knowledge/geek/ai/llm-integration/claude-tool-use](../../../knowledge/geek/ai/llm-integration/claude-tool-use) — the `stop_reason == "tool_use"` detection and full `response.content` append rule used in Step 4 come directly from that methodology.

## Steps

1. **Define the three tool schemas using JSON Schema draft 2020-12 conventions.**

   Each tool entry has three required keys: `name`, `description`, and `input_schema`. The description is the model's only signal for selecting the right tool — write it from the model's perspective ("Call when…").

   ```python
   # tools/definitions.py
   TOOLS = [
       {
           "name": "get_weather",
           "description": (
               "Call when the user asks about current weather or temperature for a city. "
               "Do NOT call for historical weather or forecasts beyond 7 days."
           ),
           "input_schema": {
               "type": "object",
               "$schema": "https://json-schema.org/draft/2020-12/schema",
               "properties": {
                   "city": {
                       "type": "string",
                       "description": "City name with optional country code, e.g. 'Kyiv, UA'",
                   },
                   "unit": {
                       "type": "string",
                       "enum": ["celsius", "fahrenheit"],
                       "description": "Temperature unit. Defaults to celsius.",
                   },
               },
               "required": ["city"],
               "additionalProperties": False,
           },
       },
       {
           "name": "book_flight",
           "description": (
               "Call when the user explicitly requests to book a flight. "
               "Requires departure city, destination city, and date. "
               "Do NOT call for flight searches or price queries."
           ),
           "input_schema": {
               "type": "object",
               "$schema": "https://json-schema.org/draft/2020-12/schema",
               "properties": {
                   "origin": {
                       "type": "string",
                       "description": "IATA airport code, e.g. 'KBP' for Kyiv Boryspil",
                   },
                   "destination": {
                       "type": "string",
                       "description": "IATA airport code, e.g. 'LIS' for Lisbon",
                   },
                   "date": {
                       "type": "string",
                       "description": "ISO 8601 date: YYYY-MM-DD",
                       "pattern": r"^\d{4}-\d{2}-\d{2}$",
                   },
                   "seat_class": {
                       "type": "string",
                       "enum": ["economy", "business", "first"],
                       "description": "Cabin class. Defaults to economy.",
                   },
               },
               "required": ["origin", "destination", "date"],
               "additionalProperties": False,
           },
       },
       {
           "name": "query_db",
           "description": (
               "Call when you need to look up structured data from the internal database "
               "(orders, customers, products). Do NOT use for weather or flight booking."
           ),
           "input_schema": {
               "type": "object",
               "$schema": "https://json-schema.org/draft/2020-12/schema",
               "properties": {
                   "table": {
                       "type": "string",
                       "enum": ["orders", "customers", "products"],
                       "description": "Target database table.",
                   },
                   "filters": {
                       "type": "object",
                       "description": "Key-value pairs for WHERE clause, e.g. {\"status\": \"shipped\"}",
                       "additionalProperties": {"type": ["string", "number", "boolean"]},
                   },
                   "limit": {
                       "type": "integer",
                       "minimum": 1,
                       "maximum": 100,
                       "description": "Max rows to return. Defaults to 10.",
                   },
               },
               "required": ["table"],
               "additionalProperties": False,
           },
       },
   ]
   ```

2. **Define Pydantic v2 models that mirror each tool's `input_schema`.**

   Pydantic validates arguments before the tool implementation runs, rejecting hallucinated enum values and missing required fields before they can corrupt external state.

   ```python
   # tools/validators.py
   from __future__ import annotations
   from typing import Literal
   from pydantic import BaseModel, Field, model_validator

   class GetWeatherInput(BaseModel):
       city: str
       unit: Literal["celsius", "fahrenheit"] = "celsius"

   class BookFlightInput(BaseModel):
       origin: str = Field(pattern=r"^[A-Z]{3}$", description="3-letter IATA code")
       destination: str = Field(pattern=r"^[A-Z]{3}$", description="3-letter IATA code")
       date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
       seat_class: Literal["economy", "business", "first"] = "economy"

       @model_validator(mode="after")
       def origin_ne_destination(self) -> "BookFlightInput":
           if self.origin == self.destination:
               raise ValueError("origin and destination must differ")
           return self

   class QueryDbInput(BaseModel):
       table: Literal["orders", "customers", "products"]
       filters: dict[str, str | int | bool] = Field(default_factory=dict)
       limit: int = Field(default=10, ge=1, le=100)

   VALIDATORS: dict[str, type[BaseModel]] = {
       "get_weather": GetWeatherInput,
       "book_flight": BookFlightInput,
       "query_db": QueryDbInput,
   }
   ```

3. **Implement stub tool handlers that return typed dicts.**

   In production these call real APIs and DB connections. Keep each handler synchronous — `ThreadPoolExecutor` handles concurrency externally.

   ```python
   # tools/handlers.py
   import json
   from datetime import date

   def get_weather(city: str, unit: str = "celsius") -> dict:
       # Replace with real weather API call (e.g. Open-Meteo, WeatherAPI)
       return {"city": city, "temperature": 18, "unit": unit, "condition": "partly cloudy"}

   def book_flight(
       origin: str, destination: str, date: str, seat_class: str = "economy"
   ) -> dict:
       # Replace with real booking API call
       return {
           "booking_id": "FLT-20260502-001",
           "origin": origin,
           "destination": destination,
           "date": date,
           "seat_class": seat_class,
           "status": "confirmed",
       }

   def query_db(
       table: str, filters: dict | None = None, limit: int = 10
   ) -> dict:
       # Replace with real DB query (SQLAlchemy, asyncpg, etc.)
       return {
           "table": table,
           "rows": [],
           "count": 0,
           "filters_applied": filters or {},
       }

   REGISTRY: dict[str, callable] = {
       "get_weather": get_weather,
       "book_flight": book_flight,
       "query_db": query_db,
   }
   ```

4. **Write the parallel dispatcher that validates then executes all tool_use blocks.**

   Execute all blocks from a single response concurrently — Claude batches them intentionally to reduce round-trips. Return all results in one `user` message.

   ```python
   # tools/dispatcher.py
   from __future__ import annotations
   import json
   from concurrent.futures import ThreadPoolExecutor, as_completed
   from pydantic import ValidationError
   from tools.validators import VALIDATORS
   from tools.handlers import REGISTRY

   def _call_one(block) -> tuple[str, str]:
       """Validate + execute a single tool_use block. Returns (tool_use_id, json_result)."""
       tool_use_id = block.id
       name = block.name
       raw_input = block.input  # dict from Claude

       # Step 1: validate with Pydantic before touching external systems
       validator = VALIDATORS.get(name)
       if validator is None:
           result = {"error": f"unknown tool '{name}'", "code": "UNKNOWN_TOOL"}
           return tool_use_id, json.dumps(result)

       try:
           validated = validator.model_validate(raw_input)
       except ValidationError as exc:
           # Return structured error so Claude can self-correct arguments
           result = {
               "error": "argument validation failed",
               "code": "INVALID_ARGS",
               "details": exc.errors(include_url=False),
           }
           return tool_use_id, json.dumps(result)

       # Step 2: call the real handler
       handler = REGISTRY[name]
       try:
           output = handler(**validated.model_dump())
           return tool_use_id, json.dumps(output)
       except Exception as exc:
           result = {"error": str(exc), "code": "TOOL_ERROR", "tool": name}
           return tool_use_id, json.dumps(result)

   def dispatch_parallel(tool_use_blocks: list) -> list[dict]:
       """Execute all tool_use blocks in parallel. Returns tool_result list."""
       results = []
       with ThreadPoolExecutor(max_workers=len(tool_use_blocks) or 1) as pool:
           futures = {pool.submit(_call_one, block): block for block in tool_use_blocks}
           for future in as_completed(futures):
               tool_use_id, content = future.result()
               results.append({
                   "type": "tool_result",
                   "tool_use_id": tool_use_id,
                   "content": content,
               })
       return results
   ```

5. **Build the main agent loop with `tool_choice="auto"` and a max-turns guard.**

   Append `response.content` (the full list, including `tool_use` blocks) as the assistant message — omitting tool_use blocks from history causes an API error on the next turn.

   ```python
   # agent.py
   import anthropic
   from tools.definitions import TOOLS
   from tools.dispatcher import dispatch_parallel

   client = anthropic.Anthropic()
   MAX_TURNS = 12

   def run_agent(user_message: str) -> str:
       messages = [{"role": "user", "content": user_message}]

       for turn in range(MAX_TURNS):
           response = client.messages.create(
               model="claude-sonnet-4-6",
               max_tokens=4096,
               tools=TOOLS,
               tool_choice={"type": "auto"},
               # disable_parallel_tool_use defaults to False — Claude may batch tools
               messages=messages,
           )

           # Always append the full content list (includes tool_use blocks)
           messages.append({"role": "assistant", "content": response.content})

           if response.stop_reason == "end_turn":
               text_blocks = [b for b in response.content if b.type == "text"]
               return text_blocks[0].text if text_blocks else ""

           if response.stop_reason == "max_tokens":
               raise RuntimeError("Response truncated — increase max_tokens")

           if response.stop_reason == "tool_use":
               tool_blocks = [b for b in response.content if b.type == "tool_use"]
               tool_results = dispatch_parallel(tool_blocks)
               messages.append({"role": "user", "content": tool_results})
               continue

       raise RuntimeError(f"Agent did not finish within {MAX_TURNS} turns")

   if __name__ == "__main__":
       reply = run_agent(
           "Check weather in Lisbon, book me a flight KBP→LIS on 2026-06-15 economy, "
           "and pull the last 5 shipped orders from the database."
       )
       print(reply)
   ```

6. **Verify parallel dispatch by asserting all three tools are called in one turn.**

   Run the agent and inspect `messages` after the first tool turn. Claude should batch all three into a single `tool_use` response when `disable_parallel_tool_use` is `False`.

   ```python
   # smoke_test.py
   import anthropic
   from tools.definitions import TOOLS
   from tools.dispatcher import dispatch_parallel

   client = anthropic.Anthropic()

   response = client.messages.create(
       model="claude-sonnet-4-6",
       max_tokens=2048,
       tools=TOOLS,
       tool_choice={"type": "auto"},
       messages=[{
           "role": "user",
           "content": (
               "Simultaneously: check weather in Warsaw, book KBP→WAW on 2026-07-01, "
               "and fetch top 3 customers."
           ),
       }],
   )

   tool_blocks = [b for b in response.content if b.type == "tool_use"]
   assert len(tool_blocks) == 3, f"Expected 3 tool calls, got {len(tool_blocks)}"
   names_called = {b.name for b in tool_blocks}
   assert names_called == {"get_weather", "book_flight", "query_db"}, names_called
   print("Parallel dispatch OK:", names_called)
   ```

## Verify

Run the smoke test and the full agent:

```bash
ANTHROPIC_API_KEY=<your-key> python smoke_test.py
# Expected: Parallel dispatch OK: {'get_weather', 'book_flight', 'query_db'}

ANTHROPIC_API_KEY=<your-key> python agent.py
# Expected: natural-language summary of weather, booking confirmation, and DB rows
```

Confirm no validation bypass: pass an invalid `seat_class` like `"premium"` in `BookFlightInput` — Pydantic must raise `ValidationError` before `book_flight()` is called. Set a breakpoint in `_call_one` or add `print` to confirm the `INVALID_ARGS` error path fires.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `anthropic.BadRequestError: messages: roles must alternate` | `tool_use` blocks were stripped from assistant message before appending to history | Append the full `response.content` list (type `list[TextBlock | ToolUseBlock]`), not just `response.content[0].text` |
| Only 1 tool called even though 3 are independent | `disable_parallel_tool_use=True` is set, or tools have descriptions that imply ordering | Remove `disable_parallel_tool_use` override; rewrite descriptions so they are clearly independent |
| `ValidationError` fires on valid input | Pydantic pattern for IATA code is too strict (e.g. `^[A-Z]{3}$` fails lowercase) | Normalize `raw_input` with `.upper()` before `model_validate`, or relax the pattern and validate case-insensitively |
| Agent loops more than 5 turns on a simple query | Claude keeps calling `query_db` with different filters expecting non-empty rows | Stub handler returns `rows: []` — Claude retries; seed the stub with realistic data or add a `no_results_is_final: true` hint in the description |
| `KeyError` in `REGISTRY` after validation passes | A new tool schema was added to `TOOLS` but not to `REGISTRY` or `VALIDATORS` | Keep `TOOLS`, `VALIDATORS`, and `REGISTRY` in sync — add a startup assertion that all three share the same key set |
| `max_tokens` `RuntimeError` mid-loop | `max_tokens=4096` is too small for a multi-tool turn with large DB results | Truncate tool results to 4000 chars before returning, or raise `max_tokens` to 8192 |

## Next

- [llm-fallback-chains](../llm-fallback-chains/playbook.md) — wrap the agent with provider fallback so tool calls survive Anthropic rate-limits by retrying on `claude-haiku-4-5-20251001`.
- [knowledge/geek/ai/llm-integration/function-calling-patterns](../../../knowledge/geek/ai/llm-integration/function-calling-patterns) — production patterns for result truncation, tool routing for 15+ tool sets, and human-in-loop checkpoints before destructive operations.
- [knowledge/geek/ai/llm-integration/claude-tool-use](../../../knowledge/geek/ai/llm-integration/claude-tool-use) — forced tool-call pattern (`tool_choice={"type":"tool","name":"..."}`) for guaranteed typed JSON extraction without agentic loop overhead.

## References

- [knowledge/geek/ai/llm-integration/claude-tool-use](../../../knowledge/geek/ai/llm-integration/claude-tool-use) — defines the `stop_reason == "tool_use"` detection contract, full `response.content` append rule, and parallel tool execution with `ThreadPoolExecutor`; Steps 4 and 5 implement exactly these patterns.
- [knowledge/geek/ai/llm-integration/function-calling-patterns](../../../knowledge/geek/ai/llm-integration/function-calling-patterns) — provides the argument-validation-before-dispatch rule (Step 4 `_call_one`), `additionalProperties: false` schema constraint (Step 1), structured error format with `code` key (Steps 4 and Troubleshooting), and `max_iterations` termination guard (Step 5).
