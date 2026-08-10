# Kiro
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

Kiro is AWS's agentic IDE and CLI whose distinguishing feature is a **spec-driven** working mode: instead of prompting an agent straight into code, you drive it through three generated artefacts — `requirements.md` → `design.md` → `tasks.md` — and only then let it implement. It is built on Code OSS (the open-source base of VS Code), so it takes Open VSX extensions, themes and imported VS Code settings.

Kiro is the successor product to Amazon Q Developer's IDE surface. Around the spec core it adds two configuration mechanisms that are the parts most often cited as novel:

- **Steering files** (`.kiro/steering/*.md`) — persistent project context injected into the agent under four inclusion modes.
- **Agent hooks** (`.kiro/hooks/`, JSON) — event-triggered automations, three of which can *block* the agent.

Positioning for a solopreneur: it is a **workflow shape** worth copying and a **product** worth not adopting. The shape (three artefacts, gated phases, persistent project rules, event hooks) is exactly the SDD flow faion already runs. The product is a credit-metered, vendor-hosted IDE that competes with the editor the user already has.

## Current state

| Fact | Value | Source date |
|------|-------|-------------|
| Public preview | July 2025 | reported 2025-07 |
| **General availability** | **2025-11-17** (with team features + CLI) | kiro.dev/blog/general-availability, SiliconANGLE 2025-11-17 |
| IDE version (latest) | **1.0.138**, released 2026-07-13 | kiro.dev/changelog/ide, fetched 2026-08-03 |
| CLI version (latest) | **2.16.0**, released 2026-07-31 | kiro.dev/changelog/cli, fetched 2026-08-03 |
| Web surface | last notable update 2026-07-01 (sandbox → AWS resources, Figma/Stripe/Supabase connectors) | kiro.dev/changelog/web, fetched 2026-08-03 |
| Model roster | Claude Opus 5 available in IDE/CLI/Web since **2026-07-24**; Claude Sonnet 4.5 + open-weight models on the free tier | kiro.dev/changelog/models, fetched 2026-08-03 |
| Maintainer | Amazon Web Services (AWS) | — |
| License | **Proprietary** SaaS product; the editor shell derives from Code OSS (MIT). Kiro itself is not open source. | 2026-08-03 |

**Pricing** — kiro.dev/pricing, fetched **2026-08-03**, per user per month:

| Plan | Price | Credits |
|------|-------|---------|
| Free | $0 | 50 credits/mo; open-weight models + Claude Sonnet 4.5 |
| Pro | $20 | 1,000 |
| Pro+ | $40 | 2,000 |
| Pro Max | $100 | 5,000 |
| Power | $200 | 10,000 |

Add-on credits **$0.04 each**. Credits reset monthly, do **not** roll over. Team plans mirror individual prices and add consolidated billing, usage analytics, SAML/SCIM SSO. GovCloud is ~20% more expensive and has **no free tier**. New users signing in via social login or AWS Builder ID get $20 credited toward a subscription. AWS Startups offers eligible startups **one year of Kiro Pro+** (announced around GA, 2025-11).

Solopreneur read: the free tier's 50 credits/month is a demo, not a working allowance. The realistic entry point is $20/mo **on top of** whatever coding-agent subscription the user already pays for. That is the single biggest argument against adoption.

## Mechanics

### Spec workflow

A spec lives under `.kiro/specs/<feature-name>/` and produces three files:

| File | Contents |
|------|----------|
| `requirements.md` (or `bugfix.md` for the bug flow) | User stories + acceptance criteria in EARS format, or bug analysis |
| `design.md` | Technical architecture and implementation considerations |
| `tasks.md` | Discrete, executable implementation tasks |

The documented sequence is Requirements (or Bug Analysis) → Design → Tasks → Implementation. Kiro's own docs describe the human checkpoints as *iterative confirmations* ("Confirm when requirements meet your needs", "Confirm the design is feasible"), not hard gates — and it ships a **Quick Spec** mode that explicitly "auto-generate[s] all three artifacts **without approval gates**" (kiro.dev/docs/specs, fetched 2026-08-03).

### EARS usage

Kiro's requirements-first doc states that requirements in EARS format "are: Unambiguous and testable; Easy to translate into test cases; Traceable through implementation; Clear for both technical and non-technical stakeholders", and uses the template `WHEN [condition] THE SYSTEM SHALL [action]` (kiro.dev/docs/specs/feature-specs/requirements-first, fetched 2026-08-03). Note the dialect: **ALL-CAPS keywords, no comma** before the actor — a deviation from Mavin's canonical `When <trigger>, the <system> shall <response>`.

