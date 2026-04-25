# Templates — Field Descriptions as Inline Mini-Prompts

## Pydantic

```python
from pydantic import BaseModel, Field
from typing import Literal

class Invoice(BaseModel):
    total_cents: int = Field(
        description=(
            "Invoice total in CENTS as an integer. "
            "Convert: $19.99 -> 1999, €1234.50 -> 123450. "
            "If invoice shows tax separately, include tax in this total. "
            "If amount is illegible, set to 0 and add a note in `parser_notes`."
        )
    )
    issue_date_iso: str = Field(
        description=(
            "ISO-8601 YYYY-MM-DD. "
            "If only month/year visible, use day=01. "
            "If date is missing, set to '0000-00-00'."
        )
    )
    is_paid: bool = Field(
        description=(
            "True only if the invoice contains an explicit 'PAID' stamp, "
            "balance-due of 0, or a payment-confirmation line. "
            "Do NOT infer from due-date being past."
        )
    )
    currency_iso: Literal["USD", "EUR", "UAH", "GBP"] = Field(
        description="ISO-4217 currency code. Use the symbol on the invoice; if absent, default to USD."
    )
```

## OpenAI structured output (descriptions in JSON Schema)

```python
schema = {
    "type": "object",
    "properties": {
        "summary_under_50_words": {
            "type": "string",
            "description": "Tight summary, 30-50 English words. Past tense. No bullet points."
        },
        "primary_topic": {
            "type": "string",
            "enum": ["tech", "finance", "health", "politics", "other"],
            "description": "Primary topic of the article. 'other' only if none of the above clearly fit."
        }
    },
    "required": ["summary_under_50_words", "primary_topic"],
    "additionalProperties": False
}
```

## Anthropic tool input schema

```json
{
  "name": "create_pr",
  "input_schema": {
    "type": "object",
    "properties": {
      "diff_summary": {
        "type": "string",
        "description": "What this PR changes, 100-150 words. Group by file. Use past tense."
      },
      "title": {
        "type": "string",
        "description": "Conventional Commits title — max 50 chars, format: 'type: subject'. type ∈ {feat, fix, chore, refactor, docs}. Derived from diff_summary above."
      },
      "branch_name": {
        "type": "string",
        "description": "kebab-case slug derived from the title. Prefix with 'feat/' or 'fix/' as appropriate."
      }
    },
    "required": ["diff_summary", "title", "branch_name"]
  }
}
```

## Pattern templates

### Numeric with units

```python
amount_usd_cents: int = Field(
    description="Amount in US-cents as integer. $X.YY -> int(X*100 + YY). Never include the dollar sign."
)
```

### Constrained string

```python
slug_kebab: str = Field(
    description="URL slug. Lowercase, words joined by hyphens, ASCII only, max 60 chars. Derived from `title`."
)
```

### Boolean with rule

```python
should_escalate: bool = Field(
    description="True ONLY if (a) severity is 'high' or 'critical' AND (b) topic is 'safety' or 'legal'. False otherwise."
)
```

### List with cardinality

```python
top_3_keywords: list[str] = Field(
    description="Exactly 3 lowercase keywords from the body. Single-word preferred. Order by frequency."
)
```

### Edge-case sentinel

```python
parser_notes: str = Field(
    description="Free-text note about edge cases encountered during parsing. Empty string if parse was clean."
)
```
