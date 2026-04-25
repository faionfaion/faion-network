# LLM Prompts — Prompt-Cache Prefix Order

## Prompt 1: Audit prefix stability

```
Given this prompt structure, identify which segments are STABLE and which are VOLATILE across calls. Reorder so stable segments come first.

Mark where you'd place a cache_control breakpoint.

Output: reordered prompt structure with stability annotation per segment.

Structure:
{paste current prompt builder code}
```

## Prompt 2: Find cache invalidators

```
Look at this prompt and find every place where data is interpolated. For each:
- Mark VOLATILE (changes per call) or STABLE (changes rarely)
- Suggest where to move VOLATILE pieces (usually: into the user message, not system prompt)

Output: list of {segment, vol/stable, suggested_position}.

Prompt builder:
{paste here}
```

## Prompt 3: Cost estimator

```
Given:
- System prompt size: X tokens
- Tools size: Y tokens
- Average user msg: U tokens
- Average output: O tokens
- Calls per session: N

Compute:
1. Without caching: total tokens billed
2. With caching: total tokens billed (cache write 1.25x, cache read 0.1x)
3. Savings %

Use Anthropic Claude pricing (cite the public rate card).
```

## Prompt 4: Add cache_control to existing code

```
Take this Python code that builds Anthropic API requests and add appropriate cache_control breakpoints. Follow these rules:
- System prompts > 1024 tokens get cache_control
- Stable tool blocks get cache_control
- User messages NEVER get cache_control
- ≤ 4 breakpoints total

Code:
{paste here}
```
