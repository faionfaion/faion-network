# LLM Prompts — Tool Description as Prompt

## Prompt 1: Rewrite tool descriptions

```
For each tool below, rewrite the description to follow this structure:

1. One-sentence "use this when ..."
2. One-sentence "do NOT use this when ..."
3. Input contract (if not obvious from schema)
4. Output contract (shape, limits)
5. Side effects (mutating? idempotent?)

Keep under 200 tokens per description. No marketing prose. No implementation details.

Tools:
{paste tool list}
```

## Prompt 2: Disambiguate similar tools

```
The following tools have overlapping use cases. Add CLEAR "do NOT use this when..." lines that point to the other tool when applicable:

Tool A: {description}
Tool B: {description}

Output: rewritten descriptions with mutual anti-triggers.
```

## Prompt 3: Audit existing tool catalog

```
For each tool below, score 0-5:
- Has when-to-use trigger? (0/1)
- Has when-NOT-to-use anti-trigger? (0/1)
- Side effects called out? (0/1)
- Output shape stated? (0/1)
- Avoids marketing prose? (0/1)

Output: ranked list, lowest score first. These are your top rewrite candidates.
```

## Prompt 4: New-tool description writer

```
You are creating a new tool: {name}.

Write a tool description following the standard structure (use-when, NOT-use-when, input contract, output contract, side effects). The description is the prompt the model will see when deciding whether to call this tool — write for that audience, not for human docs.

Function signature: {signature}
Function purpose: {one sentence}
```
