# recipes/

Workflow recipes: platform-neutral F027 pipelines an agent picks from and `faion workflow build` compiles into a Claude Dynamic Workflow and a Codex chain. The agent chooses the shape; the CLI has no model and must never guess one.

**Card-first rule.** The card is the contract. An agent must be able to pick a recipe and invoke it having read `<name>.card.md` and nothing else — never open `recipe.json` to work out what to pass. Every `{{var:…}}` the recipe declares is documented in the card's Inputs; if the card and the recipe disagree, the card is the bug report.

## Catalog

| Recipe | Tier | Stages | Shape |
|--------|------|--------|-------|
| `sdd-feature/` | free | 6 | intake → plan → bootstrap gate → per-task fan-out over worktrees → review → gated fix. One written feature, built. |
| `research-first-build/` | free | 14 | research plan → three sourced catalogs (one a market landscape) → evidence gate → quantified concept pick → lever gate → design → plan → fan-out → assets → bootstrap gate → review → gated fix. Decides what to build before building it. |
| `article-pipeline/` | free | 6 | outline → per-section fan-out → assemble → gated editorial pass → translate → language review. Content only, never code. |
| `audit-and-fix/` | free | 4 | bootstrap → machine checks → cited review → gated fix. No fan-out; the smallest recipe here. |

Four different stage shapes on purpose: the catalog teaches by contrast, so an agent picking between them is comparing pipelines, not reading four spellings of one.

## Layout

```
INDEX.xml              # L2 index SKILL.md routes into, generated — never hand-edit
recipes/<name>/
├── meta.json          # tier gate for the whole recipe dir
├── recipe.json        # the F027 recipe — what the CLI compiles
└── <name>.card.md     # the contract, six ordered sections, ≤40 lines
```

Schemas: [`recipe-meta`](../../../docs/schemas/recipe-meta.schema.json) · [`recipe`](../../../docs/schemas/recipe.schema.json) · [`card`](../../../docs/schemas/card.schema.json). Regenerate `INDEX.xml` with `scripts/regen-fragment-index.py`.

## Rules

- Card shape, fixed order, nothing added or dropped: `# <name>` · `## Purpose` · `## Invoke` · `## Inputs` · `## Outputs` · `## When NOT to use` · `## Cost`.
- Only `corpus:` fragment references. A shipped recipe that composes a user-space fragment resolves on the author's machine and nowhere else.
- Fragment tier ≤ recipe tier, and `validate-recipes.py` enforces it. Every recipe and every fragment pack ships at tier **free**: the pipeline is the mechanism that makes an agent's output correct, and gating the mechanism does not sell tiers — it makes free-tier output worse. What a tier buys is the content a pipeline consumes.
- A `bootstrap` stage wherever the pipeline runs tests. The g3/g4 pipelines burned fix rounds on a missing venv; an environment is a stage, not an assumption.
- Service identity and paths are vars, never literals — two runs of the same recipe must not collide on a service name, a port or a state directory.
- A research stage composes a research-role fragment, and every one of those includes `corpus:research-source-discipline` — the corpus instructs the fetch, it never substitutes for it. `validate-recipes.py` fails a research-role fragment that drops the block.
- **A stage that produces something declares it.** `produces` on a stage is the contract the emitted workflow checks before marking it ok — `files` (paths, `{{var:NAME}}` and nothing else, because a path derived from an earlier stage's *result* is an assertion the run could argue with), `committed` (those paths must be tracked and unmodified — `deploy-gh.sh` rsyncs a working tree, so an untracked deliverable looks shipped and is absent from every clone), and `item_commit` (fan-out only: each item must leave one sha in `<run>/<stage>/<index>.commit`, counted only if it resolves, is reachable from HEAD, postdates the run baseline, changes a path and is not another item's commit). A stage's own return is not evidence: an agent that wrote nothing still returns a well-formed object, and an executor that refused still returns careful prose.
- A stage fills exactly the slots its fragments declare — every `{{slot:}}` in the prompt, the verifier and the fixer, includes expanded, and nothing beyond them. A stale slot key is invisible at compile time and simply never reaches a prompt.
- Validate before shipping: `python3 scripts/validate-recipes.py` (the three schemas above, card sections and var coverage, fragment resolution, tier monotonicity, slot coverage, the research sourcing block, `INDEX.xml` agreement, and `faion workflow validate` on every recipe).

## Gotchas

- `vfs-pack` ships `.md` and `.xml` only, so the **cards ship in the CLI blob but `recipe.json` does not** — same gap F029 has with `scripts/*.py`. Until the packer's allowlist widens, a recipe body reaches a user through the repo, not the binary.
- The gate verifier contract is `{clean, findings}` — the emitted artifact branches on `verdict.clean`. Any verifier fragment other than `corpus:gate-runner` must return that shape.
- `corpus:gate-runner` and `corpus:gate-fixer` read `{{slot:subject}}` — one file, a directory or a repo, whatever this pipeline gates. A stage whose own prompt also names the thing (`article-pipeline`'s editor) fills both slots from the same var.
- Fan-out only ranges over an earlier stage's JSON array (`stage:<id>.file#<path>`) — there is no fan-out over a var, which is why `research-first-build` runs its three axes as three stages of one fragment.
- Tier comes from `<name>/meta.json`; `scripts/regen-tier-manifest.py` walks it alongside knowledge, playbooks, fragments and tools.
