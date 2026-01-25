---
id: function-calling-patterns
name: "Function Calling Patterns"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Function Calling Patterns

Advanced patterns for implementing tool use and function calling in production systems.

## Parallel Tool Calls

```python
def execute_parallel_tools(tool_calls: list) -> list:
    """Execute multiple tool calls in parallel."""
    import concurrent.futures

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if function_name in TOOL_REGISTRY:
                future = executor.submit(
                    TOOL_REGISTRY[function_name],
                    **arguments
                )
                futures[future] = tool_call.id

        for future in concurrent.futures.as_completed(futures):
            tool_call_id = futures[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"error": str(e)}

            results.append({
                "tool_call_id": tool_call_id,
                "content": json.dumps(result)
            })

    return results
```

## Tool Router

```python
from dataclasses import dataclass
from typing import Dict, List, Callable, Any
import re

@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    parameters: dict
    examples: List[str] = None  # Example queries this tool handles

class ToolRouter:
    """Route queries to appropriate tools."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get_tool_definitions(self) -> List[dict]:
        """Get OpenAI tool definitions."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    def execute(self, query: str) -> Dict[str, Any]:
        """Execute query with tool routing."""
        messages = [{"role": "user", "content": query}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.get_tool_definitions(),
            tool_choice="auto"
        )

        message = response.choices[0].message
        result = {"query": query, "tool_calls": [], "final_response": None}

        # Handle tool calls
        while message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name in self.tools:
                    tool_result = self.tools[tool_name].function(**arguments)
                else:
                    tool_result = {"error": f"Unknown tool: {tool_name}"}

                result["tool_calls"].append({
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": tool_result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # Get next response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.get_tool_definitions()
            )
            message = response.choices[0].message

        result["final_response"] = message.content
        return result

# Usage
router = ToolRouter(client)

router.register(Tool(
    name="get_weather",
    description="Get weather for a location",
    function=get_weather,
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["location"]
    }
))

result = router.execute("What's the weather in Tokyo?")
```

## Agentic Tool Loop

```python
from typing import Optional
import logging

class AgentExecutor:
    """Execute tools in an agentic loop."""

    def __init__(
        self,
        client,
        tools: List[dict],
        tool_registry: Dict[str, Callable],
        model: str = "gpt-4o",
        max_iterations: int = 10
    ):
        self.client = client
        self.tools = tools
        self.tool_registry = tool_registry
        self.model = model
        self.max_iterations = max_iterations
        self.logger = logging.getLogger(__name__)

    def run(self, user_request: str, system_prompt: str = "") -> Dict:
        """Run agent until task complete or max iterations."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_request})

        iteration = 0
        tool_history = []

        while iteration < self.max_iterations:
            self.logger.info(f"Iteration {iteration + 1}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # No tool calls - task complete
            if not message.tool_calls:
                return {
                    "success": True,
                    "response": message.content,
                    "iterations": iteration + 1,
                    "tool_history": tool_history
                }

            # Execute tool calls
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                self.logger.info(f"Calling {tool_name} with {arguments}")

                if tool_name in self.tool_registry:
                    try:
                        result = self.tool_registry[tool_name](**arguments)
                    except Exception as e:
                        result = {"error": str(e)}
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                tool_history.append({
                    "iteration": iteration + 1,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            iteration += 1

        return {
            "success": False,
            "error": "Max iterations reached",
            "iterations": iteration,
            "tool_history": tool_history
        }

# Usage
agent = AgentExecutor(
    client=client,
    tools=tools,
    tool_registry=TOOL_REGISTRY,
    max_iterations=5
)

result = agent.run(
    user_request="Find the weather in Paris and convert the temperature to Fahrenheit",
    system_prompt="You are a helpful assistant. Use tools when needed."
)
```

## Production Tool Service

```python
from dataclasses import dataclass
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import logging
import time

class ToolCallPolicy(Enum):
    AUTO = "auto"
    REQUIRED = "required"
    NONE = "none"

@dataclass
class ToolConfig:
    max_tool_calls: int = 10
    timeout_per_tool: int = 30
    parallel_execution: bool = True
    policy: ToolCallPolicy = ToolCallPolicy.AUTO

class ToolService:
    """Production-ready tool calling service."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[ToolConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or ToolConfig()
        self.tools: Dict[str, dict] = {}
        self.implementations: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: dict,
        implementation: Callable
    ):
        """Register a tool with its implementation."""
        self.tools[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.implementations[name] = implementation

    def execute(
        self,
        messages: List[Dict],
        policy: Optional[ToolCallPolicy] = None
    ) -> Dict[str, Any]:
        """Execute a conversation with tool support."""
        policy = policy or self.config.policy
        tool_calls_made = 0
        start_time = time.time()

        tool_choice = {
            ToolCallPolicy.AUTO: "auto",
            ToolCallPolicy.REQUIRED: "required",
            ToolCallPolicy.NONE: "none"
        }[policy]

        while tool_calls_made < self.config.max_tool_calls:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=list(self.tools.values()) if self.tools else None,
                tool_choice=tool_choice if self.tools else None
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "success": True,
                    "content": message.content,
                    "tool_calls_made": tool_calls_made,
                    "duration": time.time() - start_time
                }

            messages.append(message)

            # Execute tools
            tool_results = self._execute_tools(message.tool_calls)
            tool_calls_made += len(message.tool_calls)

            for result in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": result["id"],
                    "content": json.dumps(result["result"])
                })

        return {
            "success": False,
            "error": "Max tool calls exceeded",
            "tool_calls_made": tool_calls_made,
            "duration": time.time() - start_time
        }

    def _execute_tools(self, tool_calls: list) -> List[Dict]:
        """Execute tool calls."""
        if self.config.parallel_execution:
            return self._execute_parallel(tool_calls)
        else:
            return self._execute_sequential(tool_calls)

    def _execute_sequential(self, tool_calls: list) -> List[Dict]:
        """Execute tools sequentially."""
        results = []

        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = self.implementations[name](**args)
            except Exception as e:
                self.logger.error(f"Tool {name} failed: {e}")
                result = {"error": str(e)}

            results.append({
                "id": tool_call.id,
                "name": name,
                "result": result
            })

        return results

    def _execute_parallel(self, tool_calls: list) -> List[Dict]:
        """Execute tools in parallel."""
        import concurrent.futures

        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}

            for tool_call in tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                future = executor.submit(
                    self._safe_execute,
                    name,
                    args
                )
                futures[future] = tool_call

            for future in concurrent.futures.as_completed(futures):
                tool_call = futures[future]
                result = future.result()

                results.append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "result": result
                })

        return results

    def _safe_execute(self, name: str, args: dict) -> Any:
        """Safely execute a tool with error handling."""
        try:
            if name not in self.implementations:
                return {"error": f"Unknown tool: {name}"}
            return self.implementations[name](**args)
        except Exception as e:
            self.logger.error(f"Tool {name} error: {e}")
            return {"error": str(e)}
```

## Best Practices

1. **Tool Organization**
   - Group related tools
   - Use tool routers for complex systems
   - Register tools centrally

2. **Execution Strategy**
   - Parallel execution for independent tools
   - Sequential for dependent operations
   - Set iteration limits for agents

3. **Error Recovery**
   - Structured error messages
   - Allow LLM to retry with corrections
   - Log all failures

4. **Production Readiness**
   - Configuration management
   - Monitoring and logging
   - Timeout and resource limits

## References

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
