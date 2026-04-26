# Progressive Disclosure Skills — 3-Level Pyramid

## Summary

Author Claude Skills as a strict three-level pyramid: (1) YAML frontmatter — name + description + triggers, always loaded into the system prompt; (2) `SKILL.md` body — loaded only when the skill is activated by trigger match; (3) `scripts/`, `references/`, `assets/` — loaded only when the activated `SKILL.md` explicitly tells Claude to read them. Each level pays a context cost only at activation, not by default.

## Why

Anthropic's Skills system was built specifically to solve "the import everything anti-pattern" — agents that pre-load all instructions into the system prompt blow context budgets and degrade reasoning quality. Progressive disclosure mirrors how a senior engineer reads a codebase: scan the index, open the chapter that matches the task, follow only the references that are actually relevant. Empirically, Claude's tool-selection accuracy holds well past 25 skills when each one obeys this rule, and collapses past ~10 when bodies are inlined into the system prompt.

## When To Use

- Authoring any reusable capability whose instructions exceed ~100 lines.
- Domain-specific workflows reused across multiple projects (deploy procedures, commit conventions, design-review rules).
- Building a Claude Code agent that ships with several skills and must keep base context under ~5k tokens.
- Migrating a long `CLAUDE.md` into modular skills as project complexity grows.

## When NOT To Use

- One-off instructions that apply to a single session — inline into `CLAUDE.md` instead.
- Logic that should run as code, not text — package as an MCP tool.
- Tiny rules under ~20 lines — skill machinery overhead exceeds the win.
- Workflows where the "skill" would actually be a prompt template — use `prompts/` in MCP, not Skills.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-levels.xml` | The three loading levels and what belongs in each. |
| `content/02-frontmatter-rules.xml` | Frontmatter fields, trigger phrasing, and length caps. |
| `content/03-anti-patterns.xml` | Common failures: oversized SKILL.md, missing triggers, inlined references. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skill-frontmatter.yaml` | Working frontmatter with all required fields and a trigger-rich description. |
| `templates/skill-body.md` | Minimal `SKILL.md` skeleton showing how to defer to `references/` and `scripts/`. |
