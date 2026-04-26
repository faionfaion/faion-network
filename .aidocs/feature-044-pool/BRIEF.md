# Subagent BRIEF — feature-044 pool

You are a Task subagent dispatched by the parent orchestrator (/faion-poll-agents pool=10) to fill ONE batch slot for feature-044 (geek-tier knowledge content). You work inside a git worktree off `main`. The parent does NOT write methodology files — you do.

## Working directory

Worktree of `faion-network` (relative paths only — never absolute `/home/...` paths leak into main).

## Input

ONE line from `QUEUE.txt`, format `<domain>:<category>:<count>`. Examples:

- `agents:so-:4` — fill 4 slots in agent-methodologies, category `so-`
- `sdlc:lang-:4` — fill 4 slots in sdlc-ai-methodologies, category `lang-`

`<domain>` ∈ `{agents, sdlc}`.

| domain | output dir | state dir |
|--------|-----------|-----------|
| `agents` | `skills/faion/knowledge/geek/ai/ai-agents/<slug>/` | `.aidocs/agent-methodologies/` |
| `sdlc`   | `skills/faion/knowledge/geek/sdlc-ai/<slug>/`        | `.aidocs/sdlc-ai-methodologies/` |

## MANDATORY pre-flight (before ANY file write)

`Read` these in order:

