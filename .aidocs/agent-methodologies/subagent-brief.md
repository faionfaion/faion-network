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

## Methodology format (canonical)

**Source of truth:** `docs/skill-authoring.md`. Read it before writing if you have not. Summary:

```
skills/faion/knowledge/geek/ai/ai-agents/<slug>/
├── CLAUDE.md          # one line: @AGENTS.md
├── AGENTS.md          # routing doc, <80 lines, strict shape
├── texts/
│   ├── README.md      # one-line index per text file
│   ├── 01-<topic>.md  # 30-80 lines, one concept per file
│   └── ...            # add more only if value is real
└── templates/
    ├── README.md      # one-line index per template
    └── <real-file>    # at least one reusable artifact (under 60 lines)
```

`scripts/` is OPTIONAL — include only when a verifier/applier/generator carries real value. Do NOT create empty folders.

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

## Texts

| File | What's inside |
|------|---------------|
| `texts/01-foo.md` | one-liner |
| `texts/02-bar.md` | one-liner |

## Templates / Scripts

- `templates/<file>` — short purpose
```

Hard caps (`docs/skill-authoring.md` § "Token budget"):
- `AGENTS.md` ≤ 120 lines (target 50-80)
- Each text ≤ 150 lines (target 30-80)
- Each template ≤ 80 lines (target 20-50)

## Per-slug procedure

For each slug in `slugs`:

1. Read `sources[slug]` — find the entry matching the slug
2. Verify the slug is NOT already in `methodologies.jsonl` (duplicate guard)
3. Create `skills/faion/knowledge/geek/ai/ai-agents/<slug>/`
4. Write `CLAUDE.md` containing the single line: `@AGENTS.md`
5. Write `AGENTS.md` per the strict shape above
6. Create `texts/`:
   - `texts/README.md` with one-line index
   - 1-3 short text files (`01-*.md`, `02-*.md`) covering the rule deeply
7. Create `templates/`:
   - `templates/README.md` with one-line index
   - At least one real reusable file (Python schema / JSON / prompt template / config snippet)
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
- [ ] Cited source (URL or project path) in `AGENTS.md` references or in a text
- [ ] BOTH `When To Use` AND `When NOT To Use` non-empty
- [ ] Not a near-duplicate of an accepted methodology (search `methodologies.jsonl`)
- [ ] Maps to exactly one category prefix
- [ ] At least one reusable file in `templates/`

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

- Single 200-line README — split into `texts/`
- Empty `templates/` or `scripts/` — omit folder
- 5-file rigid pattern (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) — RETIRED
- Skip `When NOT To Use` — agent cannot reject the methodology safely
- Inline templates as fenced code blocks longer than ~30 lines — move to `templates/`
- Vague rules — every methodology must be testable
