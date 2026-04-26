---
paths:
  - "**/faion-network/skills/**"
  - "**/skills/**/SKILL.md"
  - "**/skills/**/AGENTS.md"
  - "**/skills/**/CLAUDE.md"
  - "**/skills/**/content/**"
  - "**/skills/**/templates/**"
  - "**/skills/**/scripts/**"
---

# Rule: Skill Authoring

**Applies when:** creating or modifying any skill, methodology, or its content under `faion-network/skills/`.

**Rule:** follow the structure and conventions defined in [`docs/skill-authoring.md`](../docs/skill-authoring.md).

## Core requirements

- Each methodology folder has `CLAUDE.md` → `@AGENTS.md`.
- `AGENTS.md` is the routing doc (Markdown): methodology summary, why, when to use, when NOT to use, index of content/templates/scripts. Under 80 lines.
- Body lives in three folders: `content/` (semantic XML, one concept per file), `templates/` (real reusable files in native syntax), `scripts/` (verifiers/appliers, optional).
- **`content/*.xml` is semantic XML, not Markdown** — closed tag vocabulary (`<text>`, `<rule>`, `<example>`, `<antipattern>`, `<reference>`, …), no formatting tags, source code wrapped in `<code lang="..."><![CDATA[ ... ]]></code>`. Tag glossary: `knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`.
- Each content file references the templates/scripts it uses via `<reference path="...">`.
- **No `README.md` inside `content/`, `templates/`, or `scripts/`** — all file indexes live in the methodology `AGENTS.md` (single source of truth).
- An agent entering a methodology folder must get **minimally sufficient context** from `AGENTS.md` to decide relevance — without loading the full content.

## Anti-patterns (do not use)

- Single 200+ line `README.md` for a methodology.
- `README.md` inside `content/`, `templates/`, or `scripts/` (index everything from `AGENTS.md`).
- Markdown bodies under `content/` — must be semantic XML.
- Formatting tags in XML (`<bold>`, `<heading>`, `<br>`) — tags must describe role, not appearance.
- 5-file rigid pattern (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) — replaced by the new structure.
- `AGENTS.md` without "When NOT to use".
- Inline templates as fenced code blocks longer than ~30 lines (move to `templates/`).
- Vague rules like "use good practices" — every methodology must have a concrete, testable rule.

## Migration

The 15 already-shipped agent-builder methodologies under `knowledge/geek/ai/ai-agents/` use the old 5-file pattern. They stay as-is. New methodologies must follow the new structure.

---

**Full spec:** [`../docs/skill-authoring.md`](../docs/skill-authoring.md)
