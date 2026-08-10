# BMAD Method
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

BMAD ("Breakthrough Method for Agile Ai Driven Development") is an installable pack of agent personas, skills, and document templates that turns "an idea or change request into working software without giving up the thinking" (README, fetched 2026-08-03). It splits work into two phases: a **planning phase** that produces durable markdown artefacts (brief → PRFAQ → PRD → UX → architecture → epics/stories), and an **implementation phase** where each story file carries all the context the dev agent needs, so no agent has to reconstruct project state from a chat log.

The distribution unit as of the v6 line is a **skill** — a directory with `SKILL.md`, optional `customize.toml`, `references/`, `assets/`, `agents/`. Personas are themselves skills (`bmad-agent-pm` = "talk to John"). Installation writes them into whatever agent runtime you use; the installer supports 42 agent platforms as of v6.5.0 (CHANGELOG, 2026-04-26).

**It was built to write code.** The planning half is domain-neutral; everything from `bmad-create-epics-and-stories` downward assumes a repository, a test suite, and a dev agent with file access. A CX designer, a course author, or a services consultant does not use BMAD as-is and should not try.

## Current state

| Fact | Value | Source & date |
|---|---|---|
| Repo | `bmad-code-org/BMAD-METHOD` | GitHub API, 2026-08-03 |
| Stars | **51,439** | GitHub API, 2026-08-03 |
| Forks | 5,902 | GitHub API, 2026-08-03 |
| Latest release | **v6.10.0**, published **2026-07-03** | GitHub Releases API, 2026-08-03 |
| Last push to `main` | 2026-08-03T10:20Z | GitHub API, 2026-08-03 |
| License | **MIT** — "Copyright (c) 2025 BMad Code, LLC" (repo API reports `NOASSERTION` because the LICENSE file carries an extra contributor-provenance paragraph) | `LICENSE` via GitHub API, 2026-08-03 |
| Maintainer | BMad Code, LLC (Brian Madison / "BMad") | LICENSE + bmadcode.com, 2026-08-03 |
| Price | **Free**, open source. No paid tier for the core method. | README + LICENSE, 2026-08-03 |
| Install | `npx bmad-method install` | README, 2026-08-03 |

### Adjudicating the landscape-doc claim #1

> *"Alive and actively developed — v6.3.0 (April 2026) brought a Marketplace and parallel story development; the branch reached v6.8; ~49k stars."*

**Mostly true, three corrections — all dated:**

