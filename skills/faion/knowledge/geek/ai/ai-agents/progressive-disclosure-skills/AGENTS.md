---
slug: progressive-disclosure-skills
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Author Claude Skills as a strict three-level pyramid: (1) YAML frontmatter — name + description + triggers, always loaded into the system prompt; (2) SKILL.
content_id: "50fec46431a9bdd3"
tags: [skills, context-management, progressive-disclosure, prompt-engineering, anthropic]
---
# Progressive Disclosure Skills — 3-Level Pyramid

## Summary

**One-sentence:** Author Claude Skills as a strict three-level pyramid: (1) YAML frontmatter — name + description + triggers, always loaded into the system prompt; (2) SKILL.

**One-paragraph:** Author Claude Skills as a strict three-level pyramid: (1) YAML frontmatter — name + description + triggers, always loaded into the system prompt; (2) SKILL.md body — loaded only when the skill is activated by trigger match; (3) scripts/, references/, assets/ — loaded only when the activated SKILL.md explicitly tells Claude to read them. Each level pays a context cost only at activation, not by default.

## Applies If (ALL must hold)

- Authoring any reusable capability whose instructions exceed ~100 lines.
- Domain-specific workflows reused across multiple projects (deploy procedures, commit conventions, design-review rules).
- Building a Claude Code agent that ships with several skills and must keep base context under ~5k tokens.
- Migrating a long CLAUDE.md into modular skills as project complexity grows.

## Skip If (ANY kills it)

- One-off instructions that apply to a single session — inline into CLAUDE.md instead.
- Logic that should run as code, not text — package as an MCP tool.
- Tiny rules under ~20 lines — skill machinery overhead exceeds the win.
- Workflows where the "skill" would actually be a prompt template — use prompts/ in MCP, not Skills.

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

- parent skill: `geek/ai/ai-agents/`
