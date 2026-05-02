# Methodology XML Schema

**Goal:** one self-contained `methodology.xml` file per methodology, holding both catalog metadata (stripped before injection) and agent-facing content (returned via the `/faion` skill).

This supersedes:
- The 5-file Markdown pattern (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md` + `agent-integration.md`).
- The intermediate AGENTS.md + `content/*.xml` shape (used by ~88 methodologies under `geek/ai/ai-agents/` and `geek/sdlc-ai/`).

## Folder Layout

```
<tier>/<group>/<domain>/<methodology>/
├── methodology.xml       # REQUIRED — single source of truth
├── templates/            # OPTIONAL — real reusable files (kept as-is)
└── scripts/              # OPTIONAL — real executables (kept as-is)
```

Removed from methodology folders: `CLAUDE.md`, `AGENTS.md`, `README.md`, `content/`, `*.md` body files. Routing happens at the parent skill level (e.g. `geek/sdlc-ai/AGENTS.md` lists all child methodology slugs and one-line summaries).

`templates/` and `scripts/` keep native syntax — never wrap working code in XML.

## Root Element

```xml
<?xml version="1.0" encoding="UTF-8"?>
<methodology slug="lint-megalinter-polyglot">
  <metadata>...</metadata>
  <content>...</content>
</methodology>
```

Attributes:
- `slug` — REQUIRED. Kebab-case. MUST equal the folder name.

Children — in this order:
1. `<metadata>` — required, exactly one.
2. `<content>` — required, exactly one.

## Metadata (NOT exposed to LLM)

The `<metadata>` element is stripped before content injection. It powers the catalog, search, filtering, SEO, and cross-references.

### Mandatory

| Tag | Value |
|-----|-------|
| `<tier>` | `free` \| `solo` \| `pro` \| `geek` |
| `<group>` | `dev` \| `ai` \| `marketing` \| `research` \| `product` \| `pm` \| `ba` \| `ux` \| `comms` \| `infra` \| `sdd` \| `sdlc-ai` |
| `<domain>` | parent skill folder name (e.g. `ai-agents`, `software-developer`, `growth-marketer`) |
| `<summary>` | catalog snippet, ≤200 chars, plain text, no markup |

### Recommended

| Tag | Value |
|-----|-------|
| `<tags><tag>...</tag></tags>` | keyword tags, lowercase kebab-case |
| `<category>` | sub-category prefix (e.g. `lint`, `test`, `mr`, `gov`) |
| `<difficulty>` | `beginner` \| `intermediate` \| `advanced` |
| `<created>` | ISO date `YYYY-MM-DD` |
| `<updated>` | ISO date `YYYY-MM-DD` |

### Cross-references (optional)

| Tag | Purpose |
|-----|---------|
| `<related><ref slug="..."/></related>` | bidirectional peers |
| `<requires><ref slug="..."/></requires>` | prerequisites |
| `<superseded-by><ref slug="..."/></superseded-by>` | newer alternative |

### Applicability (optional)

| Tag | Purpose |
|-----|---------|
| `<applies-to>` | `agents` \| `humans` \| `both` (default `both`) |
| `<tools><tool>claude-code</tool></tools>` | target AI tools |
| `<languages><language>python</language></languages>` | programming languages |
| `<frameworks><framework>django</framework></frameworks>` | frameworks |

### Provenance (rare)

| Tag | Purpose |
|-----|---------|
| `<author>` | origin (person, org, paper) |
| `<source>` | URL or citation |
| `<version>` | semver |
| `<repo-path>` | auto-derived; do not hand-write |
| `<github-url>` | auto-derived; do not hand-write |

## Content (returned to LLM via /faion)

The `<content>` element carries everything the agent receives at runtime. The first child MUST be `<title>`.

### Required

| Tag | Purpose |
|-----|---------|
| `<title>` | one-line headline; comes first |

### Top-level prose blocks

Use these as direct children of `<content>` to structure the methodology.

| Tag | Purpose |
|-----|---------|
| `<summary>` | TL;DR (1-3 sentences). Distinct from `<metadata>/<summary>`. |
| `<why>` | rationale — what it solves, why it works |
| `<when-to-use>` | concrete triggers; use `<list>/<item>` inside |
| `<when-not-to-use>` | anti-cases; one-line reason each |
| `<how-to>` | step-by-step instructions; use `<step>` children |
| `<warning>` | strong caution |

### Structural blocks

| Tag | Purpose |
|-----|---------|
| `<section name="...">` | escape hatch; use only when no specific tag fits |
| `<rule>` / `<rules>` | testable directive(s); children: `<statement>`, `<rationale>` |
| `<example type="good\|bad" title="...">` | concrete worked example; children: `<code>`, `<note>`, `<p>` |
| `<antipattern>` | failure mode; children: `<description>`, `<reason>` |
| `<note>` | short commentary |

### Resource descriptors

Reference real files inside `templates/` or `scripts/`:

| Tag | Purpose |
|-----|---------|
| `<files><file path="..." purpose="..."/></files>` | generic file index |
| `<templates><template path="templates/..." purpose="..."/></templates>` | template index |
| `<scripts><script path="scripts/..." purpose="..."/></scripts>` | script index |
| `<commands><command name="...">...</command></commands>` | CLI commands |

### LLM-operational

| Tag | Purpose |
|-----|---------|
| `<prompt purpose="...">` | LLM prompt template; wrap body in CDATA if it contains markup |
| `<checklist><check>...</check></checklist>` | verification list |
| `<verify><step>...</step></verify>` | verification procedure |

### Reference / linking

| Tag | Purpose |
|-----|---------|
| `<reference path="templates/...">` | hard dependency on a file the agent may load |
| `<see-also><ref slug="..."/></see-also>` | soft cross-reference to peer methodology |
| `<see-also><link href="..."/></see-also>` | external link |

### Inline (used inside the blocks above)

| Tag | Purpose |
|-----|---------|
| `<p>` | paragraph of plain prose |
| `<text>` | generic text wrapper (use last) |
| `<code lang="...">` | source code; ALWAYS wrap body in CDATA |
| `<list><item>...</item></list>` | bullet list |
| `<term name="...">` | definition term |

## Autonomous-Agent Sufficiency

Schema correctness is necessary but not sufficient. A methodology with `<applies-to>agents</applies-to>` or `<applies-to>both</applies-to>` (default) MUST be applicable by an autonomous coding agent without external help. Beyond the schema-required `<title>`, every such methodology MUST include the blocks below — this is the de-facto standard adopted in the feature-048 sufficiency rewrite (47 methodologies, May 2026).

### Required content blocks

| Block | Minimum |
|-------|---------|
| `<when-to-use>` | ≥1 concrete trigger inside `<list>/<item>` (signal that fires the methodology) |
| `<when-not-to-use>` | ≥1 anti-trigger; one-line reason each |
| `<how-to>` with `<step>` children OR `<checklist>` with `<check>` children | how-to: ≥5 ordered steps; checklist: ≥8 items |
| `<commands>` | ≥1 real CLI command (`<command name="...">` with runnable body); omit only when the workflow truly produces no shell output |
| `<prompt purpose="...">` | ≥1 reusable LLM prompt in CDATA when the workflow involves generation/classification/audit |
| `<verify>` with `<step>` children | ≥3 verification steps; each MUST cite a concrete command, file check, or measurable pass criterion |
| `<example type="good">` + (`<example type="bad">` OR `<antipattern>`) | at least one good and one failure-mode example |
| `<see-also>` | ≥2 cross-references (`<ref slug="...">` for internal peers, `<link href="...">` for external docs) |

### Why these four questions

Sufficiency answers what an agent asks at runtime:

1. **WHEN do I trigger this?** → `<when-to-use>` + `<when-not-to-use>`.
2. **WHAT do I run?** → `<how-to>` / `<checklist>` + `<commands>` + `<prompt>`.
3. **HOW do I know it worked?** → `<verify>` with concrete pass criteria.
4. **WHAT does success vs failure look like?** → `<example>` + `<antipattern>`.

Skip any of the four and the agent guesses. The `/faion` skill returns the methodology body verbatim — nothing fills the gaps at runtime.

### Length parity (rewrites)

For methodology rewrites, new `<content>` text length MUST be ≥80% of the original (validator rule 10). New methodologies have no parity floor but should still be deep enough to satisfy the four-question test above (typically ≥250 lines / ≥10KB).

### Recommended additions

- `<warning>` for irreversible or costly mistakes (e.g. "do NOT use Flexible SSL with HTTPS origin").
- `<template path="templates/...">` referencing a real file in `templates/` when the agent copies a config skeleton.
- `<rule>` / `<rules>` for testable invariants the agent can grep-check.
- `<note>` for short caveats inside steps.

## Closed Tag Vocabulary

The full closed list lives in [`docs/methodology-tag-glossary.xml`](methodology-tag-glossary.xml). Validation rejects any tag outside that file.

## Worked Example — Minimal

A small `solo`-tier methodology, single rule, no templates:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<methodology slug="git-conventional-commits">
  <metadata>
    <tier>solo</tier>
    <group>dev</group>
    <domain>software-developer</domain>
    <summary>Use Conventional Commits format (type: subject) so changelog tooling and AI agents can parse history.</summary>
    <tags>
      <tag>git</tag>
      <tag>commits</tag>
      <tag>changelog</tag>
    </tags>
    <difficulty>beginner</difficulty>
    <created>2026-04-27</created>
  </metadata>
  <content>
    <title>Conventional Commits</title>
    <summary>Every commit subject MUST start with a type prefix (feat, fix, chore, docs, refactor, test) followed by a colon and a short imperative sentence.</summary>
    <why>
      <p>Tooling (changelog generators, semantic-release, AI release-note writers) needs a deterministic format to extract change type. Free-form messages force humans to summarize, AI to guess.</p>
    </why>
    <when-to-use>
      <list>
        <item>Any project that publishes releases or auto-generates changelogs.</item>
        <item>Repos where AI agents draft PR descriptions or release notes.</item>
      </list>
    </when-to-use>
    <when-not-to-use>
      <list>
        <item>Throwaway scratch repos — overhead exceeds value.</item>
      </list>
    </when-not-to-use>
    <rule>
      <statement>Commit subject MUST match `^(feat|fix|chore|docs|refactor|test|perf|build|ci|style|revert): .{1,50}$`.</statement>
      <rationale>50-char limit ensures readability in `git log --oneline` and GitHub UI.</rationale>
    </rule>
    <example type="good">
      <code lang="text"><![CDATA[fix: handle empty cart on checkout
feat: add export-to-CSV for invoices
chore: bump pytest to 8.2]]></code>
    </example>
    <example type="bad">
      <code lang="text"><![CDATA[updated stuff
WIP
asdf]]></code>
      <note>No type prefix; not parseable.</note>
    </example>
  </content>
</methodology>
```

## Worked Example — Comprehensive

See [`templates/methodology-example-comprehensive.xml`](../skills/faion-network-templates/methodology-example-comprehensive.xml) for a full geek-tier methodology with templates, scripts, and cross-references.

## Migration Mapping

### From OLD shape (5-file pattern)

| Old | Goes to |
|-----|---------|
| `README.md` H1 | `<content>/<title>` |
| `README.md` first paragraph | `<content>/<summary>` AND `<metadata>/<summary>` (truncated to 200 chars) |
| `README.md` "Why" / "Why It Matters" | `<content>/<why>` |
| `README.md` "When To Use" | `<content>/<when-to-use>` |
| `README.md` "When NOT To Use" | `<content>/<when-not-to-use>` |
| `README.md` "How To" / numbered steps | `<content>/<how-to>` with `<step>` children |
| `checklist.md` items | `<content>/<checklist>/<check>` |
| `examples.md` good/bad blocks | `<content>/<example type="good\|bad">/<code>` |
| `llm-prompts.md` prompts | `<content>/<prompt purpose="...">` (CDATA body) |
| `templates.md` referencing real files | move file into `templates/`, declare via `<content>/<templates>/<template path="..." purpose="..."/>` |
| `agent-integration.md` | merge usage notes into `<content>/<how-to>` and `<content>/<note>` |

### From NEW shape (AGENTS.md + content/*.xml)

| Old | Goes to |
|-----|---------|
| `AGENTS.md` H1 | `<content>/<title>` |
| `AGENTS.md` Summary | `<content>/<summary>` AND `<metadata>/<summary>` (≤200 chars) |
| `AGENTS.md` Why | `<content>/<why>` |
| `AGENTS.md` When To Use | `<content>/<when-to-use>` |
| `AGENTS.md` When NOT To Use | `<content>/<when-not-to-use>` |
| `AGENTS.md` Content table | absorbed; the body lives directly under `<content>` now |
| `AGENTS.md` Templates/Scripts tables | `<content>/<templates>` / `<content>/<scripts>` |
| `content/01-foo.xml` rules | inlined under appropriate top-level block (`<rules>`, `<rule>`, `<example>`, etc.) |

`templates/` and `scripts/` folders stay where they are.

## Validation Rules

A methodology passes validation iff:

1. **Well-formed XML** (parses without errors).
2. **Root** is `<methodology>` with `slug` attribute matching folder name.
3. **`<metadata>` and `<content>` both present**, in that order.
4. **All mandatory metadata fields** present: `<tier>`, `<group>`, `<domain>`, `<summary>` (≤200 chars).
5. **`<content>/<title>`** present and non-empty.
6. **All tags** appear in `methodology-tag-glossary.xml`.
7. **Required attributes** on `<reference>`, `<file>`, `<template>`, `<script>`, `<ref>`, `<section>` are present.
8. **No empty body** of `<rule>`, `<rules>`, `<example>`, `<antipattern>`, `<files>`, `<templates>`, `<scripts>`.
9. **Code blocks** under `<code>` are wrapped in `<![CDATA[...]]>`.
10. **Length parity** — total text content of `<content>` is ≥80% of the original markdown body length (detects accidental summarization). Skip when migrating from XML-only sources.

The validator script enforces all rules above. See [`scripts/validate-methodology-xml.py`](../scripts/validate-methodology-xml.py).

## Subagent Contract — `/faion`

When the `/faion` skill returns a methodology to the agent's prompt, it:

1. Parses the requested `methodology.xml`.
2. Strips `<metadata>` entirely.
3. Wraps the body in `<faion-methodology slug="...">...</faion-methodology>`.
4. Returns only that wrapped body.

Example output injected into the agent's context:

```xml
<faion-methodology slug="lint-megalinter-polyglot">
  <title>MegaLinter as the Polyglot Quality Umbrella in CI</title>
  <summary>...</summary>
  <why>...</why>
  <when-to-use>...</when-to-use>
  ...
</faion-methodology>
```

The catalog generator does the inverse: reads `<metadata>`, ignores `<content>`.

## Skill-level Router (AGENTS.md, XML body)

Skill-level `AGENTS.md` files (e.g. `geek/sdlc-ai/AGENTS.md`) keep the `.md` filename but the body is **XML — no metadata block, just a list of methodology entries with minimal routing fields**. Identity (tier / group / skill) is derived from the path.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<router>
  <methodology slug="lang-go-tygo-frontend-contract">
    <reference path="lang-go-tygo-frontend-contract/methodology.xml">Body</reference>
    <title>Go ↔ TS Contract via Tygo</title>
    <summary>Generate TypeScript types from Go structs to keep frontend typed against backend.</summary>
    <when-to-use>
      <item>Go backend with TS frontend</item>
      <item>API contract drift caught in CI</item>
    </when-to-use>
    <when-not-to-use>
      <item>OpenAPI is primary contract</item>
      <item>No TypeScript on frontend</item>
    </when-not-to-use>
  </methodology>

  <methodology slug="lint-megalinter-polyglot">
    <reference path="lint-megalinter-polyglot/methodology.xml">Body</reference>
    <title>MegaLinter for Polyglot Repos</title>
    <summary>One linter container running 50+ linters; CI-only, never pre-commit.</summary>
    <when-to-use>
      <item>Polyglot repo (3+ languages)</item>
    </when-to-use>
    <when-not-to-use>
      <item>Single-language repo</item>
    </when-not-to-use>
  </methodology>
</router>
```

### Router rules

1. Filename: `AGENTS.md` (extension preserved for Claude Code auto-load).
2. First line: `<?xml version="1.0" encoding="UTF-8"?>`.
3. Root element: `<router>`. Exactly one per file.
4. Children of `<router>`: only `<methodology>` entries — no metadata, no scope, no how-to.
5. Each `<methodology>` MUST have:
   - `slug` attribute equal to a real subfolder name.
   - First child `<reference path="<slug>/methodology.xml">Body</reference>`.
   - Then exactly: `<title>`, `<summary>` (≤200 chars), `<when-to-use>` (2-5 `<item>`), `<when-not-to-use>` (2-5 `<item>`).
6. Closed vocabulary — only tags from `methodology-tag-glossary.xml` (see "Router" section).
7. The `<methodology>` tag is reused with two different shapes — root in `methodology.xml` (with `<metadata>` + `<content>`) vs child of `<router>` (entry shape). Validator distinguishes by parent.

A separate validator `scripts/validate-router-xml.py` (added in feature-047) enforces these rules.

## Anti-patterns

- **Putting catalog data in `<content>`.** Tier/group/domain belong in metadata; they are NOT prompt content.
- **Free-text inside top-level `<content>`** without a wrapper element. Wrap in `<p>`, `<summary>`, `<why>`, etc.
- **Formatting tags** (`<bold>`, `<heading>`, `<br>`). Glossary rejects them.
- **Skipping `<when-not-to-use>`.** Without anti-cases agents mis-apply the methodology.
- **Methodology without `<commands>` or `<verify>`.** Schema-valid but agent-useless: the agent has no way to act or check the result. Fails the sufficiency rules above.
- **Wrapping working code in XML attributes.** Code goes in `<code>` with CDATA.
- **Empty `<templates>` / `<scripts>` blocks.** Omit instead.
- **Inventing tags** outside the glossary. Update `methodology-tag-glossary.xml` first, with rationale.

## Related

- [`docs/methodology-tag-glossary.xml`](methodology-tag-glossary.xml) — closed tag vocabulary
- [`scripts/validate-methodology-xml.py`](../scripts/validate-methodology-xml.py) — validator
- [`docs/skill-authoring.md`](skill-authoring.md) — parent spec (folder structure, routing)
- `.aidocs/feature-045-methodology-xml-migration/` — migration pool state
