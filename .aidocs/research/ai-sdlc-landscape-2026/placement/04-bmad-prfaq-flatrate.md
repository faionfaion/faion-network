# Placement — BMAD, PRFAQ, flat-rate planning
**Slice:** BMAD Method, PRFAQ, Web Bundles / flat-rate · **Author pass:** 4 of 10 · **Date:** 2026-08-04

## Verdict summary

| Approach | Dossier | Placement decision | Target path | Tier |
|---|---|---|---|---|
| PRFAQ (method) | 🟢 | New methodology, from Amazon primaries | `knowledge/product/working-backwards-prfaq/` | solo |
| PRFAQ (as a gate) | 🟢 | New Phase 2.5 | `workflows/idea-to-prod/` | n/a |
| Two-phase gate; context-complete units | 🟡 | Already owned; no change | `idea-to-prod`; `sdd-batch-orchestrator` | — |
| `customize.toml` 3-layer merge | 🟡 | Out of slice (CLI/VFS) | — | — |
| Personas, Marketplace, below `create-epics-and-stories`, web-bundle shelf | 🟡 | Reject | — | — |
| One-way-valve handoff discipline | 🟡 | New methodology | `knowledge/sdlc-ai/multi-surface-planning-handoff/` | solo |
| Quota-pool topology | 🟡 | New methodology | `knowledge/ai-core/workflow-runtime-budget-topology/` | solo |
| `skills/bmad-*/` (46 dirs) | — | **Delete** | — | — |

## Workflow changes

All in `skills/faion/workflows/idea-to-prod/`. **Not `brainstorm`**: brainstorm is divergent (30 recs × 10 personas) over a question already accepted as worth answering; PRFAQ is convergent and can return *kill*. `idea-to-prod` has the `.product/` contract to land it in — and it jumps from Phase 2 ("we picked a stack") to Phase 3 ("write `spec.md`") with nothing asking whether a customer wants this.

| File | Change |
|---|---|
| `content/20-phases.xml` | Insert `<section title="Phase 2.5 — Concept gate (PRFAQ)">` between Phase 2 and 3. Trigger: `brainstorm.md` exists, `.product/prfaq.md` does not. Subagent runs `product/working-backwards-prfaq` → `.product/prfaq.md` with frontmatter `stage`, `concept_type`, `verdict: proceed\|revise\|kill`. Third clause on the existing **Advance condition (invariant)**: Phase 3 starts only on `proceed`; `revise` loops back |
| `content/10-bootstrap.xml` | Add `├── prfaq.md` to the `.product/` layout block |
| `content/60-stop-conditions.xml` | New stop: `kill` halts the loop, run counts as **successful** — a killed concept is the gate working |
| `content/50-failure-modes.xml` | New mode "concept gate unanswerable": 2–3 exchanges with no articulable customer → redirect to `../brainstorm/`, re-enter 2.5 |
| `AGENTS.md` | `version` 1.0.0→1.1.0, `last_verified: 2026-08-04`, one `success_criteria` line, phase list + content-table row |
| `decisions.xml` | New `<decision topic="concept-gate-before-sdd">`. Rejected: Phase 2 as validation (ranks options, never asks if the category is wanted); a post-deploy check (build already paid for) |
| `catalog.json` | `"2.5-concept-gate"` into `idea-to-prod.phases`, bump version/date, extend `notes` |

Flat-rate needs no workflow change: "one session → one artefact → one commit" *is* the existing advance invariant.

## New content proposed

**1. `product/working-backwards-prfaq` — solo.** Press release + customer FAQ + internal FAQ ending in a `proceed/revise/kill` **judgement, not a score** (false precision; bodies are CLI-only so no number surfaces). Generalise BMAD's `{concept_type}` past its four values with service business, creative-media, physical product — one slug then serves `marketing/`, `comms/`, `hr/`. Checked `product/INDEX.xml` (112): nearest are `what-you-dont-know-about-launch-pre-mortem` (launch-time, not concept-time) and `kill-criteria-template` / `kill-or-keep-criteria` (thresholds, not a narrative gate); `product-discovery`, `continuous-discovery`, `ac-quality-rubric` also cleared. Zero `prfaq|working-backward` hits across 23 indexes, re-confirmed today. Solo not free: the 30% preview carries the four essentials and walls the FAQ banks. Shape per `ai-agents/context-graph-engineering/`. **Blocker:** nobody read Bryar & Carr or Amazon's own PR/FAQ description — read them first, or we ship BMAD's reading of Amazon.

