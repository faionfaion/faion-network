# Templates — Weak-Model Preselection

## Two-stage filter+reason (Anthropic, Python)

```python
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()

class FilterResult(BaseModel):
    rationale: str           # 1 sentence — keeps the model honest
    kept_ids: list[int]      # ONLY ids, never full content

def stage1_filter(items: list[dict]) -> list[int]:
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system="Return strictly the FilterResult JSON.",
        messages=[{
            "role": "user",
            "content": f"Items: {items}\nKeep at most 10 most relevant; return their ids."
        }],
        # ... structured output configured here
    )
    parsed = FilterResult.model_validate_json(msg.content[0].text)
    return parsed.kept_ids

def stage2_reason(items: list[dict], kept_ids: list[int]) -> str:
    selected = [it for it in items if it["id"] in kept_ids]
    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"Selected items: {selected}\nWrite a synthesis."
        }],
    )
    return msg.content[0].text
```

## Same shape (OpenAI)

```python
filter_resp = openai.responses.create(
    model="gpt-...-mini",
    response_format={"type": "json_schema", "json_schema": filter_schema},
    input=...,
)
selected = filter_resp.parsed.kept_ids

reason_resp = openai.responses.create(
    model="gpt-...",     # strong
    input=[{"role": "user", "content": str([items[i] for i in selected])}],
)
```

## Three-stage (filter → expand → write)

```python
ids   = haiku_filter(corpus)           # 100 → 10
exps  = haiku_expand(corpus[ids])      # full content for the 10
draft = sonnet_synthesize(exps)        # one tight output
```

## Rank-then-select

```python
class Score(BaseModel):
    rationale: str
    items: list[ScoredItem]    # {id, score} pairs

class ScoredItem(BaseModel):
    id: int
    score: float

scored = haiku_score(items)
top_n = sorted(scored.items, key=lambda x: -x.score)[:5]
result = sonnet_use(top_n)
```

## Fallback handling

```python
ids = haiku_filter(corpus)
if not ids:
    # filter dropped everything — fall back to strong model on full set
    ids = list(range(len(corpus)))
result = strong_model([corpus[i] for i in ids])
```
