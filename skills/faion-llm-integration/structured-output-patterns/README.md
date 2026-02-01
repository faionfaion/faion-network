---
id: structured-output-patterns
name: "Structured Output Patterns"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Structured Output Patterns

Advanced patterns for production-grade structured output handling with LLMs.

## Output Parsing with Retry

```python
from typing import TypeVar, Type
import json
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class OutputParsingError(Exception):
    """Error parsing LLM output."""
    pass

@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((json.JSONDecodeError, OutputParsingError))
)
def parse_with_retry(
    client,
    prompt: str,
    output_class: Type[T],
    model: str = "gpt-4o"
) -> T:
    """Parse LLM output with automatic retry on failure."""
    schema = output_class.model_json_schema()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Return valid JSON matching this schema: {json.dumps(schema)}"
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return output_class(**data)
    except Exception as e:
        raise OutputParsingError(f"Failed to parse output: {e}")
```

## Streaming Structured Output

```python
def stream_structured_output(
    client,
    prompt: str,
    model: str = "gpt-4o"
):
    """Stream JSON output with partial parsing."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Return JSON with streaming support. Output complete JSON object."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        stream=True
    )

    accumulated = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            accumulated += chunk.choices[0].delta.content

            # Try to parse partial JSON for progress updates
            try:
                partial = json.loads(accumulated + '"}]}')
                yield {"partial": partial, "complete": False}
            except:
                pass

    # Final complete parse
    yield {"partial": json.loads(accumulated), "complete": True}
```

## Production Structured Output Service

```python
from dataclasses import dataclass
from typing import Type, TypeVar, Optional, List
from pydantic import BaseModel, ValidationError
import logging
import json

T = TypeVar('T', bound=BaseModel)

@dataclass
class StructuredOutputConfig:
    max_retries: int = 3
    use_structured_outputs: bool = True  # OpenAI structured outputs
    fallback_to_json_mode: bool = True
    validate_output: bool = True

class StructuredOutputService:
    """Production service for structured LLM outputs."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[StructuredOutputConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or StructuredOutputConfig()
        self.logger = logging.getLogger(__name__)

    def extract(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str = ""
    ) -> Optional[T]:
        """Extract structured data from text."""
        for attempt in range(self.config.max_retries):
            try:
                if self.config.use_structured_outputs:
                    result = self._extract_structured(prompt, output_class, system_prompt)
                else:
                    result = self._extract_json_mode(prompt, output_class, system_prompt)

                if self.config.validate_output:
                    # Pydantic validation happens automatically
                    return result

                return result

            except ValidationError as e:
                self.logger.warning(f"Validation error (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise
            except json.JSONDecodeError as e:
                self.logger.warning(f"JSON parse error (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise

        return None

    def _extract_structured(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str
    ) -> T:
        """Use OpenAI structured outputs."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=output_class
        )

        return response.choices[0].message.parsed

    def _extract_json_mode(
        self,
        prompt: str,
        output_class: Type[T],
        system_prompt: str
    ) -> T:
        """Use JSON mode with schema in prompt."""
        schema = output_class.model_json_schema()

        messages = [
            {
                "role": "system",
                "content": f"{system_prompt}\n\nReturn valid JSON matching: {json.dumps(schema)}"
            },
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )

        data = json.loads(response.choices[0].message.content)
        return output_class(**data)

    def batch_extract(
        self,
        items: List[str],
        output_class: Type[T],
        system_prompt: str = ""
    ) -> List[Optional[T]]:
        """Extract from multiple items."""
        results = []
        for item in items:
            try:
                result = self.extract(item, output_class, system_prompt)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Extraction failed: {e}")
                results.append(None)
        return results
```

## Usage Example

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

client = OpenAI()

# Define output schema
class ProductReview(BaseModel):
    product_name: str
    rating: int = Field(ge=1, le=5)
    sentiment: str = Field(pattern="^(positive|negative|neutral)$")
    pros: List[str]
    cons: List[str]
    would_recommend: bool

