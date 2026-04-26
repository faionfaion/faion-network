# Subagent Brief — SDLC+AI Methodologies Tick

You are a Task subagent. The orchestrator has selected N=3-5 candidate methodology slugs. Write the methodology folders + update state + commit.

## Working directory

`/home/nero/workspace/projects/faion-net/faion-network`

## Inputs (filled by orchestrator)

| Variable | Meaning |
|----------|---------|
| `slugs` | List of N slugs to write this tick |
| `sources` | Map `slug → relative path under .aidocs/sdlc-ai-methodologies/research/` |
| `categories` | Map `slug → category prefix` (one of `lang- lint- test- tracker- kb- task- mr- inc- sec- gov-`) |
| `cycle` | Current cycle number |

## MANDATORY pre-flight (before ANY file write)

Before creating or editing a single methodology file, you MUST `Read`:

1. `docs/skill-authoring.md` — full structure spec
2. `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml` — closed tag vocabulary for `content/*.xml`

Skipping these is the #1 cause of rejected ticks. The conventions are non-obvious (semantic XML, no `README.md` inside subfolders, role-bearing tag names).

## Methodology format (canonical)

**Source of truth:** `docs/skill-authoring.md` (which you just read). Output path:

```
skills/faion/knowledge/geek/sdlc-ai/<slug>/
├── CLAUDE.md          # @AGENTS.md
├── AGENTS.md          # routing, Markdown, <80 lines
├── content/           # semantic XML, one concept per file
│   ├── 01-<topic>.xml
│   └── ...
└── templates/         # OPTIONAL: real reusable artifact
    └── <name>.<ext>
```

`scripts/` optional. **NO `README.md` inside `content/`, `templates/`, or `scripts/`** — every file indexed in the methodology `AGENTS.md`. Empty folders forbidden.

### `AGENTS.md` strict shape

```markdown
# <Title>

## Summary

<one paragraph>

## Why

<one paragraph; cite empirical anchor or mechanism>

## When To Use

- <trigger 1>
- <trigger 2>

## When NOT To Use

- <anti-case 1>
- <anti-case 2>

## Content

| File | What's inside |
|------|---------------|
| `content/01-foo.xml` | one-liner |

## Templates

| File | Purpose |
|------|---------|
| `templates/<file>` | one-liner |
```

(Add `## Scripts` table only if `scripts/` exists.)

Hard caps: `AGENTS.md` ≤ 120 lines, each `content/*.xml` ≤ 150, each template ≤ 80.

### Semantic XML for `content/`

Closed tag vocabulary (from `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`). Tags describe ROLE. Skeleton:

```xml
<text id="01-rule" title="The Rule">
  <summary>One-sentence summary.</summary>
  <rule>State the testable rule.</rule>
  <example>
    <code lang="python"><![CDATA[
def example(): ...
    ]]></code>
  </example>
  <antipattern>
    <code lang="python"><![CDATA[
def bad(): ...
    ]]></code>
    <why>Why this fails.</why>
  </antipattern>
  <reference path="templates/schema.py">Pydantic shape</reference>
  <reference href="https://...">External source</reference>
</text>
```

NO formatting tags. NO Markdown bodies under `content/`.

## Per-slug procedure

For each slug:

1. Read `sources[slug]` — locate the entry
2. Verify slug NOT already in `methodologies.jsonl`
3. Create `skills/faion/knowledge/geek/sdlc-ai/<slug>/`
4. Write `CLAUDE.md` with single line `@AGENTS.md`
5. Write `AGENTS.md` per shape above
6. Create `content/` with 1-3 short XML files using the closed tag vocabulary
7. Create `templates/` only if a real reusable artifact exists
8. Append JSONL row to `.aidocs/sdlc-ai-methodologies/methodologies.jsonl`:
   ```json
   {"id":"S-NNN","slug":"<slug>","category":"<prefix>","source":"<source-stem>","accepted_at":"YYYY-MM-DD","title":"<title>","one_liner":"<summary>","cycle":<N>}
   ```

## After all N slugs done

1. Update `.aidocs/sdlc-ai-methodologies/state.json`: increment `accepted`, set `current_cycle`, bump category counters, update `phase` if threshold crossed
2. Append progress line to `.aidocs/sdlc-ai-methodologies/progress.md`
3. Append to `faion-network/CHANGELOG.md` under `## [Unreleased]`:
   ```
   - sdlc-ai-methodologies: cycle <N> +<M> (<accepted>/52)
   ```
4. Commit:
   ```bash
   git add -A
   git commit -m "sdlc-ai: cycle <N> +<M> (<accepted>/52)"
   ```
   (50-char title, no Co-Authored-By, no emojis)

## Quality gates (REJECT a slug if any fail)

- [ ] Concrete, testable rule
- [ ] Cited source (URL or project path) in `AGENTS.md` or via `<reference href="...">`
- [ ] BOTH `When To Use` AND `When NOT To Use` non-empty
- [ ] Not a near-duplicate (check `methodologies.jsonl`)
- [ ] Maps to exactly one category
- [ ] At least one `content/*.xml` using closed tag vocabulary
- [ ] No `README.md` inside `content/`, `templates/`, or `scripts/`
- [ ] No formatting XML tags

Skip rejected slugs; log rejection in `progress.md`.

## Return

Print to stdout:

```
ACCEPTED: <count>
COMMIT: <SHA>
SLUGS:
  <slug-1>: <category> — <one-liner>
  ...
REJECTED: <count>
  <slug-x>: <reason>
```

## Anti-patterns (forbidden)

- Single 200-line `README.md` — split into `content/`
- `README.md` inside `content/`, `templates/`, or `scripts/`
- Markdown bodies under `content/` — must be semantic XML
- Formatting XML tags (`<bold>`, `<heading>`, `<br>`)
- Empty `templates/` or `scripts/` folder
- 5-file rigid pattern (RETIRED)
- Skipping `When NOT To Use`
- Inline code blocks > 30 lines — move to `templates/`
- Vague non-testable rules
