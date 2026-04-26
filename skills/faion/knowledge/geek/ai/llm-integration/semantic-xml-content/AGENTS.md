# Semantic XML Content for Agents

## Summary

A convention for authoring methodology content as semantic XML — not as XML for formatting, but as a tag vocabulary where each tag carries meaning the agent can act on. Replaces free-form Markdown bodies with structured, machine-parseable elements (`<rule>`, `<example>`, `<antipattern>`, `<reference>`) that Claude was fine-tuned to recognize. Layout, indentation, and prose flow are irrelevant — what matters is the tag hierarchy and attribute values.

## Why

Anthropic explicitly recommends XML tags as Claude's preferred input structure: tags reduce misinterpretation, separate instructions from data, and let the model apply different policies per content type. Markdown can only signal headings and lists; semantic XML tells the agent "this is a rule, this is an antipattern, this is a code example" — distinctions Claude already knows how to honor. Result: more reliable rule-following, fewer hallucinations, easier validation, and a closed grammar that can be checked by a script.

## When To Use

- Authoring `content/*.xml` files inside any new methodology under `faion-network/skills/`.
- Writing reference docs that an agent will load and apply (rules, checklists, examples).
- Migrating an old Markdown methodology when its content needs to be agent-actionable.
- Designing tool-use prompts where input data must be cleanly separated from instructions.

## When NOT To Use

- Routing docs (`AGENTS.md`, `SKILL.md`) — humans read these too; Markdown stays.
- README files for humans — XML hurts readability without giving the agent anything new.
- Code files (`.py`, `.json`, `.sh`) — keep native syntax; never wrap working code in XML.
- One-off prompts that are not loaded by any skill — overhead is not justified.

## Texts

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Why semantic XML works for Claude; semantic vs formatting tags; the four guarantees XML gives an agent. |
| `content/02-tag-design.xml` | Tag naming rules, attribute conventions, nesting rules, when to add a new tag vs reuse an existing one. |
| `content/03-anti-patterns.xml` | Concrete anti-patterns: formatting tags, inconsistent naming, over-nesting, mixing CDATA with prose. |

## Templates

| File | Purpose |
|------|---------|
| `templates/methodology-text.xml` | Skeleton for a `content/*.xml` file with all standard tags wired up. |
| `templates/tag-glossary.xml` | Closed vocabulary of recommended tags with one-line semantics for each. |

## Related

- `knowledge/geek/ai/claude-code/` — Claude Code skill authoring
- `docs/skill-authoring.md` — methodology folder structure (the parent spec that requires this convention)
