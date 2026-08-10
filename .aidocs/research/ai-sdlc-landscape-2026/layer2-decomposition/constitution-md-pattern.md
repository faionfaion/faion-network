# The `constitution.md` Pattern
**Layer:** 2 — Decomposition · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
A `constitution.md` is a single, short, always-loaded, versioned file holding the small set of rules a project will not break, each with the reason it exists and an explicit procedure for changing it. It is not a style guide, not architecture documentation, and not a spec: it is the appeal court that other documents and other agents cite when they disagree. Three independent systems converged on the same artifact — GitHub Spec Kit calls it `.specify/memory/constitution.md`, Agent OS splits the same job across `agent-os/standards/` + `agent-os/product/`, and our SDD calls it `constitution.md` at the project root. The pattern is worth taking; none of the three implementations is worth taking whole.

## Current state
The pattern has no version. Its three reference implementations do:

| Implementation | Artifact | Version / date | Enforced by | Source |
|---|---|---|---|---|
| **GitHub Spec Kit** | `.specify/memory/constitution.md` | tool v0.15.2, released 2026-08-03; template `templates/constitution-template.md` | Nothing mechanical. Cited as authority by `templates/commands/converge.md` and the `/plan` Constitution Gate — both LLM-obeyed prose | GitHub API + raw files, 2026-08-03 |
| **Spec Kit's own constitution** (a real, filled example) | 13,252 bytes · 1,743 words · 214 lines · 5 principles + 3 sections | **v1.0.0, Ratified 2026-06-19, Last Amended 2026-06-19** | self-declared: "Every PR and review MUST verify compliance… Unjustified violations block merge" | raw.githubusercontent.com, 2026-08-03 |
| **Agent OS v3** | no single file — `agent-os/standards/*.md` + `index.yml` + `agent-os/product/{mission,roadmap,tech-stack}.md` | v3.0.0, 2026-01-20; last push 2026-05-05 | Nothing. Loaded on demand via `/inject-standards` | raw files + CHANGELOG, 2026-08-03 |
| **faion SDD (ours)** | `constitution.md` at project root; declares where `project-spec/` lives | no version field, no amendment procedure, no size cap | pre-commit hooks enforce adjacent rules (CHANGELOG.md); the constitution itself is unenforced | repo root `AGENTS.md`, read 2026-08-03 |

**Claim 4 adjudicated — "`constitution.md` is the single most stealable idea in Spec Kit, independent of the tool": CONFIRMED.** Evidence, all dated 2026-08-03: (a) it is the only Spec Kit artifact with a defined lifecycle independent of the command chain — semver, a ratification date, an amendment procedure, and a Sync Impact Report; (b) it is the only artifact that a *different* command treats as authority — `converge.md` states "The project constitution (`/memory/constitution.md`) is **non-negotiable**. Code that violates a MUST principle is the highest-severity finding"; (c) it survives deleting every other file — `spec.md`/`plan.md`/`tasks.md` are per-feature and disposable, the constitution is not; (d) it is the one file whose value does not depend on running `specify` at all. Everything else in Spec Kit is choreography around an agent; this is a durable asset the owner keeps.

## Mechanics

### How Spec Kit defines it
`templates/constitution-template.md` (fetched 2026-08-03) is a fill-in-the-blanks skeleton with a fixed shape:
```markdown
# [PROJECT_NAME] Constitution
## Core Principles
### [PRINCIPLE_1_NAME]      <!-- e.g. "I. Library-First" -->
[PRINCIPLE_1_DESCRIPTION]
### [PRINCIPLE_2_NAME] … through [PRINCIPLE_5_NAME]
## [SECTION_2_NAME]         <!-- e.g. Additional Constraints, Security Requirements -->
## [SECTION_3_NAME]         <!-- e.g. Development Workflow, Review Process, Quality Gates -->
## Governance
**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
```
Five principle slots, two free-form sections, a Governance section, and a version footer. Principles are numbered with Roman numerals and may be marked `(NON-NEGOTIABLE)` — Spec Kit's own constitution uses this on exactly one principle: *"II. Test-Backed Change (NON-NEGOTIABLE)"*. The template's inline comments push a specific voice: statements are imperative and testable ("Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr"), not aspirational.

