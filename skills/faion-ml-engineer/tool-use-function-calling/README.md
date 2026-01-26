# Tool Use and Function Calling

Comprehensive guide to implementing LLM tool use and function calling in production systems.

## Overview

Function calling (also called tool use) enables LLMs to interact with external systems by generating structured outputs that specify which functions to call and with what parameters. The LLM does not execute functions directly - it analyzes user intent and produces structured JSON that your code then executes.

**Key Insight:** Tool calling is the foundation of agentic AI systems. Modern frameworks like LangChain, LlamaIndex, AutoGen, and CrewAI all rely on this capability.

## Key Concepts

### Function Calling Flow

```
User Message → LLM Analysis → Tool Selection → Structured Output → Code Execution → Result → LLM Response
```

1. **Context Assembly:** System message, tool definitions, and user message form the complete context
2. **Intent Analysis:** LLM determines if a tool call is needed
3. **Tool Selection:** LLM chooses appropriate tool(s) and extracts parameters
4. **Structured Output:** LLM returns JSON with function name and arguments
5. **Execution:** Your code executes the actual function
6. **Result Processing:** Results are sent back to LLM for final response

### Tool Definitions

Tool definitions describe available functions to the LLM:

| Component | Purpose | Example |
|-----------|---------|---------|
| Name | Unique identifier | `get_weather` |
| Description | What the tool does | "Get current weather for a location" |
| Parameters | JSON Schema for inputs | `{location: string, unit: enum}` |
| Required | Mandatory parameters | `["location"]` |

**Important:** Tool definitions consume tokens on every LLM call. Be concise but descriptive.

### Structured Output

LLMs generate structured JSON for tool calls:

```json
{
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\": \"Paris\", \"unit\": \"celsius\"}"
      }
    }
  ]
}
```

### Tool Choice Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `auto` | LLM decides whether to call tools | General conversations |
| `required` | LLM must call at least one tool | Extraction tasks |
| `none` | Tools disabled for this call | Follow-up questions |
| `{name}` | Force specific tool | Deterministic workflows |

## Provider Comparison

### Feature Matrix

| Feature | OpenAI | Claude | Gemini | Local (Ollama) |
|---------|--------|--------|--------|----------------|
| Parallel tool calls | Yes | Yes | Yes | Model-dependent |
| Streaming tool calls | Yes | Yes | Yes | Limited |
| Tool choice modes | auto/required/none/specific | auto/any/tool | auto/none/specific | Limited |
| Max tools | 128 | 64 | 128 | Model-dependent |
| Structured output | JSON mode + tools | Tools only | JSON mode + tools | Limited |
| Interleaved thinking | No | Yes (extended) | No | No |

### Provider Selection Guide

| Scenario | Recommended Provider | Reason |
|----------|---------------------|--------|
| General purpose agents | OpenAI GPT-4o | Reliable, fast, good tool accuracy |
| Complex reasoning chains | Claude 3.5 Sonnet | Extended thinking, long context |
| Multimodal + grounding | Gemini 2.0 | 2M context, Google Search integration |
| Privacy-sensitive | Local (Ollama) | No data leaves your infrastructure |
| High volume, cost-sensitive | GPT-4o-mini or Gemini Flash | Lower cost per token |
| Code generation agents | Claude 3.5 Sonnet | Best code quality |

### API Differences

**OpenAI:**
- Uses `tools` parameter with `type: "function"`
- Returns `tool_calls` array in message
- Requires `tool_call_id` in response

**Claude:**
- Uses `tools` parameter with `input_schema`
- Returns `tool_use` content blocks
- Uses `tool_result` content type in response

**Gemini:**
- Uses `tools` with `function_declarations`
- Returns `function_call` in response
- Supports `function_response` for results

## When to Use Tool Calling

### Good Use Cases

| Use Case | Example |
|----------|---------|
| Data retrieval | Fetch weather, stock prices, user data |
| External API calls | Send emails, create tickets, post messages |
| Database operations | Query, insert, update records |
| File operations | Read, write, search files |
| Calculations | Complex math, unit conversions |
| Search | Web search, document search, RAG |
| Code execution | Run code, execute scripts |
| System commands | Manage resources, trigger workflows |

### When NOT to Use

