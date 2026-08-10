# BMAD PRFAQ (Working Backwards)
**Layer:** 2 — Decomposition · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

`bmad-prfaq` is BMAD's implementation of Amazon's **Working Backwards** method: before building anything, write the press release announcing the finished product, then answer the hardest questions a customer and a skeptical stakeholder would ask. If you can't write a compelling press release, the product isn't ready.

BMAD's framing, verbatim from the shipped `SKILL.md` (read 2026-08-03):

> "Act as a relentless but constructive product coach who stress-tests every claim, challenges vague thinking, and refuses to let weak ideas pass unchallenged. The user walks in with an idea. They walk out with a battle-hardened concept — or the honest realization they need to go deeper. **Both are wins.**"
>
> "**This is hardcore mode.** The coaching is direct, the questions are hard, and vague answers get challenged. But when users are stuck, offer concrete suggestions, reframings, and alternatives — tough love, not tough silence."

**This is the one piece of BMAD with zero software dependency.** It reads no code, writes no code, and touches no repository. Its only inputs are a human with an idea and optionally some documents. It works identically for a SaaS product, a coaching programme, a physical product, a nonprofit initiative, or an internal tool — and the skill explicitly detects which of those it is (see `{concept_type}` below).

### Adjudicating the landscape-doc claim #2

> *"PRFAQ skill — Amazon Working Backwards, 5-phase interactive review. A pure product instrument, not an engineering one."* 🟢

**Confirmed on all three counts**, read directly from `skills/bmad-prfaq/SKILL.md` and `references/*` on 2026-08-03:

1. ✅ **Amazon Working Backwards** — named as such in the skill's own overview.
2. ✅ **5 phases** — the skill ships an explicit stage table with exactly five rows (reproduced below). BMAD calls them "Stages", not "phases"; the count is right.
3. ✅ **Pure product instrument** — its `bmad-manifest.json` places it in `"phase-name": "1-analysis"`, `preceded-by: [brainstorming, perform-research]`, `followed-by: [create-prd]`, `is_required: false`. It sits entirely upstream of anything engineering-shaped. Its two subagents do document scanning and web research; neither reads source code.

One nuance the claim misses: it is **not purely interactive**. It ships a `--headless` / `-H` mode that produces a complete first-draft PRFAQ from structured input with no conversation at all.

## Current state

