# Tool Use Templates

Reusable templates for tool definitions, agent implementations, and configuration.

---

## Tool Definition Templates

### Basic Tool Template

```python
# Template: Basic Tool Definition
TOOL_TEMPLATE = {
    "name": "{tool_name}",  # snake_case, action verb prefix
    "description": "{Brief description of what the tool does. Include when to use it.}",
    "parameters": {
        "type": "object",
        "properties": {
            "{param_name}": {
                "type": "{type}",  # string, number, integer, boolean, array, object
                "description": "{What this parameter is for}"
            }
        },
        "required": ["{required_params}"]
    }
}
```

### CRUD Tool Templates

```python
# Template: Create Tool
CREATE_TOOL = {
    "name": "create_{resource}",
    "description": "Create a new {resource}. Use this when the user wants to add a new {resource} to the system.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the {resource}"
            },
            "data": {
                "type": "object",
                "description": "Additional data for the {resource}",
                "properties": {},
                "additionalProperties": True
            }
        },
        "required": ["name"]
    }
}

# Template: Read Tool
READ_TOOL = {
    "name": "get_{resource}",
    "description": "Retrieve a {resource} by ID. Use this to fetch details of a specific {resource}.",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Unique identifier of the {resource}"
            },
            "include_related": {
                "type": "boolean",
                "description": "Whether to include related data",
                "default": False
            }
        },
        "required": ["id"]
    }
}

# Template: List Tool
LIST_TOOL = {
    "name": "list_{resources}",
    "description": "List {resources} with optional filtering and pagination.",
    "parameters": {
        "type": "object",
        "properties": {
            "filter": {
                "type": "object",
                "description": "Filter criteria",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["active", "inactive", "all"]
                    },
                    "created_after": {
                        "type": "string",
                        "format": "date-time"
                    }
                }
            },
            "page": {
                "type": "integer",
                "minimum": 1,
                "default": 1
            },
            "page_size": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 20
            },
            "sort_by": {
                "type": "string",
                "enum": ["created_at", "updated_at", "name"]
            },
            "sort_order": {
                "type": "string",
                "enum": ["asc", "desc"],
                "default": "desc"
            }
        },
        "required": []
    }
}

# Template: Update Tool
UPDATE_TOOL = {
    "name": "update_{resource}",
    "description": "Update an existing {resource}. Only provided fields will be modified.",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "ID of the {resource} to update"
            },
            "updates": {
                "type": "object",
                "description": "Fields to update",
                "additionalProperties": True
            }
        },
        "required": ["id", "updates"]
    }
}

# Template: Delete Tool
DELETE_TOOL = {
    "name": "delete_{resource}",
    "description": "Delete a {resource}. This action cannot be undone.",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "ID of the {resource} to delete"
            },
            "confirm": {
                "type": "boolean",
                "description": "Confirmation flag - must be true to proceed"
            }
        },
        "required": ["id", "confirm"]
    }
}
```

### Search Tool Template

```python
SEARCH_TOOL = {
    "name": "search_{domain}",
    "description": "Search {domain} using natural language query. Returns ranked results.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query in natural language"
            },
            "filters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category"
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "format": "date"},
                            "end": {"type": "string", "format": "date"}
                        }
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 10
            },
            "include_highlights": {
                "type": "boolean",
                "default": True
            }
        },
        "required": ["query"]
    }
}
```

### API Integration Tool Template

```python
API_TOOL = {
    "name": "{service}_api",
    "description": "Call {Service} API. {Brief description of service capabilities}.",
    "parameters": {
        "type": "object",
        "properties": {
            "endpoint": {
                "type": "string",
                "description": "API endpoint path",
                "enum": ["/users", "/orders", "/products"]
            },
            "method": {
                "type": "string",
                "enum": ["GET", "POST", "PUT", "DELETE"],
                "default": "GET"
            },
            "params": {
                "type": "object",
                "description": "Query parameters for GET requests"
            },
            "body": {
                "type": "object",
                "description": "Request body for POST/PUT requests"
            }
        },
        "required": ["endpoint"]
    }
}
```

### File Operation Tool Templates

