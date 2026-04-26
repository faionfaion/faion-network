# Subagent Brief — Agent-Methodologies Tick

You are a Task subagent. The orchestrator (main thread) has selected N=3-5 candidate methodology slugs to promote in this tick. Your job: write the methodology folders + update state + commit. The orchestrator will verify and schedule the next tick.

## Working directory

`/home/nero/workspace/projects/faion-net/faion-network`

(Repo root for `faion-network`. `git` operates here.)

## Inputs (filled by orchestrator)

| Variable | Meaning |
|----------|---------|
| `slugs` | List of N slugs to write this tick |
| `sources` | Map `slug → relative path under .aidocs/agent-methodologies/research/` |
| `categories` | Map `slug → category prefix` (one of `so- mm- tu- pl- lp- mem- cli- eval- cost- mcp-`) |
| `cycle` | Current cycle number (post-increment after write) |

## MANDATORY pre-flight (before ANY file write)

Before creating or editing a single methodology file, you MUST `Read`:

1. `docs/skill-authoring.md` — full structure spec (folder shape, `AGENTS.md` strict shape, anti-patterns)
2. `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml` — closed tag vocabulary for `content/*.xml`

Skipping these is the #1 cause of rejected ticks. The conventions are non-obvious (semantic XML, no `README.md` inside subfolders, role-bearing tag names) and cannot be inferred from existing 5-file methodologies.

## Methodology format (canonical)

**Source of truth:** `docs/skill-authoring.md` (which you just read).

```
skills/faion/knowledge/geek/ai/ai-agents/<slug>/
├── CLAUDE.md          # one line: @AGENTS.md
├── AGENTS.md          # routing doc, Markdown, <80 lines, strict shape
├── content/           # semantic XML, one concept per file
│   ├── 01-<topic>.xml
│   └── 02-<topic>.xml
└── templates/         # OPTIONAL: real reusable artifacts (Pydantic, JSON, prompt, etc.)
    └── <name>.<ext>
```

`scripts/` is also OPTIONAL — include only when a verifier/applier/generator carries real value. **NO `README.md` inside `content/`, `templates/`, or `scripts/`** — every subfolder file is indexed in the methodology `AGENTS.md` (single source of truth). Empty folders are forbidden — omit them.

### `AGENTS.md` strict shape

```markdown
# <Title>

## Summary

<one paragraph: what the rule IS, plain language>

## Why

<one paragraph: what it solves, cite the empirical anchor or mechanism>

## When To Use

- <concrete trigger 1>
- <concrete trigger 2>

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
| `templates/<file>` | one-liner |
```

(Add `## Scripts` table only if `scripts/` exists.)

Hard caps (`docs/skill-authoring.md` § "Token budget"):
- `AGENTS.md` ≤ 120 lines (target 50-80)
- Each `content/*.xml` ≤ 150 lines (target 30-80)
- Each template ≤ 80 lines (target 20-50)

### Semantic XML for `content/`

Closed tag vocabulary (from `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`). Tags describe ROLE, not appearance. Skeleton:

```xml
<text id="01-rule" title="The Rule">
  <summary>One-sentence summary.</summary>

  <rule>State the testable rule here.</rule>

  <example>
    <code lang="python"><![CDATA[
def example(): ...
    ]]></code>
  </example>

  <antipattern>
    <code lang="python"><![CDATA[
def bad_example(): ...
    ]]></code>
    <why>Explain why this fails.</why>
  </antipattern>

  <reference path="templates/schema.py">Pydantic shape used by this rule</reference>
  <reference href="https://...">External source</reference>
</text>
```

NO formatting tags (`<bold>`, `<heading>`, `<br>`). NO Markdown bodies under `content/`.

## Per-slug procedure

For each slug in `slugs`:

1. Read `sources[slug]` — find the entry matching the slug
2. Verify the slug is NOT already in `methodologies.jsonl` (duplicate guard)
3. Create `skills/faion/knowledge/geek/ai/ai-agents/<slug>/`
4. Write `CLAUDE.md` containing the single line: `@AGENTS.md`
5. Write `AGENTS.md` per the strict shape above
6. Create `content/`:
   - 1-3 short XML files (`01-*.xml`, `02-*.xml`) covering the rule deeply
   - Each file uses the closed tag vocabulary from the tag glossary
7. Create `templates/` only if a real reusable artifact exists (Python schema, JSON, prompt, config snippet)
8. Append a JSONL row to `.aidocs/agent-methodologies/methodologies.jsonl`:
   ```json
   {"id":"M-NNN","slug":"<slug>","category":"<prefix>","source":"<source-file-stem>","accepted_at":"YYYY-MM-DD","title":"<title>","one_liner":"<10-25 word summary>","cycle":<N>}
   ```
   (`id` = next sequential M-NNN)

## After all N slugs done

1. Update `.aidocs/agent-methodologies/state.json`:
   - `accepted += N`
   - `current_cycle = <cycle>`
   - `categories[<prefix>].accepted += 1` for each promoted slug
   - `last_tick_at = "YYYY-MM-DD"`
   - update `phase` if threshold crossed (see loop-prompt phases table)
2. Append a single line to `.aidocs/agent-methodologies/progress.md`:
   ```
   [YYYY-MM-DD HH:MM] cycle=<N> promoted <N> — <slug-1> (<cat>), <slug-2> (<cat>), ... → <accepted>/50
   ```
3. Append to `faion-network/CHANGELOG.md` under `## [Unreleased]`:
   ```
   - agent-methodologies: cycle <N> +<N> (<accepted>/50)
   ```
4. Commit:
   ```bash
   git add -A
   git commit -m "agents: cycle <N> +<M> (<accepted>/50)"
   ```
   (50-char title, no `Co-Authored-By`, no emojis — repo `AGENTS.md` rule)

## Quality gates (REJECT a slug if any fail)

- [ ] Concrete, testable rule (not "use good practices")
- [ ] Cited source (URL or project path) inside `AGENTS.md` or in a content file via `<reference href="...">`
- [ ] BOTH `When To Use` AND `When NOT To Use` non-empty
- [ ] Not a near-duplicate of an accepted methodology (search `methodologies.jsonl`)
- [ ] Maps to exactly one category prefix
- [ ] At least one `content/*.xml` file using the closed tag vocabulary
- [ ] No `README.md` inside `content/`, `templates/`, or `scripts/`
- [ ] No formatting tags (`<bold>`, `<heading>`, `<br>`) inside XML

If a slug fails: skip it, log the rejection in `progress.md`, continue with the rest. Do NOT lower N — orchestrator picks more next tick.

## Return

Print to stdout for orchestrator to parse:

```
ACCEPTED: <count>
COMMIT: <SHA>
SLUGS:
  <slug-1>: <category> — <one-liner>
  <slug-2>: <category> — <one-liner>
  ...
REJECTED: <count>
  <slug-x>: <reason>
```

## Anti-patterns (do NOT do)

- Single 200-line `README.md` — split into `content/`
- `README.md` inside `content/`, `templates/`, or `scripts/` — forbidden
- Markdown bodies under `content/` — must be semantic XML
- Formatting tags in XML (`<bold>`, `<heading>`, `<br>`) — describe role, not appearance
- Empty `templates/` or `scripts/` folder — omit
- 5-file rigid pattern (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) — RETIRED
- Skip `When NOT To Use` — agent cannot reject the methodology safely
- Inline templates as fenced code blocks longer than ~30 lines — move to `templates/`
- Vague rules — every methodology must be testable
