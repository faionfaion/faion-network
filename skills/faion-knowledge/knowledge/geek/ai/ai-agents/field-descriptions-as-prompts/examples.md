# Examples — Field Descriptions as Inline Mini-Prompts

## Example 1: Currency conversion errors → 0%

Before:
```python
total: float = Field(description="invoice total")
```
Errors: ~12% returned dollars when cents were expected, ~8% off-by-cents.

After:
```python
total_cents: int = Field(
    description=(
        "Total in CENTS as integer. $19.99 -> 1999. "
        "Never include currency symbol. Includes tax."
    )
)
```
Errors: < 0.5% on the same 1000-invoice eval.

## Example 2: ISO-8601 with edge cases

```python
published_iso: str = Field(
    description=(
        "ISO-8601 YYYY-MM-DD. "
        "If only month visible, use day=01. "
        "If only year visible, use 01-01. "
        "If 'NYT 2024' visible, year is 2024 (NYT is a publisher, not a date prefix)."
    )
)
```

The "NYT 2024" hint cuts a specific failure mode where the parser previously emitted "2024-NY-T1".

## Example 3: Boolean with explicit forbiddance

```python
is_genuine_complaint: bool = Field(
    description=(
        "True if the message expresses dissatisfaction. "
        "Sarcastic praise counts as complaint. "
        "Pure questions do NOT count. "
        "Comments asking for refunds DO count."
    )
)
```

The "do NOT" line is load-bearing — the model would otherwise mark questions as complaints 30% of the time.

## Example 4: Dependency reference

```python
class Article(BaseModel):
    body: str
    summary: str = Field(
        description="3-sentence summary of `body` above. Same tense and tone."
    )
    title: str = Field(
        description="Sharp 6-10 word title derived from `body` and `summary`. No clickbait."
    )
```

Naming the dependent field in the description re-grounds the model on what it's summarizing.

## Example 5: Enum value choice rules

```python
priority: Literal["low", "medium", "high", "critical"] = Field(
    description=(
        "low = informational. "
        "medium = should be addressed within a sprint. "
        "high = needs same-day attention. "
        "critical = production down or data loss imminent."
    )
)
```

Without these rules, the model splits high vs critical near 50/50 on borderline cases.

## Example 6: Numerical bounds

```python
confidence_0_to_1: float = Field(
    description=(
        "Confidence in [0.0, 1.0]. "
        "0.0 = guessing. 0.5 = uncertain. 1.0 = certain. "
        "Round to 2 decimals. Never use 1.0 unless the answer is logically derived."
    )
)
```

## Example 7: Forbidden patterns

```python
slug_kebab: str = Field(
    description=(
        "kebab-case slug, max 60 chars, ASCII lower. "
        "Derived from `title`. "
        "DO NOT include articles (a/an/the). "
        "DO NOT include the year unless the title mentions a year. "
        "DO NOT use special characters or emoji."
    )
)
```

## Example 8: Anti-example (description that asks for reasoning)

Don't:
```python
verdict: str = Field(
    description="Explain your reasoning, then give the verdict."
)
```

Do (split into separate fields):
```python
class Output(BaseModel):
    reasoning: str = Field(description="Step-by-step analysis of evidence.")
    verdict: Literal["approve", "reject"] = Field(description="Final call. Must follow from reasoning above.")
```
