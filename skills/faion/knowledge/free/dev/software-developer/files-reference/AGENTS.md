# Files Reference

## Summary

A catalog index of all methodology files in the `software-developer` skill, grouped by language and domain (Python, Django, JavaScript/TypeScript, Go, Rust, Ruby, PHP, Java, C#, API Design, Testing, Frontend, Architecture, Database, Infrastructure, Dev Practices). Used as a routing map to find the right methodology subfolder by topic. The list predates the folder restructure and may be stale — always verify existence with a filesystem lookup before loading a path.

## Why

The `software-developer` skill contains 200+ methodology entries across many languages. A grouped catalog lets an agent identify the topical group (e.g. "Go") in one read, then resolve the actual subfolder path via `Glob`, rather than scanning the entire tree. Faster routing, lower context cost.

## When To Use

- Routing step inside `software-developer` orchestrator: determining which subfolder covers a given task topic.
- Building a documentation index or sidebar from the canonical catalog.
- Validating that referenced methodology folders exist before dispatching a task.

## When NOT To Use

- As a semantic search tool ("how do I handle errors?") — the list is name-based; use `Grep` over actual AGENTS.md files.
- As an authoritative tier map — some files listed under `free/` cover topics that belong logically to other tiers; trust the directory tree.
- Dumping the full catalog into context — it is too large (200+ entries); filter to the relevant topical section only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-catalog.xml` | Full grouped file catalog: Python, Django, JS/TS, Go, Rust, Ruby, PHP, Java, C#, API Design, Testing, Browser Automation, Frontend, Architecture, Database, Infrastructure, Dev Practices. |

## Templates

none
