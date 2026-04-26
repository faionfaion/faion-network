# Examples — Semantic Field Naming

## Example 1: The Instructor case (90-point swing)

A multiple-choice benchmark scored 4.5% with a schema that had `final_choice: str`. Same prompt, same model, same options — renaming the single field to `answer: str` raised accuracy to 95%.

The model's pre-training gives `answer` an enormously higher prior than `final_choice`. Field name was the bottleneck.

## Example 2: Currency confusion

```python
# BAD — model sometimes returns dollars, sometimes cents
class Invoice(BaseModel):
    total: float

# GOOD — unit pinned in the name AND type
class Invoice(BaseModel):
    total_cents: int
```

A typical hallucination is the model writing $19.99 as `19.99` when the intent was 1999 cents. Naming it `total_cents` and typing it `int` cuts these errors.

## Example 3: Booleans without direction

```python
# BAD
class Order(BaseModel):
    flag: bool   # what does True mean?
    status: str  # is this open or closed or...

# GOOD
class Order(BaseModel):
    is_paid: bool
    is_shipped: bool
    payment_status: Literal["pending", "paid", "refunded"]
```

## Example 4: From neromedia pipeline

Before:
```python
class Story(BaseModel):
    text: str
    output: str
    score: float
```

After:
```python
class Story(BaseModel):
    body_markdown: str
    one_line_hook: str
    relevance_score_0_to_1: float
```

Hallucinations dropped: the model stopped putting markdown in `output`, the score stopped drifting outside [0,1].

## Example 5: Enum naming

```python
# BAD
class Triage(BaseModel):
    label: Literal["a", "b", "c"]

# GOOD
class Triage(BaseModel):
    priority: Literal["low", "medium", "high", "critical"]
```

The bad version forces the model to guess what `a`/`b`/`c` mean from prompt context. The good version maps to its pre-trained understanding of priority levels.

## Example 6: Field-name + description synergy

```python
class Comment(BaseModel):
    is_genuine_complaint: bool = Field(
        description="True only if the comment expresses dissatisfaction with a product or service. Sarcasm counts as complaint. Pure questions do not."
    )
```

Name carries the question; description carries the rules.

## Example 7: Repository signal

In a `git diff` agent:

```python
# BAD
class Change(BaseModel):
    file: str
    lines: int
    type: str

# GOOD
class FileChange(BaseModel):
    path_relative_to_repo_root: str
    net_lines_added: int
    change_kind: Literal["create", "modify", "delete", "rename"]
```

Each field name now lets the model recruit relevant repo-coding priors.

## Example 8: Anti-redundancy

```python
# BAD — every name suffixed _value or _data
class Stats(BaseModel):
    age_value: int
    name_data: str
    total_result: float

# GOOD — drop the redundant suffixes
class Stats(BaseModel):
    age_years: int
    full_name: str
    total_revenue_usd: float
```
