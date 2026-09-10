---
type: change-request
cr_id: CR-014
title: "62 templates whose body is empty, and the six-line header that hides them from the gate"
priority: P1
created: 2026-09-10
status: proposed
affected_components: [faion-network/skills/faion/knowledge, scripts/validate-methodology-templates.py]
blocks: "publication — 40 of them are advertised in a `## Templates` row a customer follows"
relates_to: ".aidocs/improvements/CR-012-templates-that-fail-when-run.md; .aidocs/improvements/CR-011-rules-that-say-nothing.md"
---

# Change Request: templates that deliver nothing

CR-012 is about templates that fail when run. This is the adjacent class, found while sweeping it:
templates that **cannot** fail, because there is nothing in them.

## The measurement

Every figure reproduces with `scripts/lib/envelope_inline.py`'s header stripper — the same one the
F-077 tooling uses — applied to every file under a `templates/` path segment.

| | |
|---|---|
| Templates whose body is empty or a placeholder line | **62** |
| …**declared** in a `## Templates` row | **40** |
| …not declared anywhere | 22 |
| Median body size after the five-key header comes off | **2 bytes** |
| Files whose **on-disk size** is ≥ 50 bytes | **62 of 62** |

The three groups:

| Group | Count | What is in the file |
|---|--:|---|
| **(a) empty** | **37** | `{}`, or nothing at all after the header. 30 of the 37 are `.json`. |
| **(b) keys, no values** | 1 | `{"entries": []}` |
| **(c) placeholder line only** | **24** | `# Fill per artefact. See AGENTS.md.` · `echo "skeleton — fill per artefact"` · `# Skeleton — replace placeholder values before applying.` · `example_key: example_value` |

## Why the gate passes all 62, and this is the finding

`validate-methodology-templates.py` B3.2 is *"templates are non-empty (heuristic: >50 bytes, not
literal TBD placeholder)"*. It measures **`path.stat().st_size`** — the whole file, header included.
The five-key header is itself 200-300 bytes, so **a template consisting only of a header passes a
non-emptiness check by 4× to 6×.** The check is satisfied by the thing every template has and says
nothing about the thing that varies.

That is the **sixth** green-but-vacuous gate found in this corpus, after the `pipefail` path race,
`validate-recipes.py` counting a failed publish as a pass, the lexicon attestation self-attesting,
`content_id` matching 0 of 2,520, and CR-011's `testable="true"` constant. The pattern named in
CR-011 §0 holds: **this corpus's gates are green in proportion to how little they check.**

## Where they are

Not evenly spread. **34 of the 62 are in `ux/`**, concentrated in three families that read like one
generation run that created files and never filled them:

- `ux/spatial-*` (5 slugs) — `spatial-spec.json`, `panel-spec.json`, `interaction-spec.json`,
  `tool-stack-config.json`, `xr-scene-audit.py`
- `ux/vui-*` and `ux/voice-ui` (6 slugs) — `dialog-spec.json`, `privacy-spec.json`,
  `iot-voice-config.json`, `test-plan.json`, `inclusivity-report.json`, `voice-spec.json`
- `ux/*-a11y` (9 slugs) — `focus-order.json`, `comfort-settings.json`, `ar-anchor-schema.json`, …

The rest are single files in `ml-engineering`, `sdlc-ai`, `infra`, `pm`, `backend`, `security`,
`research`.

Two are worse than empty: `rag-eval-pipeline/templates/report-skeleton.json.header.txt` and
`rag-eval-production-monitoring/templates/query-log-schema.json.header.txt` are **zero-byte files
whose names say they are the header of a JSON file that does not exist beside them**.

## What is NOT in this set, deliberately

A short template is not an empty one, and the line matters because 70 more files are under 80 bytes
of body and are **correct**:

- `sdlc-ai/kb-agents-md-context-pyramid/templates/CLAUDE.md.template` is exactly `@AGENTS.md`. That
  is the complete, correct content of that file — the docs convention says so.
- `ba/*/templates/*.csv` are header rows (`requirement_id,verdict,evidence_url,sample_size,sources`).
  A CSV template *is* its header row.
- `sdlc-ai/lang-ruby-sorbet-strict-floor/templates/sorbet-config` is four real flags.
- `dev/pnpm-package-management/templates/pnpm-workspace.yaml` is three real globs.

So the rule cannot be "under N bytes fails". It has to be "the body is empty, or the body is only a
placeholder", which is what the 62 were selected by.

## Options

1. **Write the 40 declared bodies, delete or declare the 22 undeclared, then tighten B3.2.** The
   only order that leaves the gate honest: tightening first turns 40 slugs red and the baseline
   would have to absorb them, which is the thing `check-validators.sh` exists to prevent.
2. **Tighten B3.2 first and widen the baseline by 40 lines.** Cheap, and it converts a real finding
   into a permanent exception list. This is how the other five vacuous gates got that way.
3. **Delete all 62 and their rows.** Defensible for (a) — a `{}` promises nothing — but it removes a
   `## Templates` row a customer may already have read, and for the `ux/spatial-*` family the row is
   the only place the artefact shape is named at all.
4. **Leave them.** A paying user follows a row to a file containing `{}`.

## Recommendation

**Option 1**, and the sequencing is the whole recommendation: the content first, the gate last. The
40 declared ones are real writing — each needs the artefact shape its methodology's
`02-output-contract.xml` already specifies, which is the good news: **the shape is not a judgement
call, it is derivable from the contract next to it.** `regen-methodology-validators.py` already
generates a validator from that same schema, so a generator is plausible for the `.json` majority
(31 of the 40) rather than 40 hand-authored files.

The 22 undeclared ones are a smaller decision: a template no row names is invisible to a reader
anyway, so deleting them costs nothing a user can observe.

## What this does not settle

- **Whether B3.2 should measure the body or be replaced.** A non-emptiness check that passes on a
  header is not a weak check, it is the wrong check; the alternative is asserting the body against
  the methodology's own output contract, which is a bigger gate and a separate decision.
- **The 70 correct short files.** They prove the byte-count rule cannot be the gate, and no rule
  proposed here distinguishes them from a future stub *except* the placeholder-line test.
