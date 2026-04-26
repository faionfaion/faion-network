# Tool Use Code Examples

Complete code examples for implementing tool use across different LLM providers.

---

## OpenAI Examples

### Basic Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

# Define tools
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
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Tool implementation
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulated weather API call."""
    # In production, call actual weather API
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "conditions": "sunny"
    }

# Execute conversation
messages = [{"role": "user", "content": "What's the weather in Tokyo?"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# Handle tool calls
if message.tool_calls:
    messages.append(message)

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Execute the function
        if function_name == "get_weather":
            result = get_weather(**arguments)

        # Add result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    print(final_response.choices[0].message.content)
```

### Parallel Tool Calls (OpenAI)

```python
import concurrent.futures
from openai import OpenAI
import json

client = OpenAI()

# Multiple tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get latest news headlines",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"}
                },
                "required": ["topic"]
            }
        }
    }
]

# Tool registry
TOOL_REGISTRY = {
    "get_weather": lambda location: {"location": location, "temp": 22},
    "get_stock_price": lambda symbol: {"symbol": symbol, "price": 150.50},
    "get_news": lambda topic: {"topic": topic, "headlines": ["News 1", "News 2"]}
}

def execute_tools_parallel(tool_calls: list) -> list:
    """Execute multiple tool calls in parallel."""
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}

        for tool_call in tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if func_name in TOOL_REGISTRY:
                future = executor.submit(TOOL_REGISTRY[func_name], **args)
                futures[future] = tool_call

        for future in concurrent.futures.as_completed(futures):
            tool_call = futures[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"error": str(e)}

            results.append({
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return results

# Query that triggers multiple tools
messages = [
    {"role": "user", "content": "What's the weather in NYC, Apple stock price, and tech news?"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    messages.append(message)

    # Execute all tools in parallel
    tool_results = execute_tools_parallel(message.tool_calls)

    for result in tool_results:
        messages.append({
            "role": "tool",
            **result
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    print(final_response.choices[0].message.content)
```

### Structured Output with Tools (OpenAI)

```python
from openai import OpenAI
from pydantic import BaseModel
import json

client = OpenAI()

# Define structured output schema
class WeatherResponse(BaseModel):
    location: str
    temperature: float
    unit: str
    conditions: str
    humidity: int
    wind_speed: float

# Tool with structured output
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_structured_weather",
            "description": "Get detailed weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "include_forecast": {"type": "boolean", "default": False}
                },
                "required": ["location"]
            }
        }
    }
]

def get_structured_weather(location: str, include_forecast: bool = False) -> dict:
    """Return structured weather data."""
    return WeatherResponse(
        location=location,
        temperature=22.5,
        unit="celsius",
        conditions="partly cloudy",
        humidity=65,
        wind_speed=12.3
    ).model_dump()

# Use with response_format for guaranteed structure
messages = [{"role": "user", "content": "Get weather for London"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_structured_weather"}}
)

# Process tool call
message = response.choices[0].message
if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_structured_weather(**args)

    print(f"Structured result: {json.dumps(result, indent=2)}")
```

---

## Claude (Anthropic) Examples

### Basic Tool Use

```python
import anthropic
import json

client = anthropic.Anthropic()

# Define tools (Claude format)
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location. Use this when the user asks about weather conditions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g., 'Tokyo, Japan'"
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
]

# Tool implementation
def get_weather(location: str, unit: str = "celsius") -> dict:
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "conditions": "sunny",
        "humidity": 65
    }

# Initial request
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather like in Paris?"}]
)

# Handle tool use
if response.stop_reason == "tool_use":
    # Find tool use block
    tool_use_block = next(
        block for block in response.content
        if block.type == "tool_use"
    )

    # Execute tool
    tool_name = tool_use_block.name
    tool_input = tool_use_block.input

    if tool_name == "get_weather":
        result = get_weather(**tool_input)

    # Continue conversation with result
    final_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather like in Paris?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": json.dumps(result)
                    }
                ]
            }
        ]
    )

    # Extract text response
    text_block = next(
        block for block in final_response.content
        if block.type == "text"
    )
    print(text_block.text)
```

### Claude Extended Thinking with Tools

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "search_database",
        "description": "Search product database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "category": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]

# Enable extended thinking for complex reasoning
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Allow up to 10k tokens for thinking
    },
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "Find laptops under $1000 and calculate 15% discount on the cheapest one"
        }
    ]
)

# Process response with thinking blocks
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking[:200]}...")
    elif block.type == "tool_use":
        print(f"Tool call: {block.name}({block.input})")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

### Claude Streaming with Tools

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_stock_data",
        "description": "Get stock market data",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "period": {"type": "string", "enum": ["1d", "1w", "1m", "1y"]}
            },
            "required": ["symbol"]
        }
    }
]

def get_stock_data(symbol: str, period: str = "1d") -> dict:
    return {"symbol": symbol, "price": 150.50, "change": 2.3, "period": period}

# Streaming response
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's Apple's stock doing today?"}]
) as stream:
    tool_use_block = None

    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                tool_use_block = {
                    "id": event.content_block.id,
                    "name": event.content_block.name,
                    "input": ""
                }
        elif event.type == "content_block_delta":
            if hasattr(event.delta, "partial_json"):
                tool_use_block["input"] += event.delta.partial_json
        elif event.type == "content_block_stop":
            if tool_use_block:
                # Parse and execute tool
                tool_input = json.loads(tool_use_block["input"])
                result = get_stock_data(**tool_input)
                print(f"Tool result: {result}")
                tool_use_block = None
        elif event.type == "text":
            print(event.text, end="", flush=True)
```

---

## Gemini Examples

### Basic Function Calling

```python
import google.generativeai as genai
import json

genai.configure(api_key="YOUR_API_KEY")

# Define function declarations (Gemini format)
get_weather_func = genai.protos.FunctionDeclaration(
    name="get_weather",
    description="Get current weather for a location",
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            "location": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                description="City name"
            ),
            "unit": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                enum=["celsius", "fahrenheit"]
            )
        },
        required=["location"]
    )
)

# Create tool
weather_tool = genai.protos.Tool(
    function_declarations=[get_weather_func]
)

# Initialize model with tools
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[weather_tool]
)

# Tool implementation
def get_weather(location: str, unit: str = "celsius") -> dict:
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "conditions": "sunny"
    }

# Start chat
chat = model.start_chat()

# Send message
response = chat.send_message("What's the weather in Berlin?")

# Handle function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call

    # Execute function
    if function_call.name == "get_weather":
        args = dict(function_call.args)
        result = get_weather(**args)

    # Send function response
    response = chat.send_message(
        genai.protos.Content(
            parts=[
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_call.name,
                        response={"result": result}
                    )
                )
            ]
        )
    )

    print(response.text)
```

### Gemini with Google Search Grounding

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Enable Google Search as a tool
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[genai.protos.Tool(google_search_retrieval={})]
)

# Query with grounding
response = model.generate_content(
    "What are the latest developments in quantum computing this week?"
)

print(response.text)

# Access grounding metadata
if response.candidates[0].grounding_metadata:
    for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.web.uri}")
```

---

## Multi-Provider Abstraction

### Unified Tool Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable
import json

class ToolProvider(ABC):
    """Abstract base class for tool-calling providers."""

    @abstractmethod
    def format_tools(self, tools: List[Dict]) -> Any:
        """Format tools for the provider."""
        pass

    @abstractmethod
    def execute(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Execute conversation with tools."""
        pass

    @abstractmethod
    def parse_tool_calls(self, response: Any) -> List[Dict]:
        """Parse tool calls from response."""
        pass

