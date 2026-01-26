# Structured Output for LLMs

Structured output ensures LLMs return data in consistent, parseable formats like JSON. This is essential for integrating LLM outputs into applications, APIs, and automated pipelines.

## When to Use

- API responses requiring specific format
- Data extraction from unstructured text
- Form filling automation
- Database record generation
- Configuration generation
- Any application needing reliable parsing
- Multi-step workflows with LLM outputs
- Agent tool responses

## Key Concepts

### Output Format Methods

| Method | Reliability | Provider Support | Use Case |
|--------|-------------|------------------|----------|
| **Native Structured Output** | Very High | OpenAI, Google | Schema-guaranteed responses |
| **JSON Mode** | High | OpenAI, Anthropic, Google | Valid JSON without schema guarantee |
| **Tool/Function Calling** | High | All major providers | Action-oriented outputs |
| **Prompt Engineering** | Medium | All | Fallback method |
| **Grammar Constraints** | Very High | Local models (Outlines) | Token-level enforcement |

### JSON Mode vs Structured Output

```
JSON Mode:
- Guarantees valid JSON syntax
- Does NOT guarantee schema compliance
- Model may omit fields or add extras
- Simpler to implement

Structured Output:
- Guarantees valid JSON AND schema compliance
- All required fields present
- No unexpected fields
- Requires schema definition
```

### Three Approaches (Pydantic AI Framework)

1. **Tool Output** (Default): Schema provided as tool parameters. Widely supported, works well.
2. **Native Output**: Model produces JSON compliant with provided schema. Best reliability.
3. **Prompted Output**: Schema injected in prompt, response parsed. Fallback method.

## Provider Comparison

### Feature Matrix

| Feature | OpenAI | Claude | Gemini | Local (Ollama) |
|---------|--------|--------|--------|----------------|
| JSON Mode | Yes | Yes | Yes | Varies |
| Native Structured Output | Yes (`response_format`) | No | Yes | With Outlines |
| Function/Tool Calling | Yes | Yes | Yes | Some models |
| Pydantic SDK Integration | Yes | Via Instructor | Via Instructor | Via Outlines |
| Max Context | 128K | 200K | 2M | Varies |
| Schema Complexity | High | Medium | High | Medium |

### OpenAI

**Strengths:**
- Native `response_format` with JSON Schema
- Direct Pydantic model support in SDK
- `beta.chat.completions.parse()` for typed responses
- Strict schema enforcement

**Implementation:**
```python
from openai import OpenAI
from pydantic import BaseModel

class Output(BaseModel):
    field: str

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=Output
)
result = response.choices[0].message.parsed  # Typed Output object
```

### Anthropic (Claude)

**Strengths:**
- Excellent instruction following
- Long context for complex schemas
- Strong reasoning for nested structures
- Tool use for structured responses

**Implementation:**
- JSON Mode: Include schema in prompt, parse response
- Tool Use: Define tool with output schema
- Third-party: Use `instructor` library for Pydantic integration

**Note:** Claude does not have native `response_format` parameter. Use tool calling or prompt-based approaches.

### Google (Gemini)

**Strengths:**
- Native JSON Schema support
- Massive context window (2M tokens)
- Good for complex document extraction
- Grounding capabilities

**Implementation:**
```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(
    prompt,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=schema
    )
)
```

### Local Models (Ollama + Outlines)

**Strengths:**
- Privacy (no API calls)
- No API costs
- Token-level schema enforcement
- Full control

**Implementation:**
```python
import outlines
from pydantic import BaseModel

class Output(BaseModel):
    field: str

model = outlines.models.transformers("mistral-7b")
generator = outlines.generate.json(model, Output)
result = generator(prompt)  # Guaranteed schema compliance
```

## Pydantic Integration

### Why Pydantic?

1. **Type Safety**: Python types define schema structure
2. **Validation**: Built-in data validation with custom rules
3. **JSON Schema**: Auto-generates JSON Schema from models
4. **IDE Support**: Autocomplete and type checking
5. **SDK Integration**: Native support in OpenAI SDK

