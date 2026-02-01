---
id: structured-output-basics
name: "Structured Output Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Structured Output Basics

## Overview

Structured output ensures LLMs return data in consistent, parseable formats like JSON. This is essential for integrating LLM outputs into applications, APIs, and automated pipelines.

## When to Use

- API responses requiring specific format
- Data extraction from unstructured text
- Form filling automation
- Database record generation
- Configuration generation
- Any application needing reliable parsing

## Key Concepts

### Output Format Options

| Method | Reliability | Flexibility | Provider |
|--------|-------------|-------------|----------|
| JSON Mode | High | Medium | OpenAI, Anthropic |
| Structured Outputs | Very High | High | OpenAI |
| Prompt Engineering | Medium | High | All |
| Output Parsers | Medium | High | LangChain |

### JSON Mode vs Structured Outputs

```
JSON Mode: Guarantees valid JSON, but not schema compliance
Structured Outputs: Guarantees both valid JSON AND schema compliance
```

## Provider Implementations

### OpenAI JSON Mode

```python
from openai import OpenAI
import json

client = OpenAI()

def extract_with_json_mode(text: str) -> dict:
    """Extract structured data using JSON mode."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract entities from text. Return JSON with: {entities: [{name, type, context}]}"
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Usage
result = extract_with_json_mode(
    "Apple CEO Tim Cook announced a new iPhone model at their Cupertino headquarters."
)
# {"entities": [{"name": "Apple", "type": "company", "context": "..."}, ...]}
```

### OpenAI Structured Outputs

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

client = OpenAI()

# Define schema with Pydantic
class Entity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type: person, company, location, product")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class ExtractionResult(BaseModel):
    entities: List[Entity]
    summary: str
    language: str

def extract_structured(text: str) -> ExtractionResult:
    """Extract data with guaranteed schema compliance."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract entities and provide a summary."
            },
            {"role": "user", "content": text}
        ],
        response_format=ExtractionResult
    )

    return response.choices[0].message.parsed

# Usage
result = extract_structured(
    "Elon Musk visited Berlin to open a new Tesla factory."
)
print(result.entities[0].name)  # "Elon Musk"
print(result.summary)
```

### Anthropic JSON Output

```python
from anthropic import Anthropic
import json

client = Anthropic()

def extract_with_claude(text: str, schema: dict) -> dict:
    """Extract structured data with Claude."""
    schema_str = json.dumps(schema, indent=2)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Extract information from the following text and return valid JSON matching this schema:

Schema:
```json
{schema_str}
```

Text:
{text}

Return only valid JSON, no other text."""
            }
        ]
    )

    # Extract JSON from response
    content = response.content[0].text

    # Handle potential markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    return json.loads(content.strip())

# Schema definition
schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "features": {"type": "array", "items": {"type": "string"}},
        "in_stock": {"type": "boolean"}
    },
    "required": ["product_name", "price"]
}

result = extract_with_claude(
    "The new iPhone 15 Pro costs $999 and features a titanium design, A17 chip, and improved camera.",
    schema
)
```

### Function-Based Structured Output

```python
# Using function calling for structured output
def get_structured_response(
    prompt: str,
    schema: dict,
    client,
    model: str = "gpt-4o"
) -> dict:
    """Use function calling to enforce output structure."""
    tools = [{
        "type": "function",
        "function": {
            "name": "return_structured_data",
            "description": "Return the extracted data in structured format",
            "parameters": schema
        }
    }]

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "return_structured_data"}}
    )

    # Extract function call result
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)

# Usage
schema = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "topics": {"type": "array", "items": {"type": "string"}},
        "urgency": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["sentiment", "topics", "urgency"]
}

result = get_structured_response(
    "Analyze this customer feedback: 'I love the product but shipping was slow!'",
    schema,
    client
)
```

## Complex Schemas

### Task Extraction Example

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

class Subtask(BaseModel):
    title: str
    estimated_hours: Optional[float] = None
    completed: bool = False

class Task(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[str] = None
    assignee: Optional[str] = None
    tags: List[str] = []
    subtasks: List[Subtask] = []
    estimated_hours: Optional[float] = Field(None, ge=0)

    @validator('due_date')
    def validate_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class ProjectExtraction(BaseModel):
    project_name: str
    tasks: List[Task]
    total_estimated_hours: float
    team_members: List[str]

def extract_project_plan(description: str) -> ProjectExtraction:
    """Extract project plan from natural language description."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a project planning assistant. Extract tasks and project details from the description."
            },
            {"role": "user", "content": description}
        ],
        response_format=ProjectExtraction
    )

    return response.choices[0].message.parsed
```

### Form/Document Extraction

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None

class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    due_date: Optional[str] = None
    vendor: ContactInfo
    customer: ContactInfo
    items: List[InvoiceItem]
    subtotal: float
    tax: Optional[float] = None
    total: float
    currency: str = "USD"
    notes: Optional[str] = None

def extract_invoice(text: str) -> Invoice:
    """Extract invoice data from text or OCR output."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract invoice information. Calculate totals if not provided."
            },
            {"role": "user", "content": f"Extract invoice data:\n\n{text}"}
        ],
        response_format=Invoice
    )

    return response.choices[0].message.parsed
```

## References

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema](https://json-schema.org/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| JSON schema definition | sonnet | Schema design |
| Output validation | haiku | Format checking |
