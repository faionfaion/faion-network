# Examples — Weak-Model Preselection

## Example 1: News pipeline (neromedia)

200 RSS items/hour from 30 feeds. Native Sonnet over the full set would cost ~$3/hour.

Filter stage (Haiku):
- input: 200 items × 100 tokens = 20K tokens
- output: list of 10 IDs + 1-sentence rationale = 200 tokens
- cost: ~$0.005

Synthesis stage (Sonnet):
- input: 10 items × 500 tokens = 5K tokens
- output: 3 posts × 300 tokens = 900 tokens
- cost: ~$0.06

Total: $0.07 vs $3 → 40× cheaper.

## Example 2: Code review subagent (faion-cli)

Project has 800 changed files. Reading them all costs $5+ per review.

Filter stage (Haiku):
- input: list of file paths + brief diff stats
- output: list of files-most-likely-to-need-review
- output schema: `{rationale: str, paths: list[str]}`
- typically narrows 800 → 20-40

Review stage (Sonnet/Opus):
- reads only the 20-40 files
- ~50× cheaper than the naive approach

## Example 3: Customer support routing

User message → Haiku classifies into one of 12 categories → routed to category-specific Sonnet prompt with category-specific tools.

```python
class Route(BaseModel):
    rationale: str
    category: Literal["billing", "auth", "bug", "feature", ...]

route = haiku_classify(message)
result = sonnet_handlers[route.category](message)
```

Routing cost: $0.0001. Handler cost: $0.01-0.05. Saves ~80% vs single big model with all tools.

## Example 4: Memory retrieval

Agent has 1000 prior conversation turns in long-term memory.

Naive: dump all 1000 into context — slow, expensive, often blows window.

With preselection:
- Embedding search (no LLM) → top 50 candidates
- Haiku reranks 50 → top 10
- Sonnet uses 10 turns + current message

Each layer narrows; each layer is cheaper than the next.

## Example 5: Rejection / Refusal first

```python
class Pre(BaseModel):
    is_safe: bool
    is_in_scope: bool
    rationale: str

pre = haiku_check(user_input)
if not pre.is_safe or not pre.is_in_scope:
    return canned_refusal(pre.rationale)

# only here do we burn the strong model
return sonnet_handle(user_input)
```

A cheap pre-filter catches ~90% of refusals at <$0.001/each.

## Example 6: Cache-friendly pre-filter

When the prompt is identical across many inputs (e.g., classifying a stream), put the cheap model behind prompt caching:

```python
filter_resp = client.messages.create(
    model="claude-haiku-4-5",
    system=[
        {"type": "text", "text": LONG_RUBRIC, "cache_control": {"type": "ephemeral"}}
    ],
    messages=[{"role": "user", "content": item}]
)
```

Now even the cheap stage costs ~10% per call.
