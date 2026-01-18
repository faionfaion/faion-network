# M-LLM-005: Function Calling / Tool Use

## Overview

Function calling enables LLMs to invoke external tools, APIs, and code. The model outputs structured function calls that your application executes. This bridges the gap between language understanding and real-world actions.

**When to use:** When LLMs need to interact with external systems, perform calculations, access databases, or execute code.

## Core Concepts

### 1. Function Calling Flow

```
User Query
    ↓
LLM analyzes and selects function
    ↓
LLM outputs: { function: "name", args: {...} }
    ↓
Application executes function
    ↓
Result returned to LLM
    ↓
LLM generates final response
```

### 2. Function Definition Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Name** | Unique identifier | `search_database` |
| **Description** | When to use this function | "Search product database by filters" |
| **Parameters** | Input schema | JSON Schema object |
| **Required** | Mandatory parameters | `["query"]` |
| **Returns** | Output format | "List of products" |

### 3. Provider Comparison

| Provider | Feature | Syntax |
|----------|---------|--------|
| **OpenAI** | `tools` parameter | JSON Schema |
| **Claude** | `tools` parameter | JSON Schema |
| **Gemini** | `function_declarations` | OpenAPI-like |
| **Mistral** | `tools` parameter | JSON Schema |

## Best Practices

### 1. Write Clear Descriptions

```python
# Bad: Vague description
{
    "name": "search",
    "description": "Search things"
}

# Good: Specific description
{
    "name": "search_products",
    "description": "Search the product catalog. Use when user asks about products, prices, or availability. Returns product name, price, and stock status."
}
```

### 2. Use Strict Schemas

```python
{
    "name": "create_order",
    "description": "Create a new order for a customer",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "Unique customer identifier (UUID format)"
            },
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"},
                        "quantity": {"type": "integer", "minimum": 1}
                    },
                    "required": ["product_id", "quantity"]
                },
                "minItems": 1
            },
            "shipping_address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "country": {"type": "string"},
                    "postal_code": {"type": "string"}
                },
                "required": ["street", "city", "country"]
            }
        },
        "required": ["customer_id", "items", "shipping_address"]
    }
}
```

### 3. Handle Errors Gracefully

```python
def execute_function(name: str, args: dict) -> dict:
    try:
        result = functions[name](**args)
        return {"success": True, "result": result}
    except KeyError:
        return {"success": False, "error": f"Unknown function: {name}"}
    except TypeError as e:
        return {"success": False, "error": f"Invalid arguments: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Execution failed: {e}"}
```

## Common Patterns

### Pattern 1: OpenAI Function Calling

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'San Francisco, CA'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"  # or "required" to force tool use
)

# Check if model wants to call a function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # Execute the function
    result = get_weather(**function_args)

    # Send result back to model
    messages = [
        {"role": "user", "content": "What's the weather in Tokyo?"},
        response.choices[0].message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    ]

    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
```

### Pattern 2: Claude Tool Use

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "search_database",
        "description": "Search the product database for items matching criteria",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "category": {
                    "type": "string",
                    "enum": ["electronics", "clothing", "home", "sports"]
                },
                "max_price": {
                    "type": "number",
                    "description": "Maximum price in USD"
                }
            },
            "required": ["query"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Find me laptops under $1000"}]
)

# Process tool use
if response.stop_reason == "tool_use":
    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id

            # Execute tool
            result = execute_tool(tool_name, tool_input)

            # Continue conversation with result
            messages = [
                {"role": "user", "content": "Find me laptops under $1000"},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        }
                    ]
                }
            ]

            final = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )
```

### Pattern 3: Parallel Function Calls

```python
# Model can request multiple function calls simultaneously
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo, London, and NYC?"}
    ],
    tools=tools
)

# Process multiple tool calls
if response.choices[0].message.tool_calls:
    tool_results = []

    for tool_call in response.choices[0].message.tool_calls:
        result = execute_function(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Send all results back
    messages.extend(tool_results)
```

### Pattern 4: Function Chaining

```python
def process_with_functions(user_input: str, max_iterations: int = 5) -> str:
    messages = [{"role": "user", "content": user_input}]

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        messages.append(message)

        # No more function calls needed
        if not message.tool_calls:
            return message.content

        # Execute all function calls
        for tool_call in message.tool_calls:
            result = execute_function(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Max iterations reached"
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Vague descriptions | Wrong function selected | Be specific about when to use |
| Missing required fields | Runtime errors | Validate schema completeness |
| No error handling | Crashes on failure | Return structured errors |
| Unsafe function execution | Security risks | Sandbox, validate inputs |
| No rate limiting | API abuse | Throttle function calls |

## Security Considerations

### Input Validation
```python
def safe_execute(name: str, args: dict) -> dict:
    # Validate function exists
    if name not in allowed_functions:
        return {"error": "Function not allowed"}

    # Validate arguments
    schema = function_schemas[name]
    errors = validate_against_schema(args, schema)
    if errors:
        return {"error": f"Invalid arguments: {errors}"}

    # Sanitize inputs
    sanitized_args = sanitize(args)

    # Execute with timeout
    try:
        with timeout(30):  # 30 second limit
            return allowed_functions[name](**sanitized_args)
    except TimeoutError:
        return {"error": "Function timed out"}
```

### Permission Levels
```python
function_permissions = {
    "read_data": ["user", "admin"],
    "write_data": ["admin"],
    "delete_data": ["admin"],
    "execute_code": []  # No one can use this
}

def check_permission(function_name: str, user_role: str) -> bool:
    return user_role in function_permissions.get(function_name, [])
```

## Tools & References

### Related Skills
- faion-openai-api-skill
- faion-claude-api-skill
- faion-gemini-api-skill

### Related Agents
- faion-prompt-engineer-agent

### External Resources
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Claude Tool Use](https://docs.anthropic.com/claude/docs/tool-use)
- [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Checklist

- [ ] Functions have clear, specific descriptions
- [ ] Parameter schemas are complete and typed
- [ ] Required fields are marked
- [ ] Error handling implemented
- [ ] Security validation in place
- [ ] Rate limiting configured
- [ ] Parallel calls supported if needed
- [ ] Function chaining handled
- [ ] Timeouts set
- [ ] Logging enabled

---

*Methodology: M-LLM-005 | Category: LLM/Orchestration*
*Related: faion-openai-api-skill, faion-claude-api-skill, faion-gemini-api-skill*