1. `docs/skill-authoring.md` — full structure spec
2. `rules/skill-authoring.md` — non-negotiable shape rules
3. `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml` — closed tag vocabulary for `content/*.xml`
4. `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/methodology-text.xml` — content/*.xml skeleton
5. `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/AGENTS.md` — semantic XML methodology
6. `.aidocs/<state-dir>/methodologies.jsonl` — existing slugs (duplicate guard)
7. `.aidocs/<state-dir>/state.json` — current category counts
8. ALL `.aidocs/<state-dir>/research/*.md` files relevant to your category — pick candidates from here
9. `.aidocs/<state-dir>/candidates.md` (if exists) — additional curated candidates

Skipping these is the #1 cause of rejected batches.

## What "research" means in this BRIEF

The agent does the FULL research-and-write loop:

1. Read all research files for your category.
2. Mine candidates: extract every distinct rule/technique/pattern that fits the category prefix.
3. Cross-check against `methodologies.jsonl` — exclude duplicates and near-duplicates.
4. If research files are thin for the category, do extra discovery: web search for production patterns, scan the user's projects (`/home/nero/workspace/projects/`) for real implementations, extract from Anthropic/OpenAI/Google/MCP docs. Append your findings to `.aidocs/<state-dir>/research/AGENT-99-pool-extension.md` (append-only).
5. Pick the `<count>` strongest candidates that:
   - Have a concrete, testable rule (not "use good practices")
   - Cite at least one source URL OR a real path inside `/home/nero/workspace/projects/`
   - Are clearly distinct from every accepted methodology
   - Map to the specified category prefix
6. Write each as a methodology folder in NEW shape (see below).

## Methodology format (canonical, NEW shape)

```
<slug>/
├── CLAUDE.md          # one line: @AGENTS.md
├── AGENTS.md          # routing doc, Markdown, 50-80 lines (hard cap 120)
├── content/           # semantic XML, one concept per file
│   ├── 01-<topic>.xml
│   └── 02-<topic>.xml  (optional, when warranted)
├── templates/         # OPTIONAL: real reusable artifacts (.py, .json, .txt) — under 80 lines each
└── scripts/           # OPTIONAL: verifier/applier/generator code
```

NO `README.md` inside `content/`, `templates/`, or `scripts/` — every file indexed in the methodology `AGENTS.md`. Empty folders forbidden.

### `AGENTS.md` strict shape

```markdown
# <Methodology Title>

## Summary

<one paragraph: what the rule IS, plain language>

## Why

<one paragraph: what it solves, cite empirical anchor or mechanism>

## When To Use

- <concrete trigger 1>
- <concrete trigger 2>

## When NOT To Use

- <anti-case 1, with one-line reason>
- <anti-case 2, with one-line reason>

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | one-liner |

## Templates

| File | Purpose |
|------|---------|
| `templates/<file>` | one-liner |
```

(Add `## Scripts` table only if `scripts/` exists.)

### `content/*.xml` (semantic XML)

Closed tag vocabulary from `tag-glossary.xml`. Tags describe ROLE, not appearance. NO `<bold>`, `<heading>`, `<br>`. NO Markdown bodies.

Skeleton (use `methodology-text.xml` as starting point):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<text id="01-rule" title="The Rule">
  <summary>One-sentence summary.</summary>

  <section title="Concept name">
    <p>Plain explanation, one or two sentences.</p>

    <rule testable="true">
      <statement>The concrete rule.</statement>
      <rationale>Why this rule exists / empirical anchor.</rationale>
    </rule>

    <example type="good">
      <code lang="python"><![CDATA[
# correct
      ]]></code>
      <note>Why it works.</note>
    </example>

    <example type="bad">
      <code lang="python"><![CDATA[
# incorrect
      ]]></code>
      <note>Why it breaks.</note>
    </example>

    <antipattern>
      <description>Common failure mode.</description>
      <reason>Why it fails.</reason>
    </antipattern>

    <reference path="templates/schema.py">One-line purpose.</reference>
    <reference href="https://...">External source.</reference>
  </section>
</text>
```

Hard caps: `AGENTS.md` ≤120 lines, each `content/*.xml` ≤150, each template ≤80.

## Per-slot procedure (repeat for each of the `<count>` slots)

1. Pick one fresh candidate (from your mined list).
2. Compute slug — lowercase, hyphenated, ≤40 chars, descriptive.
3. Verify slug NOT in `methodologies.jsonl`.
4. Create folder `<output-dir>/<slug>/`.
5. Write `CLAUDE.md` (single line `@AGENTS.md`).
6. Write `AGENTS.md` per shape above.
7. Create `content/` with 1-3 short XML files using the closed tag vocabulary.
8. Create `templates/` ONLY if a real reusable artifact exists. NEVER create empty folder.
9. Append JSONL row to `.aidocs/<state-dir>/methodologies.jsonl`:

```json
{"id":"<X>-NNN","slug":"<slug>","category":"<prefix>","source":"<source-stem>","accepted_at":"YYYY-MM-DD","title":"<title>","one_liner":"<10-25 word summary>","cycle":<current_cycle+1>}
```

(`<X>` = `M` for agents, `S` for sdlc; `NNN` = next sequential)

## After all slots done

1. Update `.aidocs/<state-dir>/state.json`:
   - `accepted += <count>`
   - `current_cycle += 1`
   - `categories[<prefix>].accepted += <count>`
   - `last_tick_at = "YYYY-MM-DD"`
   - update `phase` if threshold crossed

2. Append to `.aidocs/<state-dir>/progress.md`:
   ```
   [YYYY-MM-DD HH:MM] pool-batch <line> — promoted <slug-1>, <slug-2>, ... → <accepted>/<target>
   ```

3. Append to `CHANGELOG.md` under `## [Unreleased]`:
   ```
   - <domain>-methodologies: pool-batch +<count> (<accepted>/<target>)
   ```

4. Stage + commit (50-char title, no Co-Authored-By, no emojis):
   ```bash
   git add -A
   git commit -m "<domain>: pool +<count> <category> (<accepted>/<target>)"
   ```

5. Merge worktree → main with flock to serialize:
   ```bash
   flock /tmp/faion-network-merge.lock bash -c '
     cd /home/nero/workspace/projects/faion-net/faion-network
     git fetch origin main
     git merge --ff-only <worktree-branch> || {
       git pull --rebase origin main
       git push origin main
     }
     git push origin main
   '
   ```

   If merge fails (CHANGELOG conflict): rebase on main, resolve "keep both" for the `## [Unreleased]` section, re-stage, retry.

## Quality gates (REJECT a slot if any fail)

- [ ] Concrete, testable rule (in `AGENTS.md` Summary AND `content/*.xml` `<rule>`)
- [ ] At least one cited source — URL in `AGENTS.md` OR `<reference href="...">` in content
- [ ] BOTH `When To Use` AND `When NOT To Use` non-empty in `AGENTS.md`
- [ ] Slug NOT a near-duplicate of an accepted methodology
- [ ] Maps to exactly one category prefix
- [ ] At least one `content/*.xml` file using ONLY tags from `tag-glossary.xml`
- [ ] No `README.md` inside `content/`, `templates/`, or `scripts/`
- [ ] No formatting tags (`<bold>`, `<heading>`, `<br>`) in any XML
- [ ] No Markdown body inside `content/*.xml`

If a slot fails all attempts: skip it, log rejection in `progress.md`, continue with the rest. Do NOT lower `<count>` — orchestrator picks more next tick.

## Return

Print to stdout for parent to parse:

```
BATCH: <line>
ACCEPTED: <count>
COMMIT: <SHA>
SLUGS:
  <slug-1>: <category> — <one-liner>
  <slug-2>: <category> — <one-liner>
REJECTED: <count>
  <slug-x>: <reason>
```

## Anti-patterns (forbidden)

- Single 200-line `README.md` for a methodology
- `README.md` inside `content/`, `templates/`, or `scripts/`
- Markdown bodies under `content/` (must be semantic XML)
- Formatting XML tags
- Empty `templates/` or `scripts/` folder
- 5-file rigid pattern (RETIRED)
- Skipping `When NOT To Use`
- Inline code blocks > 30 lines (move to `templates/`)
- Vague non-testable rules
- Absolute paths in writes (`/home/...`) — use worktree-relative
- `--no-verify` on commits — fix the hook issue instead

## Hard rule

Every methodology MUST have semantic XML content using the closed tag vocabulary. Every methodology MUST have explicit `When To Use` and `When NOT To Use`. Every methodology MUST cite at least one external source or project path. No exceptions.
