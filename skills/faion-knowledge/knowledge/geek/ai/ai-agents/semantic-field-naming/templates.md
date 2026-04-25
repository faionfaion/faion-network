# Templates — Semantic Field Naming

## Pydantic — naming conventions

```python
from typing import Literal
from pydantic import BaseModel, Field

# Numeric: unit in the name
class CustomerStats(BaseModel):
    age_years: int
    monthly_spend_usd: float
    days_since_last_login: int
    confidence_0_to_1: float

# Boolean: direction explicit
class OrderFlags(BaseModel):
    is_first_order: bool
    has_promo_code: bool
    requires_age_verification: bool
    should_notify_supplier: bool

# Enum: semantic values
class Verdict(BaseModel):
    decision: Literal["approve", "reject", "needs_more_info"]
    severity: Literal["low", "medium", "high", "critical"]

# String: format in name
class Article(BaseModel):
    body_markdown: str
    title_max_70_chars: str
    slug_kebab: str
    iso_published_date: str
```

## Pydantic — when you must keep a legacy name

```python
class Legacy(BaseModel):
    answer: str = Field(validation_alias="final_choice")
    # external API still sends "final_choice"; we use "answer" internally because
    # the model writes the field by alias too in some configs — pick what the LLM sees
```

For LLM-facing schemas, the LLM sees the *primary* field name, not the alias. Pick the primary name with the highest semantic prior.

## Renaming worksheet

```
For each existing field, ask:
  1. Could a reader infer the value just from the name?
  2. Is the unit / format / cardinality embedded?
  3. Is the field name the WORD the model has the strongest prior for?
  4. Could renaming it to a more conventional name reduce description length?

If "no" to any → rename.
```

## Common rename map

| If you have | Use instead |
|-------------|-------------|
| `final_choice`, `final_answer` | `answer` |
| `output`, `result` | name what the result IS (`summary`, `decision`, `verdict`) |
| `data` | name the contents (`items`, `findings`, `entries`) |
| `value` | name the kind (`amount_usd`, `count`, `score`) |
| `flag` | `is_X`, `has_Y`, `should_Z` |
| `code` | `error_code`, `status_code`, `currency_code` |
| `name` | `customer_name`, `product_name`, `slug` |
| `id` | `order_id`, `customer_uuid`, `slug` (only if globally unique-typed) |
| `type` | `event_type`, `error_type` (one word per domain) |

## Anti-template (don't do this)

```python
class Out(BaseModel):
    field_a: int           # bad
    field_b: str           # bad
    output_value: float    # redundant
    final_result: str      # redundant
    f: bool                # cryptic
    data1: dict            # numbered
```
