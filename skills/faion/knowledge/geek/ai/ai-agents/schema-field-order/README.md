# Schema Field Order — Autoregressive Steering

**Category:** `so-` (structured output)

## The Rule

In a structured-output schema (JSON schema, Pydantic model, tool input schema, `response_format`), **place dependent fields AFTER their dependencies**. The model generates left-to-right and each field can attend only to fields that came before it.

If field B is conceptually derived from field A, A must appear earlier in the schema than B.

## Why It Works

LLMs are autoregressive: they emit tokens one at a time, each conditioned on everything emitted before. Structured output is no exception — schema fields are filled in declaration order. A field defined *later* in the schema sees all fields defined *earlier* as context, but **not vice versa**.

That means:
- Putting `summary` before `body` forces the model to write the summary *before* it has written the body — it must guess what the body will say.
- Putting `body` before `summary` lets the summary actually summarize the produced body.

This is free chain-of-thought: every "thought" field placed before the "answer" field acts as scratchpad. Every "input echo" field placed before "output" acts as a re-grounding step.

## When To Use

- Whenever your schema has fields where one *depends on* another (almost always)
- When you want a "reasoning before answer" effect without using extended-thinking APIs
- When you want a "title from content" pattern — content first, title last
- When you need re-grounding on long inputs — put a field that restates the question before the answer

## When NOT To Use

- Schemas with no semantic dependency (pure parallel extraction of independent facts) — order doesn't matter
- When your runtime parses fields in arbitrary order (rare; almost all do declaration-order generation)

## Canonical Examples

### Wrong order

```python
class Article(BaseModel):
    title: str        # generated first — model has no content yet, must hallucinate
    summary: str      # also too early
    body: str         # generated last — but title/summary already locked in
```

### Right order

```python
class Article(BaseModel):
    body: str         # generated first — full content
    summary: str      # generated next — sees body, can compress it
    title: str        # generated last — sees both, picks sharpest hook
```

### Reasoning-before-answer

```python
class Decision(BaseModel):
    options_considered: list[str]   # scratchpad
    risks_per_option: list[str]     # more scratchpad
    chosen_option: str              # final answer — sees its own reasoning
```

### Re-ground on long input

```python
class Critique(BaseModel):
    restate_user_intent: str        # forces the model to re-encode the question
    findings: list[Finding]
    overall_verdict: Literal["approve", "request_changes"]
```

## Common Anti-Patterns

| Anti-pattern | Why it hurts | Fix |
|--------------|--------------|-----|
| `id` field first based on title that doesn't exist yet | model invents a placeholder, then writes a title that doesn't match the slug | move `id` last |
| `confidence` before `answer` | model commits to confidence with no answer to be confident about | move `confidence` last |
| `next_action` before `analysis` | action is decided blind | analysis first, action last |
| `tags` before `summary` | tags pulled from thin air | summary first, tags last |

## Field-Description Reinforcement

Even with correct order, write the description to make the dependency explicit:

```python
class Article(BaseModel):
    body: str = Field(description="Full article content; write this first.")
    title: str = Field(description="A sharp title derived from the body above. 6-10 words.")
```

Field descriptions ARE part of the prompt the model sees during generation; the description tells it both *what* the field is and *that* it should look back at the previous fields.

## Verifying

Run the same task with both orders, compare:
1. **Coherence**: do the dependent fields actually reflect the source fields?
2. **Hallucination rate**: how often does the early field commit to something the later field contradicts?
3. **Token cost**: reversed order is usually FASTER overall because the model isn't backtracking.

## References

See `templates.md` for snippets in OpenAI / Anthropic / Gemini / Pydantic-Outlines.
See `examples.md` for real production examples from neromedia and faion-cli.
See `checklist.md` for review checklist.
See `llm-prompts.md` for prompts that exemplify the rule.
