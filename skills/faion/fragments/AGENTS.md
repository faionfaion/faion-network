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
| `research/` | free | `research-source-discipline` (the shared sourcing block), `research-market-analyst`, `research-evidence-table`, `research-desk-brief` |
| `gate/` | free | `gate-commit-discipline` (the shared commit block), `gate-bootstrap`, `gate-runner` (+ schema), `gate-fixer` |
| `sdd/` | free | `sdd-intake-analyzer`, `sdd-planner`, `sdd-task-executor`, `sdd-wave-coordinator`, `sdd-code-reviewer`, `sdd-fix-applier` (+ schemas) |
| `build/` | free | `build-domain-cataloger`, `build-concept-synthesizer` (+ schema), `build-solution-designer`, `build-asset-director` |
| `article/` | free | `article-outliner` (+ schema), `article-section-writer`, `article-assembler`, `article-editor-reviewer`, `article-translator`, `article-language-reviewer` |
| `search/` | free | `search-refine` — the second-pass block `faion search` emits below strong coverage; not a role, so exempt from the role rules |

`INDEX.xml` is the L2 index `SKILL.md` routes into — one entry per pack
plus every `corpus:<name>` beneath it. Generated: never hand-edit, run
`scripts/regen-fragment-index.py`.

## Shape

- Static text first, `{{slot:…}}` last under an `Inputs:` heading. `≤80`
  lines, English, one role per file.
- Every **role** fragment — one opening `You are a|an|the <role>.` — states
  its hard boundary in that paragraph: what it writes and what it must
  never touch. A shared include block or an emitted block is exempt from
  both this and the `Inputs:` rule.
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
pack no fragment here required a URL, an access date, a confidence tag or a
source floor — the prompts asked for less than an unprompted agent does.

## The commit rule (every role that writes a file)

A deliverable git has never seen does not survive a clone, and
`deploy-gh.sh` rsyncs a working tree — so it ships anyway. Two pipeline
runs ended with **23 and 9 untracked deliverables**; both reported success.
So **every fragment whose output contract names a file it writes includes
`{{include:corpus:gate-commit-discipline}}`** — exactly `git add` and
`git commit`, exactly the paths that contract names, never `git add -A`,
never `--no-verify`, never a push. Those roles' boundaries no longer forbid
git outright: a role cannot be told both to commit and never to run git.
The block sits in `gate/` (cross-pack, and a gate on delivery) and, like
`research-source-discipline`, declares no slots and carries no role line.
The other half is the stage's `produces` contract, which the emitted
workflow reads back with `git ls-files` and `git status` — see
[`recipes/AGENTS.md`](../recipes/AGENTS.md). The corpus asks; the artifact
verifies.

## Validation

`python3 scripts/validate-fragments.py` (validator 9) holds the rules above:
`meta.json` against [`fragment-pack-meta.schema.json`](../../../docs/schemas/fragment-pack-meta.schema.json),
flat name uniqueness, include resolution, schema pairing, the line cap,
role-fragment shape, the names-a-tool tier direction, `INDEX.xml` agreement.
Recipe-side rules — fragment tier ≤ recipe tier, slot coverage, the sourcing
gate — are in `scripts/validate-recipes.py`.

## Gotchas

- Instruction plus tool, never instruction alone: `research-evidence-table`
  names `source-table` (`tools/research/`), which exits 1 when a
  load-bearing claim is unsourced. That tool pack moved to **free** with
  this one — a free fragment naming a solo tool is uninvokable, and
  `validate-fragments.py` fails it.
- Fragment tier ≤ recipe tier. Every pack here is **free**, as is every
  recipe: this layer is the mechanism that makes an agent's output
  correct, and a paid mechanism only degrades the free tier. Paid content
  is what a pipeline consumes.
- A bare reference resolves against the **user** space first; recipes must
  always write `corpus:`.
- `research-source-discipline` declares no slots on purpose — give it one
  and every stage that includes it has to fill it.