class OpenAIProvider(ToolProvider):
    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            }
            for tool in tools
        ]

    def execute(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.format_tools(tools),
            tool_choice="auto"
        )
        return response

    def parse_tool_calls(self, response) -> List[Dict]:
        message = response.choices[0].message
        if not message.tool_calls:
            return []
        return [
            {
                "id": tc.id,
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments)
            }
            for tc in message.tool_calls
        ]

class ClaudeProvider(ToolProvider):
    def __init__(self, client, model: str = "claude-sonnet-4-20250514"):
        self.client = client
        self.model = model

    def format_tools(self, tools: List[Dict]) -> List[Dict]:
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool["parameters"]
            }
            for tool in tools
        ]

    def execute(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=self.format_tools(tools),
            messages=messages
        )
        return response

    def parse_tool_calls(self, response) -> List[Dict]:
        tool_calls = []
        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "arguments": block.input
                })
        return tool_calls

class UnifiedToolExecutor:
    """Execute tools across different providers."""

    def __init__(self, provider: ToolProvider, tool_registry: Dict[str, Callable]):
        self.provider = provider
        self.tool_registry = tool_registry

    def run(self, query: str, tools: List[Dict], max_iterations: int = 5) -> Dict:
        messages = [{"role": "user", "content": query}]
        iteration = 0
        tool_history = []

        while iteration < max_iterations:
            response = self.provider.execute(messages, tools)
            tool_calls = self.provider.parse_tool_calls(response)

            if not tool_calls:
                return {
                    "success": True,
                    "response": self._extract_text(response),
                    "tool_history": tool_history
                }

            # Execute tools
            for tool_call in tool_calls:
                name = tool_call["name"]
                args = tool_call["arguments"]

                if name in self.tool_registry:
                    result = self.tool_registry[name](**args)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                tool_history.append({
                    "tool": name,
                    "arguments": args,
                    "result": result
                })

                # Add result to messages (provider-specific format)
                messages = self._add_tool_result(messages, response, tool_call, result)

            iteration += 1

        return {
            "success": False,
            "error": "Max iterations reached",
            "tool_history": tool_history
        }

    def _extract_text(self, response) -> str:
        """Extract text from provider response."""
        if hasattr(response, 'choices'):  # OpenAI
            return response.choices[0].message.content
        else:  # Claude
            for block in response.content:
                if block.type == "text":
                    return block.text
        return ""

    def _add_tool_result(self, messages, response, tool_call, result):
        """Add tool result to messages in provider-specific format."""
        # Implementation depends on provider
        # This is a simplified version
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(result)
        })
        return messages

