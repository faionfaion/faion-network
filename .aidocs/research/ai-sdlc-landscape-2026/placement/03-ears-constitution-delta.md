# Placement — EARS, constitution.md, spec-delta
**Slice:** three tool-independent patterns · **Author pass:** 3 of 10 · **Date:** 2026-08-04

## Verdict summary

| Pattern | Placement decision | Target path | Tier |
|---|---|---|---|
| EARS notation | New methodology; grammar as data; linter in Go | `knowledge/sdd/ears-requirements/` + `faion-cli/internal/earslint/` | **free** |
| EARS × FR-NNN | Amend in place, no new slug | `sdd/spec-requirements/content/{01-core-rules,02-output-contract}.xml` | unchanged (solo) |
| `constitution.md` | New methodology + one playbook + bootstrap wiring | `sdd/constitution-md/`, `playbooks/govern-decide/write-the-project-constitution/` | **free** |
| spec-delta | New methodology, cross-linked both ways | `sdd/spec-delta-format/` | **solo** |
| all three | Workflow wiring — no new workflow | `workflows/{sdd-batch-orchestrator,idea-to-prod}/` | n/a |

## Workflow changes

**W1** · `sdd-batch-orchestrator/content/07-verify-review-fix-loop.xml` §Verify matrix — add *"SDD artefacts, every surface: `faion lint requirements <feature>/spec.md`; warnings-only, `--strict` only after tuning."* Replaces nothing; there is no artefact check today.

**W2** · same file §Reviewer verdict shape — add *"every FAIL blocker cites a `spec.md` line or a `constitution.md` rule id (`R-NN`); a blocker citing neither is a nit."* The Compliance section made operational.

**W3** · `content/02-phases.xml` Phase 3 PLAN — append *"FR statements follow `sdd/ears-requirements`; where `user-flows.md` exists the planner **generates** them from it (happy → `When`, negative → `If … then`, precondition → `While`)."* Generation, not detection, fixes the `if`/`when` trap.

**W4** · `sdd-batch-orchestrator/AGENTS.md` `success_criteria` — add *"Every FR parses as an EARS pattern or carries `ears_pattern: n-a` with a reason."* Bump 2.0.0→2.1.0, `last_verified`→2026-08-04, mirror into `catalog.json`.

**W5** · `idea-to-prod/content/10-bootstrap.xml` §Directory layout — add `constitution.md` to `.product/` + *"after Phase 2 locks decisions the orchestrator writes it (≤20 rules, one-sentence why each); Phases 3-6 read it. `decisions.md` stays append-only history; the constitution is the standing set — a stale rule is amended, not appended."*

**W6** · `idea-to-prod/content/20-phases.xml` Phase 3 — "SDD quartet: spec.md, design.md, test-plan.md, implementation-plan.md" is stale against our own doc set. Replace with `spec.md`, `plan.md`, conditional `user-flows.md`/`ui-ux-design.md`, `TASK_*.md`, `readiness.md`; add *"`spec.md` is delta-only per `sdd/spec-delta-format`."* Bump 1.0.0→1.1.0 + catalog.json.

## New content proposed

Shape = the `context-graph-engineering` reference: `AGENTS.md` + `CLAUDE.md` + 14-key `meta.json` + `content/01-core-rules · 02-output-contract · 03-failure-modes · 04-procedure · 05-examples · 06-decision-tree` + `scripts/validate-<slug>.py` (`--self-test`, exit 0/1/2) + templates valid against their own contract.

**N1 · `sdd/ears-requirements`, `free`.** Produces: five patterns verbatim; the derived order `Where ≺ While ≺ When ≺ If/Then` with evidence; the E/W rule table, one citation per rule; ten rewrites; refusal routing (goal → `roadmap.md`, invariant → `project-spec/`, quality attribute → rewrite or drop). Plus `templates/{ears-rules.json,ears-fixtures.tsv,mavin-guide-mirror.md}`.
Checked, none defines a sentence grammar: `ba/{requirements-documentation,requirement-quality-scorecard,ba-requirements-mgmt,data-driven-requirements,ai-assisted-requirements-elicitation}`, `sdd/{spec-requirements,user-flows-template}`. One live EARS mention exists and it is hostile — `ba/requirement-quality-scorecard/AGENTS.md:27` lists *"a different formal quality model (e.g. EARS-only) already in use"* as a **Skip If**; amend to *"EARS-only, with no requirement ids or verification methods"*, else adopting EARS tells the user to skip the scorecard.
`free`: the linter emits codes (`E005`, `W107`) and paywalling an error message's explanation makes the free binary unusable. Also the upsell surface into the solo `sdd` cluster.

