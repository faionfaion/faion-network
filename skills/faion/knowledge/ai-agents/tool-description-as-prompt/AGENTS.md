# Tool Description as Prompt

## Summary

**One-sentence:** Treat each tool description as a zero-shot teaching prompt with five named parts under 200 tokens, validated against a catalog-audit rubric.

**One-paragraph:** A tool definition becomes part of the system context every time the model decides whether to call a tool. Anthropic's engineering team reported state-of-the-art on SWE-bench achieved by rewriting descriptions, not changing the model. This methodology enforces a five-part structure (use-when, do-NOT-use-when, input contract, output contract, side effects), caps each description at 200 tokens, requires mutual anti-triggers between overlap pairs, mandates `MUTATING:` markers on destructive tools, and verifies the result with an audit-rubric schema that scores each tool 0-5 across the axes. Catalogs are re-evaluated quarterly; both tool-selection and argument-fill error rates are tracked as primary regression signals.

**Ефективно для:**

- MCP-агрегатори і tool-каталоги &gt; 10 інструментів — структуроване опис різко знижує mis-selection.
- Команди, в яких опис інструмента =  marketing-blurb або docstring — швидке покращення SWE-bench-style accuracy.
- Side-effect інструменти (DELETE, DROP, ROLLOUT) — MUTATING-prefix зупиняє accidental calls.
- Description-schema drift аудити — лінт-rule cross-check блокує phantom-arguments ще до production.

## Applies If (ALL must hold)

- Catalog has ≥3 tools whose names share a verb-class (search/get/list etc.) or use cases overlap.
- The catalog is reachable by an agent loop (Claude, GPT, Llama agents — anything that picks tools by description).
- A 50-task eval set or trace store exists to measure pre/post selection-error rate.

## Skip If (ANY kills it)

- Single-tool catalogs where there is no selection problem to begin with.
- One-off scripts where the agent calls a fixed sequence and tool-pick is hard-coded.
- Catalogs whose tools are auto-generated from OpenAPI specs and overwritten on every regen (apply at the spec layer instead).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool catalog | JSON / Python dict / MCP server list | repo / MCP gateway |
| Eval set | 50 representative task prompts | recorded user requests or synthetic set |
| Trace store | per-call (tool_name, args, outcome) | LangSmith / Phoenix / internal logs |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[verb-object-tool-naming]] | Naming has to be sound before descriptions are tuned. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: structured-description-required, under-200-tokens, anti-trigger-on-overlap, mutating-marker, latency/pagination caps, schema-match | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for catalog-audit rubric + examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: marketing-prose, overlap-without-anti-trigger, silent-mutation, schema-description-drift, unbounded-pagination | 800 |
| `content/04-procedure.xml` | essential | 5-step audit → score → detect-overlap → rewrite → measure procedure | 800 |
| `content/06-decision-tree.xml` | essential | Branches on audit-score + mutating + overlap | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score_catalog` | haiku | Five 0/1 checks against templates; deterministic. |
| `detect_overlap` | haiku | Lexical similarity + verb-class clustering. |
| `rewrite_description` | sonnet | Needs balance of brevity + completeness; light judgment. |
| `measure_eval_delta` | haiku | Counting tool-selection errors over fixed eval set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/anthropic-tool-definition.py` | Anthropic SDK tool definition using the 5-part structure |
| `templates/openai-tool-definition.py` | OpenAI SDK function definition using the 5-part structure |
| `templates/mcp-tool-description.py` | MCP `@mcp.tool()` decorator with structured docstring |
| `templates/tool-family-with-anti-triggers.py` | Pattern: read_file + grep_repo with mutual anti-triggers |
| `templates/side-effect-tools.py` | Pattern: apply_patch + dry_run_patch with `MUTATING:` marker |
| `templates/pagination-pattern.py` | Pattern: list_issues with explicit per-page + max-page cap |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-description-as-prompt.py` | Validate the audit JSON against the rubric schema | After each catalog audit; pre-commit on the audit artefact |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[verb-object-tool-naming]] — naming sets the lexical anchor; description fills the gap.
- [[terse-default-tool-output]] — description must declare summary/full mode and token bands.

## Decision tree

See `content/06-decision-tree.xml`. The tree first asks for the tool's 5-axis audit score (5/5 = keep), then asks whether the tool mutates state (yes → `MUTATING:` rewrite), then whether any peer description has cosine &gt; 0.8 (yes → mutual-anti-trigger rewrite). Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/anthropic-tool-definition.py`

```python
tools = [
    {
        "name": "search_docs",
        "description": (
            "Search the indexed documentation for passages matching a query. "
            "Use this when the user asks a how-to or reference question and you don't already have the answer. "
            "Do NOT use this for code search — use `grep_repo` instead. "
            "Returns up to 10 passages ranked by relevance; each includes title, path, and a 200-char excerpt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language question."},
                "max_results": {"type": "integer", "default": 10, "description": "1-50."},
            },
            "required": ["query"],
        },
    },
]
```

### `templates/openai-tool-definition.py`

```python
tools = [{
    "type": "function",
    "function": {
        "name": "create_pr",
        "description": (
            "Create a pull request from the current working branch. "
            "Use this when the user has finalized changes and wants them on the remote. "
            "Do NOT use this if the working tree is dirty (run `git_status` first). "
            "Side effect: pushes branch and opens a PR on GitHub. Returns the PR URL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["title"],
        },
    },
}]
```

### `templates/mcp-tool-description.py`

```python
@mcp.tool()
def query_warehouse(sql: str) -> list[dict]:
    """
    Execute a read-only SQL query against the warehouse.

    Use this when the user asks for analytics that require SQL.
    Do NOT use this for transactional or write operations.
    Returns up to 1000 rows; truncate with LIMIT if larger sets are needed.

    Side effect: none (read-only, sandboxed read-replica).
    Latency: 1-30s depending on query.
    """
    ...
```

### `templates/tool-family-with-anti-triggers.py`

```python
read_file = {
    "name": "read_file",
    "description": (
        "Read a file's contents from the local repo. "
        "Use this when you need to inspect specific code/text. "
        "Do NOT use this for searching across files — use `grep_repo`. "
        "Do NOT use this on files larger than 50KB without `offset`/`limit`."
    ),
}

grep_repo = {
    "name": "grep_repo",
    "description": (
        "Search the repository for a regex pattern. "
        "Use this when you need to find where something appears across many files. "
        "Do NOT use this if you already know the file path — use `read_file`. "
        "Returns matches grouped by file, max 200 lines."
    ),
}
```

### `templates/side-effect-tools.py`

```python
{
    "name": "apply_patch",
    "description": (
        "MUTATING: Apply a unified-diff patch to the repo. "
        "Use this AFTER you have validated the patch with `dry_run_patch`. "
        "Do NOT use this on a dirty working tree. "
        "Returns: {applied: bool, conflicts: list[str]}."
    ),
}
```

### `templates/pagination-pattern.py`

```python
{
    "name": "list_issues",
    "description": (
        "List GitHub issues in the current repo. "
        "Use this to find context for a bug fix or feature. "
        "Returns 30 per page; pass `cursor` from the previous response to paginate. "
        "Do NOT loop more than 5 pages — narrow the query if you need more."
    ),
}
```