**2. `sdlc-ai/multi-surface-planning-handoff` — solo.** Chat has zero authority; one session → one artefact → one commit; provenance frontmatter; close the thread; repo wins on conflict; gate on the committed file. Plus the never-paste list and the ChatGPT Business $25-vs-Plus $20 no-train-default upgrade. Checked 91 `sdlc-ai` slugs: `ai-coding-agent-handoff-protocol` is agent→agent in-repo, `adr-supersession-detection` detects the symptom. Nothing covers surface→surface. Say in-body the rules are derived from the failure mode, not observed teams.

**3. `ai-core/workflow-runtime-budget-topology` — solo.** Pools held, what each may touch, ceiling behaviour, and that a flat-rate agent SDK is not a free one. All nine `ai-core` cost slugs price *the reader's product's* bill; none prices *their own workflow*. Carries Scenario A ≈$3 vs B ≈$26, marked modelled-not-measured. **Pricing-rule hazard, flag in-file:** USD per session and quota percentages fine, tokens as an engineering unit fine, denominating a Faion offering in tokens never.

**Registration, all three:** write `meta.json` → `regen-tier-manifest.py --diff`, inspect, run → **hand-add** `<methodology slug tier path><summary/></methodology>` alphabetically in the domain `INDEX.xml`, bump its `count=` (`product` 112→113; likewise `sdlc-ai`, `ai-core`). **Never run `build-domain-index-v2.py`.** Optional once (1) exists: reference it from `playbooks/discover-validate/idea-to-validated-mvp/AGENTS.md`.

## `skills/bmad-*/` disposition

**Delete.** `git clean -fdn skills/bmad-*`, then `git clean -fd`.

Committing makes four defects permanent: 76 files point at a `_bmad/` root that does not exist, so every skill's activation Step 1 fails; zero of 3,070 manifest entries cover these paths, so no gating, serving or search; it is a rival methodology system (own personas, config root, artefact names, four skills already deprecated-in-v7) inside the tree we sell one opinionated SDD lifecycle from; and it is unattributed MIT prose in a commercial product. A curated subset (`bmad-prfaq` only) fixes none of these and parks a competitor's prose beside the methodology we are about to write. "Extract then delete" already happened — the dossiers *are* the extraction.

**Lost, precisely:** 46 live `/bmad-*` skills that load into every session here via the `~/workspace/.claude` symlink — a real loss to Ruslan's personal surface, zero to the product; dropping 46 `SKILL.md` descriptions from every session listing is itself a context saving. Plus `bmad-prfaq`'s four `references/` files, inventoried but never read line-by-line — re-fetchable from a public MIT repo in minutes. **Mitigation first:** record the `BMAD-METHOD@main` SHA as of 2026-08-03 in `bmad-method.md`.

## Rejected

Persona cast and `party-mode` — `brainstorm/04-reviewer-roles.xml` does roles-as-lenses better. Everything below `create-epics-and-stories` — `sdd-batch-orchestrator` owns it. The Marketplace and the `_bmad/` config root. A separate `prfaq-verdict-rubric` slug — fold into `02-output-contract.xml`. A new `discover-validate` playbook — duplicates `idea-to-validated-mvp` stages 1–2. Corpus upload to a Gem/Custom GPT — breaks D-001 sealing and tier gating. "Save tokens" in user-facing copy. `preceded-by`/`followed-by` index edges and `faion export --protocol` — real, but schema/CLI questions, out of slice.

## Risks / conflicts with other slices

- `workflows/idea-to-prod/content/20-phases.xml` — **highest risk.** spec-kit, kiro, openspec, spec-delta, constitution-md and EARS all plausibly want Phase 3. I insert a section and amend one rule; a wholesale rewrite destroys that silently.
- `workflows/catalog.json` plus `idea-to-prod/{AGENTS.md,decisions.xml,content/10-bootstrap.xml,content/50-failure-modes.xml,content/60-stop-conditions.xml}` — same-file contention; several passes will each bump `idea-to-prod.version` to 1.1.0.
- `knowledge/{sdlc-ai,product,ai-core}/INDEX.xml` `count=` — agents-md-standard, decision-journal-adr, checkpoint-rollback and three-tier-verification will all add `sdlc-ai` entries. Whoever lands second must **re-count, not increment**.
- `skills/tier-manifest.json` — already `M` on `_temp_main` alongside a modified `knowledge/ai-agents/INDEX.xml`. Regenerated wholesale: never hand-edit; regen once, last, after all `meta.json` land. It will also pick up the seven orphaned `sdd` methodologies (corpus defect #1) — correct, not a bug.
- **Exactly one pass may execute the `bmad-*` delete.**
