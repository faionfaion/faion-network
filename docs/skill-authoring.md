# Skill Authoring — Structure & Conventions

**Goal:** an agent entering a methodology folder gets minimally sufficient context to decide whether this methodology applies to its task — without loading the full content.

This is the source of truth for the shape of skills and methodologies in `faion-network/skills/`. Supersedes the older 5-file pattern (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`).

## Routing-first principle

Auto-loaded `AGENTS.md` is the only thing the agent must read to route. It must answer:
- What this methodology IS (one paragraph)
- When TO use it (concrete triggers)
- When NOT to use it (anti-cases)
- Where the actual content lives (texts/templates/scripts index)

If `AGENTS.md` cannot answer those four within ~80 lines, split or rewrite. Full content is loaded on demand from `texts/`.

## Skill folder

```
<skill-name>/
├── CLAUDE.md          # @AGENTS.md (entrypoint convention)
├── AGENTS.md          # what the skill is, when to use, when NOT, methodology index
├── SKILL.md           # frontmatter + skill summary (only at skill root)
└── <methodology-1>/
    └── ...
```

`SKILL.md` frontmatter: `name`, `description` (with trigger keywords for auto-discovery), `tier` (free/solo/pro/geek), `user-invocable`. Per Claude Code skill rules — see `knowledge/geek/ai/claude-code/skills/`.

## Methodology folder

Each methodology under a skill is a self-contained folder:

```
<methodology>/
├── CLAUDE.md          # @AGENTS.md
├── AGENTS.md          # routing doc (Markdown, under 80 lines) — single index for all subfolders
├── content/           # methodology body — semantic XML, one concept per file
│   ├── 01-<topic>.xml
│   └── 02-<topic>.xml
├── templates/         # real reusable files referenced from content (optional)
│   └── ...
└── scripts/           # verifier / applier / generator code (optional)
    └── ...
```

`templates/` and `scripts/` are optional — include only when they carry real reusable artifacts. Empty folders are not allowed.

**No `README.md` inside `content/`, `templates/`, or `scripts/`.** All file indexes live in the methodology's `AGENTS.md` (single source of truth for routing).

**Body format split:**
- `AGENTS.md` stays Markdown — humans read it, GitHub renders it, agents auto-load it as context.
- `content/*.xml` is **semantic XML for agents** — closed tag vocabulary, no formatting tags, role-bearing structure (`<rule>`, `<example>`, `<antipattern>`, `<reference>`). See methodology `knowledge/geek/ai/llm-integration/semantic-xml-content/` for the convention and tag glossary.
- `templates/*` keep native syntax (`.py`, `.json`, `.txt`, etc.) — never wrap working code in XML.

### AGENTS.md (the routing doc)

Strict shape, under 80 lines:

```markdown
# <Methodology Title>

## Summary

<One paragraph: what the rule / methodology IS. Plain language.>

## Why

<One paragraph: what it solves. Cite the empirical anchor or the mechanism.>

## When To Use

- <concrete trigger 1>
- <concrete trigger 2>
- ...

## When NOT To Use

- <anti-case 1, with one-line reason>
- <anti-case 2, with one-line reason>

## Content

| File | What's inside |
|------|---------------|
| `content/01-foo.xml` | one-liner |
| `content/02-bar.xml` | one-liner |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.py` | one-liner |
| `templates/prompt.txt` | one-liner |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/verify.sh` | one-liner |
```

The agent reads `AGENTS.md` first. If the methodology is relevant, it then loads the specific content files it needs. `AGENTS.md` itself must fit in ~5k tokens.

### Content (semantic XML)

- One concept per file. Split a 300-line doc into 4–8 small files instead.
- Root element: `<text id="NN-slug" title="...">`. First child: `<summary>` (one sentence).
- Use the closed tag vocabulary from `knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`. New tags require a glossary update.
- No formatting tags (no `<bold>`, `<heading>`, `<br>`). Tag names describe role, not appearance.
- Wrap source code in `<code lang="...">` with a CDATA section. Escape `<`, `>`, `&` in element text.
- When a content file uses a template or script, declare it with `<reference path="templates/schema.py">one-line purpose</reference>`.
- No 200-line files. If content grows past ~150 lines, split it.

Skeleton: `knowledge/geek/ai/llm-integration/semantic-xml-content/templates/methodology-text.xml`.

### Templates folder

REAL files, not prose. Example:

```
templates/
├── schema.py        # Pydantic / dataclass example
├── tool-defn.json   # JSON tool definition
└── prompt.txt       # short prompt template
```

Each file under ~60 lines. Content files reference them by relative path via `<reference path="...">`. The methodology `AGENTS.md` lists every template with a one-line purpose — no separate `templates/README.md`.

### Scripts folder

Executable verifiers / appliers / generators. Each script has a top-of-file docstring or header explaining input → output. Indexed in the methodology `AGENTS.md` — no separate `scripts/README.md`.

## Token budget per methodology

| File | Target | Hard cap |
|------|--------|----------|
| `AGENTS.md` | 50–80 lines | 120 |
| Each file in `content/` | 30–80 lines | 150 |
| Each template | 20–50 lines | 80 |
| Each script | as needed | — |

If you blow the cap, split, don't stretch.

## Anti-patterns

- **One giant `README.md`.** Split into `content/`. Keep `AGENTS.md` as routing only.
- **`README.md` inside `content/`, `templates/`, or `scripts/`.** Index every file from the methodology `AGENTS.md` — one place, one source of truth.
- **Markdown bodies for methodology content.** Content lives in semantic XML under `content/`; Markdown stays in `AGENTS.md` and human-facing READMEs only.
- **Formatting tags in XML** (`<bold>`, `<heading>`, `<br>`). Tags must describe role, never appearance — see `semantic-xml-content/`.
- **Skipping `When NOT To Use`.** Without anti-cases the agent cannot reject the methodology safely; it will mis-apply.
- **Inline templates as fenced code blocks longer than ~30 lines.** Move to `templates/` and reference.
- **Vague rules** (`use good practices`). Every methodology must have a concrete, testable rule.
- **5-file rigid pattern** (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`). Replaced by this structure. Don't add new methodologies in the old shape.
- **Empty `templates/` or `scripts/` folder.** Omit the folder instead.

## How agents discover methodologies

1. Session starts with cwd somewhere under the project. Workspace + project + repo `AGENTS.md` auto-load.
2. The agent identifies a relevant skill from the `faion` umbrella (`knowledge/<tier>/<group>/<name>/`).
3. It reads `<skill>/AGENTS.md` to see the methodology index.
4. For each candidate methodology, it reads `<methodology>/AGENTS.md` (cheap — under 80 lines).
5. It loads only the `content/*.xml` files it actually needs.
6. It opens `templates/` or runs `scripts/` on demand.

This is why every level needs a tight routing doc: each Read should narrow the search, never bulk-load.

## Migration note

The 15 already-shipped agent-builder methodologies under `knowledge/geek/ai/ai-agents/` use the old 5-file pattern. They stay as-is (out of scope for the active migration). New methodologies must follow this doc.

## Related

- `directory-structure.md` — repo-wide layout
- `knowledge/geek/ai/claude-code/skills/` — Claude Code skill authoring (frontmatter, tools, permissions)
- `knowledge/geek/ai/claude-code/project-docs-convention/` — `CLAUDE.md` / `AGENTS.md` / `.agents/` convention
- `knowledge/geek/ai/llm-integration/semantic-xml-content/` — semantic XML convention and tag glossary for `content/*.xml`