```python
FILE_READ_TOOL = {
    "name": "read_file",
    "description": "Read content from a file. Use for text files, configs, or data files.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path to read"
            },
            "encoding": {
                "type": "string",
                "default": "utf-8"
            },
            "max_lines": {
                "type": "integer",
                "description": "Maximum lines to read (for large files)"
            }
        },
        "required": ["path"]
    }
}

FILE_WRITE_TOOL = {
    "name": "write_file",
    "description": "Write content to a file. Creates file if it doesn't exist.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path to write"
            },
            "content": {
                "type": "string",
                "description": "Content to write"
            },
            "mode": {
                "type": "string",
                "enum": ["overwrite", "append"],
                "default": "overwrite"
            }
        },
        "required": ["path", "content"]
    }
}

FILE_LIST_TOOL = {
    "name": "list_files",
    "description": "List files in a directory with optional pattern matching.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory path to list"
            },
            "pattern": {
                "type": "string",
                "description": "Glob pattern to filter files (e.g., '*.py')"
            },
            "recursive": {
                "type": "boolean",
                "default": False
            }
        },
        "required": ["directory"]
    }
}
```

### Database Tool Template

```python
DATABASE_QUERY_TOOL = {
    "name": "query_database",
    "description": "Execute a database query. Supports SELECT queries only for safety.",
    "parameters": {
        "type": "object",
        "properties": {
            "table": {
                "type": "string",
                "description": "Table name to query",
                "enum": ["users", "orders", "products", "logs"]
            },
            "columns": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Columns to select (empty for all)"
            },
            "where": {
                "type": "object",
                "description": "WHERE conditions as key-value pairs"
            },
            "order_by": {
                "type": "string",
                "description": "Column to order by"
            },
            "limit": {
                "type": "integer",
                "maximum": 1000,
                "default": 100
            }
        },
        "required": ["table"]
    }
}
```

---

## Provider-Specific Templates

### OpenAI Tool Format

```python
def create_openai_tool(name: str, description: str, parameters: dict) -> dict:
    """Create tool in OpenAI format."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
            "strict": True  # Enable strict mode for guaranteed schema compliance
        }
    }

# Example
openai_tool = create_openai_tool(
    name="get_weather",
    description="Get weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["location"],
        "additionalProperties": False
    }
)
```

### Claude Tool Format

```python
def create_claude_tool(name: str, description: str, parameters: dict) -> dict:
    """Create tool in Claude/Anthropic format."""
    return {
        "name": name,
        "description": description,
        "input_schema": parameters
    }

# Example
claude_tool = create_claude_tool(
    name="get_weather",
    description="Get weather for a location. Use when user asks about weather conditions.",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country, e.g., 'Tokyo, Japan'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
    }
)
```

### Gemini Tool Format

```python
import google.generativeai as genai

def create_gemini_tool(name: str, description: str, parameters: dict) -> genai.protos.Tool:
    """Create tool in Gemini format."""

    def schema_to_proto(schema: dict) -> genai.protos.Schema:
        """Convert JSON Schema to Gemini proto."""
        type_map = {
            "string": genai.protos.Type.STRING,
            "number": genai.protos.Type.NUMBER,
            "integer": genai.protos.Type.INTEGER,
            "boolean": genai.protos.Type.BOOLEAN,
            "array": genai.protos.Type.ARRAY,
            "object": genai.protos.Type.OBJECT
        }

        props = {}
        for name, prop in schema.get("properties", {}).items():
            props[name] = genai.protos.Schema(
                type=type_map.get(prop["type"], genai.protos.Type.STRING),
                description=prop.get("description", ""),
                enum=prop.get("enum")
            )

        return genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties=props,
            required=schema.get("required", [])
        )

    func_decl = genai.protos.FunctionDeclaration(
        name=name,
        description=description,
        parameters=schema_to_proto(parameters)
    )

    return genai.protos.Tool(function_declarations=[func_decl])
```

---

## Agent Templates

### Basic Agent Template