### Basic Pattern

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Entity(BaseModel):
    """Extracted entity from text."""
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type: person, company, location")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class ExtractionResult(BaseModel):
    """Complete extraction result."""
    entities: List[Entity]
    summary: str
    language: str = Field(default="en")
```

### Validation and Retry

```python
from pydantic import BaseModel, ValidationError

def extract_with_retry(prompt: str, model: BaseModel, max_retries: int = 3):
    """Extract structured data with validation retry."""
    for attempt in range(max_retries):
        response = get_llm_response(prompt)
        try:
            return model.model_validate_json(response)
        except ValidationError as e:
            prompt = f"Previous output failed validation: {e}\n\nPlease try again."
    raise ValueError("Max retries exceeded")
```

## Schema Design Principles

### Required vs Optional Fields

```python
class Good(BaseModel):
    # Required: Core data that must be present
    id: str
    name: str

    # Optional: Data that may not be extractable
    email: Optional[str] = None
    phone: Optional[str] = None
```

### Enums for Controlled Values

```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority  # LLM must choose from enum values
```

### Nested Structures

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    address: Address  # Nested model
    contacts: List[Address] = []  # List of nested models
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Invalid JSON | Model added text | Use native structured output |
| Missing fields | Schema too complex | Simplify or use defaults |
| Wrong types | Ambiguous schema | Add field descriptions |
| Validation errors | Data doesn't match | Implement retry logic |

### Robust Extraction

```python
import json
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)

def safe_extract(response: str, model: Type[T]) -> T:
    """Safely extract structured data from LLM response."""
    content = response

    # Handle markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    # Parse and validate
    data = json.loads(content.strip())
    return model.model_validate(data)
```

## Performance Considerations

### Token Efficiency

- Shorter field names reduce output tokens
- Enums are more efficient than free-form strings
- Flat structures are faster than deep nesting

### Latency

- Native structured output adds minimal latency
- Grammar-constrained generation may be slower
- Retry loops significantly increase latency

### Cost

- Schema in prompt increases input tokens
- Complex schemas increase output tokens
- Failed validations waste API calls

## Best Practices

1. **Start Simple**: Begin with flat schemas, add nesting as needed
2. **Use Descriptions**: Field descriptions improve LLM accuracy
3. **Set Defaults**: Optional fields should have sensible defaults
4. **Validate Early**: Catch errors before downstream processing
5. **Log Failures**: Track validation errors for schema refinement
6. **Test Edge Cases**: Empty inputs, missing data, malformed text
7. **Version Schemas**: Track schema changes for compatibility

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Provider-specific code examples |
| [templates.md](templates.md) | Reusable schema templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for schema design |

## External Resources

### Official Documentation

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/tool-use)
- [Google AI JSON Mode](https://ai.google.dev/gemini-api/docs/json-mode)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema Specification](https://json-schema.org/)

### Libraries and Frameworks

- [Pydantic AI](https://ai.pydantic.dev/) - Python framework for LLM agents
- [Instructor](https://github.com/jxnl/instructor) - Structured outputs for any LLM
- [Outlines](https://github.com/outlines-dev/outlines) - Grammar-constrained generation
- [LangChain Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)

### Articles and Guides

- [Pydantic for LLMs Guide](https://pydantic.dev/articles/llm-intro)
- [Agenta Structured Output Guide](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms)
- [AWS Structured Output Guide](https://builder.aws.com/content/2wzRXcEcE7u3LfukKwiYIf75Rpw/how-to-get-structured-output-from-llms-a-practical-guide)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-llm-integration](../faion-llm-integration/CLAUDE.md) | LLM API usage patterns |
| [faion-ai-agents](../faion-ai-agents/CLAUDE.md) | Tool use and agent outputs |
| [faion-rag-engineer](../faion-rag-engineer/CLAUDE.md) | Document extraction |