# Usage
from openai import OpenAI

client = OpenAI()
provider = OpenAIProvider(client)

tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }
]

registry = {
    "get_weather": lambda location: {"temp": 22, "location": location}
}

executor = UnifiedToolExecutor(provider, registry)
result = executor.run("What's the weather in London?", tools)
print(result)
```

---

## Agentic Tool Use Examples

### ReAct Agent Pattern

```python
from openai import OpenAI
import json
from typing import List, Dict, Any

client = OpenAI()

class ReActAgent:
    """Reasoning and Acting agent with tools."""

    SYSTEM_PROMPT = """You are a helpful assistant that solves problems step by step.

For each step:
1. THOUGHT: Analyze what you need to do next
2. ACTION: If needed, call a tool to get information
3. OBSERVATION: Process the tool result
4. Repeat until you can provide a final answer

When you have enough information, provide a clear final answer."""

    def __init__(self, tools: List[Dict], tool_registry: Dict[str, Any], max_steps: int = 10):
        self.tools = tools
        self.tool_registry = tool_registry
        self.max_steps = max_steps

    def run(self, query: str) -> Dict:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]

        steps = []

        for step in range(self.max_steps):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[{"type": "function", "function": t} for t in self.tools],
                tool_choice="auto"
            )

            message = response.choices[0].message

            # Record thought
            if message.content:
                steps.append({
                    "type": "thought",
                    "content": message.content
                })

            # Check if done
            if not message.tool_calls:
                return {
                    "success": True,
                    "answer": message.content,
                    "steps": steps
                }

            # Execute tools
            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                steps.append({
                    "type": "action",
                    "tool": name,
                    "arguments": args
                })

                if name in self.tool_registry:
                    result = self.tool_registry[name](**args)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                steps.append({
                    "type": "observation",
                    "result": result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        return {
            "success": False,
            "error": "Max steps reached",
            "steps": steps
        }

# Example tools for research agent
tools = [
    {
        "name": "search_web",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_page",
        "description": "Read content from a webpage",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to read"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        }
    }
]

# Tool implementations
def search_web(query: str) -> Dict:
    # Simulated search results
    return {
        "results": [
            {"title": "Result 1", "url": "https://example.com/1", "snippet": "..."},
            {"title": "Result 2", "url": "https://example.com/2", "snippet": "..."}
        ]
    }

def read_page(url: str) -> Dict:
    # Simulated page content
    return {"content": f"Content from {url}...", "title": "Page Title"}

def calculate(expression: str) -> Dict:
    try:
        # WARNING: eval is dangerous, use a safe math parser in production
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Run agent
agent = ReActAgent(
    tools=tools,
    tool_registry={
        "search_web": search_web,
        "read_page": read_page,
        "calculate": calculate
    }
)

result = agent.run("What is the population of France and what's 15% of that number?")
print(json.dumps(result, indent=2))
```

### Multi-Agent Tool Orchestration

```python
from openai import OpenAI
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

client = OpenAI()

class AgentRole(Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"

@dataclass
class Agent:
    name: str
    role: AgentRole
    system_prompt: str
    tools: List[Dict]
    tool_registry: Dict[str, Any]

class MultiAgentOrchestrator:
    """Orchestrate multiple specialized agents."""

    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents

    def run_agent(self, agent_name: str, task: str, context: str = "") -> Dict:
        agent = self.agents[agent_name]

        messages = [
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nTask: {task}"}
        ]

        max_iterations = 5
        results = []

        for _ in range(max_iterations):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[{"type": "function", "function": t} for t in agent.tools] if agent.tools else None,
                tool_choice="auto" if agent.tools else None
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "agent": agent_name,
                    "response": message.content,
                    "tool_results": results
                }

            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if name in agent.tool_registry:
                    result = agent.tool_registry[name](**args)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                results.append({"tool": name, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        return {
            "agent": agent_name,
            "error": "Max iterations reached",
            "tool_results": results
        }

    def run_pipeline(self, task: str, agent_sequence: List[str]) -> Dict:
        """Run agents in sequence, passing context forward."""
        context = ""
        pipeline_results = []

        for agent_name in agent_sequence:
            result = self.run_agent(agent_name, task, context)
            pipeline_results.append(result)
            context = f"Previous agent ({agent_name}) output:\n{result.get('response', '')}"

        return {
            "task": task,
            "pipeline": pipeline_results,
            "final_output": pipeline_results[-1].get("response") if pipeline_results else None
        }

# Define specialized agents
researcher = Agent(
    name="researcher",
    role=AgentRole.RESEARCHER,
    system_prompt="You are a research specialist. Gather information using available tools.",
    tools=[
        {
            "name": "search",
            "description": "Search for information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    ],
    tool_registry={
        "search": lambda query: {"results": [f"Result for: {query}"]}
    }
)

analyst = Agent(
    name="analyst",
    role=AgentRole.ANALYST,
    system_prompt="You are a data analyst. Analyze information and extract insights.",
    tools=[
        {
            "name": "analyze_data",
            "description": "Analyze data and extract patterns",
            "parameters": {
                "type": "object",
                "properties": {"data": {"type": "string"}},
                "required": ["data"]
            }
        }
    ],
    tool_registry={
        "analyze_data": lambda data: {"insights": ["Insight 1", "Insight 2"]}
    }
)

writer = Agent(
    name="writer",
    role=AgentRole.WRITER,
    system_prompt="You are a content writer. Create clear, engaging content.",
    tools=[],
    tool_registry={}
)

# Create orchestrator
orchestrator = MultiAgentOrchestrator({
    "researcher": researcher,
    "analyst": analyst,
    "writer": writer
})

# Run pipeline
result = orchestrator.run_pipeline(
    task="Research AI trends and write a summary",
    agent_sequence=["researcher", "analyst", "writer"]
)

print(json.dumps(result, indent=2))
```

---

## Error Handling Examples

### Robust Error Handling

```python
from openai import OpenAI
import json
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    EXECUTION_ERROR = "execution_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_TOOL = "unknown_tool"

@dataclass
class ToolError:
    type: ErrorType
    message: str
    details: Dict[str, Any] = None
    recoverable: bool = True

def safe_tool_executor(
    tool_name: str,
    arguments: Dict,
    tool_registry: Dict,
    timeout: float = 30.0
) -> Dict:
    """Execute tool with comprehensive error handling."""
    import signal

    # Check if tool exists
    if tool_name not in tool_registry:
        return {
            "success": False,
            "error": ToolError(
                type=ErrorType.UNKNOWN_TOOL,
                message=f"Tool '{tool_name}' not found",
                recoverable=False
            ).__dict__
        }

    # Validate arguments (simplified)
    tool_func = tool_registry[tool_name]

    try:
        # Timeout handling (Unix only)
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Tool {tool_name} timed out after {timeout}s")

        # Set timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout))

        try:
            result = tool_func(**arguments)
            return {
                "success": True,
                "result": result
            }
        finally:
            signal.alarm(0)  # Cancel timeout

    except TimeoutError as e:
        return {
            "success": False,
            "error": ToolError(
                type=ErrorType.TIMEOUT_ERROR,
                message=str(e),
                recoverable=True
            ).__dict__
        }
    except TypeError as e:
        return {
            "success": False,
            "error": ToolError(
                type=ErrorType.VALIDATION_ERROR,
                message=f"Invalid arguments: {e}",
                details={"arguments": arguments},
                recoverable=True
            ).__dict__
        }
    except Exception as e:
        return {
            "success": False,
            "error": ToolError(
                type=ErrorType.EXECUTION_ERROR,
                message=str(e),
                recoverable=True
            ).__dict__
        }

# Usage with retry logic
def execute_with_retry(
    client,
    messages: list,
    tools: list,
    tool_registry: dict,
    max_retries: int = 3
) -> Dict:
    """Execute tools with automatic retry on recoverable errors."""

    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return {"success": True, "response": message.content}

        messages.append(message)
        all_succeeded = True

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = safe_tool_executor(name, args, tool_registry)

            if not result["success"]:
                all_succeeded = False
                if not result["error"].get("recoverable", True):
                    return {"success": False, "error": result["error"]}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        if all_succeeded:
            # Get final response
            final = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return {"success": True, "response": final.choices[0].message.content}

    return {"success": False, "error": "Max retries exceeded"}
```

---

## Testing Examples

### Unit Testing Tools

```python
import pytest
from unittest.mock import Mock, patch
import json

# Tool under test
def get_user_orders(user_id: str, limit: int = 10) -> dict:
    """Get orders for a user."""
    # In production, this calls a database
    pass

class TestGetUserOrders:
    """Unit tests for get_user_orders tool."""

    def test_valid_user_returns_orders(self):
        with patch('module.get_orders_from_db') as mock_db:
            mock_db.return_value = [
                {"id": "1", "total": 100},
                {"id": "2", "total": 200}
            ]

            result = get_user_orders("user123", limit=2)

            assert len(result["orders"]) == 2
            mock_db.assert_called_once_with("user123", 2)

    def test_invalid_user_returns_empty(self):
        with patch('module.get_orders_from_db') as mock_db:
            mock_db.return_value = []

            result = get_user_orders("invalid_user")

            assert result["orders"] == []

    def test_handles_database_error(self):
        with patch('module.get_orders_from_db') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")

            result = get_user_orders("user123")

            assert "error" in result
            assert "Database" in result["error"]

# Integration test with LLM
class TestToolIntegration:
    """Integration tests for tool calling."""

    @pytest.fixture
    def mock_client(self):
        return Mock()

    def test_llm_calls_correct_tool(self, mock_client):
        # Mock LLM response with tool call
        mock_response = Mock()
        mock_response.choices[0].message.tool_calls = [
            Mock(
                id="call_123",
                function=Mock(
                    name="get_user_orders",
                    arguments='{"user_id": "user123", "limit": 5}'
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        # Execute
        result = execute_with_tools(
            mock_client,
            "Get last 5 orders for user123",
            tools=[...],
            tool_registry={"get_user_orders": get_user_orders}
        )

        # Verify tool was called correctly
        assert "get_user_orders" in str(result)
```

---

## Performance Optimization

### Caching Tool Results

```python
import hashlib
import json
from functools import wraps
from typing import Dict, Any, Optional
import redis
from datetime import timedelta

class ToolCache:
    """Cache for tool results."""

    def __init__(self, redis_client: redis.Redis, default_ttl: int = 300):
        self.redis = redis_client
        self.default_ttl = default_ttl

    def _make_key(self, tool_name: str, arguments: Dict) -> str:
        """Generate cache key from tool name and arguments."""
        args_str = json.dumps(arguments, sort_keys=True)
        hash_val = hashlib.md5(args_str.encode()).hexdigest()
        return f"tool_cache:{tool_name}:{hash_val}"

    def get(self, tool_name: str, arguments: Dict) -> Optional[Dict]:
        """Get cached result."""
        key = self._make_key(tool_name, arguments)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set(self, tool_name: str, arguments: Dict, result: Dict, ttl: int = None):
        """Cache result."""
        key = self._make_key(tool_name, arguments)
        ttl = ttl or self.default_ttl
        self.redis.setex(key, ttl, json.dumps(result))

def cached_tool(cache: ToolCache, ttl: int = None):
    """Decorator to cache tool results."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            tool_name = func.__name__

            # Check cache
            cached = cache.get(tool_name, kwargs)
            if cached:
                return cached

            # Execute tool
            result = func(**kwargs)

            # Cache result
            cache.set(tool_name, kwargs, result, ttl)

            return result
        return wrapper
    return decorator

# Usage
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = ToolCache(redis_client)

@cached_tool(cache, ttl=60)
def get_weather(location: str) -> Dict:
    """Get weather - cached for 60 seconds."""
    # Expensive API call
    return {"location": location, "temp": 22}
```

---

## Related Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklists |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for tool design |
