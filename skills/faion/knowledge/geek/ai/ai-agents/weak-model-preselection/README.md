# Weak-Model Preselection

**Category:** `mm-` (multi-model orchestration)

## The Rule

Run a CHEAP, FAST model over the long input first to **filter, classify, or extract references**. Then pass only the filtered set (often just IDs, paths, or short labels) to the EXPENSIVE, STRONG model that does the actual reasoning.

In short: the weak model returns *what to look at*; the strong model returns *what it means*.

## Why It Works

Strong models cost 5-30× more per token. The expensive part of a hard task is *reasoning over the right context*, not *finding the right context*. A small model is usually plenty for "tag, classify, rank, extract refs" — it can run on the full corpus and produce a 100× shorter input for the big model.

This is the agent-level analogue of speculative decoding: small predictor narrows the search, big oracle verifies/uses.

## When To Use

- Long input with mostly irrelevant noise (search over docs, dedupe news, pick code files to read)
- Pre-classification before downstream-model branching (route, then dispatch)
- High-volume preselection where every token saved compounds (RSS pipelines, log analysis)
- Any pipeline where the strong model receives more than ~5K tokens of input *of which most is irrelevant*

## When NOT To Use

- Short inputs (~under 1K tokens) — the routing overhead exceeds the savings
- Tasks where the cheap model's filter mistakes are catastrophic (medical, legal, security gates) — use cheap model only as ranker, never sole gatekeeper
- When the strong model needs the FULL context for emergent insights (e.g., long-context literary analysis)

## Pattern Variants

### A. Filter-then-reason

```
Cheap model → list[bool] keep_flags → strong model receives only the True items
```

### B. Reference-extract-then-load

```
Cheap model → list[file_path]      → strong model is given those files only
```

### C. Classify-then-route

```
Cheap model → category               → routed to specialized strong-model prompt
```

### D. Rank-then-select-top-N

```
Cheap model → score per item         → strong model gets top-N by score
```

## Canonical Example (faion-net news pipeline)

Stage 1 (Haiku):
```
Given 200 RSS items, return the 10 most likely to be interesting to a tech-savvy UA audience.
Return ONLY a JSON list of `{rss_id: int, score: float}`.
```

Stage 2 (Sonnet):
```
Given these 10 items (full text), pick 3 to publish, write a hook for each.
```

Cost goes from ~200K tokens × Sonnet → 200K × Haiku + 10K × Sonnet ≈ 80% saved.

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Big model does the filter itself | Add a Haiku/Mini stage in front |
| Cheap model returns full content (just regurgitates) | Force schema to return refs/IDs only — `list[int]`, `list[str]` |
| Cheap model has different tokenizer/persona than expected | Use the SAME family if possible (Haiku → Sonnet, gpt-4o-mini → gpt-4o) |
| No fallback — when cheap model returns 0 items, pipeline dies | Add `if filtered.is_empty: pass full set to strong model` |
| Filter is permissive — keeps 80% of items | Tune until <30% kept; otherwise no savings |

## Combining Tricks

- + **schema-field-order**: cheap model schema = `[reasoning, kept_ids]` so it briefly justifies the filter before listing IDs
- + **file-reference-passing**: cheap model returns file paths instead of file content
- + **prompt caching**: cache the long prompt + tool defs across both stages (same family)

## References

See `templates.md` for snippets, `examples.md` for production cases, `checklist.md` for review.
