# Templates — Confidence-Thresholded Cascade

## Two-level cascade (Pydantic + Anthropic)

```python
from pydantic import BaseModel, Field
from typing import Literal
from anthropic import Anthropic

client = Anthropic()

class CheapAnswer(BaseModel):
    reasoning: str
    answer: str
    confidence_0_to_1: float = Field(description="Self-assessed confidence; 1.0 = certain.")

class StrongAnswer(BaseModel):
    reasoning: str
    answer: str

THRESHOLD = 0.85

def cascade(task: str) -> str:
    cheap = client.messages.create(
        model="claude-haiku-...",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Task: {task}\nReturn structured."}]
    )
    parsed = CheapAnswer.model_validate_json(cheap.content[0].text)

    if parsed.confidence_0_to_1 >= THRESHOLD:
        return parsed.answer

    strong = client.messages.create(
        model="claude-opus-...",
        max_tokens=2048,
        messages=[{"role": "user", "content": f"Task: {task}"}]
    )
    return parse_strong(strong)
```

## Three-level cascade

```python
def cascade_3(task):
    cheap = haiku(task)
    if cheap.confidence >= 0.92:
        return cheap.answer
    mid = sonnet(task)
    if mid.confidence >= 0.85:
        return mid.answer
    return opus(task)
```

## Logprob-based confidence (OpenAI)

```python
resp = openai.responses.create(
    model="gpt-...-mini",
    input=task,
    response_format={"type": "json_schema", "json_schema": cheap_schema},
    logprobs=True,
)
# Extract token-level logprobs for the "answer" field
ans_logprobs = extract_answer_logprobs(resp)
mean_prob = exp(mean(ans_logprobs))

if mean_prob >= 0.95:
    return resp.parsed.answer
```

## Confidence with explicit "don't know" exit

```python
class CheapAnswer(BaseModel):
    reasoning: str
    answer: str | None = None        # None = explicit IDK
    confidence_0_to_1: float
    requires_escalation: bool = Field(
        description="Set true ONLY if you cannot answer reliably."
    )

if parsed.requires_escalation or parsed.confidence_0_to_1 < THRESHOLD:
    escalate()
```

## Per-tenant thresholds

```python
THRESHOLDS = {
    "premium": 0.70,    # cheap and accept more often
    "free":    0.95,    # rarely escalate
    "internal":1.00,    # always escalate (testing strong model)
}

def cascade(task, tenant):
    threshold = THRESHOLDS[tenant.tier]
    ...
```

## OpenRouter auto-routing

```python
import requests

resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json={
    "model": "openrouter/auto",   # OpenRouter's built-in cascade
    "messages": [...],
})
```

OpenRouter's `/auto` mode implements the cascade for you.

## Span instrumentation

```python
with tracer.start_as_current_span("cascade") as span:
    cheap_result = cheap(task)
    span.set_attribute("cascade.cheap_confidence", cheap_result.confidence)
    if cheap_result.confidence >= THRESHOLD:
        span.set_attribute("cascade.escalated", False)
        return cheap_result.answer
    span.set_attribute("cascade.escalated", True)
    return strong(task)
```