1. ✅ **v6.3.0 / Marketplace / parallel story development — CONFIRMED.** CHANGELOG dates v6.3.0 at **2026-04-09**; the release notes list "marketplace-based plugin installation replacing custom content" and "parallel story development by replacing spec-wip singleton with status-tracked spec files". (CHANGELOG.md, fetched 2026-08-03. A secondary write-up dates the release 2026-04-10 and adds "4 breaking changes, 13 features, 1 refactor, 5 bug fixes" — vibesparking.com, 2026-04-11.)
2. ⚠️ **The Marketplace was retired five weeks later.** v6.7.0 (**2026-05-17**) records "Removed community modules picker; bundled marketplace registry fully retired." Anyone citing the Marketplace as a live 2026 differentiator is citing a five-week-old feature. (CHANGELOG.md, 2026-08-03.)
3. ❌ **"the branch reached v6.8" is stale.** The line reached **v6.9.0 (2026-06-21)** and **v6.10.0 (2026-07-03)**, which added `bmad-loop` (unattended dev orchestration), `bmad-dev-auto`, `bmad-forge-idea` (Socratic idea pressure-testing), a rewritten `bmad-architecture`, and party-mode with persistent memory. (CHANGELOG.md + Releases API, 2026-08-03.)
4. ❌ **"~49k stars" is stale.** **51,439** as of 2026-08-03. (A June 2026 secondary source did report ~49k / 5.7k forks, so the doc's number was correct when written and has simply drifted.)

Net: the claim understates how alive it is, and overstates the Marketplace.

## Mechanics

### Personas (as shipped in the v6.x skills)

| Persona | Skill | Role |
|---|---|---|
| **Mary** | `bmad-agent-analyst` | Strategic business analyst, requirements expert |
| **John** | `bmad-agent-pm` | Product manager, PRD creation and requirements discovery |
| **Winston** | `bmad-agent-architect` | System architect, technical design lead |
| **Sally** | `bmad-agent-ux-designer` | UX designer and UI specialist |
| **Amelia** | `bmad-agent-dev` | Senior engineer, story execution and implementation |
| **Paige** | `bmad-agent-tech-writer` | Technical documentation and knowledge curation |

> ⚠️ **The "Analyst → PM → Architect → Scrum Master → Dev → QA" lineup is the v4/v5 shape and is stale.** v6.3.0 (2026-04-09) "consolidated three agent personas into Developer agent (Amelia)" — a secondary write-up says four merged into one. There is no separately-personified Scrum Master or QA agent in the shipped v6 skill set; sprint mechanics live in skills (`bmad-sprint-planning`, `bmad-sprint-status`, `bmad-correct-course`, `bmad-retrospective`) and QA lives in review skills (`bmad-code-review`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-qa-generate-e2e-tests`). Reimplement the *roles*, not the six-avatar cast.

### Phase order

Two levels of "phase" exist, and they are not the same thing.

**Delivery loop** (README, 2026-08-03): `Clarify → Plan → Build and verify → Learn and adjust`.

**Named phases** in skill manifests: the only value present in the installed set is `"phase-name": "1-analysis"` (on `bmad-prfaq`). Phase membership is expressed structurally via `preceded-by` / `followed-by` arrays in each skill's `bmad-manifest.json`, not by a global phase list. Example, verbatim from `bmad-prfaq/bmad-manifest.json`:

```json
{
  "module-code": "bmm",
  "capabilities": [{
    "name": "working-backwards",
    "menu-code": "WB",
    "phase-name": "1-analysis",
    "preceded-by": ["brainstorming", "perform-research"],
    "followed-by": ["create-prd"],
    "is-required": false,
    "output-location": "{planning_artifacts}"
  }]
}
```

The practical planning chain a user walks:

```
brainstorming ──┐
                ├─→ product-brief ─→ prfaq ─→ prd ─→ ux ─→ architecture ─→ epics-and-stories
research    ────┘                                                                │
                                                                                 ▼
                                          sprint-planning → create-story → dev-story → code-review
                                                                                 │
                                                     correct-course ←────────────┤
                                                     retrospective  ←────────────┘
```

### Skill inventory (46 skills in the drop we hold, 2026-08-03)

**Planning / analysis:** `bmad-brainstorming`, `bmad-forge-idea`, `bmad-domain-research`, `bmad-market-research`, `bmad-technical-research`, `bmad-product-brief`, `bmad-prfaq`, `bmad-prd` (+ deprecated `bmad-create-prd`, `bmad-edit-prd`, `bmad-validate-prd`), `bmad-spec`, `bmad-ux`, `bmad-architecture` (+ deprecated `bmad-create-architecture`), `bmad-create-epics-and-stories`, `bmad-check-implementation-readiness`.

**Execution:** `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-create-story`, `bmad-dev-story`, `bmad-dev-auto`, `bmad-quick-dev`, `bmad-correct-course`, `bmad-retrospective`, `bmad-checkpoint-preview`.

**Review / QA:** `bmad-code-review`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-qa-generate-e2e-tests`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`.

**Docs / meta:** `bmad-document-project`, `bmad-generate-project-context`, `bmad-index-docs`, `bmad-shard-doc`, `bmad-help`, `bmad-customize`, `bmad-advanced-elicitation`, `bmad-party-mode`.

**Personas:** the six above.

Four skills are explicitly marked `DEPRECATED — will be removed in v7`.

### Artefact names

`prfaq-{project_name}.md` · `product-brief.md` · PRD (via `bmad-prd`) · `DESIGN.md` + `EXPERIENCE.md` (the v6.8.0 two-spine UX model, 2026-05-25) · architecture spine · `spec-{slug}.md` with a `status` field (the v6.3.0 replacement for the `spec-wip.md` singleton — this is *what* "parallel story development" means) · epics + story files · `project-context.md` · `index.md` · sprint status file · `.decision-log` (v6.8.0).

### Configuration surface

- `{project-root}/_bmad/bmm/config.yaml` — resolves `{user_name}`, `{communication_language}`, `{document_output_language}`, `{planning_artifacts}`, `{project_knowledge}`.
- Three-layer override merge, base → team → user: `{skill-root}/customize.toml` → `{project-root}/_bmad/custom/{skill-name}.toml` → `{skill-name}.user.toml`. Scalars override, tables deep-merge, arrays-of-tables key on `code`/`id`, other arrays append.
- Resolver: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`, with a documented manual-merge fallback if the script is missing.
- Activation contract every skill runs: resolve workflow block → run `activation_steps_prepend` → load `persistent_facts` (entries prefixed `file:` are globs under project root) → load config → greet → run `activation_steps_append`.

**This is the single most reimplementable thing in BMAD** and it is orthogonal to software: a base/team/user TOML merge over a declarative activation contract works for any skill system.

### Ecosystem modules

BMM (the method itself), BMB (BMad Builder), TEA (Test Architect), BMGD (Game Dev Studio), CIS (Creative Intelligence Suite), plus community modules like Whiteport Design Studio (v6.1.0). Module code appears as `module-code` in each manifest.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | BMAD-METHOD repo README | https://github.com/bmad-code-org/BMAD-METHOD | Positioning, delivery loop, MIT license, `npx bmad-method install`, module list, one-line web-bundles mention | 2026-08-03 |
| 2 | CHANGELOG.md | https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md | Dated version history v6.0.0 → v6.10.0; the authoritative source for the Marketplace add (v6.3.0) and removal (v6.7.0) | 2026-08-03 |
| 3 | GitHub REST API (repo + releases) | `gh api repos/bmad-code-org/BMAD-METHOD` | Stars 51,439 / forks 5,902 / last push / latest tag v6.10.0 @ 2026-07-03 | 2026-08-03 |
| 4 | LICENSE | `gh api .../contents/LICENSE` | MIT, BMad Code LLC, 2025 | 2026-08-03 |
| 5 | `web-bundles/` tree + `bundles.json` | `gh api .../contents/web-bundles` | Six bundles, `releaseTag: web-bundles-v1.0.0`, `releasedAt: 2026-05-25`, per-bundle `knowledgeFiles` | 2026-08-03 |
| 6 | BMad v6.3.0 changelog write-up (secondary) | https://www.vibesparking.com/en/blog/ai/bmad/2026-04-11-bmad-v630-changelog/ | Release-day framing: Marketplace, 4→1 agent merge, parallel stories, PRFAQ arrival | 2026-08-03 |
| 7 | Local skill drop | `skills/bmad-*/` (untracked, mtime 2026-07-23) | 46 skills, 37 `customize.toml`, 1 `bmad-manifest.json`, 2.5 MB | 2026-08-03 |

## What to borrow for faion

1. **The two-phase split as a hard gate, not a suggestion.** Planning produces committed markdown; implementation reads it. Our SDD lifecycle (`backlog/ → todo/ → in-progress/ → done/`) already has this bone structure — BMAD's contribution is that *nothing* in phase 2 is allowed to invent context, and `bmad-check-implementation-readiness` is a named, runnable gate. We have `readiness.md` as a document; making it an executable check is the borrow.
2. **Context-complete work units.** `bmad-create-story` exists purely to produce "a dedicated story file with all the context the agent will need to implement it later." That is a *format* claim, not a software claim: a wedding planner's vendor brief, a course module spec, and a client onboarding packet all benefit. This generalises cleanly to non-technical solopreneurs.
3. **The three-layer customization merge.** base `customize.toml` → team `.toml` → user `.user.toml`, with typed merge semantics. Our 2,622 methodologies currently have no user-override channel at all. This is a concrete product feature we could ship without touching content.
4. **`preceded-by` / `followed-by` on every capability.** A machine-readable adjacency graph over skills. Our `INDEX.xml` files carry slug + domain but no sequencing edges. Adding them would let `faion search` answer "what comes after this" instead of only "what matches this."
5. **Intent consolidation.** v6.7.0 folded Create/Update/Validate into one `bmad-prd` skill and deprecated three others. We have near-duplicate slugs across domains (`stakeholder-engagement`, `-advanced`, `-pm-traditional`, `-advanced-pm-traditional` — four entries for one topic). BMAD's answer is intents inside one skill, not four skills.
6. **Adversarial review as a first-class, separable step.** `bmad-review-adversarial-general` and `bmad-review-edge-case-hunter` are explicitly "attitude-driven" vs "method-driven" and run in parallel layers. That decomposition is domain-neutral.

## What NOT to borrow — and why

- **The persona cast.** Six named avatars (Mary, John, Winston, Sally, Amelia, Paige) are a UX affordance for people who miss having a team. They add a naming layer with no retrieval value, they've already churned once (v6.3.0 merged 3–4 personas into Amelia), and for a solo non-technical buyer "talk to Winston the architect" is noise. Borrow the roles as *review lenses*, not as characters.
- **Everything from `create-epics-and-stories` downward.** Epics, stories, sprint planning, `dev-story`, `dev-auto`, `code-review`, e2e generation, `correct-course`, retrospectives. This is Scrum-for-agents. It presumes a repo, a test suite, and file-writing agents. A CX designer has none of those and would be paying for scaffolding they can never load.
- **The Marketplace.** Added 2026-04-09, retired 2026-05-17. Five weeks. Do not build a plugin registry because BMAD briefly had one.
- **`bmad-party-mode` / anti-consensus club.** Multi-persona roundtables are fun and expensive. We already gate brainstorming behind explicit user request for exactly this reason.
- **The `_bmad/` runtime directory.** BMAD skills hard-depend on `{project-root}/_bmad/bmm/config.yaml` and a Python resolver script living in the user's project. That is a second config root competing with ours. Take the *merge semantics*, not the directory.
- **`npx` / Node install path.** Our CLI is a Go single binary with a sealed embedded VFS (D-001). Adopting a Node installer would break both the cross-platform and content-sealing pillars.

## Mapping to our corpus

Ground truth read 2026-08-03: `skills/tier-manifest.json` v8, `updated: 2026-05-07`, `last_synced: 2026-05-23`, **3,070 entries** — free 129 / solo 841 / pro 1,405 / geek 695. Knowledge indices: `product/INDEX.xml` 340 lines, `pm/INDEX.xml` 856, `sdd/INDEX.xml` 274, `sdlc-ai/INDEX.xml` 277.

**Where BMAD's planning chain already has a home in our corpus:**

| BMAD skill | Nearest faion methodology |
|---|---|
| `bmad-brainstorming` | our `faion` skill's diverge–converge brainstorming path |
| `bmad-domain/market/technical-research` | `research/` domain |
| `bmad-product-brief` | `product/product-discovery`, `product/continuous-discovery` |
| `bmad-prd` | `pm/` requirements cluster + `sdd/spec-requirements`, `sdd/spec-structure`, `sdd/template-spec` |
| `bmad-ux` | `ux/` domain + our `ui-ux-design.md` per-feature doc |
| `bmad-architecture` | `architecture/` domain + `sdd/architecture-decision-records-planning` |
| `bmad-create-epics-and-stories` | `sdd/impl-plan-components`, `sdd/impl-plan-task-format`, `sdd/writing-implementation-plans` |
| `bmad-check-implementation-readiness` | `readiness-checklist` (our `readiness.md` gate) |
| `bmad-create-story` (context-complete unit) | `sdlc-ai/ai-coding-agent-handoff-protocol`, `sdlc-ai/kb-agents-md-context-pyramid` |

**Confirmed gaps (grepped all 22 `INDEX.xml` files, 2026-08-03):**

- **Zero hits** for `prfaq`, `working-backward`, `press-release`, or `amazon` across the entire corpus. Amazon Working Backwards is absent. See `bmad-prfaq.md`.
- **Zero methodologies on planning-phase economics** — no slug in any domain covers where an AI-assisted planning session's cost actually lands. `ai-core/` has eleven cost slugs (`inference-cost-unit-economics`, `cost-quality-pareto-template`, `weekly-llm-cost-review-template`, …) but all of them are about *your product's* inference bill, not *your own workflow's*. See `flat-rate-planning.md`.
- **No skill-sequencing edges.** Our `INDEX.xml` carries `slug`/`domain`/`group`/`tier`; nothing equivalent to `preceded-by`/`followed-by`.
- **No user-override channel** for methodology content.

### Verdict on the untracked `skills/bmad-*/` directories: **DELETE**

State as found (2026-08-03, branch `_temp_main`): 46 directories, 2.5 MB, all untracked (`??` in `git status`), mtime 2026-07-23. Someone ran a BMAD install into our skills root and walked away.

Four independent reasons this cannot stay:

1. **It is broken as installed.** 80 files across the drop reference `{project-root}/_bmad/...`. There is **no `_bmad/` directory in this repo.** Every skill's Step 1 (`resolve_customization.py`) and Step 4 (load `_bmad/bmm/config.yaml`) fail. Only 1 of 46 skills (`bmad-prfaq`) even has a `bmad-manifest.json`; 37 of 46 have `customize.toml`. This is a partial, non-functional install.
2. **It is invisible to the product.** `grep -c bmad tier-manifest.json` → **0**. Not one of the 3,070 manifest entries covers these paths. The CLI cannot tier-gate them, the backend cannot serve them, and `faion search` cannot find them. They are dead weight inside a 330 MB repo we already tell agents not to scan.
3. **It is a second, competing methodology system.** We sell one opinionated SDD lifecycle. Shipping a rival one — with its own personas, its own config root, its own artefact names, and four skills already marked deprecated-in-v7 — inside the same `skills/` tree guarantees drift and confuses every agent that loads the directory.
4. **License hygiene we haven't done.** MIT (BMad Code, LLC, 2025) permits redistribution *with the copyright notice and permission notice*. The drop as it sits carries no attribution at our repo level, and `faion-network` is the thing we sell. Vendoring third-party MIT content into a commercial knowledge base without an attribution file is a defect we should not create by accident.

**Do this:** `git clean` them out. Keep exactly two things, as our own writing under our own license: (a) the PRFAQ methodology, rewritten from Amazon's public Working Backwards method rather than copied — see `bmad-prfaq.md`; (b) the three-layer `customize.toml` merge semantics as a design note, which is an idea and not copyrightable expression. If we later want any BMAD *text* verbatim, vendor it deliberately into a `vendor/` path with a `LICENSES/` file and a manifest entry — never as an untracked drop in `skills/`.

## Open questions / staleness risk

- **High churn.** Seven minor releases between 2026-03-12 (v6.1.0) and 2026-07-03 (v6.10.0) — roughly one every 16 days, with breaking changes in at least v6.3.0. Anything in this dossier below the "what to borrow" section has a half-life measured in weeks. The stable facts are the *shape* (two phases, context-complete units, override merge); the unstable facts are skill names and personas.
- **v7 is signposted.** Four skills carry "will be removed in v7". Whatever consolidation v7 brings will likely invalidate the skill inventory above.
- **License field ambiguity.** GitHub's API reports `NOASSERTION` while the LICENSE file is plainly MIT with an added provenance paragraph about community contributions. If we ever vendor BMAD text, that paragraph needs a lawyer's eye, not mine.
- **Unverified: how BMAD actually performs for non-technical users.** Every source I could reach is either the maintainer's own docs or a developer blog. There is no independent evidence in what I fetched that the planning half works for someone with no repo. Our own 🟡 verdict rests on reading the skill contents, not on observed non-technical usage.
- **Not checked:** the `bmad-utility-skills` repo (`bmad-os-skill-to-bundle`), the module ecosystem (BMB/TEA/BMGD/CIS) beyond names, and the docs site's `how-to`/`tutorials` trees. If we ever build our own bundle packager, `bmad-os-skill-to-bundle` is the prior art to read first.
