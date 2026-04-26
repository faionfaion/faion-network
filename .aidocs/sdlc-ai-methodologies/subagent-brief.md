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

## Methodology format (canonical)

**Source of truth:** `docs/skill-authoring.md`. Output path:

```
skills/faion/knowledge/geek/sdlc-ai/<slug>/
├── CLAUDE.md          # @AGENTS.md
├── AGENTS.md          # routing, <80 lines
├── texts/
│   ├── README.md
│   ├── 01-<topic>.md
│   └── ...
└── templates/
    ├── README.md
    └── <real-file>
```

`scripts/` optional. Empty folders forbidden.

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

## Texts

| File | What's inside |
|------|---------------|
| `texts/01-foo.md` | one-liner |

## Templates / Scripts

- `templates/<file>` — short purpose
```

Hard caps: `AGENTS.md` ≤ 120 lines, each text ≤ 150, each template ≤ 80.

## Per-slug procedure

For each slug:

1. Read `sources[slug]` — locate the entry
2. Verify slug NOT already in `methodologies.jsonl`
3. Create `skills/faion/knowledge/geek/sdlc-ai/<slug>/`
4. Write `CLAUDE.md` with single line `@AGENTS.md`
5. Write `AGENTS.md` per shape above
6. Create `texts/` (`README.md` index + 1-3 short text files)
7. Create `templates/` (`README.md` index + ≥1 reusable artifact)
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
- [ ] Cited source (URL or project path)
- [ ] BOTH `When To Use` AND `When NOT To Use` non-empty
- [ ] Not a near-duplicate (check `methodologies.jsonl`)
- [ ] Maps to exactly one category
- [ ] At least one reusable file in `templates/`

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

- Single 200-line README — split into `texts/`
- Empty `templates/` or `scripts/` folder
- 5-file rigid pattern (RETIRED)
- Skipping `When NOT To Use`
- Inline code blocks > 30 lines — move to `templates/`
- Vague non-testable rules