The `/speckit.constitution` command (`templates/commands/constitution.md`, fetched 2026-08-03) enforces the lifecycle in prose:
- **Semver on a prose document.** MAJOR = backward-incompatible governance/principle removal or redefinition. MINOR = new principle/section added, or materially expanded guidance. PATCH = clarifications, wording, typo fixes, non-semantic refinements. *"If version bump type ambiguous, propose reasoning before finalizing."*
- **No placeholders may survive.** "Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet — explicitly justify any left)."
- **Governance must contain three things:** the amendment procedure, the versioning policy, and compliance-review expectations.
- **Sync Impact Report** — prepended as an HTML comment at the top of the file on every update: version change old → new, modified principles (old title → new title if renamed), added sections, removed sections, follow-up TODOs.
- **Unknowns become tracked debt:** `TODO(<FIELD_NAME>): explanation`, listed in the Sync Impact Report as deferred.
- **Never regenerate:** "Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file."

Real headings from Spec Kit's own filled constitution (v1.0.0, ratified 2026-06-19): *I. Code Quality & Architectural Discipline · II. Test-Backed Change (NON-NEGOTIABLE) · III. CLI & User-Experience Consistency · IV. Offline-First Performance & Resource Discipline · V. Minimal Dependencies & Safe, Idempotent File Operations*, then *Security & Cross-Platform Constraints*, *Development Workflow & Quality Gates*, *Governance*. Note that at 1,743 words for 5 principles they are averaging ~350 words per principle — well past "scannable".

### How Agent OS defines it
Agent OS has no constitution file and this is a deliberate design choice. The same job is split three ways:
- **`agent-os/standards/`** — many small files (`api/response-format.md`, `database/migrations.md`, `root/naming.md`), each one rule-cluster, each written under the standing instruction: *"Write concise standards — use minimal words. Standards must be scannable by AI agents without bloating context windows."*
- **`agent-os/standards/index.yml`** — slug → one-line description, rebuilt by `/index-standards`, so the agent can pick which standards to load without reading them all.
- **`agent-os/product/{mission,roadmap,tech-stack}.md`** — the "what this product is" layer, authored by `/plan-product`.

Loading is **on demand**, via `/inject-standards`, which auto-suggests from `index.yml` or takes explicit paths (`/inject-standards api/response-format`). Crucially it formats differently per consumer: **full text** into a conversation, **file references** into a Skill or a plan. And `/discover-standards` step 3 is titled *"Ask Why, Then Draft Each Standard"* — the rationale is obtained from the human before the standard is written.

**The trade Agent OS made:** many small on-demand files instead of one always-loaded file. It buys unlimited total volume and pays with retrieval risk — a standard that is never injected has zero effect, and the agent decides. Spec Kit made the opposite trade.

### How ours defines it
Per the repo root `AGENTS.md` (read 2026-08-03): *"**constitution.md** — Tech decisions, standards, architecture. Declares per-project `project-spec/` location."* It sits alongside `roadmap.md` in the SDD document set, above the feature lifecycle `backlog/ → todo/ → in-progress/ → done/`.

Ours is the only one of the three that solves the **delegation** problem — the constitution does not try to contain the domain model, it *declares where the domain model lives* (`project-spec/`: domain, business rules, data model, deploy, invariants). That indirection is why our `spec.md` can be delta-only. Spec Kit has no equivalent and consequently pulls everything toward one file.

What ours is missing, measured against the other two: **no version field, no ratification date, no amendment procedure, no item cap, no required "why" per item, and no statement of what happens when code violates it.** It is a document with authority and no constitutional law.