**Linter ships both ways, one source of truth.** `templates/ears-rules.json` (code, severity, pattern, rationale, citation) + `templates/ears-fixtures.tsv` (line → expected pattern → expected codes) **are** the grammar spec and live in the methodology. `scripts/validate-ears-requirements.py` is dev-time only: replays fixtures, asserts every PASS line in `05-examples.xml` passes and every FAIL line emits exactly its declared codes. Runtime is Go — `faion-cli/internal/earslint/` (stdlib `regexp`/`strings`/`unicode`, RE2-safe; normalize → last-match head-marker split → classify+lint), wired via `internal/cli/lint.go` + `root.go` as `faion lint requirements <path>… [--strict] [--lenient] [--json] [--fix]`. Rules embed by `go:embed` from a `make`-generated copy with a CI byte-identity check; both implementations must pass the fixtures. No runtime Python. Read `labeth/ears-lint-go` (MIT) first.

**N2 · `sdd/constitution-md`, `free`.** Produces: the durable/cross-cutting/contestable/checkable test; the ≤20-rule cap as the enabling constraint for always-loading; a one-sentence why per rule obtained *before* the rule; stable `R-NN` ids; a Compliance statement; semver + ratified/amended dates + Sync Impact Report as an HTML comment; `TODO(<FIELD>)`; the `project-spec/` delegation pointer — the one place we beat Spec Kit and Agent OS. Ships an empty `templates/constitution.md` (examples in comments, never pre-filled opinions) and `scripts/validate-constitution.py` (rule count, word cap, why present, footer parses, sections present, no `[PLACEHOLDER]`) — structural only; `03-failure-modes.xml` states semantic enforcement is impossible. Checked: `constitution` appears in 174 live files as a concept and in **zero** slugs; `sdlc-ai/task-spec-kit-three-step` demands a Constitution Gate and never defines one. Cross-link `sdd/{architecture-decision-records,client-conventions-as-code,quality-gates-confidence}`, `sdlc-ai/ai-convention-anchoring`.

**N2b · `playbooks/govern-decide/write-the-project-constitution`, `free`** — the goal-shaped entry a non-technical owner searches for. `meta.json` `domain: govern-decide` + `content/01-playbook.xml`; stages elicit ("what have you had to explain twice?") → draft → cap → ratify → amend; methodology ref `sdd/constitution-md`.

**N3 · `sdd/spec-delta-format`, `solo`.** Produces: four verbs incl. RENAMED; merge order `RENAMED → REMOVED → CHANGED → ADDED`; verify-then-move archive ordering; the scenario-loss check; the single-file template (baseline by *reference* + git ref, `## Out of Scope`, ids inside operation blocks). `solo` because it is inert without `sdd/project-spec-structure` (solo) — a free entry pointing at a gated prerequisite is a broken promise. Checked: only `sdlc-ai/task-spec-kit-three-step` and `dev/spec-driven-debugging` come close. Two live anchors get a `<reference>` back: `project-spec-structure/content/03-delta-update.xml` (mandates a same-PR delta, never defines one) and `readiness-checklist/content/01-checklist.xml` rule `i8-spec-delta`.

**Registration, each item.** (1) 14-key `meta.json` (`content_id` 16 hex, `complexity`, `produces`, `est_tokens`, `tags`). (2) `regen-tier-manifest.py` — **it hard-codes `TODAY="2026-05-23"` and `NEW_VERSION=8`; patch both or it stamps a stale `last_synced`.** (3) **Hand-add** to `sdd/INDEX.xml` as `<methodology slug tier path><summary>` at its **C-locale** position (`spec-advanced-guidelines` < `spec-delta-format` < `spec-requirements`) and bump `count`. (4) `validate-methodology-{v2,xml,scripts,templates}.py`; playbook → `validate-playbook-v3.py` + `validate-playbook-taxonomy.py`. (5) `regen-domains-xml.py` for `<domain id="sdd" count>` + `total_methodologies`. (6) `audit-index-coverage.py` to prove no orphan. (7) CHANGELOG under `## [Unreleased]`. (8) Workflows → `validate-workflow-v2.py` + `catalog.json`. **Never run `build-domain-index-v2.py`.**

## EARS × spec-requirements composition rule

**EARS composes; it neither replaces nor competes. `spec-requirements` owns identity and metadata; EARS owns exactly one field — the statement sentence.**

1. Every requirement keeps its `FR-NNN`/`NFR-NNN` id, `priority`, `verification_method` and traceability, unchanged.
2. The sentence after the id MUST parse as one of the five patterns (or Complex) for **every `FR-NNN`**. No exceptions.
3. For **`NFR-NNN`** it MUST parse where the requirement is a system response to a condition; where it is not (architectural constraints, quality attributes) it carries `ears_pattern: n-a` + a one-line reason — explicit and recorded, never silent.
4. Never an EARS sentence without an `FR-NNN`; never an `FR-NNN` without a parsing statement or a recorded `n-a`.
5. `r5-no-vague-language` (`fast, easy, simple, robust, scalable`) is superseded by W103/W104/W108/W112, a strict superset with a citation per token. Delete the inline list; point at `ears-rules.json`.
6. `verification_method` is *suggested* from `ears_pattern` (event → integration · state → state-machine · unwanted → negative · ubiquitous → property/monitor · optional-feature → flag matrix). Never auto-filled.
7. Edits: `01-core-rules.xml` gains `r7-ears-conformance` + rewritten `r5`; `02-output-contract.xml` gains `ears_pattern`, `ears_violations[]`, forbidden pattern `f5` (*any FR failing classification in a final artefact*), and an item schema for `requirements` (it has none). Bump `version` + `last_reviewed`.