```python
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, field
import json

@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    model: str = "gpt-4o"
    max_iterations: int = 10
    max_tokens: int = 4096
    temperature: float = 0.7
    tools: List[Dict] = field(default_factory=list)
    system_prompt: str = ""

class BaseAgent:
    """Base agent template with tool support."""

    def __init__(self, client, config: AgentConfig, tool_registry: Dict[str, Callable]):
        self.client = client
        self.config = config
        self.tool_registry = tool_registry
        self.conversation_history: List[Dict] = []

    def reset(self):
        """Reset conversation history."""
        self.conversation_history = []

    def add_message(self, role: str, content: str):
        """Add message to history."""
        self.conversation_history.append({"role": role, "content": content})

    def execute_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute a tool by name."""
        if name not in self.tool_registry:
            return {"error": f"Unknown tool: {name}"}

        try:
            return self.tool_registry[name](**arguments)
        except Exception as e:
            return {"error": str(e)}

    def run(self, user_input: str) -> Dict[str, Any]:
        """Run agent with user input."""
        messages = []

        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})

        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_input})

        tool_history = []

        for iteration in range(self.config.max_iterations):
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                tools=[{"type": "function", "function": t} for t in self.config.tools] if self.config.tools else None,
                tool_choice="auto" if self.config.tools else None,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )

            message = response.choices[0].message

            if not message.tool_calls:
                # Add to history and return
                self.add_message("user", user_input)
                self.add_message("assistant", message.content)

                return {
                    "success": True,
                    "response": message.content,
                    "iterations": iteration + 1,
                    "tool_history": tool_history
                }

            # Process tool calls
            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                result = self.execute_tool(name, args)

                tool_history.append({
                    "tool": name,
                    "arguments": args,
                    "result": result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        return {
            "success": False,
            "error": "Max iterations reached",
            "tool_history": tool_history
        }
```

### ReAct Agent Template

```python
from typing import List, Dict, Any, Callable
import json

REACT_SYSTEM_PROMPT = """You are a helpful assistant that solves problems using a structured approach.

For each step in solving a problem:

1. **Thought**: Analyze the current situation and decide what to do next
2. **Action**: If needed, use a tool to gather information or perform an action
3. **Observation**: Process the result of the action

Continue this cycle until you can provide a complete answer.

When you have gathered enough information, provide your final answer clearly.

Available tools:
{tool_descriptions}

Guidelines:
- Think step by step
- Use tools when you need external information
- Don't make assumptions - verify with tools
- Provide clear, complete answers
"""

class ReActAgent:
    """ReAct (Reasoning and Acting) agent template."""

    def __init__(
        self,
        client,
        tools: List[Dict],
        tool_registry: Dict[str, Callable],
        model: str = "gpt-4o",
        max_steps: int = 10
    ):
        self.client = client
        self.tools = tools
        self.tool_registry = tool_registry
        self.model = model
        self.max_steps = max_steps

    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions."""
        tool_desc = "\n".join([
            f"- {t['name']}: {t['description']}"
            for t in self.tools
        ])
        return REACT_SYSTEM_PROMPT.format(tool_descriptions=tool_desc)

    def run(self, query: str) -> Dict[str, Any]:
        """Run ReAct loop."""
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": query}
        ]

        trace = []

        for step in range(self.max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[{"type": "function", "function": t} for t in self.tools],
                tool_choice="auto"
            )

            message = response.choices[0].message

            # Record thought
            if message.content:
                trace.append({
                    "step": step + 1,
                    "type": "thought",
                    "content": message.content
                })

            # Check if done
            if not message.tool_calls:
                return {
                    "success": True,
                    "answer": message.content,
                    "trace": trace
                }

            # Execute actions
            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                trace.append({
                    "step": step + 1,
                    "type": "action",
                    "tool": name,
                    "arguments": args
                })

                if name in self.tool_registry:
                    result = self.tool_registry[name](**args)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                trace.append({
                    "step": step + 1,
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
            "trace": trace
        }
```

### Specialized Agent Templates