### Steering — four inclusion modes (confirmed)

Files in `.kiro/steering/` (workspace) or `~/.kiro/steering/` (global), YAML front-matter:

| Mode | Front-matter | Behaviour (quoted from docs) |
|------|--------------|------------------------------|
| Always (default) | `inclusion: always` | "These files are loaded into every Kiro interaction automatically." |
| Conditional | `inclusion: fileMatch` + `fileMatchPattern: "components/**/*.tsx"` | "Files are automatically included only when working with files that match the specified pattern." |
| Manual | `inclusion: manual` | "Files are available on-demand by referencing them with `#steering-file-name`" |
| **Auto** | `inclusion: auto` + `name:` + `description:` | "Files are automatically included when your request matches the description." |

Three foundation files are generated by default and included in every interaction: `product.md`, `tech.md`, `structure.md`.

### Hooks — trigger types and blocking (confirmed)

JSON configs under `.kiro/hooks/` (workspace level). Trigger set as documented on kiro.dev/docs/hooks (fetched 2026-08-03):

| Trigger | Fires | Can block? |
|---------|-------|-----------|
| `SessionStart` | Session begins | No |
| `UserPromptSubmit` | User submits a prompt | **Yes** |
| `PreToolUse` | Before tool executes | **Yes** |
| `PostToolUse` | After tool executes | No |
| `PreTaskExec` | Before a spec task starts | **Yes** |
| `PostTaskExec` | After a spec task finishes | No |
| `PostFileCreate` | After a file is created by the agent | No |
| `PostFileSave` | After a file is saved by the agent | No |
| `PostFileDelete` | After a file is deleted by the agent | No |
| `Stop` | Agent completes its turn | No |

Blocking mechanism: **exit code 2**, with STDERR returned to the agent. Manual hooks were removed and replaced by manual-inclusion steering files.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | Specs — IDE Docs | https://kiro.dev/docs/specs/ | Three-file structure, phase list, Quick Spec bypassing approval gates | 2026-08-03 |
| 2 | Requirements-First Workflow | https://kiro.dev/docs/specs/feature-specs/requirements-first/ | Kiro's EARS description + `WHEN … THE SYSTEM SHALL …` template; no validation language anywhere | 2026-08-03 |
| 3 | Steering — IDE Docs | https://kiro.dev/docs/steering/ | Four inclusion modes with exact front-matter; `.kiro/steering/` + `~/.kiro/steering/`; product/tech/structure defaults | 2026-08-03 |
| 4 | Hooks — IDE Docs | https://kiro.dev/docs/hooks/ | Full trigger table, blockable set, exit-code-2 semantics, `.kiro/hooks/` JSON | 2026-08-03 |
| 5 | Pricing | https://kiro.dev/pricing/ | Five plans, credit allowances, $0.04 add-on, GovCloud caveat | 2026-08-03 |
| 6 | Kiro is generally available | https://kiro.dev/blog/general-availability/ | GA announcement, team + CLI | 2026-08-03 (published 2025-11-17) |
| 7 | AWS launches Kiro into GA — SiliconANGLE | https://siliconangle.com/2025/11/17/aws-launches-kiro-general-availability-team-features-cli-support/ | Independent GA date confirmation, Code OSS base, price points | 2026-08-03 (published 2025-11-17) |
| 8 | IDE / CLI / Web / Models changelogs | https://kiro.dev/changelog/ | Version + date pins used in "Current state" | 2026-08-03 |
| 9 | AWS Startups — 1 year of Kiro Pro+ | https://aws.amazon.com/aws-startups/learn/power-your-startup-with-1-year-of-kiro-pro-plus-now-available-through-aws-startups/ | Startup credit programme | 2026-08-03 |

## Claims adjudicated

**Claim 1 — "Kiro is an AWS IDE with a spec-driven core: `requirements.md` (EARS) → `design.md` → `tasks.md`, plus steering files and agent hooks; requirements and design phases must complete before implementation."**
→ **Mostly TRUE, one part OVERSTATED.** The three-file core, EARS in `requirements.md`, steering and hooks are all confirmed. The *"must complete before implementation"* part is not what the docs say: the confirmations are framed as iterative checkpoints, and **Quick Spec explicitly generates all three artefacts with no approval gates**. So the ordering is a strong default, not an enforced gate. GA: **2025-11-17**. Pricing as tabled above, checked 2026-08-03.

