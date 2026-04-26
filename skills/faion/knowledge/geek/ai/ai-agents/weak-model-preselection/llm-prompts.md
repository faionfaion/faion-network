# LLM Prompts — Weak-Model Preselection

## Prompt 1: Filter prompt (Haiku-class model)

```
You are a fast filter. You will receive {n} items. Your job is to select the at most {k} most relevant for {downstream task}.

Return STRICT JSON matching this schema:
{
  "rationale": "one sentence justifying your top picks",
  "kept_ids": [int, ...]   // at most k ids; in order of relevance
}

Items:
{items}
```

## Prompt 2: Classifier prompt

```
Classify the input into exactly ONE of: {categories}.

Return STRICT JSON:
{
  "rationale": "one sentence",
  "category": "<one of the above>"
}

Input:
{input}
```

## Prompt 3: Ranker prompt

```
Score each item from 0.0 (irrelevant) to 1.0 (perfect match) for {criterion}.

Return STRICT JSON:
{
  "rationale": "one sentence",
  "scores": [
    {"id": ..., "score": ...},
    ...
  ]
}

Items:
{items}
```

## Prompt 4: Reference extractor

```
Read the long text. Return ONLY the file paths / URLs / IDs that are relevant to {question}. Do NOT return any content from the text itself.

Return STRICT JSON:
{
  "rationale": "one sentence",
  "refs": [str, ...]
}

Text:
{text}
```

## Prompt 5: Two-stage instruction (single agent that calls both)

```
You are an orchestrator. The task is too large to handle in one shot. Use this protocol:

1. Call `filter` tool with all candidates → returns kept ids
2. For each kept id, call `expand` tool to fetch full content
3. Synthesize the final answer using ONLY expanded content

Do NOT skip step 1. Do NOT pass full candidates to step 3.
```
