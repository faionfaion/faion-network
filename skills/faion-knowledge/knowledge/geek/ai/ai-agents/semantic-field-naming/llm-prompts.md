# LLM Prompts — Semantic Field Naming

## Prompt 1: Schema rename pass

```
Review this Pydantic schema. For every field name, check:
1. Is it specific, English, and semantically loaded?
2. Does it embed unit / format / cardinality where relevant?
3. Booleans: do they start with is_/has_/should_/requires_?
4. Could the field be renamed to a more conventional name that the LLM has stronger priors for (e.g., final_choice → answer)?

For each issue, output:
- field_old_name → field_new_name
- one-sentence reason

Schema:
{paste here}
```

## Prompt 2: Generate names from descriptions

```
Given these field descriptions, propose semantically-loaded field NAMES (not generic placeholders).

Rules:
- lower_snake_case
- ≥ 2 tokens
- units in name
- bool starts with is_/has_/should_

Descriptions:
{list}
```

## Prompt 3: A/B name evaluator

```
Two candidate names: {A} vs {B}.

Score each on:
- Specificity (1-5)
- Pre-training prior strength (1-5) — how many times has this exact name appeared in training-grade text?
- Cognitive load to read in the schema (1-5, lower is better)

Pick the winner.
```

## Prompt 4: Self-check inside the agent

Add to system prompt of agents that emit schemas:

```
When designing a schema field, ask: "If a reader sees only this name (no description), can they tell what the value will be?" If not, rename.
```
