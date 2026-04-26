# Semantic Field Naming

**Category:** `so-` (structured output)

## The Rule

Field NAMES are part of the prompt. Choose names that are specific, English, and semantically loaded — never `field1`, `val`, `data`, `output`. Renaming a single field can swing accuracy by tens of points.

## Empirical anchor

Instructor (2024-09) reported that renaming a single field from `final_choice` to `answer` lifted model accuracy from **4.5% → 95%** on a benchmark — a 90-point swing from one token.

## Why It Works

The structured-output pipeline turns your schema into part of the prompt the model is conditioned on. The model has *seen* tens of millions of `answer` keys and has very high prior probability for what should follow. It has barely seen `final_choice` — it has to *guess* what to put there.

Naming = priming. Specific, semantically-loaded names recruit pre-trained knowledge for free.

## When To Use

- Always. Costs nothing.
- Especially for fields with units (`age_years`, `price_usd`, `weight_kg`)
- For Booleans — make truth explicit (`is_returning_customer`, not `flag`)
- For enums-mapped strings — the field name should reflect the enum's domain (`severity` not `level`)

## When NOT To Use

- Never. Even legacy schemas should at least add `description` to compensate for cryptic names.

## Patterns

| Bad | Good | Why |
|-----|------|-----|
| `val: int` | `customer_age_years: int` | Unit + entity + range hint |
| `flag: bool` | `is_returning_customer: bool` | Truth-direction explicit |
| `output: str` | `summary_under_50_words: str` | Format encoded in name |
| `data: list` | `validated_email_addresses: list[str]` | Validation state in name |
| `result: dict` | `pricing_breakdown_usd: PricingBreakdown` | Type + domain |
| `final_choice: str` | `answer: str` (or `recommended_action`) | Use the high-prior name |
| `score: float` | `confidence_0_to_1: float` | Range in name |

## Common Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| `output_data`, `result_value`, `final_answer` (redundant suffixes) | Drop the suffix; let the field name carry the meaning |
| `field_a`, `field_b`, `field_c` | Replace with what they mean |
| Languages mixed (`montant_usd`, `total_eur`) | Stick to one language; English has the highest prior |
| Single-letter (`x`, `y`, `n`) | Spell out (`x_coordinate`, `count`) |
| Plurals when single (`items: Item`) | Match the cardinality |

## Composition

- + **schema-field-order**: name + position together steer most strongly
- + **field-descriptions-as-prompts**: descriptions clarify when names alone aren't enough
- + **enum constraints**: enum members benefit from the same naming rule (use `approve`/`reject`, not `1`/`0`)

## References

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

Source: [Bad Schemas could break your LLM Structured Outputs — Instructor](https://python.useinstructor.com/blog/2024/09/26/bad-schemas-could-break-your-llm-structured-outputs/)
