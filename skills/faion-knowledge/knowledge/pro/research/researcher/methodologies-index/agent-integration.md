# Agent Integration — Methodologies Index

## Status: index, not a methodology

This directory is a **table of contents** for 22 research methodologies grouped into 5 topic files (idea generation, market analysis, user research, business model planning, naming and domains). The companion `checklist.md`, `templates.md`, `examples.md`, and `llm-prompts.md` files are empty stubs — there is no methodology content to integrate against.

## Why no full agent-integration here

A meaningful agent-integration document needs concrete decisions: when to use, when to skip, where it fails, prompt patterns, CLI tools, gotchas. None of those apply to a routing index. Writing them here would either duplicate the per-methodology integration docs (correct location) or invent generic boilerplate (waste).

## Where to put real agent-integration content

For each of the 22 listed methodologies, the agent-integration belongs alongside its actual implementation file in the parent `methodologies-detail/` decomposition (or wherever the 5-file methodology pattern is honored). Examples of correct targets:

- `pro/research/market-researcher/market-research-tam-sam-som/agent-integration.md`
- `pro/research/user-researcher/jobs-to-be-done/agent-integration.md`
- `pro/research/market-researcher/competitor-analysis/agent-integration.md`

## How agents should treat this directory

1. Read `README.md` to resolve methodology slug → topic file.
2. Open the referenced topic file (e.g. `user-research.md`) for methodology body.
3. For agentic execution patterns, look up the methodology's own `agent-integration.md` in its dedicated folder, not here.
4. Skip `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md` in this directory — they are placeholder stubs.

## Recommended follow-up

Either delete the four empty stub files (lint noise) or replace this index with a single `INDEX.md` at the parent `researcher/` level. The current 5-file pattern is misapplied: an index does not need a checklist.

## References

- Parent skill: `pro/research/researcher/CLAUDE.md`
- Sibling sub-skills: `faion-market-researcher`, `faion-user-researcher`
