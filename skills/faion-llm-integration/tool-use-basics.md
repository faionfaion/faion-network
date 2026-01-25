---
id: tool-use-basics
name: "Tool Use Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Tool Use Basics

## Overview

Tool use enables LLMs to interact with external systems by calling functions, APIs, or executing code. This extends LLM capabilities beyond text generation to perform real-world actions like searching the web, querying databases, or controlling applications.

## When to Use

- Accessing real-time data (weather, stocks, news)
- Performing calculations with precision
- Interacting with databases or APIs
- Executing code safely
- Building AI agents
- Multi-step task automation

## Key Concepts

### Tool Use Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│  LLM    │────▶│ Execute │────▶│   LLM   │
│ Request │     │ Decides │     │  Tool   │     │ Response│
└─────────┘     │ Tool    │     └─────────┘     └─────────┘
                └─────────┘           │
                     ▲                │
                     └────────────────┘
                      Tool Result
```

### Supported Providers

| Provider | Feature Name | Max Tools |
|----------|--------------|-----------|
| OpenAI | Function Calling | 128 |
| Anthropic | Tool Use | 64 |
| Google | Function Calling | 64 |
| Ollama | Tools | Varies |

## Implementation

### OpenAI Function Calling

```python
from openai import OpenAI
import json
from typing import List, Dict, Callable

client = OpenAI()

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country, e.g., 'London, UK'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search the product database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["electronics", "clothing", "books", "all"]
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Tool implementations
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Mock weather function."""
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "sunny"
    }

def search_database(query: str, category: str = "all", max_results: int = 5) -> list:
    """Mock database search."""
    return [
        {"name": f"Product {i}", "price": 10 * i, "category": category}
        for i in range(1, min(max_results + 1, 6))
    ]

TOOL_REGISTRY = {
    "get_weather": get_weather,
    "search_database": search_database
}

def chat_with_tools(messages: List[Dict]) -> str:
    """Chat with tool use capability."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # or "none", "required", or specific tool
    )

    message = response.choices[0].message

    # Check if tool call is needed
    if message.tool_calls:
        # Add assistant message with tool calls
        messages.append(message)

        # Execute each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute the function
            if function_name in TOOL_REGISTRY:
                result = TOOL_REGISTRY[function_name](**arguments)
            else:
                result = {"error": f"Unknown function: {function_name}"}

            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Get final response
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        return final_response.choices[0].message.content

    return message.content

# Usage
messages = [{"role": "user", "content": "What's the weather in Paris?"}]
response = chat_with_tools(messages)
print(response)
```

### Anthropic Tool Use

```python
from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g., 'London, UK'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

def chat_with_claude_tools(user_message: str) -> str:
    """Chat with Claude using tools."""
    messages = [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Process tool use
    while response.stop_reason == "tool_use":
        # Extract tool use blocks
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute tool
        tool_result = TOOL_REGISTRY[tool_use_block.name](**tool_use_block.input)

        # Continue conversation
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(tool_result)
                }]
            }
        ]

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

    # Get text response
    return next(
        block.text for block in response.content
        if hasattr(block, "text")
    )
```

### Tool Definition Generator

```python
from typing import Callable, get_type_hints
import inspect

def generate_tool_definition(func: Callable) -> dict:
    """Generate OpenAI tool definition from Python function."""
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    doc = inspect.getdoc(func) or ""

    # Parse docstring for parameter descriptions
    param_descriptions = {}
    for line in doc.split("\n"):
        if ":" in line and line.strip().startswith(":param"):
            parts = line.split(":", 2)
            if len(parts) >= 3:
                param_name = parts[1].replace("param", "").strip()
                param_descriptions[param_name] = parts[2].strip()

    # Build properties
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if name in ["self", "cls"]:
            continue

        param_type = hints.get(name, str)

        # Map Python types to JSON schema types
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }

        properties[name] = {
            "type": type_map.get(param_type, "string"),
            "description": param_descriptions.get(name, "")
        }

        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\n")[0] if doc else "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

# Usage
def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int
) -> dict:
    """Calculate monthly mortgage payment.

    :param principal: Loan amount in dollars
    :param annual_rate: Annual interest rate (e.g., 0.05 for 5%)
    :param years: Loan term in years
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return {"monthly_payment": round(payment, 2)}

tool_def = generate_tool_definition(calculate_mortgage)
print(json.dumps(tool_def, indent=2))
```

### Code Execution Tool

```python
import subprocess
import tempfile
import os

def execute_python(code: str, timeout: int = 30) -> dict:
    """Safely execute Python code in a sandbox."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    ) as f:
        f.write(code)
        temp_path = f.name

    try:
        # Execute with timeout
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {"error": f"Execution timed out after {timeout} seconds"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        os.unlink(temp_path)

# Tool definition for code execution
CODE_EXECUTION_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Execute Python code and return the output. Use for calculations, data processing, or generating results.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
                }
            },
            "required": ["code"]
        }
    }
}
```

## Best Practices

1. **Tool Design**
   - Clear, specific descriptions
   - Well-defined parameter schemas
   - Handle errors gracefully

2. **Security**
   - Validate all inputs
   - Sandbox code execution
   - Limit tool permissions

3. **Performance**
   - Execute independent tools in parallel
   - Set appropriate timeouts
   - Cache frequently used results

4. **Error Handling**
   - Return structured error messages
   - Allow LLM to recover from errors
   - Log all tool executions

5. **Testing**
   - Test tools independently
   - Test tool selection by LLM
   - Test error recovery

## Common Pitfalls

1. **Vague Descriptions** - LLM can't choose the right tool
2. **Missing Parameters** - Function fails with missing args
3. **No Error Handling** - Crashes propagate to user
4. **Infinite Loops** - No iteration limit in agent loops
5. **Security Holes** - Unsafe code execution
6. **No Timeout** - Tools can hang indefinitely

## References

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