### What belongs in it
A rule belongs in the constitution if it passes all four:
1. **Durable** — it outlives the current feature. If it changes when a feature ships, it belongs in `spec.md` or `plan.md`.
2. **Cross-cutting** — it constrains more than one area. A rule about one module belongs in that module's `AGENTS.md`.
3. **Contestable** — a competent person could reasonably have decided otherwise. If it is the framework default or industry-standard behavior, writing it down is noise. (Agent OS's filter — *unusual · opinionated · tribal · consistent* — is the sharpest phrasing of this test.)
4. **Checkable** — a reviewer can say violated / not violated without a debate. "Write clean code" fails. "No `print()` in production Python (ruff T20)" passes.

Concretely, it belongs in the constitution: non-negotiable technical invariants (single Go binary, offline-first, no async without explicit approval); quality floors that block a merge (pre-commit hooks are mandatory, never `--no-verify`); language and documentation policy (docs/code English, user Ukrainian, no ASCII art, no emoji in commits); the commit and CHANGELOG contract; the pointer to `project-spec/`; the amendment procedure itself; and the compliance statement — what actually happens when a rule is broken.

### What does not belong in it
- **The domain model, business rules, data model, deploy topology.** These live in `project-spec/`. The constitution names the path; it does not inline the content. This is the boundary Spec Kit lacks and the main reason its own constitution reached 1,743 words.
- **Anything feature-scoped.** Requirements, acceptance criteria, user flows, UI decisions → `spec.md`, `user-flows.md`, `ui-ux-design.md`.
- **Anything the linter already enforces.** If `ruff`/ESLint/pre-commit fails the build, the rule is enforced by machine; restating it in prose costs tokens on every load and buys nothing. State the *policy* ("hooks are mandatory, fix the cause, never skip") once; do not restate the rule list.
- **Tutorials, rationale essays, architecture diagrams, ADRs.** ADRs are per-decision and append-only (`sdd/architecture-decision-records`). The constitution is the small standing set; an ADR is the record of one change to it.
- **Aspirations.** "We value quality." Unfalsifiable, unenforceable, pure token cost.
- **Roadmap, timeline, or anything with a date in it** other than the ratification and amendment dates.
- **A default tech stack you did not choose.** Agent OS ships `profiles/default/global/tech-stack.md` pre-filled with React 18 + Tailwind v4 + Vite + Node/Express + PostgreSQL (fetched 2026-08-03). A constitution that arrives pre-populated with someone else's opinions gets ignored wholesale, which destroys the authority of the parts that were real.

### The user's four proposed rules — assessed
| Rule | Verdict | Reasoning |
|---|---|---|
| **10-20 items max** | **Adopt, as a hard cap.** | Directly supported by measurement: Spec Kit's own constitution is 5 principles / 1,743 words — averaging ~350 words each, which is a section, not a rule. A cap forces the "is this contestable?" test to actually bite. 10-20 *items* at 20-40 words each lands the file at ~400-700 words, roughly a quarter of Spec Kit's. Enforce it mechanically (a word/item count in a pre-commit hook), because a soft cap is not a cap. |
| **Each item has a "why"** | **Adopt, with a length limit.** | Agent OS makes this a *procedure* — `/discover-standards` step 3 is "Ask Why, Then Draft Each Standard", and it obtains the why from the human before writing. Two effects: a rule nobody can justify never gets written (the cap defends itself), and an agent that knows *why* can reason about edge cases instead of applying the rule blindly. Cap the why at one sentence, or it becomes the essay the cap was meant to prevent. |
| **Explicit amendment procedure** | **Adopt, borrowing Spec Kit's semver + Sync Impact Report.** | This is the piece we are missing outright. Spec Kit's MAJOR/MINOR/PATCH definitions for a prose document are directly reusable, as is the machine-readable HTML-comment diff header. Without an amendment procedure a constitution either ossifies (nobody dares change it, so it drifts from reality and gets ignored) or erodes silently (anyone edits it, so it means nothing). For a solopreneur the procedure is short — but it must be *written*, because "future me" is a different person than "me now". |
| **Always-loaded, not on-demand** | **Adopt — with the size cap as its precondition.** | These two rules are one rule. On-demand loading is what Agent OS chose, and its failure mode is silent: a standard that is never injected has zero effect, and the *agent* decides whether to inject. For rules that must never be broken, "the model chose not to retrieve it" is not an acceptable failure mode. But always-loaded is only affordable if the file is small — which is exactly why the 10-20 cap is not a style preference but the enabling constraint. Corollary: anything that cannot fit in the always-loaded file must be *referenced* from it (`project-spec/`, methodology slugs) so the pointer is always loaded even when the content is not. |

### Token cost of always-loading — measured
Measured against real files on 2026-08-03. Token estimates use ~3.7 bytes/token for English markdown; treat as ±10%.

| File | Bytes | Words | ≈ Tokens | % of a 200k window | % of a 1M window |
|---|---|---|---|---|---|
| Spec Kit's own `constitution.md` (v1.0.0) | 13,252 | 1,743 | **~3,600** | 1.8% | 0.36% |
| A 20-item constitution at ~35 words/item incl. "why" | ~4,600 | ~700 | **~1,250** | 0.6% | 0.13% |
| A 12-item constitution at ~35 words/item | ~2,800 | ~420 | **~750** | 0.4% | 0.08% |

The per-load number is not the cost. Three multipliers are:
1. **Every session start.** One load per session, plus one per context compaction. A long working day is easily 5-15 loads.
2. **Every subagent.** This is the real bill. A constitution injected into a fan-out of 8 subagents costs 8× per wave. At our pool sizes (7-language translation fan-outs, batch SDD executors) a 3,600-token constitution costs ~29k tokens per wave; a 750-token one costs ~6k. Over a multi-wave batch the difference is measured in hundreds of thousands of tokens.
3. **Attention dilution, which has no token price.** A 1,743-word document read on every turn competes with the actual task. Past roughly a page, additional rules do not reliably change behavior — they just cost money. This is why the cap is a *behavioral* argument first and an economic one second.

**Mitigation that keeps the always-loaded guarantee:** put the constitution at a stable position in the prompt so it sits inside the cached prefix. It is the ideal cache candidate — small, identical across every call in a session, and changed only by an explicit amendment. A constitution that changes on every load is not a constitution.

**The rule that follows from the arithmetic:** always-loaded is affordable only under a hard cap. Choose one — a small always-loaded file, or a large on-demand corpus. A large always-loaded file is the one combination that is wrong.

## Recommended template
Target: ≤ 20 items, ≤ 700 words total, ≤ ~1,300 tokens.

```markdown
<!--
Sync Impact Report
Version: 1.2.0 → 1.3.0
Modified: R-04 "No async Python" → "No concurrency primitives without approval"
Added: R-17 (offline-first)
Removed: none
Deferred: TODO(SECURITY_REVIEW_CADENCE): not yet decided
-->

# <Project> Constitution

**Version:** 1.3.0 · **Ratified:** 2026-06-19 · **Last amended:** 2026-08-03
**Project spec:** `.product/project-spec/`   <!-- the constitution declares, it does not inline -->

## Scope
This file holds the rules this project does not break. Everything else lives
elsewhere: domain and data model in `project-spec/`, feature requirements in
`spec.md`, per-module conventions in that module's `AGENTS.md`.
Max 20 rules. Adding one means justifying it or removing another.

## Rules

### R-01 — Single Go binary, no runtime dependencies (NON-NEGOTIABLE)
*Why:* cross-platform install for non-technical users is the product; any runtime
dependency reintroduces the install failure we exist to remove.

### R-02 — Pre-commit hooks are mandatory; never `--no-verify`
*Why:* the hook is the only automated gate between a bad commit and main.
A skipped hook is an unreviewed change.

### R-03 — Docs and code in English; user-facing conversation in Ukrainian
*Why:* English source saves ~30% tokens on every agent read; the user reads Ukrainian.

### R-04 — No concurrency primitives (asyncio, threads) without explicit approval
*Why:* every concurrency bug we have shipped cost more to diagnose than the
throughput it bought. Exceptions are named per-project, not assumed.

… (R-05 … R-N, same shape, ≤ 40 words each including the why)

## Compliance
Violating a rule blocks the change. A violation that is genuinely warranted is
justified in the commit body and, if it recurs, becomes an amendment — not a habit.
Agents cite the rule id (`R-04`) when they refuse; humans do the same when they override.

## Amendment procedure
1. Amendments are proposed as a diff to this file, never as a verbal exception.
2. Version bump: **MAJOR** = a rule removed or its meaning reversed ·
   **MINOR** = a rule added or materially widened · **PATCH** = wording only.
3. Update the `Last amended` date and prepend a Sync Impact Report comment.
4. If the change invalidates something in `project-spec/` or a `plan.md`, that is
   named in the report as a follow-up TODO.
5. Unknowns are recorded as `TODO(<FIELD>): explanation`, never left as a blank.
```

Design notes on the template: stable rule **ids** (`R-04`) so agents, commits and refusals can cite them and so a renamed rule is still traceable; the `**Project spec:**` pointer in the header is the delegation boundary that keeps the file small; the Sync Impact Report is an HTML comment so it is machine-readable and invisible when rendered; `(NON-NEGOTIABLE)` is reserved for the rules that block a merge, and if more than three carry it the tag has stopped meaning anything.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Spec Kit `templates/constitution-template.md` | https://raw.githubusercontent.com/github/spec-kit/main/templates/constitution-template.md | 5 principle slots, 2 free sections, Governance, version footer | 2026-08-03 |
| 2 | Spec Kit `templates/commands/constitution.md` | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/constitution.md | semver bump rules; Sync Impact Report; `TODO(<FIELD>)`; never regenerate | 2026-08-03 |
| 3 | Spec Kit's own `.specify/memory/constitution.md` | https://raw.githubusercontent.com/github/spec-kit/main/.specify/memory/constitution.md | filled real example: v1.0.0, ratified 2026-06-19; 13,252 B / 1,743 w / 214 lines; 5 principles | 2026-08-03 |
| 4 | Spec Kit `templates/commands/converge.md` | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/converge.md | "constitution is **non-negotiable**"; MUST-violations are highest severity; skip gracefully if unfilled | 2026-08-03 |
| 5 | Agent OS `commands/agent-os/inject-standards.md` | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/inject-standards.md | on-demand loading; full-text vs file-reference per consumer; `root` keyword | 2026-08-03 |
| 6 | Agent OS `commands/agent-os/discover-standards.md` | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/discover-standards.md | "Ask Why, Then Draft"; unusual/opinionated/tribal/consistent filter; "minimal words… without bloating context windows" | 2026-08-03 |
| 7 | Agent OS `commands/agent-os/index-standards.md` | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/index-standards.md | `index.yml` as retrieval index over prose standards | 2026-08-03 |
| 8 | Agent OS `profiles/default/global/tech-stack.md` | https://raw.githubusercontent.com/buildermethods/agent-os/main/profiles/default/global/tech-stack.md | pre-filled default stack — the anti-pattern | 2026-08-03 |
| 9 | Agent OS CHANGELOG `## [3.0] - 2026-01-20` | https://raw.githubusercontent.com/buildermethods/agent-os/main/CHANGELOG.md | why the standards layer was kept while the pipeline was deleted | 2026-08-03 |
| 10 | faion-network repo root `AGENTS.md` | `~/workspace/projects/faion-net/faion-network/AGENTS.md` | our `constitution.md` definition; SDD document set; lifecycle | read 2026-08-03 |
| 11 | `skills/faion/knowledge/sdd/INDEX.xml` | local | v3.0, `count="90"`, generated 2026-05-25 — used for the corpus mapping below | read 2026-08-03 |

## What to borrow for faion
1. **Semver + ratification date + `Last amended` on our `constitution.md`.** Three lines, immediate. It is the difference between a document with authority and a document with a date.
2. **The Sync Impact Report as an HTML comment.** Machine-readable amendment history that costs nothing when rendered and gives an agent the diff without a `git log`.
3. **A hard item cap enforced by a pre-commit hook.** We already require CHANGELOG.md via a hook; the same mechanism can count rules and words. The cap is the whole pattern — everything else follows from it.
4. **A "why" per rule, obtained before the rule is written** (Agent OS's procedure, not just a template field).
5. **Stable rule ids so refusals are citable.** An agent that says "blocked by R-04" is auditable; one that says "that seems risky" is not.
6. **A written Compliance section.** Spec Kit's constitution states that unjustified violations block merge; ours states nothing. A rule with no stated consequence is a suggestion.
7. **The `TODO(<FIELD>): explanation` convention** for known unknowns, so a gap is tracked debt rather than an invisible blank.
8. **Keep our delegation pointer** — `constitution.md` declaring where `project-spec/` lives is the one place we are ahead of both tools, and it is what makes the cap achievable. Do not lose it while borrowing.

## What NOT to borrow — and why
1. **Spec Kit's five-principle-section shape.** Its own filled example runs 1,743 words — ~350 per principle. That is an essay collection, not a constitution, and it is the direct cause of the token cost measured above. Take the *lifecycle* mechanics; reject the shape.
2. **`.specify/memory/` as the location.** Burying the highest-authority document three levels into a tool-owned directory hides it from the human who is supposed to own it. Ours belongs at the project root where a non-technical owner will actually see it.
3. **Agent OS's on-demand loading for constitutional rules.** Correct for a large standards corpus, wrong for non-negotiables: it makes the agent the gatekeeper of whether a rule applies. Use on-demand for `project-spec/` and methodology content; never for the constitution.
4. **A pre-filled default constitution.** See Agent OS's `tech-stack.md`. Ship an empty template with worked *examples in comments* (Spec Kit does this correctly — every slot has an `<!-- Example: … -->`), never pre-made opinions.
5. **Free-form `[SECTION_2_NAME]` / `[SECTION_3_NAME]` slots.** An unnamed section is where the cap goes to die. Fixed sections only: Scope, Rules, Compliance, Amendment procedure.
6. **Restating linter rules in prose.** Our own root `AGENTS.md` currently inlines a ruff quick-reference and a per-project lint tool table. That is documentation, not constitution — it belongs in `.agents/`, and inlining it into an always-loaded file is exactly the cost this dossier is about.

## Mapping to our corpus
Verified against `skills/faion/knowledge/sdd/INDEX.xml` (v3.0, `count="90"`, generated 2026-05-25), `skills/faion/knowledge/sdlc-ai/INDEX.xml`, and `skills/tier-manifest.json` (v8, 3070 entries, updated 2026-05-07).

**Searched for an existing constitution methodology: there is none.** `find skills -iname "*constitution*"` returns zero directories (2026-08-03), and `grep constitution skills/tier-manifest.json` returns zero entries. The only mention anywhere in the corpus is the tag `constitution-gate` and the rule `constitution-gate-evidence` inside `sdlc-ai/task-spec-kit-three-step` (geek, v1.1.0) — which requires `plan.md` to contain a `Constitution Gate` section citing the standards consulted, but never defines what a constitution *is* or how to write one. **The document our own root `AGENTS.md` names first in the SDD document list has no methodology behind it.**

**Adjacent, partially overlapping:**
- `sdd/architecture-decision-records` + `sdd/architecture-decision-records-planning` (solo) and `sdd/adr-consequence-evidence-binding` (geek) — ADRs are the per-decision record; the constitution is the standing set. Complementary, and the boundary between them needs stating explicitly in whatever we write.
- `sdd/client-conventions-as-code` (pro) — closest existing slug in spirit; scoped to client engagements, not to the owner's own project constitution.
- `sdd/definition-of-done-template` (pro), `sdd/definition-of-ready-template` (pro), `sdd/definition-of-done-multi-role` (geek) — standing criteria, but gate-scoped rather than project-scoped.
- `sdd/quality-gates-confidence` (solo) — the enforcement side of a Compliance section.
- `sdlc-ai/ai-convention-anchoring` (solo) and `sdlc-ai/kb-agents-md-context-pyramid` (geek) — the always-loaded-context mechanics the token-cost section depends on.
- `sdlc-ai/gov-conventional-commits-enforced`, `gov-license-compliance-scan`, `gov-sonarqube-ai-code-gate` (all geek) — mechanical governance; the constitution is the human-readable layer above them.
- `sdlc-ai/adr-supersession-detection` (geek) and `sdd/decision-log-reconstruction-from-git` (pro) — amendment-drift detection; reusable for detecting a constitution that has quietly stopped matching the code.
- `sdd/project-spec-structure` — the delegation target our constitution points at. **Exists on disk, absent from `INDEX.xml` and `tier-manifest.json`.**

**Proposed new methodology:**
- **slug:** `constitution-md` · **domain:** `sdd` · **tier:** **`free`**
  The pattern as documented here: what belongs in it and what does not (the four-part durable/cross-cutting/contestable/checkable test), the ≤20-item cap and why the cap is the enabling constraint for always-loading, one-sentence "why" per rule obtained before writing, stable rule ids, a Compliance statement, semver + ratification/amendment dates + Sync Impact Report, and the delegation pointer to `project-spec/`. Ships the template above plus a validator script (count rules, count words, assert every rule has a why, assert the version footer parses, assert no unreplaced `[PLACEHOLDER]`).
  **Tier rationale — `free`, deliberately.** It is the first file a new user creates, it is the artifact that makes every other methodology land correctly, and at 129 free entries out of 3,070 the free tier's job is to demonstrate that the corpus is worth paying for. A constitution the user writes on day one and reads every day afterwards is the strongest possible free-tier exhibit. It also has no dependency on any paid methodology.
- **Companion, tier `pro`:** `constitution-amendment-protocol` — only if the amendment mechanics outgrow a section of the above. Default position: keep it in one file. A pattern about brevity should not ship as three documents.

**Corpus defect blocking this (third dossier to report it):**
`skills/faion/knowledge/sdd/` holds **99** directories; `INDEX.xml` declares **90**. Absent from both `INDEX.xml` and `tier-manifest.json`: `project-spec-structure`, `plan-md-structure`, `quality-gates`, `readiness-checklist`, `user-flows-template`, `ui-ux-design-template`, `cr-bug-tracking`. Root `AGENTS.md` cites every one of them by name as the authority for a lifecycle document. Until the index and manifest are regenerated, a `constitution-md` methodology that points at `sdd/project-spec-structure` would point at something the retriever cannot reach and the tier gate does not know exists.

## Open questions / staleness risk
- **Staleness: low.** This is a pattern, not a release. The Spec Kit mechanics cited (semver, Sync Impact Report) are stable across 0.11 → 0.15; the Agent OS side has not moved since 2026-05-05. The item most likely to rot is the token arithmetic, which depends on context-window sizes and subagent fan-out costs.
- **The 10-20 cap is asserted, not measured.** The evidence is directional (Spec Kit's own file is 1,743 words and its authors are the pattern's inventors) but nobody has run an experiment on where added rules stop changing model behavior. Do not present the number as empirical in customer-facing copy — present it as a forcing constraint, which is defensible on its own terms.
- **Untested for non-technical users.** Every worked example in all three implementations is code-shaped. Whether a non-technical solopreneur can write 12 contestable, checkable rules about their own product is unknown, and it is the single highest-value thing to test before shipping `constitution-md` at the free tier. A different question set — closer to "what have you had to explain twice?" — may be required.
- **Enforcement is unsolved.** Every implementation surveyed, including ours, enforces the constitution by asking a model to obey prose. The only mechanical enforcement possible is structural (item count, required sections, version footer parses, every rule has a why) — never semantic. Be honest about that boundary in the methodology rather than implying the file is a gate.
- **Interaction with prompt caching not verified.** The claim that a stable constitution sits inside the cached prefix is architecturally sound but was not measured against a live harness; the placement rules differ per runtime (Claude Code vs our Go CLI vs subagent spawns).