```python
# Research Agent
RESEARCH_AGENT_CONFIG = AgentConfig(
    name="research_agent",
    model="gpt-4o",
    max_iterations=15,
    system_prompt="""You are a research assistant. Your goal is to gather comprehensive information on topics.

Approach:
1. Break down the research question into sub-questions
2. Use search tools to find relevant information
3. Cross-reference multiple sources
4. Synthesize findings into a coherent summary

Always cite your sources and note any conflicting information.""",
    tools=[
        {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "num_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        },
        {
            "name": "read_webpage",
            "description": "Read and extract content from a webpage",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    ]
)

# Code Assistant Agent
CODE_AGENT_CONFIG = AgentConfig(
    name="code_assistant",
    model="gpt-4o",
    max_iterations=10,
    system_prompt="""You are a coding assistant. Help users write, understand, and debug code.

Approach:
1. Understand the user's goal
2. Read relevant files if needed
3. Write or modify code
4. Test changes when possible
5. Explain your changes

Follow best practices and write clean, documented code.""",
    tools=[
        {
            "name": "read_file",
            "description": "Read a source file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        },
        {
            "name": "run_command",
            "description": "Run a shell command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        }
    ]
)

# Data Analysis Agent
DATA_AGENT_CONFIG = AgentConfig(
    name="data_analyst",
    model="gpt-4o",
    max_iterations=10,
    system_prompt="""You are a data analysis assistant. Help users analyze and visualize data.

Approach:
1. Understand the analysis goal
2. Explore the data structure
3. Clean and prepare data as needed
4. Perform analysis
5. Create visualizations
6. Summarize insights

Always explain your methodology and findings clearly.""",
    tools=[
        {
            "name": "query_data",
            "description": "Query data using SQL-like syntax",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "dataset": {"type": "string"}
                },
                "required": ["query", "dataset"]
            }
        },
        {
            "name": "create_chart",
            "description": "Create a data visualization",
            "parameters": {
                "type": "object",
                "properties": {
                    "chart_type": {"type": "string", "enum": ["bar", "line", "scatter", "pie"]},
                    "data": {"type": "object"},
                    "title": {"type": "string"}
                },
                "required": ["chart_type", "data"]
            }
        }
    ]
)
```

---

## Configuration Templates

### Tool Service Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"

class ToolChoiceMode(Enum):
    AUTO = "auto"
    REQUIRED = "required"
    NONE = "none"

@dataclass
class ToolServiceConfig:
    """Configuration for tool service."""

    # Model settings
    model: str = "gpt-4o"
    max_tokens: int = 4096
    temperature: float = 0.7

    # Tool execution
    execution_mode: ExecutionMode = ExecutionMode.PARALLEL
    tool_choice: ToolChoiceMode = ToolChoiceMode.AUTO

    # Limits
    max_tool_calls: int = 10
    max_iterations: int = 5
    timeout_per_tool: int = 30

    # Error handling
    retry_on_error: bool = True
    max_retries: int = 3
    retry_delay: float = 1.0

    # Caching
    enable_cache: bool = True
    cache_ttl: int = 300

    # Logging
    log_tool_calls: bool = True
    log_tool_results: bool = True

    # Security
    validate_inputs: bool = True
    sanitize_outputs: bool = True

# Environment-specific configs
DEVELOPMENT_CONFIG = ToolServiceConfig(
    model="gpt-4o-mini",
    max_iterations=3,
    log_tool_calls=True,
    log_tool_results=True
)

PRODUCTION_CONFIG = ToolServiceConfig(
    model="gpt-4o",
    max_iterations=5,
    enable_cache=True,
    validate_inputs=True,
    sanitize_outputs=True
)

TESTING_CONFIG = ToolServiceConfig(
    model="gpt-4o-mini",
    max_iterations=2,
    enable_cache=False,
    timeout_per_tool=5
)
```

### Tool Registry Configuration

```yaml
# tools.yaml - Tool registry configuration
tools:
  weather:
    name: get_weather
    description: Get current weather for a location
    module: tools.weather
    function: get_weather
    timeout: 10
    cache_ttl: 300
    rate_limit: 100/minute

  search:
    name: web_search
    description: Search the web
    module: tools.search
    function: search_web
    timeout: 30
    cache_ttl: 60
    rate_limit: 10/minute

  database:
    name: query_database
    description: Query the database
    module: tools.database
    function: run_query
    timeout: 60
    cache_ttl: 0
    requires_auth: true

defaults:
  timeout: 30
  cache_ttl: 300
  rate_limit: 60/minute
  retry_count: 3
```

### Loader for YAML Config

```python
import yaml
from typing import Dict, Any
import importlib

def load_tools_from_config(config_path: str) -> Dict[str, Any]:
    """Load tools from YAML configuration."""

    with open(config_path) as f:
        config = yaml.safe_load(f)

    tools = {}
    tool_registry = {}
    defaults = config.get("defaults", {})

    for tool_name, tool_config in config.get("tools", {}).items():
        # Merge with defaults
        full_config = {**defaults, **tool_config}

        # Build tool definition
        tools[tool_name] = {
            "name": full_config["name"],
            "description": full_config["description"],
            "parameters": full_config.get("parameters", {
                "type": "object",
                "properties": {},
                "required": []
            })
        }

        # Load implementation
        module = importlib.import_module(full_config["module"])
        func = getattr(module, full_config["function"])

        # Wrap with timeout and retry
        tool_registry[tool_name] = wrap_tool(
            func,
            timeout=full_config.get("timeout", 30),
            retry_count=full_config.get("retry_count", 3)
        )

    return {
        "tools": list(tools.values()),
        "registry": tool_registry
    }

