# fragments/

Role prompts the CLI composes into pipelines. One `meta.json` per pack
directory gates every fragment beneath it; recipes address them as
`corpus:<name>` and the name is the **file basename, flat across the whole
tree** — so `build/` and `research/` may not both ship a `market-analyst`,
and a per-pack `AGENTS.md` would make `corpus:AGENTS` ambiguous. That is
why this file sits here and not inside each pack.

## Packs

| Pack | Tier | Roles |
|------|------|-------|
| `research/` | solo | `research-source-discipline` (the shared sourcing block), `research-market-analyst`, `research-evidence-table`, `research-desk-brief` |
| `gate/` | solo | `gate-bootstrap`, `gate-runner` (+ schema), `gate-fixer` |
| `sdd/` | solo | `sdd-intake-analyzer`, `sdd-planner`, `sdd-task-executor`, `sdd-wave-coordinator`, `sdd-code-reviewer`, `sdd-fix-applier` (+ schemas) |
| `build/` | pro | `build-domain-cataloger`, `build-concept-synthesizer` (+ schema), `build-solution-designer`, `build-asset-director` |
| `article/` | pro | `article-outliner` (+ schema), `article-section-writer`, `article-assembler`, `article-editor-reviewer`, `article-translator`, `article-language-reviewer` |

## Shape

- Static text first, `{{slot:…}}` last under an `Inputs:` heading. `≤80`
  lines, English, one role per file.
- Every fragment states its hard boundary in its opening paragraph — what
  it writes and what it must never touch.
- A fragment returning structured output ships a paired
  `<name>.schema.md`; the recipe names it in `output.schema`.
- `{{include:<ref>}}` composes shared blocks at build time. `faion frag
  get` prints a body **raw**, so a resolving reference is not proof the
  included block reached the prompt.

## The sourcing rule (research roles)

**faion never goes to the internet — the calling agent does.** The corpus
carries the durable half (what to source, what makes a claim load-bearing,
how to tag confidence, what a finished evidence artifact looks like); URLs,
figures and dates are fetched live, because they rot.

So: **every research-role fragment includes
`{{include:corpus:research-source-discipline}}`**, and that block keeps its
four anchors — URL plus access date, the H/M/L definitions, the "no
reliable public figure found" path, and `faion fact add` provenance.
`scripts/validate-recipes.py` asserts both: a fragment whose opening role
line names a researcher, analyst, market, competitor or evidence role and
omits the include is a failure, not a style note.

Measured 2026-08-11, one brief, blind judges: the pipeline run produced
**14 competitors and 0 source URLs**; a plain agent that went to the web
produced **31 and 108**, and won on research depth. Before the `research/`
pack, no fragment here required a URL, an access date, a confidence tag or
a source floor, and none named a web tool — the prompts asked for less than
an unprompted agent does by default.

## Gotchas

- Instruction plus tool, never instruction alone: `research-evidence-table`
  names `source-table` (`tools/research/`, tier solo), which exits 1 when a
  load-bearing claim is unsourced. The research pack is tier **solo** for
  exactly that reason — a free fragment naming a solo tool is uninvokable.
- Fragment tier ≤ recipe tier. `research/` and `gate/` are solo so solo
  recipes can compose them.
- A bare reference resolves against the **user** space first; recipes must
  always write `corpus:`.
- `research-source-discipline` declares no slots on purpose — give it one
  and every stage that includes it has to fill it.