# Initialize service
service = StructuredOutputService(
    client=client,
    model="gpt-4o",
    config=StructuredOutputConfig(
        max_retries=3,
        use_structured_outputs=True,
        validate_output=True
    )
)

# Extract structured data
review_text = """
The XYZ Headphones are fantastic! Sound quality is excellent and
they're very comfortable. Battery life could be better though.
I'd give them 4 out of 5 stars and would recommend to anyone
looking for good wireless headphones.
"""

result = service.extract(
    prompt=review_text,
    output_class=ProductReview,
    system_prompt="Extract product review details from the text."
)

print(f"Product: {result.product_name}")
print(f"Rating: {result.rating}/5")
print(f"Pros: {', '.join(result.pros)}")
print(f"Cons: {', '.join(result.cons)}")
print(f"Recommend: {'Yes' if result.would_recommend else 'No'}")

# Batch processing
reviews = [
    "Love this product! 5 stars all the way.",
    "Terrible quality, broke after one week. 1 star.",
    "It's okay, nothing special. 3 stars."
]

results = service.batch_extract(
    items=reviews,
    output_class=ProductReview,
    system_prompt="Extract product review details."
)

for i, result in enumerate(results):
    if result:
        print(f"Review {i+1}: {result.rating}/5 - {result.sentiment}")
```

## Best Practices

### Schema Design

1. **Use clear field names**
   - Descriptive, unambiguous names
   - Follow naming conventions (snake_case or camelCase)

2. **Provide descriptions for complex fields**
   - Use Field(description="...") for Pydantic
   - Helps LLM understand expected content

3. **Set reasonable defaults**
   - Use Optional for nullable fields
   - Provide default values when appropriate

4. **Use enums for constrained values**
   - Enum types enforce valid values
   - Better than string validation

### Validation

1. **Use Pydantic for type safety**
   - Automatic validation on instantiation
   - Custom validators for complex rules

2. **Add custom validators**
   ```python
   @validator('email')
   def validate_email(cls, v):
       if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
           raise ValueError('Invalid email format')
       return v
   ```

3. **Handle validation errors gracefully**
   - Retry with corrected prompt
   - Log failures for analysis
   - Provide fallback values

### Error Handling

1. **Implement retry logic**
   - Use exponential backoff
   - Limit max retries (3-5)
   - Different strategies for different errors

2. **Fall back to JSON mode if structured fails**
   - OpenAI structured outputs may fail on complex schemas
   - JSON mode + validation is backup

3. **Log parsing failures**
   - Track failure patterns
   - Improve prompts based on failures
   - Monitor schema compliance

### Performance

1. **Cache schemas**
   - Generate JSON schema once
   - Reuse across multiple calls
   - Reduce overhead

2. **Use streaming for large outputs**
   - Progressive parsing for UX
   - Handle partial results
   - Timeout protection

3. **Batch similar extractions**
   - Process multiple items together
   - Amortize API overhead
   - Use async/await for parallelism

### Prompt Design

1. **Include schema in system prompt for JSON mode**
   ```python
   system_prompt = f"Return JSON matching: {json.dumps(schema)}"
   ```

2. **Provide examples for complex structures**
   - Few-shot learning improves accuracy
   - Show edge cases

3. **Be explicit about required vs optional**
   - Clearly state what MUST be included
   - Indicate when null/empty is acceptable

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Over-complex schemas | LLM confusion, errors | Simplify, split into multiple calls |
| Missing required fields | Incomplete data | Explicit requirements in prompt |
| No fallback | System crashes | Retry logic, fallback strategies |
| Ignoring validation | Bad data propagates | Always validate with Pydantic |
| Wrong types | Type errors downstream | Use strict type hints |
| Large schemas | Context limit exceeded | Break into smaller schemas |
| No error logging | Can't debug failures | Log all failures with context |
| Synchronous batch | Slow performance | Use async/await |

## References

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema](https://json-schema.org/)
- [Tenacity (Retry Library)](https://tenacity.readthedocs.io/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Multi-level JSON structures | sonnet | Schema complexity |
| Discriminated unions | sonnet | Type pattern |
