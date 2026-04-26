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

**Mandatory before any edit or new file:**

1. `Read` [`docs/skill-authoring.md`](../docs/skill-authoring.md) — full structure spec.
2. `Read` [`skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`](../skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml) — closed tag vocabulary for `content/*.xml`.

Skip neither. The structure rules are non-obvious (semantic XML, no `README.md` in subfolders, strict `AGENTS.md` shape) and the tag glossary is the only authoritative tag list.