**Claim 2 (critical) — "EARS in Kiro is a writing convention only — no parser, no linter, in Kiro's docs as of 2026-08-03."**
→ **TRUE for Kiro.** Nothing in kiro.dev/docs/specs or the requirements-first page mentions validating, linting, parsing, checking or enforcing EARS. The LLM is asked to *write* in EARS; nothing *verifies* it did. A malformed line costs nothing and is silently accepted downstream into `design.md` and `tasks.md`.
→ **FALSE as a market-wide claim.** See `ears-notation.md` §"Does anything machine-validate EARS": **QVscribe** (QRA Corp) has shipped automated EARS templating *and* compliance checking since **v2.10, announced 2019-08-21**, integrated with DOORS Next, Jama, Polarion, Word and Excel. Two tiny MIT-licensed OSS projects also exist (`labeth/ears-lint-go`, `tbhb/vale-ears`), both at 0 stars as of 2026-08-03. GitHub's own spec-kit received an EARS-integration request (**issue #1356, opened 2025-12-20, now closed**) that explicitly proposed EARS linting — and it did not land.
→ **Net opportunity, restated honestly:** EARS validation exists, but only inside enterprise requirements suites priced and shaped for aerospace/automotive teams. In the **AI-agent SDLC segment** — Kiro, spec-kit, Claude Code, Cursor — there is **no shipped EARS validator as of 2026-08-03**. That is the gap, and it is narrower and more defensible than "nobody has built this".

**Claim 3 — "Steering files and agent hooks already exist under other names in most stacks."**
→ **TRUE.** Steering `inclusion: always` ≈ `CLAUDE.md` / `AGENTS.md` / `.cursorrules` / `.github/copilot-instructions.md`. `inclusion: fileMatch` ≈ Cursor's glob-scoped rules. `inclusion: manual` ≈ `@file` / `#file` references. Hooks are near-identical to Claude Code hooks down to the **exit-code-2-blocks, STDERR-to-agent** convention. The one mode with genuine differentiation is `inclusion: auto` (name + description, dispatched by semantic match against the request) — that is Claude Code **Skills** dispatch by another name, and faion already exploits it heavily. Nothing here needs to be invented; naming and the blocking-hook table are the only things worth stealing verbatim.

**Claim 4 — "Four steering inclusion modes (always / conditional / manual / auto) and hook trigger types (file-save, pre/post-tool, pre/post-spec-task, and whether a hook can BLOCK a tool call)."**
→ **TRUE and now pinned.** Four modes confirmed with exact front-matter (table above). Hook triggers are richer than the claim: ten events, not four. **Yes, a hook can block a tool call** — `PreToolUse`, `UserPromptSubmit` and `PreTaskExec` are blockable via exit code 2. File events are **post-only** (`PostFileCreate/Save/Delete`) — there is no pre-file-save hook, so you cannot veto a write, only react to it.

## What to borrow for faion

1. **`PreTaskExec` as the SDD quality gate.** This is the single most transferable idea. A blocking pre-task hook is exactly where an EARS linter belongs: refuse to start implementing a task whose parent requirement does not parse. faion's SDD flow has the artefacts but no enforcement point; Kiro shows where the enforcement point goes.
2. **The three-artefact naming.** `requirements.md` / `design.md` / `tasks.md` is now the de-facto vocabulary of the segment (Kiro + spec-kit + a long tail of templates). Our `spec.md` / `plan.md` (Design + Execution Plan) / task files carry the same payload under different names. Worth documenting the mapping so our corpus is findable by people arriving from Kiro.
3. **`inclusion: auto` with `name` + `description`.** A description-matched context file is strictly better than always-on for a 2622-methodology corpus. We already do this via Skills; the lesson is to write *descriptions as dispatch keys*, not as summaries.
4. **The blockable/non-blockable split as a design principle.** Cheap checks block; expensive checks report. Publish the same table for faion gates so it is obvious which failures stop work and which only annotate.
5. **Bug flow as a first-class spec variant** (`bugfix.md` instead of `requirements.md`). We have `bugs/{todo,in-progress,done}/BUG0NN-*.md` in the SDD structure but no distinct artefact shape. Kiro's split is cleaner.

## What NOT to borrow — and why

