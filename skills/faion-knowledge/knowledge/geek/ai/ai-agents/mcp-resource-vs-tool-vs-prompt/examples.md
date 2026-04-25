# Examples — MCP Resource vs Tool vs Prompt

## Example 1: A docs server done right

- `search_docs(query)` → **Tool** (dynamic search)
- `docs://api/{endpoint}` → **Resource** (per-URI content)
- `/explain-this-doc(section)` → **Prompt** (user slash-command)

The model can decide to search OR read a specific page. The user can invoke `/explain-this-doc(api/auth)` as a starter.

## Example 2: Anti-example — everything as Tool

```
Tools:
- get_doc_index() → returns 50KB of docs index
- read_doc(path) → reads a doc
- search_docs(query) → searches docs
```

`get_doc_index` is the symptom: it's used like a resource (model "reads" it), but it consumes a tool slot and bloats every turn. Convert to `docs://_index` Resource. Now the model only loads it when explicitly relevant.

## Example 3: Anti-example — Resource that mutates

```
GET runbook://incident-foo
  → starts the incident playbook in the background
```

Wrong: Resources are read-only. Side effects make replay and audit impossible. Convert to `start_runbook(name)` Tool.

## Example 4: Linear / Jira / GitHub integration

```
Tools:
- search_issues(query)       # dynamic
- create_issue(title, body)  # mutating
- add_comment(id, body)      # mutating

Resources:
- issue://{project}/{number}     # specific issue content
- project://{name}                # project metadata

Prompts:
- /triage-bug                    # invokes search + classify Tool, then post comment
- /weekly-report                 # composes multiple Resource reads
```

The Prompts are slash commands a PM uses; the Tools are what the agent calls when reasoning; the Resources are what the agent loads on demand.

## Example 5: Codebase server

```
Tools:
- grep_repo(pattern, path)
- read_file(path, start, end)
- apply_patch(diff)            # MUTATING

Resources:
- file:///workspace/{path}     # per-file content
- repo://structure              # tree overview

Prompts:
- /implement-feature(spec)
- /find-tech-debt
```

This is essentially what Claude Code's built-in tools look like, but as an MCP server you can plug into other hosts.

## Example 6: Splitting an over-broad tool

Before:
```
exec(mode: "read"|"write"|"delete"|"list", target: str, ...)
```

After:
```
list_files(path)         # Tool
read_file(path, ...)     # Tool
write_file(path, content)# Tool — MUTATING
delete_file(path)        # Tool — MUTATING

file:///workspace/...    # Resource (alternative read path)
```

The mode-arg pattern fooled the model 25% of the time — it would write when it meant to read. Splitting into named tools fixed it.

## Example 7: Prompt as starter for an agent loop

```
Prompt: /onboard-engineer(seniority="senior", focus_area="backend")
```

Returns a multi-message starter that:
- Tells the agent to read `docs://arch/overview`
- Calls `search_issues(label="good-first-issue")`
- Drafts a 1-week plan

Without the Prompt, the user would have to type all of this every time. With it, one slash command.

## Example 8: Cross-runtime portability

A faion-mcp server exposes all three primitives. When loaded by:
- Claude Code: tools, resources, and prompts all work natively
- OpenAI Responses API: tools work, resources load via tools/call mapping, prompts collapse to system message snippets
- Vercel AI SDK: tools work; resources mapped via fetcher; prompts as system snippets

Designing with all three in mind makes the server work everywhere; designing tool-only locks you out of the slash-command UX.
