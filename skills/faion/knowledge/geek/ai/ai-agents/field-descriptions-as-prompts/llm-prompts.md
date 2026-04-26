# LLM Prompts — Field Descriptions as Inline Mini-Prompts

## Prompt 1: Generate descriptions

```
For each field below, write a 1-3 sentence `description` covering:
- What the field represents
- Format / units / range
- Edge cases (missing/ambiguous input)
- Forbidden patterns

Output: same schema, with descriptions added.

Schema:
{paste here}
```

## Prompt 2: Audit descriptions

```
Review every field description in this schema. Flag:
- Empty descriptions
- Descriptions that duplicate the field name
- Descriptions asking for reasoning (move reasoning to its own field)
- Descriptions contradicting the field name or type
- Descriptions longer than 3 sentences (tighten)

Output: list of issues with proposed rewrites.

Schema:
{paste here}
```

## Prompt 3: Edge-case enumeration

```
For each field below, list the top 5 likely failure modes:
- ambiguous input
- missing input
- conflicting input
- unit confusion
- format drift

Then propose a 1-sentence addition to the description that addresses each failure.

Schema:
{paste here}
```

## Prompt 4: Description for a constrained string

```
Field: {field_name}
Type: {type}
Constraints: {constraints, e.g., max length, regex, enum}

Write a 1-2 sentence description that an LLM can use to fill this field correctly. Include format and the most likely failure mode to avoid.
```