def wrap_tool(func, timeout: int, retry_count: int):
    """Wrap tool function with timeout and retry."""
    import functools
    import signal

    @functools.wraps(func)
    def wrapper(**kwargs):
        for attempt in range(retry_count):
            try:
                # Timeout handling
                signal.alarm(timeout)
                try:
                    result = func(**kwargs)
                    return result
                finally:
                    signal.alarm(0)
            except Exception as e:
                if attempt == retry_count - 1:
                    raise
        return None

    return wrapper
```

---

## Response Format Templates

### Standard Tool Response

```python
from dataclasses import dataclass
from typing import Any, Optional, Dict
from datetime import datetime

@dataclass
class ToolResponse:
    """Standard response format for tools."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Dict = None

    def to_dict(self) -> Dict:
        result = {"success": self.success}

        if self.success:
            result["data"] = self.data
        else:
            result["error"] = self.error
            if self.error_code:
                result["error_code"] = self.error_code

        if self.metadata:
            result["metadata"] = self.metadata

        return result

    @classmethod
    def success_response(cls, data: Any, metadata: Dict = None):
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def error_response(cls, error: str, error_code: str = None):
        return cls(success=False, error=error, error_code=error_code)

# Usage
def my_tool(**kwargs) -> Dict:
    try:
        # Do work
        result = {"value": 42}
        return ToolResponse.success_response(
            data=result,
            metadata={"cached": False, "execution_time_ms": 150}
        ).to_dict()
    except ValueError as e:
        return ToolResponse.error_response(
            error=str(e),
            error_code="VALIDATION_ERROR"
        ).to_dict()
```

### Paginated Response Template

```python
@dataclass
class PaginatedResponse:
    """Response format for paginated results."""
    items: list
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

    def to_dict(self) -> Dict:
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "page_size": self.page_size,
                "total_pages": (self.total + self.page_size - 1) // self.page_size,
                "has_next": self.has_next,
                "has_prev": self.has_prev
            }
        }

# Usage in list tools
def list_items(page: int = 1, page_size: int = 20) -> Dict:
    # Fetch from database
    total = 100  # Total count
    items = [...]  # Fetched items

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page * page_size < total,
        has_prev=page > 1
    ).to_dict()
```

---

## Testing Templates

### Tool Test Template

```python
import pytest
from unittest.mock import Mock, patch

class TestToolTemplate:
    """Template for tool unit tests."""

    @pytest.fixture
    def mock_dependencies(self):
        """Setup mock dependencies."""
        return {
            "api_client": Mock(),
            "database": Mock(),
            "cache": Mock()
        }

    def test_successful_execution(self, mock_dependencies):
        """Test tool executes successfully with valid input."""
        # Arrange
        mock_dependencies["api_client"].get.return_value = {"data": "value"}

        # Act
        result = my_tool(param="test", **mock_dependencies)

        # Assert
        assert result["success"] is True
        assert "data" in result

    def test_invalid_input_returns_error(self, mock_dependencies):
        """Test tool handles invalid input gracefully."""
        # Act
        result = my_tool(param=None, **mock_dependencies)

        # Assert
        assert result["success"] is False
        assert "error" in result

    def test_external_service_failure(self, mock_dependencies):
        """Test tool handles external service failures."""
        # Arrange
        mock_dependencies["api_client"].get.side_effect = Exception("Service unavailable")

        # Act
        result = my_tool(param="test", **mock_dependencies)

        # Assert
        assert result["success"] is False
        assert "Service unavailable" in result.get("error", "")

    def test_timeout_handling(self, mock_dependencies):
        """Test tool handles timeout correctly."""
        # Arrange
        import time
        mock_dependencies["api_client"].get.side_effect = lambda: time.sleep(60)

        # Act & Assert
        with pytest.raises(TimeoutError):
            my_tool(param="test", timeout=1, **mock_dependencies)
```

---

## Related Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Code examples |
| [llm-prompts.md](llm-prompts.md) | Prompts for tool design |