| Fact | Value | Source & date |
|---|---|---|
| Arrival | Shipped with **BMAD v6.3.0, 2026-04-09** ("Amazon PRFAQ methodology" listed among the release's 13 new features) | CHANGELOG.md + vibesparking write-up, 2026-08-03 |
| Version line | Present and unchanged through v6.10.0 (2026-07-03); **not** on the deprecated list | CHANGELOG.md, 2026-08-03 |
| License / price | MIT, free (BMad Code, LLC) | LICENSE, 2026-08-03 |
| Size as shipped | 596 lines across 9 files: `SKILL.md` 135, `customize.toml` 41, 4 `references/` (55+51+60+83), `assets/prfaq-template.md` 62, 2 `agents/` (60+49) | local read, 2026-08-03 |
| Also shipped as | **PRFAQ Coach** web bundle (Gemini Gem / ChatGPT Custom GPT), `web-bundles-v1.0.0`, released **2026-05-25** — `SKILL.md` 11,223 B + `INSTRUCTIONS.md` 5,023 B | `web-bundles/bundles.json` + contents API, 2026-08-03 |
| Web-bundle persona lineage | "Working Backwards PRFAQ challenge (**Bezos lineage**) to forge and stress-test product concepts" | `web-bundles/README.md`, 2026-08-03 |

The web-bundle existence is itself evidence for the 🟢: BMAD's maintainers picked six skills worth running *outside* an IDE, and PRFAQ is one of them. See `flat-rate-planning.md`.

## Mechanics

Reimplementable from this section alone.

### The five stages

| # | Stage | Purpose | Lives in |
|---|---|---|---|
| 1 | **Ignition** | Raw concept on the table; enforce customer-first thinking | `SKILL.md` |
| 2 | **The Press Release** | Iterative drafting with hard coaching | `references/press-release.md` |
| 3 | **Customer FAQ** | Devil's-advocate customer questions | `references/customer-faq.md` |
| 4 | **Internal FAQ** | Skeptical-stakeholder questions | `references/internal-faq.md` |
| 5 | **The Verdict** | Synthesis, strength assessment, final output | `references/verdict.md` |

Table reproduced from `SKILL.md` (2026-08-03). The routing pattern matters: `SKILL.md` holds only Stage 1 and dispatches to one reference file per subsequent stage. That is progressive disclosure — the model never loads Stage 4's question bank while doing Stage 2.

### Activation and modes

Standard BMAD activation contract (resolve `customize.toml` merge → prepend steps → persistent facts → load `_bmad/bmm/config.yaml` → greet in `{communication_language}` → append steps).

Two modes:

- **Default — full interactive coaching.** The skill's own word for it: *"the gauntlet."*
- **`--headless` / `-H`** — autonomous first draft. Validates the input schema only (**required**: customer as a specific persona, problem as concrete, stakes, solution concept; **optional**: competitive context, technical constraints, team/org context, target market, existing research). Missing or vague required fields return an error with specific guidance rather than a hallucinated draft. Explicitly instructed *not* to read referenced files itself — it fans out to subagents.

**Resume detection:** checks whether `{planning_artifacts}/prfaq-{project_name}.md` exists; if so, reads **only the first 20 lines** to extract the frontmatter `stage` field and offers to resume from the next stage. "Do not read the full document." A cheap, disciplined resume that doesn't reload the artefact into context.

### Stage 1 in detail (the part that generalises furthest)

**Customer-first enforcement**, three branches:
- User leads with a solution ("I want to build X") → redirect to the customer's problem. "Don't let them skip the pain."
- User leads with a technology ("I want to use AI/blockchain") → "challenge harder. Technology is a 'how', not a 'why'… Strip away the buzzword and ask whether anyone still cares."
- User leads with a customer problem → dig into specifics: how they cope today, what they've tried, why it hasn't been solved.

**`{concept_type}` detection** — commercial product / internal tool / open-source project / community-nonprofit initiative. Stored early and used to calibrate FAQ generation in Stages 3–4: *"Non-commercial concepts don't have 'unit economics' or 'first 100 customers' — adapt the framing to stakeholder value, adoption paths, and sustainability instead."* **This single variable is what makes the skill domain-portable**, and it is the highest-value idea in the whole file.

**Four essentials before progressing:** who is the customer (specific persona, not "everyone"); what is their problem (concrete and felt, not abstract); why does it matter (stakes and consequences); what's the initial solution concept (even rough).

**Fast-track:** if all four arrive in the opening message, acknowledge, confirm understanding, skip extended discovery, go straight to document creation and Stage 2.

**Graceful redirect:** after 2–3 exchanges with no articulable customer or problem, stop forcing it and route upstream — `bmad-brainstorming` to generate options, `bmad-forge-idea` to pressure-test an unhardened idea. *A quality gate that knows how to fail is worth more than one that grinds.*

**Contextual Gathering** — two subagents fanned out in parallel:
- **Artifact Analyzer** (`agents/artifact-analyzer.md`, 60 lines) — scans `{planning_artifacts}` and `{project_knowledge}` plus user-supplied paths; receives the product-intent summary so it knows what's relevant.
- **Web Researcher** (`agents/web-researcher.md`, 49 lines) — competitive landscape, market context, current industry data; same intent summary.
- **Graceful degradation:** if subagents are unavailable, scan the 1–2 most relevant documents inline and do targeted web searches directly. *"Never block the workflow."*
- Merge findings and **surface anything surprising that challenges the user's assumptions before proceeding.**

**Research-grounded** is a stated hard rule: *"All competitive, market, and feasibility claims in the output must be verified against current real-world data… the user deserves a PRFAQ informed by today's landscape, not yesterday's assumptions."*

**Coaching Notes Capture** — before leaving each stage, append a `<!-- coaching-notes-stage-N -->` block to the output document recording: concept type and rationale, assumptions challenged, why this direction over discussed alternatives, key subagent findings that shaped the framing, and user context that doesn't fit the PRFAQ itself. **This is the decision-provenance mechanism** — the reasoning survives inside the artefact instead of dying in the chat log.

### Output

- Working artefact: `{planning_artifacts}/prfaq-{project_name}.md`, created from `assets/prfaq-template.md` (62 lines) at the end of Stage 1, with frontmatter carrying `stage` and `inputs` (source documents used), updated progressively through all five stages.
- Declared deliverable: *"A complete PRFAQ document + PRD distillate for downstream pipeline consumption."* The distillate is what `followed-by: ["create-prd"]` consumes.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | `bmad-prfaq/SKILL.md` (135 lines) | local: `skills/bmad-prfaq/SKILL.md` | Overview, hardcore-mode framing, activation contract, headless schema, resume detection, Stage 1 in full, the five-stage table | 2026-08-03 |
| 2 | `bmad-prfaq/bmad-manifest.json` | local | `module-code: bmm`, `menu-code: WB`, `phase-name: 1-analysis`, preceded-by/followed-by, `output-location` | 2026-08-03 |
| 3 | `references/press-release.md` (60) · `customer-faq.md` (55) · `internal-faq.md` (51) · `verdict.md` (83) | local | Stages 2–5, one file each | 2026-08-03 |
| 4 | `assets/prfaq-template.md` (62) · `agents/artifact-analyzer.md` (60) · `agents/web-researcher.md` (49) | local | Output template + the two parallel subagents | 2026-08-03 |
| 5 | `web-bundles/bundles.json` | `gh api repos/bmad-code-org/BMAD-METHOD/contents/web-bundles/bundles.json` | `releaseTag: web-bundles-v1.0.0`, `releasedAt: 2026-05-25`, PRFAQ Coach entry with persona + knowledge-file list | 2026-08-03 |
| 6 | `web-bundles/README.md` | same repo path | Shelf table incl. "PRFAQ Coach — Working Backwards PRFAQ challenge (Bezos lineage)" | 2026-08-03 |
| 7 | CHANGELOG.md | https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md | v6.3.0 @ 2026-04-09; PRFAQ never deprecated through v6.10.0 | 2026-08-03 |

> **Note on Amazon primary sources.** Everything above documents *BMAD's* implementation. Amazon's own Working Backwards material (Colin Bryar & Bill Carr, *Working Backwards*, 2021; the internal PR/FAQ format) was **not** fetched in this pass — my web-search budget was exhausted on the version and pricing adjudications. If we write our own methodology, that primary reading is a prerequisite, not optional. See Open questions.

## What to borrow for faion

1. **The methodology itself — as our own writing.** Confirmed gap: grepping all 22 domain `INDEX.xml` files on 2026-08-03 for `prfaq|working-backward|press-release|amazon` returned **zero hits**. We have 2,622 methodologies and no Working Backwards. For a product aimed at solopreneurs — the exact audience most prone to building the thing before checking anyone wants it — this is a hole in the middle of the value proposition.
2. **`{concept_type}` calibration.** Detect commercial / internal / open-source / community early, and swap the question bank accordingly. This is the mechanism that makes one methodology serve a SaaS founder and a nonprofit organiser without forking it. **Generalise it further than BMAD did** — add "service business", "creative/media product", "physical product". Our corpus already spans `marketing/`, `comms/`, `research/`, `hr/`; a concept-type switch is how a single product-validation methodology reaches all of them.
3. **Stage-file routing.** One entry file holding stage 1 + a dispatch table; one file per subsequent stage. Our methodology dirs already use `content/NN-*.xml` chunks — the borrow is the *explicit routing table with a resume pointer*, so a long methodology can be paused and re-entered without reloading.
4. **Coaching notes as inline decision provenance.** `<!-- coaching-notes-stage-N -->` blocks appended to the artefact. Cheap, human-invisible in rendered markdown, and it means the "why not the alternative" survives. Directly applicable to our `spec.md` / `plan.md` / `readiness.md`.
5. **Graceful redirect on failure.** "After 2–3 exchanges with no articulable customer, stop and route upstream." Every one of our gate-shaped methodologies (`readiness-checklist`, spec validation) should name its upstream escape hatch instead of grinding.
6. **Headless mode with a validated input schema.** Required-vs-optional fields, error-with-guidance on vague input, no hallucinated draft. That is the right contract for any methodology we ever want to run non-interactively.
7. **"Both are wins."** A validation methodology whose stated success condition includes *killing the idea* is honest in a way most product frameworks aren't. Keep that framing in our voice.

## What NOT to borrow — and why

- **The literal text.** MIT permits copying with attribution, but `faion-network` is the thing we sell (3,070 tier-gated entries). Vendoring third-party prose into a commercial knowledge base creates an attribution obligation across a paid product for content we could write better. Write ours from Amazon's public method plus our own practice; cite BMAD as prior art in the research doc, not in the shipped methodology.
- **The `_bmad/` runtime coupling.** `resolve_customization.py`, `_bmad/bmm/config.yaml`, `{planning_artifacts}` — a second config root competing with ours. Our equivalent is `.product/` and `.aidocs/`, declared per-project in `constitution.md`.
- **`--headless` as our default.** BMAD makes interactive the default and headless the escape hatch, and it's right. A PRFAQ auto-generated from four fields is a nicely-formatted guess. Ours should refuse to run headless without evidence, not just without fields.
- **Two subagents as a hard requirement.** BMAD's own graceful-degradation clause admits the workflow must run without them. Our CLI is content-only — search returns hash IDs, `get-content` returns bodies, and we spend zero LLM tokens at runtime on customer work. The methodology must be executable by a human with no agents at all. Write it that way and let the agent-assisted path be an accelerant.
- **"Hardcore mode" as a tone default.** The relentless-coach register is a strong fit for a founder who asked for it and a bad fit for someone doing this for the first time. Make intensity a parameter, not a personality.
- **`menu-code: WB` and the module/menu system.** BMAD-internal navigation UX. We route through `faion search` → hash → `get-content`.

## Mapping to our corpus

Ground truth read 2026-08-03: `tier-manifest.json` v8 (`updated: 2026-05-07`, `last_synced: 2026-05-23`), 3,070 entries — free 129 / solo 841 / pro 1,405 / geek 695.

**The gap, precisely:** `grep -rio '[a-z0-9-]*(prfaq|working-backward|press-release|amazon)[a-z0-9-]*' */INDEX.xml` across all 22 domains → **no matches** (2026-08-03).

**Nearest existing neighbours** (so we place it correctly rather than duplicating):

| Our slug | Domain | Relationship to PRFAQ |
|---|---|---|
| `product-discovery` | `product/` | Upstream — finds the problem; PRFAQ pressure-tests the proposed answer |
| `continuous-discovery`, `continuous-discovery-product-planning`, `discovery-cadence-design` | `product/` | Ongoing discovery loop; PRFAQ is a one-shot gate inside it |
| `discovery-research-handoff-template` | `product/` | The handoff shape PRFAQ's output should match |
| `what-you-dont-know-about-launch-pre-mortem` | `product/` | **Closest sibling** — same adversarial spirit, applied at launch instead of at concept |
| `launch-comms-kit-template`, `product-launch`, `launch-tier-decision-frame` | `product/` | Downstream — the *real* press release; PRFAQ is the imagined one |
| `30-day-post-launch-review-template`, `post-launch-72h-watch-runbook` | `product/` | Closes the loop: did the promised press release come true? |
| `spec-requirements`, `spec-structure`, `template-spec` | `sdd/` | Downstream consumer — PRFAQ's "PRD distillate" feeds `spec.md` |
| `outcome-based-roadmaps`, `roadmap-design` | `pm/` | Consumes a validated concept |
| `ac-quality-rubric` | `product/` | The rubric pattern to reuse for scoring a PRFAQ's strength in Stage 5 |

**Recommended placement:** `skills/faion/knowledge/product/working-backwards-prfaq/`, with a companion `product/prfaq-verdict-rubric/` if Stage 5's assessment is substantial enough to stand alone. Domain `product`, group `product`.

**Tiering:** **solo**. Rationale — it is a core solopreneur instrument (argues for free), but free is deliberately thin at 129 of 3,070 entries (4.2%) and this is exactly the kind of high-perceived-value, low-delivery-cost artefact that makes the $19 tier convert. Free tier gets the 30% preview, which for a PRFAQ methodology is a genuinely useful teaser (the four essentials + the customer-first redirect rules) that leaves the FAQ question banks and the verdict rubric behind the wall.

**Link edges to add** on write: upstream from `product-discovery`; downstream to `spec-requirements`; sibling to `what-you-dont-know-about-launch-pre-mortem`.

**On the untracked `skills/bmad-prfaq/`:** delete along with the rest of the drop (see `bmad-method.md`). Its content is already extracted into this dossier — that is what a research pass is for. Keep the dossier; drop the vendored directory.

## Open questions / staleness risk

- **Amazon primary sources not yet read.** Bryar & Carr's *Working Backwards* (2021) and Amazon's own public descriptions of the PR/FAQ format are the actual origin. This dossier documents a third-party implementation of it. **Before writing our methodology, read the primary sources** — otherwise we'd be reimplementing BMAD's reading of Amazon rather than Amazon. Blocked this pass by an exhausted web-search budget.
- **Stages 2–5 read as file inventory, not line-by-line.** I read `SKILL.md` in full (135 lines) and confirmed the four `references/` files exist with their line counts (60/55/51/83). The specific question banks inside Customer FAQ and Internal FAQ, and the scoring rubric inside `verdict.md`, were **not** read in detail. If we want to compare question coverage against ours, that's a follow-up read — though for writing our own from Amazon's method, deliberately *not* reading them is the cleaner path.
- **Low staleness risk, unusually.** PRFAQ shipped 2026-04-09 and survived seven releases through 2026-07-03 untouched and un-deprecated, while `bmad-prd`, `bmad-ux`, and `bmad-architecture` were all rewritten around it. Amazon's underlying method is ~2004 vintage and hasn't moved. Of everything in the BMAD orbit, this is the piece least likely to be invalidated next month.
- **Unverified: real-world outcomes.** No independent evidence in what I fetched that BMAD's PRFAQ implementation actually kills bad ideas at a useful rate. The 🟢 rests on the method's pedigree and the skill's internal coherence, not on measured results.
- **Open design question for us:** does the verdict stage produce a *score* or a *judgement*? BMAD's `verdict.md` is 83 lines — the longest reference file — which suggests scoring. A numeric strength score is attractive for a CLI (`faion` could surface it) and dangerous (false precision on a qualitative call). Decide before writing.