| Scenario | Alternative |
|----------|-------------|
| Simple Q&A | Direct LLM response |
| Creative writing | LLM generation |
| Summarization | LLM processing |
| Translation | LLM capabilities |
| Static knowledge | RAG or fine-tuning |

## Architecture Patterns

### Single Tool Call

```
User → LLM → Tool Call → Execute → LLM → Response
```

Best for: Simple queries with one action.

### Parallel Tool Calls

```
User → LLM → [Tool A, Tool B, Tool C] → Execute All → LLM → Response
```

Best for: Independent data retrieval (e.g., get weather + stock price + news).

### Sequential Tool Calls (Agentic Loop)

```
User → LLM → Tool A → Execute → LLM → Tool B → Execute → ... → Response
```

Best for: Dependent operations where next step depends on previous result.

### Tool Router Pattern

```
User → Router LLM → Select Tool Set → Specialist LLM → Execute → Response
```

Best for: Large number of tools (>20), specialized domains.

## Best Practices Summary

### Tool Design

1. **Clear naming:** Use descriptive, action-oriented names (`get_user_orders`, not `orders`)
2. **Focused scope:** One tool, one responsibility
3. **Explicit parameters:** Use JSON Schema with descriptions and examples
4. **Sensible defaults:** Reduce required parameters where possible
5. **Consistent patterns:** Similar tools should have similar interfaces

### Implementation

1. **Error handling:** Return structured error messages, allow LLM to retry
2. **Timeouts:** Set reasonable limits for external calls
3. **Logging:** Track all tool calls for debugging and monitoring
4. **Validation:** Validate arguments before execution
5. **Rate limiting:** Protect external APIs from abuse

### Security

1. **Input validation:** Never trust LLM-generated arguments blindly
2. **Sandboxing:** Execute tools in isolated environments where possible
3. **Human approval:** Require confirmation for destructive operations
4. **Audit logging:** Record all tool executions with full context
5. **Secrets management:** Never expose credentials in tool definitions

### Performance

1. **Parallel execution:** Execute independent tools concurrently
2. **Caching:** Cache repeated tool results
3. **Batching:** Combine similar operations when possible
4. **Streaming:** Use streaming for long-running operations
5. **Token management:** Minimize tool definitions size

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many tools | Use RAG to select relevant tools per query |
| Vague descriptions | Write detailed descriptions with examples |
| Missing validation | Validate all parameters before execution |
| No error recovery | Return structured errors, allow retries |
| Infinite loops | Set max iterations for agentic loops |
| Token bloat | Trim tool definitions, use concise descriptions |

## External Links

### Official Documentation

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Google Gemini Function Calling](https://ai.google.dev/docs/function_calling)
- [OpenRouter Tool Calling](https://openrouter.ai/docs/guides/features/tool-calling)

### Guides and Tutorials

- [Function Calling with LLMs - Martin Fowler](https://martinfowler.com/articles/function-call-LLM.html)
- [Function Calling Guide - Prompt Engineering Guide](https://www.promptingguide.ai/applications/function_calling)
- [Function Calling in AI Agents](https://www.promptingguide.ai/agents/function-calling)
- [Mastering LLM Tool Calling - MLM](https://machinelearningmastery.com/mastering-llm-tool-calling-the-complete-framework-for-connecting-models-to-the-real-world/)

### Framework Documentation

- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [LlamaIndex Tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/)
- [Vercel AI SDK Tools](https://sdk.vercel.ai/docs/ai-sdk-core/tools-and-tool-calling)

### Best Practices Articles

- [Tool Best Practices - Medium](https://medium.com/@laurentkubaski/tool-or-function-calling-best-practices-a5165a33d5f1)
- [Complete 2025 Guide - Medium](https://medium.com/@sayalisureshkumbhar/how-tools-are-called-in-ai-agents-complete-2025-guide-with-examples-42dcdfe6ba38)
- [OpenAI Community Best Practices](https://community.openai.com/t/prompting-best-practices-for-tool-use-function-calling/1123036)

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Tool design and implementation checklists |
| [examples.md](examples.md) | Code examples for all providers |
| [templates.md](templates.md) | Reusable templates for tools and agents |
| [llm-prompts.md](llm-prompts.md) | Prompts for tool design and debugging |
