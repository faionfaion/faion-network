# File-Reference Passing Between Pipeline Steps

**Category:** `pl-` (pipeline & sub-task delegation)

## The Rule

When agent step N analyzes a corpus, return **only references** (file paths, IDs, URLs, doc-keys) — not the content itself. Step N+1 loads from those references on demand.

The corollary: the boundary between agent steps is a list of POINTERS, not a payload of CONTENT.

## Why It Works

Three independent benefits compound:

1. **Context economy** — content carried across steps consumes the prompt budget of every step it touches. References are tiny.
2. **Lazy loading** — step N+1 (or its tools) decides what to actually load. Often only 30% is needed.
3. **Recoverability** — refs are stable; content can change. A pipeline that resumes after a crash re-reads from refs and gets fresh state.
4. **Audit & debugging** — refs are cheap to log and replay. Content is heavy and often redacted.

This pattern is why Claude Code's subagents emit *summaries with file paths* rather than dumping file contents back to the parent — the parent re-reads what it needs.

## When To Use

- Multi-stage pipelines where each stage operates on a corpus
- Map-reduce patterns over documents
- Agents with subagents (subagent returns a slim summary + refs; parent re-fetches if needed)
- Long documents where only some passages matter to downstream
- Any time you find yourself ferrying >2K tokens of "context" between steps

## When NOT To Use

- Single-shot agents (no downstream step exists)
- When the content is small enough that lazy-loading adds more overhead than it saves
- When refs are unstable (URLs that expire, IDs that get reassigned) — use snapshotted refs
- When the downstream model lacks tools to *load by ref* (no file-read tool, no DB-fetch tool)

## Pattern Shapes

### A. Stage-output is refs

```
Stage 1: scan(corpus) → list[FileRef]
Stage 2: each_ref → load(ref) → process
```

### B. Subagent returns refs + summary

```
parent → spawn(subagent, big_task)
subagent → analyze; return {summary: "...", interesting_refs: [...]}
parent → if needs more, load(ref) directly
```

### C. Manifest-then-fetch

```
LLM sees a MANIFEST (id + 1-line description per item)
LLM picks K items by id
Code fetches the K items and feeds them to the next LLM call
```

### D. Recursive descent

```
LLM sees list of dirs → picks dir
LLM sees list of files in dir → picks file
LLM reads file → answers
```

Each level: refs in, refs out. Content never crosses more than one boundary.

## Concrete Example (faion-net news pipeline)

Stage 1 (analyzer):
```python
class Analysis(BaseModel):
    rationale: str
    relevant_paths: list[str]   # paths into the local feed cache
```

Stage 2 (writer) is given `relevant_paths`, then opens each with `Path.read_text()`. It never sees content that the analyzer flagged as irrelevant.

## Anti-Patterns

| Anti-pattern | Why it hurts | Fix |
|--------------|--------------|-----|
| Stage 1 returns "summary + content of relevant items" | content is duplicated across stages | return refs only; stage 2 re-fetches |
| Subagent returns the entire file it analyzed | parent context blows up | subagent returns summary + path |
| Refs are LLM-generated paths that don't exist | hallucinated refs break loading | constrain refs to a manifest the LLM was given |
| Refs are remote URLs that expire | rerun fails | snapshot the resource and reference the snapshot |
| Pipeline persists raw content between steps | disk and memory both bloat | persist refs only; resolve at use |

## Composition with Other Tricks

- + **schema-field-order**: schema = `[rationale, refs]` so the model justifies the picks before listing them
- + **weak-model-preselection**: cheap model produces refs; strong model loads and reasons
- + **subagent isolation**: subagent has its own context; the only thing crossing the boundary is refs + summary

## Implementation Notes

- Use **short, stable** ref formats: `path:relative/file.md`, `db:items/1234`, `gh:owner/repo@sha:path`
- Validate refs after the LLM call and before passing to next step (catch hallucinations early)
- Log the ref list at every stage boundary — best debug breadcrumb you'll ever have
- Cache the manifest the LLM was given (it shouldn't pick refs from outside the manifest)

## References

See `templates.md` for snippets across SDKs.
See `examples.md` for production cases.
See `checklist.md` for review checklist.
