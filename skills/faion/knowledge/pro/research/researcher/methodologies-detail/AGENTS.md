# Methodologies Detail Reference

## Summary

A flat reference page bundling 20 research methodologies extracted from `SKILL.md v1.1` as a human-readable cheat sheet. This is not a standalone methodology — it is a TOC with abridged summaries. The canonical agent-actionable copies live in per-methodology folders under `pro/research/researcher/` and `pro/research/market-researcher/` / `pro/research/user-researcher/`.

## Why

Large codebases benefit from a single skim-readable page covering all methodology names, their frameworks, and their agent modes. This page serves that role. Do not parse it as the source of truth for any individual methodology — fields are abridged and the `### Agent` line is a stub.

## When To Use

- Human wants a quick overview of all 20 research methodologies and their agent modes in one place.
- Agent needs to confirm a methodology name before routing to its canonical folder.
- Generating a TOC or cross-reference for documentation.

## When NOT To Use

- As the execution reference for any specific methodology — open the methodology's own folder instead.
- For agent-integration patterns, prompt templates, or CLI tools — those live in per-methodology `agent-integration.md` files (now absorbed into `content/` in the new shape).
- For mode routing in orchestrators — use `../CLAUDE.md` (Research Modes table).

## Content

| File | What's inside |
|------|---------------|
| `content/01-reference.xml` | 20-methodology reference: idea-generation through customer-interview-framework, each with framework summary and agent mode |

## Templates

none
