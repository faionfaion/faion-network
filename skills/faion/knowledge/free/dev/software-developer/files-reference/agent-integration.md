# Agent Integration — Files Reference

## When to use
- Routing step inside `faion-software-developer` orchestrator: agent looks up which methodology file to read for a given task.
- Building an autocomplete / lookup tool over the skill's catalog (CI script, `Glob` driver).
- Generating a documentation index page or sidebar from the canonical list.
- Validating that referenced methodology files actually exist on disk before a task starts.

## When NOT to use
- As a general "what should I read" prompt — the catalog is too long (200+ files) to dump verbatim into context. Always filter by domain first.
- For semantic search ("how do I handle errors?"). The list is name-based; pair with `Grep` over the actual READMEs instead.
- As authoritative tier mapping — the file lives under `free/`, but some referenced files (Rust, .NET, GraphQL) belong logically to other tiers; trust the actual directory tree, not this index.

## Where it fails / limitations
- This is purely a **catalog**, not a methodology. There is no checklist/templates/examples content to operationalize — `templates.md`, `examples.md`, `llm-prompts.md` are placeholder shells.
- Several listed files (`go-goroutines.md`, `rust-backend.md`, `csharp-aspnet-core.md`, etc.) are NOT present as flat files in this directory — the real knowledge is split into per-methodology subfolders (e.g. `go-backend/`, `python-fastapi/`). The list pre-dates the folder restructure and drifts.
- "Agent Selection" footer (haiku/sonnet/opus) is generic boilerplate copied from every methodology — ignore it for a pure index file.
- Counts and groupings (`Python: 9 files`, `Django: 11 files`) are stale relative to the live tree.

## Agentic workflow
Treat this file as a **stale-but-useful map**: agent reads it once at session start to learn topical groupings (Python, Django, Go, Rust, ...), then resolves a topic to the actual on-disk path via `Glob skills/faion/knowledge/**/<slug>/README.md`. Never rely on a path mentioned here being correct without a `Glob`/`ls` check first.

### Recommended subagents
- `faion-sdd-executor-agent` — at task pickup, reads `files-reference/README.md` to choose the right methodology folder.
- A small "catalog-validator" general-purpose subagent that walks the table and reports broken links (run on schedule, not per-task).

### Prompt pattern
```
Goal: pick the methodology to load for task <X>.
Step 1: read skills/.../software-developer/files-reference/README.md and identify the topical group (Python / Django / Go / ...).
Step 2: Glob skills/.../software-developer/<slug>/README.md.
Step 3: if missing, fall back to Grep across READMEs for the slug.
Never quote the catalog wholesale into the prompt — only the resolved path.
```

```
Audit task: walk every link in files-reference/README.md.
For each path: check existence (as flat .md OR as <slug>/README.md).
Output a Markdown table of {referenced_path, resolved_path, status}.
Do not fix anything — report only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rg` (ripgrep) | Search the catalog or its targets | https://github.com/BurntSushi/ripgrep |
| `fd` | Confirm file/folder existence | https://github.com/sharkdp/fd |
| `markdown-link-check` | Validate links in this index | `npm i -g markdown-link-check` |
| `lychee` | Faster link checker, supports relative + remote | https://lychee.cli.rs/ |
| `mdbook` / `mkdocs` | Render the catalog as browsable docs | https://rust-lang.github.io/mdBook/ , https://www.mkdocs.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Pages | SaaS | Yes | Cheap host for the rendered catalog. |
| Algolia DocSearch | SaaS | Yes | Index the catalog for fuzzy search; free tier for OSS docs. |
| Pagefind | OSS | Yes | Static-site search, no server. |

## Templates & scripts
Inline link-validator (run from worktree root):

```bash
#!/usr/bin/env bash
# scripts/validate-files-reference.sh
set -euo pipefail
ref="skills/faion/knowledge/free/dev/software-developer/files-reference/README.md"
base="$(dirname "$ref")"
missing=0
# Pull all relative .md targets
grep -oE '\]\([^)]+\.md\)' "$ref" | sed 's/](\(.*\))/\1/' | sort -u | while read -r p; do
  [[ -f "$base/$p" || -f "$base/${p%.md}/README.md" ]] || { echo "MISSING $p"; missing=1; }
done
exit $missing
```

## Best practices
- Treat the catalog as **read-only at agent runtime** — do not have agents append to it; updates must come from a human-driven restructure pass.
- When adding a new methodology folder, also add a row here in the matching topical section so future routing finds it.
- Prefer `<slug>/README.md` lookups over flat-file lookups; the migration to subfolders is the long-term direction.
- For routing prompts, include only the topical headings (## Python, ## Django, ...) — the full table costs ~3 KB of context for little gain.

## AI-agent gotchas
- The list says "python.md (876 lines)" but in practice, methodology files are short — the line counts are old. Don't promise a user "I'll read 876 lines" based on this.
- Don't auto-`Read` every file the user asks about based on this index alone — many entries 404. Always `Glob` first.
- An agent asked to "list all Go files" will paste this section verbatim; remind it to verify presence to avoid hallucinated capabilities.
- LLMs sometimes "fix" broken links by inventing nearby paths. Add a human-in-loop checkpoint before any commit that mutates this file.
- This index is one of the few files in `software-developer/` that is **not** a methodology — agents looking for `checklist.md` content will find empty boilerplate; route them away.

## References
- Worktree path: `skills/faion/knowledge/free/dev/software-developer/files-reference/README.md`
- Parent skill: `skills/faion/knowledge/free/dev/software-developer/CLAUDE.md`
- Tier manifest: `skills/faion/tier-manifest.json`
