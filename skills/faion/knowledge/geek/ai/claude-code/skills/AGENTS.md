---
slug: skills
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Complete guide to skill creation and management in Claude Code.
content_id: "fb74d67dab1b7d23"
tags: [skills, claude-code, workflow, automation, configuration]
---
# Creating or Updating Claude Code Skills

## Summary

**One-sentence:** Complete guide to skill creation and management in Claude Code.

**One-paragraph:** Complete guide to skill creation and management in Claude Code. Skills are discoverable workflows that combine tools, permissions, and knowledge into reusable packages. This methodology covers SKILL.md structure, frontmatter fields, tool permissions, naming conventions, and the distinction between global skills (committed to faion-network) and project-specific skills (gitignored locally).

## Applies If (ALL must hold)

- User explicitly asks to create, edit, update, modify, fix, or improve a skill.
- A complex workflow needs to be discoverable and reusable across sessions.
- Tool permissions must be scoped (e.g., read-only agents).
- Multi-file knowledge needs to be bundled together for Claude Code auto-discovery.
- A workflow should appear in the `/` menu as a skill option.

## Skip If (ANY kills it)

- The workflow is a one-time task — use a plain prompt instead.
- You only need a slash command with arguments — create a command, not a skill.
- The skill already exists in faion-network and only needs minor wording changes — edit the existing file.
- The workflow is project-specific business logic that should not be shared across projects.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/claude-code/`
