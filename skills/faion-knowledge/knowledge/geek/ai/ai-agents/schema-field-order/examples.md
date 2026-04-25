# Examples — Schema Field Order

## Example 1: News article generation (neromedia)

**Wrong:**
```python
class TGPost(BaseModel):
    title: str
    hook: str
    body: str
```
Result: title is generic, hook doesn't match the body that follows.

**Right:**
```python
class TGPost(BaseModel):
    body: str   # 200-500 words
    hook: str   # one-line cliff-hanger derived from body
    title: str  # 6-10 word title derived from body+hook
```
Result: tight, coherent, no hallucinated title.

## Example 2: Code review

**Wrong:**
```python
class Review(BaseModel):
    verdict: Literal["approve", "request_changes"]
    issues: list[Issue]
    summary: str
```

**Right:**
```python
class Review(BaseModel):
    issues: list[Issue]                              # find issues first
    summary: str                                     # summarize the findings
    verdict: Literal["approve", "request_changes"]   # decide based on summary
```

## Example 3: Research-then-answer

**Wrong:**
```python
class Answer(BaseModel):
    final_answer: str
    sources_used: list[str]
    reasoning: str
```

**Right:**
```python
class Answer(BaseModel):
    sources_used: list[str]
    reasoning: str
    final_answer: str
```

## Example 4: Slug from title from content

```python
class Article(BaseModel):
    body: str
    title: str
    slug: str  # derived from title — must come AFTER title
```

## Example 5: Echo input first (long-context)

```python
class TaskBreakdown(BaseModel):
    restate_goal: str             # rewrites the goal in own words
    constraints_observed: list[str]
    subtasks: list[Subtask]
```

The `restate_goal` field is *only* there to make the model re-encode the task before producing the breakdown — it consistently improves quality on long inputs.

## Example 6: Multi-step pipeline

Stage 1 schema (filter):
```python
class Filter(BaseModel):
    rationale: str
    keep: bool
```

Stage 2 schema (writer, only sees items where `keep=True`):
```python
class Writer(BaseModel):
    body: str
    title: str
```

Each stage uses field order INTERNALLY; the pipeline composes by passing only the relevant fields downstream.

## Example 7: Confidence after answer

**Wrong:** `confidence: float` first → model picks 0.85 reflexively.
**Right:** `answer: str` then `confidence: float` → confidence reflects the actual answer.

## Example 8: Tool-call argument ordering

When designing a tool input schema, the same rule applies:

```json
{
  "name": "create_pr",
  "input_schema": {
    "properties": {
      "diff_summary": {"type": "string"},
      "title": {"type": "string"},
      "branch_name": {"type": "string"}
    }
  }
}
```

`diff_summary` is generated first, then `title` (derived from summary), then `branch_name` (derived from title).