Agreeing with the dossier, tightened once: it calls EARS "advisory for NFR". Advisory is unmeasurable — recording the opt-out as a value is what separates *not applicable* from *not done*.

## Non-technical usability answer

`shall` is a real barrier and the cheapest available: the one token marking an obligation, never accidental in ordinary English, and the anchor the parser hangs on. `must` collides with prose, `will` with future tense, `should` is non-binding, `does` is description — removing `shall` deletes the parse anchor rather than simplifying anything.

Resolution: **keep `shall` as the stored form and never require a human to type it.** `user-flows.md` is already written by non-technical people and is structurally EARS minus keywords; three plain questions (what must be true first / what sets this off / what does the app do) drive generation and the founder confirms the generated sentence. Reading `shall` is not a barrier; writing it is. Lenient input normalises gofmt-style (`must`/`will`/`has to` → `shall`, info-level, `--fix`); Kiro's comma-less ALL-CAPS accepted under `--lenient`, never canonicalised. **Never reject a founder's sentence over a modal verb.** Beyond the dossier: default warnings-only, exit 0; `--strict` opt-in, CI-only; **no blocking hook in v1** — W105/W106/W107/W112 have no corpus behind them. No faion dialect: the barrier was never vocabulary but decomposition (E002, W111 — both caught, both explainable in a line). English canonical, questions localised to Ukrainian.

Copy: **"the first EARS validator that runs inside your coding agent — one binary, no DOORS, no Jama, no seat licence."** Never "nobody has built this" — QVscribe has validated EARS since 2019-08-21; `labeth/ears-lint-go` exists (MIT). Re-verify first: the 2026-08-03 pass never audited the VS Code Marketplace, StrictDoc, Doorstop or rmtoo.

## Rejected

A workflow for constitution authoring (methodology + playbook + six bootstrap lines suffice) · `constitution-amendment-protocol` as a second slug · `sdd/ears-requirement-templates` as an alternative name · EARS and spec-delta playbooks (disciplines invoked inside a workflow, not goals) · `## Unchanged (explicit)` as mandatory (unbounded, unverifiable; `## Out of Scope` + the scenario-loss check covers it) · `## Status:` inside a spec (the directory is the status) · `.aidocs/specs/<capability>/` from F049 (forks the source of truth) · semantic constitution enforcement · runtime Python in the CLI · Vale as delivery vehicle · quoting "97% fewer tokens" (n=2, GPT-5.2, confounded) · running `build-domain-index-v2.py`.

## Risks / conflicts with other slices

**Slug collisions.** `sdd/constitution-md` will be re-proposed by `layer2-decomposition/{spec-kit,agent-os}.md`, `sdd/spec-delta-format` by `openspec.md`, `sdd/ears-requirements` by `kiro.md`. **This slice owns all three;** framework passes reference the slug and add only tool-specific deltas.

**Same-file edits.** `sdd/spec-requirements/content/{01-core-rules,02-output-contract}.xml` · `ba/requirement-quality-scorecard/AGENTS.md:27` · `sdd/project-spec-structure/content/03-delta-update.xml` (OpenSpec pass wants it too) · `sdd/readiness-checklist/content/01-checklist.xml` · `sdd/user-flows-template/` · `workflows/sdd-batch-orchestrator/content/07-verify-review-fix-loop.xml` (layer-4 `three-tier-verification-ladder` adds lint tiers to the same matrix — **merge, don't overwrite**) · `workflows/idea-to-prod/content/{10-bootstrap,20-phases}.xml` (layer-3 `checkpoint-rollback-pattern` targets `40-cron-loop.xml`) · `skills/tier-manifest.json`, `sdd/INDEX.xml`, `knowledge/domains.xml`, `workflows/catalog.json`, `CHANGELOG.md` — **serialize manifest regeneration; never two passes' `regen-tier-manifest.py` in parallel worktrees**.

**Hard blocker, inherited.** Seven `sdd` methodologies exist on disk, are cited by name in the root `AGENTS.md`, and are missing from `tier-manifest.json` (six also from `sdd/INDEX.xml`: 90 declared vs ~98 dirs) — including **`project-spec-structure`** (N3's prerequisite), **`user-flows-template`** (W3's generation source) and **`readiness-checklist`** (N3's anchor). Until registered, both new slugs ship refs the retriever cannot reach — the phantom-ref failure already behind ~350 of 883 broken refs in published MDX. **Fix the registration gap before, not with, this slice.**

**Unmeasured.** The E/W rule set has never run over a real corpus — before `--strict` exists, run it across every `spec.md` in `faion-cli/.aidocs/` and `faion-network/.aidocs/` and tune. The ≤20-rule cap is a forcing constraint, not an empirical finding; never present it as measured in customer-facing copy.
