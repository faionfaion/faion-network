# Methodologies Index

## Summary

A routing table for 22 research methodologies grouped into 5 topic files: idea generation (4), market analysis (5), user research (7), business model planning (4), naming and domains (2). Use this to resolve methodology slug → topic file, then open the topic file for the full methodology body.

## Why

The 22 methodologies were originally in a single 1522-line `methodologies-detail.md`. Splitting into 5 focused files keeps each under 2000 tokens, enabling agents to load only the relevant topic without blowing context. This index is the O(1) lookup entry point.

## When To Use

- You need to find which topic file contains a specific methodology slug (e.g. `jobs-to-be-done` → `user-research.md`).
- Routing an orchestrator to the right methodology file before spawning a research subagent.
- Checking which `faion-research-agent` mode maps to a given methodology.

## When NOT To Use

- As the source of truth for methodology content — fields here are abridged stubs; open the referenced topic file.
- For agent-integration patterns per methodology — those live in each methodology's own folder under `pro/research/researcher/` and `pro/research/market-researcher/`.
- For mode routing in orchestrators — the canonical mode table is in `../CLAUDE.md` (`## Research Modes`).

## Content

| File | What's inside |
|------|---------------|
| `content/01-index.xml` | Quick-lookup table: methodology slug → topic file → agent mode |

## Templates

none
