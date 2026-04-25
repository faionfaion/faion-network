# LLM Prompts — Schema Field Order

## Prompt 1: Schema review

```
Review this Pydantic model. For each field, identify what other fields it depends on. Then check if dependent fields appear AFTER their dependencies. If not, reorder them.

Output format:
- dependency_graph: list of "B depends on A"
- order_violations: list of "B should be after A but isn't"
- reordered_model: corrected Pydantic class

Schema:
{paste schema here}
```

## Prompt 2: Add reasoning fields

```
This schema produces a final answer with no reasoning trace. Add 1-3 reasoning/scratchpad fields BEFORE the final answer. Keep them lean — single-purpose, with clear descriptions explaining what to think about.

Don't add reasoning to schemas that already have it. Don't expand the schema beyond 7 fields.

Schema:
{paste schema here}
```

## Prompt 3: Convert nested → flat-ordered

```
Take this nested schema and produce an equivalent flat schema where every field's position reflects its generation order. Output the flat version with a comment per field explaining what it depends on.

Schema:
{paste schema here}
```

## Prompt 4: Self-review of generated output

When the agent itself emits a schema-shaped output:

```
After producing your output, verify each field used the values of the fields above it. If any field contradicts an earlier field, flag it in a `_self_review` field at the END.
```
