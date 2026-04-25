# Examples — File-Reference Passing

## Example 1: News pipeline (neromedia)

Stage 1 — scan: input is the manifest of 200 cached RSS items (id + title only).
Output: `{rationale, relevant_ids: [int]}`. ~300 tokens out.

Stage 2 — write: code looks up the 10 ids in cache, loads bodies, passes them to Sonnet.

The 200 bodies (≈80K tokens) NEVER touch the LLM in stage 1 and never re-enter the prompt in stage 2 (only the 10 selected do).

## Example 2: Subagent that returned 50K tokens of content

**Before:**
Subagent reads 30 files, returns "here's everything I found" pasting full file contents into the parent context. Parent context blows past 200K, gets compacted, loses earlier work.

**After:**
Subagent returns `{summary: "Found auth bugs in 3 files", paths: ["src/a.py", "src/b.py", "src/c.py"]}`. Parent has ~200 tokens of new context; if it wants details, it Reads any path directly.

## Example 3: Repo-aware code review

Reviewer agent receives diffs of 800 changed files (40K LOC).

Stage 1 (Haiku): given path + diff-stat (insertions/deletions), classify each as `[skip|review|deep-review]`. Output is `{decisions: [{path, level}]}`. ~3K tokens out.

Stage 2 (Sonnet): for each `review`-level path, agent gets the diff content. For each `deep-review`-level path, agent also gets neighbor file refs and reads them via tool calls. Token spend now scales with importance, not with diff size.

## Example 4: Multi-doc Q&A

User asks a question across a 500-doc corpus.

```
embedding-search   → 50 candidate doc-ids       (no LLM)
LLM rerank          → 10 doc-ids                  (Haiku)
LLM synthesize      → answer using 10 doc bodies  (Sonnet)
```

Each transition: refs only. The big-model context is bounded by 10 docs, not 500.

## Example 5: Database-backed ref

```python
class Pick(BaseModel):
    rationale: str
    record_keys: list[str]   # primary keys

picks = haiku.pick(records_summary=brief_listing)
records = db.query("SELECT * FROM items WHERE id IN :ids", ids=picks.record_keys)
result = sonnet.process(records)
```

The LLM never sees the DB blob; only summaries and keys.

## Example 6: GitHub PR review

Subagent looks at a PR with 200 comments. Returns `{key_threads: [comment_id, ...], summary: "..."}`. Parent loads only the key threads.

## Example 7: Anti-example (what NOT to do)

```python
# Stage 1
analysis = haiku.run(big_corpus)
# analysis.text is 5K tokens, much of it just regurgitating the corpus

# Stage 2
result = sonnet.run(analysis.text)
# we paid Haiku to summarize, then Sonnet to re-process the summary
# total tokens: corpus + 5K summary; saved nothing
```

Fix: stage 1 returns refs; stage 2 loads from refs directly. The summary-as-content anti-pattern is the most common form of this mistake.

## Example 8: faion-cli pipeline

The Python Agent SDK pipeline engine in `projects/faion-cli/` uses `state.json` files between stages, where each state.json is a list of `{step, output_refs: [paths]}`. No stage's output is ever inlined; everything is pointer-based and idempotent.