1. **The product.** $20–$200/user/month of credits for a second IDE the user does not need. faion's buyer already pays for a coding agent; a metered editor on top is a hard no.
2. **The comma-less ALL-CAPS EARS dialect** (`WHEN … THE SYSTEM SHALL …`). It diverges from Mavin's canonical form for no gain and makes a linter's job harder (no comma boundary between condition and actor). Accept it in lenient mode; never make it canonical. Detail in `ears-notation.md`.
3. **Quick Spec.** Auto-generating all three artefacts with no approval gate is the exact failure mode SDD exists to prevent: it converts a review process into a longer prompt. If we ship a "fast path", it must still stop at the requirements gate.
4. **Credit-metered thinking as a UX.** Kiro makes the user budget their own reasoning. faion's pricing must not inherit this — it collides directly with the standing rule that faion pricing is not denominated in tokens.
5. **Steering-file sprawl.** Three always-on foundation files plus an unbounded `.kiro/steering/` directory is how context windows die. Our corpus discipline (L1 index → ≤3 buckets → L2 index → leaf) is better and should not be traded for "just put it in steering".
6. **Vendor coupling.** Web sandbox with direct AWS resource access and an assumed IAM role is a real feature and a real lock-in. faion-cli's whole premise is a single portable Go binary; do not copy anything that assumes a cloud account.

## Mapping to our corpus

| Kiro concept | faion equivalent today | Action |
|--------------|------------------------|--------|
| `requirements.md` (EARS) | `skills/faion/knowledge/sdd/spec-requirements/` — FR-NNN / NFR-NNN, verification method, priority, banned-vague-token list | Compose EARS into the `statement` field; see `ears-notation.md` §"Mapping to our corpus" |
| `design.md` | `plan.md` `## Design` section, `sdd/plan-md-structure` | Naming-only difference; document the alias |
| `tasks.md` | `plan.md` `## Execution Plan` + per-task files, `todo/ → in-progress/ → done/` | Ours is richer (lifecycle dirs); no change |
| `bugfix.md` | `bugs/{todo,in-progress,done}/BUG0NN-*.md`, `sdd/cr-bug-tracking` | Consider a distinct bug-spec artefact shape |
| Steering `always` | `AGENTS.md` per directory (project-docs-convention) | Already covered |
| Steering `fileMatch` | No direct equivalent | Gap — worth a methodology note, low priority |
| Steering `auto` | Skill `description` frontmatter dispatch | Already covered, arguably better |
| Hooks (blockable) | Claude Code hooks; `settings.json` | Already covered; borrow the gate placement, not the mechanism |
| Approval gates | `readiness.md` gate before `done/`, `sdd/readiness-checklist` | Ours gates the *exit*; Kiro gates the *entry*. Add an entry gate. |

Corpus impact: **no new domain**. At most one new methodology under `sdd/` for the requirements-entry gate, plus edits to `spec-requirements`. Nothing here justifies touching `tier-manifest.json` structure.

## Open questions / staleness risk

- **High churn.** IDE 1.0.138 on 2026-07-13, CLI 2.16.0 on 2026-07-31 — this product ships weekly. Every version, price and doc quote here is pinned to **2026-08-03** and should be re-checked before any public claim.
- **Pricing volatility.** The five-tier credit ladder is ~9 months old at GA+1. Credit-metered AI pricing across the segment has moved repeatedly; treat the table as perishable.
- **Approval-gate semantics may harden.** The docs currently read as soft checkpoints. If AWS makes them enforcing, Claim 1's overstatement becomes true and this dossier's §Claim 1 needs a rewrite.
- **Unverified:** exact preview launch day (July 2025 reported, day not pinned from a primary source); whether Kiro CLI's steering/hooks surface is identical to the IDE's (CLI docs live at separate URLs `kiro.dev/docs/cli/steering/` and were not fetched in full).
- **Unverified:** whether any Kiro-adjacent MCP server or community plugin performs EARS validation. Wikipedia mentions "community plugins via Model Context Protocol servers" for EARS but names none; the web-search budget was exhausted before this could be run down. If one exists and is credible, it changes the competitive framing in §Claim 2 — **re-check before launch messaging**.
- **Web-search budget exhausted at 200/200 on 2026-08-03**; two intended searches (VS Code Marketplace for EARS extensions; StrictDoc/Doorstop/rmtoo EARS support) were not executed. GitHub repo search was reached via WebFetch instead, so the OSS picture is solid; the VS Code Marketplace and the Python requirements-tooling ecosystem remain partly unaudited.
