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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Tag glossary is self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Background (why XML beats Markdown, what semantic tags give the agent) + 15 rules: role-bearing tag names, closed glossary, four guarantees, naming, attributes vs children, nesting, CDATA-wrapped code, reference vs see-also, indent hygiene, root + summary, one concept per file | ~2050 |
| `content/02-output-contract.xml` | essential | Schema for one content/*.xml file: `<text id title version est_tokens depth>` root + first-child `<summary>` | ~700 |
| `content/03-failure-modes.xml` | essential | 11 failure modes with detector + repair: `<bold>` tag, multi-concept file, unescaped &, no summary, ad-hoc tag, formatting-as-semantics, inconsistent vocabulary, generic over-wrapping, CDATA leaks, prose-mixed rules, XML-as-document layout | ~1550 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick concept → choose tags from glossary → draft → escape/CDATA → cross-link | ~600 |
| `content/05-examples.xml` | recommended | Paired good/bad XML fragments per rule: semantic vs formatting tags, naming, attributes, nesting, CDATA/entity hygiene | ~850 |
| `content/06-decision-tree.xml` | essential | Applicability gate, then routes by block kind: metadata attribute, code/CDATA, reference vs see-also, visual-only tag, missing glossary tag | ~500 |

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

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-techniques]] — XML delimiters in prompts are the runtime analogue.
- [[skills]] — file structure that wraps content/.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides (a) split-vs-keep when a single file approaches 150 lines, (b) reuse-existing-tag vs glossary-update, and (c) prose `<p>` vs typed element. Use it before adding any new content file or new tag.
