# Catalog Build Plan (CSV-first)

Goal: produce a reusable catalog of every domain (100) and methodology (1279) in `skills/faion/knowledge/`, stored in CSV (re-usable across renders), with a template-driven generator that emits the final tree-structured catalog page for faion.net.

## Output artifacts

| Artifact | Purpose |
|----------|---------|
| `.aidocs/catalog/data/domains.csv` | 100 rows: tier, group, domain, description (1-2 paragraphs) |
| `.aidocs/catalog/data/methodologies.csv` | 1279 rows: tier, group, domain, methodology, description (1 paragraph) |
| `.aidocs/catalog/templates/methodology.j2` | Jinja2 prompt template for the agent (description generator) |
| `.aidocs/catalog/templates/domain.j2` | Jinja2 prompt template for domain blurbs |
| `.aidocs/catalog/templates/catalog.md.j2` | Jinja2 render template (CSV → markdown tree) |
| `.aidocs/catalog/scripts/render.py` | Renderer: reads both CSVs + render template → `docs/catalog.md` |
| `.aidocs/catalog/scripts/run-batch.py` | Batch driver: picks next 50 unfilled rows, spawns agent, appends descriptions to CSV |
| `docs/catalog.md` | Final tree-structured page (re-generated any time from CSV) |

**Why CSV first:**
- One-time generation, infinite re-renders (markdown, JSON for site, RSS, etc.)
- Cheap diff: a new methodology = one new row, not full rebuild
- Site (faion.net) consumes CSV directly via `gatsby-source-csv` or `papaparse`

## CSV schemas

### `domains.csv`
```
tier,group,domain,skill_path,description
free,dev,python-developer,skills/faion/knowledge/free/dev/python-developer,"Python development specializing in..."
```

### `methodologies.csv`
```
tier,group,domain,methodology,readme_path,description
free,dev,python-developer,django-models,skills/.../django-models/README.md,"Django models are the data foundation..."
```

Empty `description` field = unprocessed. Agent fills it in. Idempotent re-runs skip filled rows.

## Templates

### Generator templates (agent prompts)

`templates/methodology.j2` — used by batch driver to format the prompt sent to the agent:

```jinja
You are filling description fields in methodologies.csv for the faion-network catalog.

For each row below, read the README.md and write ONE paragraph (3-5 sentences, English) that answers:
- What problem this methodology solves
- When to apply it
- The practical outcome / value delivered

Plain language. No marketing. No code blocks.

Rows to process ({{ batch_size }}):
{% for r in rows %}
{{ loop.index }}. tier={{ r.tier }} group={{ r.group }} domain={{ r.domain }} methodology={{ r.methodology }}
   readme: {{ r.readme_path }}
{% endfor %}

Return JSON only, mapping "tier|group|domain|methodology" → description string:
{
  "free|dev|python-developer|django-models": "...",
  ...
}
```

`templates/domain.j2` — same shape but reads SKILL.md, returns 1-2 paragraph blurb.

### Render template

`templates/catalog.md.j2`:

```jinja
# Faion Network Catalog

{{ methodology_count }} methodologies across {{ domain_count }} domain skills, organized by pricing tier.

{% for tier in tiers %}
## {{ tier.name | title }} ({{ tier.domain_count }} domains, {{ tier.method_count }} methodologies)

{% for d in tier.domains %}
### {{ d.domain }}

{{ d.description }}

{% for m in d.methodologies %}
- **{{ m.methodology }}** — {{ m.description }}
{% endfor %}

{% endfor %}
{% endfor %}
```

## Scripts (all under `scripts/catalog.py`)

Single CLI with subcommands. Main thread (Claude session) orchestrates; scripts only handle CSV I/O.

| Subcommand | Purpose |
|------------|---------|
| `init` | One-shot: walk filesystem → empty `domains.csv` + `methodologies.csv` |
| `status` | Print `phase=X done=Y/Z` (or `DONE`) |
| `pick` | Pick next 50 unfilled rows → emit JSON to stdout (consumed by main thread to build subagent prompt) |
| `update <json>` | Read JSON `{key: description}` → patch CSV in-place |
| `render` | CSV → `docs/catalog.md` + `docs/catalog.json` |

No `run-batch.py`. Orchestration lives in the main thread (model), not in Python.

## State tracking

CSV itself is the state — rows with empty `description` are "todo". No separate state.json. `catalog.py status` computes progress from CSV.

## Phases

| Phase | Iterations | Per-batch | Total agents |
|-------|------------|-----------|--------------|
| 1. Domains | 2 | 50 | 2 |
| 2. Methodologies | 26 | 50 | 26 |
| 3. Render | 1 (manual or auto) | — | 0 |
| **Total agents** | | | **28** |

## Loop wiring (main thread = controller)

`/loop` runs in dynamic (self-paced) mode. The main thread (Claude session) is the orchestrator — each tick it:

1. `python .aidocs/catalog/scripts/catalog.py status` → if `DONE`, do not ScheduleWakeup, exit.
2. `python .aidocs/catalog/scripts/catalog.py pick > /tmp/catalog-batch.json` (50 unfilled rows + phase metadata)
3. Spawn ONE `general-purpose` subagent (foreground) with prompt:
   > Read /tmp/catalog-batch.json. For each row, read the listed README/SKILL file. Generate one paragraph per row (3-5 sentences, English, plain language, practical: problem / when / value). Return JSON `{"<key>": "<description>", …}` to /tmp/catalog-result.json. Report "OK N/N".
4. `python .aidocs/catalog/scripts/catalog.py update /tmp/catalog-result.json` → patches CSV in place.
5. Print one-line status from `catalog.py status`.
6. `ScheduleWakeup` (60s, same /loop prompt) if work remains; else stop.

Main thread sees every status line, every agent failure, can intervene at any tick (e.g. fix a row, abort the loop, retry). Scripts never spawn agents — only main thread does.

### `/loop` invocation

```
/loop  Run one catalog batch. Steps in .aidocs/catalog/PLAN.md → "Loop wiring".
       Working dir: /home/nero/workspace/projects/faion-net/faion-network
```

Dynamic mode (no interval). Main thread paces with ScheduleWakeup ~60s between batches.

## Cost

- Per methodology batch: 50 × ~5KB README = 250KB read + ~10KB JSON out ≈ 80k tokens
- Phase 2 total: ~26 × 80k ≈ 2.0M tokens
- Phase 1 total: 2 × 80k = 160k tokens
- Render phase: negligible (no LLM)
- **Total:** ~2.2M tokens, ~28 agent runs

## Acceptance

- `domains.csv` — 100 rows, all `description` non-empty
- `methodologies.csv` — 1279 rows, all `description` non-empty
- `docs/catalog.md` regenerates deterministically from CSVs (run `render.py` twice → byte-identical output)
- Spot-check 5 random methodologies: descriptions are practical, not generic
- Site (faion.net) can later import either CSV directly without re-indexing the file tree

## Re-use guarantee

CSV is canonical. Future site work:
- Load `methodologies.csv` in Gatsby via `gatsby-source-csv`
- Filter/group at build time
- Generate landing pages per domain, per methodology, search index
- No need to re-walk the knowledge tree
