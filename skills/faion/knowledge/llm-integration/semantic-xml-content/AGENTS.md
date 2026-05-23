# Semantic XML Content for Agents

## Summary

**One-sentence:** A convention for authoring methodology content as semantic XML — tag names describe role (`<rule>`, `<antipattern>`, `<reference>`), not appearance.

**One-paragraph:** Tag vocabulary in which every element carries meaning the agent can act on, not formatting hints. Replaces free-form Markdown for content/*.xml files. Closed glossary in `templates/tag-glossary.xml`; new tags require a glossary update. Anthropic recommends XML as Claude's preferred input — tags reduce misinterpretation, separate instructions from data, allow different policies per type.

**Ефективно для:** автора методологій у faion-network — закриває петлю між XML-структурою і автоматизованим парсингом агентом.

## Applies If (ALL must hold)

- Authoring `content/*.xml` files in faion-network.
- Migrating Markdown methodology bodies to semantic XML.
- Building agent-facing context bundles that need typed sections.
- Tool-use system prompts where instruction vs data separation matters.

## Skip If (ANY kills it)

- Routing documents (`AGENTS.md`) — stays Markdown.
- Human-facing READMEs.
- Code files (templates/*.py, scripts/*.py) — native syntax wins.
- One-off prompts that won't be re-used.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source Markdown / draft | text | author |
| Tag glossary | XML | `templates/tag-glossary.xml` |
| Methodology skeleton | XML | `templates/methodology-text.xml` |
| Slug + title | metadata | parent AGENTS.md |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Tag glossary is self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: role-bearing tag names, closed glossary, no formatting tags, CDATA-wrapped code, escape entities | ~800 |
| `content/02-output-contract.xml` | essential | Schema for one content/*.xml file: `<text id title version est_tokens depth>` root + first-child `<summary>` | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair: `<bold>` tag, multi-concept file, unescaped &, no summary, ad-hoc tag | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick concept → choose tags from glossary → draft → escape/CDATA → cross-link | ~600 |
| `content/05-examples.xml` | medium | One worked content file (mini rule set) | ~500 |
| `content/06-decision-tree.xml` | essential | Picks per-concept file split, glossary-update path | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `migrate-markdown` | sonnet | Per-section conversion with judgment on tag choice. |
| `lint-xml` | haiku | Mechanical schema check. |
| `glossary-update` | opus | Cross-corpus impact assessment when adding a new tag. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tag-glossary.xml` | Closed vocabulary of role-bearing tags allowed in content/*.xml. |
| `templates/methodology-text.xml` | Empty `<text>` skeleton ready to fill. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-semantic-xml-content.py` | Validate that a content/*.xml file uses only glossary-listed tags and matches the root shape. | Pre-commit; CI on every methodology PR. |

## Related

- [[prompt-techniques]] — XML delimiters in prompts are the runtime analogue.
- [[claude-code:skills]] — file structure that wraps content/.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides (a) split-vs-keep when a single file approaches 150 lines, (b) reuse-existing-tag vs glossary-update, and (c) prose `<p>` vs typed element. Use it before adding any new content file or new tag.
