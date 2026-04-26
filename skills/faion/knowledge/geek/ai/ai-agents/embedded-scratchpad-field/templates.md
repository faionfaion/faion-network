# Templates — Embedded Scratchpad Field

## Reasoning before verdict

```python
from pydantic import BaseModel, Field
from typing import Literal

class Verdict(BaseModel):
    reasoning: str = Field(description="Step-by-step analysis of the evidence below.")
    confidence: Literal["low", "medium", "high"]
    decision: Literal["approve", "reject"]
```

## Plan steps before execution

```python
class Plan(BaseModel):
    plan_steps: list[str] = Field(description="Numbered steps to accomplish the goal. 3-7 items.")
    estimated_minutes: int
    final_action: str = Field(description="The single action to take next, derived from plan_steps[0].")
```

## Evidence before classification

```python
class Classification(BaseModel):
    evidence: list[str] = Field(description="Quotations from the input that support each category. Up to 5.")
    category: Literal["bug", "feature_request", "question", "spam"]
```

## Tab-CoT (math/derivation)

```python
class Step(BaseModel):
    step: str = Field(description="What this step computes.")
    intermediate_result: str

class Solution(BaseModel):
    steps: list[Step] = Field(description="Each step builds on the previous. 2-10 items.")
    final_answer: str
```

## Two-phase: scratchpad then structured fields

```python
class Output(BaseModel):
    scratchpad: str = Field(description="Free-form working notes. Brainstorm, list options, weigh tradeoffs.")
    summary: str = Field(description="Crisp summary of the scratchpad above.")
    next_action: str = Field(description="Concrete next step derived from summary.")
```

## OpenAI structured output (JSON Schema)

```python
schema = {
    "type": "object",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "Step-by-step analysis. Required before answer."
        },
        "answer": {"type": "string"}
    },
    "required": ["reasoning", "answer"],
    "additionalProperties": False
}
```

In strict mode, BOTH must be required for the schema to validate.

## Anthropic tool input schema

```json
{
  "name": "decide",
  "input_schema": {
    "type": "object",
    "properties": {
      "reasoning": {"type": "string", "description": "Analysis of options."},
      "decision": {"type": "string", "enum": ["yes", "no"]}
    },
    "required": ["reasoning", "decision"]
  }
}
```

## Length-managed scratchpad

```python
class Output(BaseModel):
    scratchpad_under_300_words: str = Field(
        description=(
            "Working notes. Cap at 300 words. "
            "Cover: assumptions, options considered, tradeoffs, chosen path."
        )
    )
    answer: str
```

The length cap in the field NAME is part of the prompt — surprisingly effective.

## Anti-template (don't do this)

```python
# BAD: scratchpad after answer
class Bad(BaseModel):
    answer: str
    reasoning: str   # post-hoc rationalization, not CoT
```
