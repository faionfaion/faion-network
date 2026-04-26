# LLM Prompts — Stream-JSON Orchestration

## Prompt 1: Generate a stream-handler skeleton

```
Write a Python class `StreamHandler` for consuming Claude Code's stream-json output. It should:

1. Spawn `claude -p "..."` as a subprocess with `--output-format stream-json`, `--allowedTools` allowlist, `--max-turns N`, closed stdin.
2. Read stdout line-by-line.
3. Dispatch events by type to handler methods (init, assistant, user, result).
4. Track cumulative cost; raise BudgetExceeded when over a threshold.
5. Return a structured Result on completion.

No external deps beyond stdlib. Use type hints.
```

## Prompt 2: Convert SDK-based agent to CLI-stream pattern

```
Take this code that uses the Claude SDK directly and convert it to spawn `claude -p` as a subprocess and consume the stream-json stream. Preserve all behavior (tool calls, budget, output) and add `--max-turns 20` and `--allowedTools` set to the same tools the SDK code allows.

Input code:
{paste here}
```

## Prompt 3: Diagnose a stream that hangs

```
This agent stream stops emitting events but doesn't exit. Suggest 5 likely causes and a check for each:

1. ...
2. ...

Code:
{paste subprocess invocation}
Recent events:
{paste last 20 events}
```

## Prompt 4: Map event types to OTel spans

```
Given the Claude Code stream-json event types (system/init, assistant, user/tool_result, result), generate Python code that creates OpenTelemetry spans following the OTel GenAI semantic conventions. Each event becomes a span; spans are properly nested.

Output: code using opentelemetry SDK only.
```
