# Tessl
**Layer:** 2 — Decomposition · **Verdict:** 🔴 skip — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

> **This file exists to record a failure, not to evaluate a tool.** Tessl was the most funded, most ambitious bet on "the spec is the artifact, the code is build output." As of 2026-08-03 that product is gone from the company's site, docs, and marketing. The reason it went is the single most useful input this research produced for our own SDD.

## What it is

**What it was pitched as (Sept 2025 – ~Jan 2026):** the *Tessl Framework* — you write a Markdown spec, annotate it with `@generate` / `@test` tags, run `tessl build`, and the framework generates the implementation, stamped as generated-do-not-edit. You then maintain the spec forever and regenerate the code. Alongside it, a *Spec Registry* of machine-readable "usage specs" describing how to use popular libraries, so an agent could consume a library's contract instead of guessing from training data. Böckeler's taxonomy calls this rung **spec-as-source**, the top of a three-level ladder (spec-first → spec-anchored → spec-as-source).

**What it is on 2026-08-03:** an **agent-skills governance platform**. Homepage tagline, quoted verbatim: *"Skills are the new code. Treat them that way."* The product is a package manager (`tessl install`, `tessl skill search`, `tessl skill publish`), a **Skills Registry** ("Find skills that make AI agents work correctly"), review/eval scoring, Snyk-powered security scanning, install policies, CI gating, an inventory of skill sprawl across an org, and the Tessl Agent for code review. Three stated pillars: security & governance, standardization & reuse, continuous optimization.

Same company, same CLI binary name, entirely different product.

## Current state

| Fact | Value | As of |
|------|-------|-------|
| Company | Tessl (Guy Podjarny, founder — also founder of Snyk) | 2026-08-03 |
| Funding | $125M at ~$500M valuation, announced **2024-11-14** (TechCrunch, Fortune). No later round found. | 2026-08-03 |
| Current positioning | "Agent Enablement Platform" / management layer for agent skills | 2026-08-03 (tessl.io) |
| Homepage tagline | **"Skills are the new code. Treat them that way."** | 2026-08-03 (tessl.io, fetched) |
| CLI | npm `tessl`, `latest` = **0.94.0**, published **2026-07-31T13:51Z**. First publish `0.0.0` on 2025-08-12. **Never reached 1.0.0.** | 2026-08-03 (npm registry API) |
| Docs | docs.tessl.io — full index at `/llms.txt`, 70+ pages, **zero** pages for `tessl build`, `.spec.md`, spec compilation, or "Tessl Framework" | 2026-08-03 (fetched `llms.txt` in full) |
| Registry | **Skills** Registry. "over 2,000 evaluated skills" at Jan-2026 launch; page heading today is "Skills Registry — Find skills that make AI agents work correctly". No spec registry, no usage specs. | 2026-08-03 (tessl.io/registry, fetched) |
| Framework GA | **Never.** Closed/private beta only, JavaScript-only, ~9 months, then unmentioned. | 2026-08-03 |
| License / price | Proprietary SaaS. Free tier + paid org plans (Pricing page exists; org roles, SSO, workspaces documented). Not open source. | 2026-08-03 |
| Public GitHub org | None found under `tessl` or `tessl-io` (GitHub API → 404 on both). Skills live under `tessl-labs/*` inside their own registry, not on GitHub. | 2026-08-03 |

**Blog signal.** Every post on tessl.io/blog from 2026-06-23 through 2026-07-30 is about agents, skills, evals, sandboxes, governance, benchmarks, and code review. Titles include *"Your agents keep making the same mistakes. Nobody has time to fix it."* (2026-06-30), *"Agents need real sandboxes"* (2026-07-30), *"The new Tessl review: now you decide what 'good' looks like"* (2026-06-23), *"AI Agent Governance: 10 Takeaways from Engineering Leaders"* (2026-06-23). Not one mentions specs, the Framework, or code generation.

## Mechanics

### Timeline — the pivot, dated

| Date | Event | Source |
|------|-------|--------|
| 2024-11-14 | Tessl raises $125M at ~$500M to "build AI that writes and maintains code" | TechCrunch, Fortune |
| Sept 2025 | *"Announcing Tessl's Products to Unlock the Power of Agents"* and *"How Tessl's Products Pioneer Spec-Driven Development"* — Framework (private beta) + Spec Registry launched | tessl.io/blog, still linked from the Jan-2026 post's footer |
| 2025-08-12 | First `tessl` npm publish (`0.0.0`) | npm registry |
| **2025-10-15** | Birgitta Böckeler, *"Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"* on martinfowler.com. Hands-on with the Framework. Observes **non-deterministic output from identical specs**; names the three-level ladder; draws the parallel to model-driven architecture (MDA) | martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| **2026-01-29** | Guy Podjarny, *"Announcing skills on Tessl: the package manager for agent skills"* — package manager, review evals + task evals, registry of 2,000+ evaluated skills, full skill lifecycle. **The post does not mention the Framework, spec-driven development, the Spec Registry, or any deprecation.** The only backward link is the footer's "More articles by Guy Podjarny" pointing at the Sept-2025 spec posts | tessl.io/blog/skills-are-software-and-they-need-a-lifecycle-introducing-skills-on-tessl/ |
| 2026-01-29 | Same day: Podjarny on X/LinkedIn — "I'm excited to announce Tessl's **package manager for agent skills**" | x.com/guypod/status/2016925019645866170 |
| 2026-06→07 | Snyk × Tessl partnership on securing the Agent Skills Registry; Tessl Academy preview; Tessl Review v2; product-wide skills framing | snyk.io/blog/snyk-tessl-partnership/, tessl.io/blog |
| 2026-07-31 | `tessl` CLI 0.94.0. Still 0.x | npm registry |
| 2026-08-03 | tessl.io, docs.tessl.io, tessl.io/registry: **no `tessl build`, no spec compilation, no Spec Registry** | fetched today |

### What "spec-driven development" means at Tessl *now*

One doc page survives with that name: `docs.tessl.io/use/spec-driven-development-with-tessl`. It defines SDD as *"a workflow where your AI coding agent gathers requirements and writes specifications before writing any code"* — and ships it as **an installable plugin**:

```bash
tessl install tessl-labs/spec-driven-development
```

The workflow it describes: agent asks clarifying questions → agent writes markdown specs into a `specs/` folder → you review and approve → agent implements against them. That is **spec-first** on Böckeler's ladder — the bottom rung, the same thing Spec Kit does, the same thing a well-written CLAUDE.md does. No regeneration. No `tessl build`. No generated-code stamp. No round-trip.

The company that raised $125M to make specs the source of truth now ships spec-driven development as a downloadable prompt.

### Why the thesis failed — the mechanism

The stated diagnosis, from the analyst side rather than the company: **if you generate code from a spec, you are fully dependent on a non-deterministic compiler.** Run the same spec twice, get two different implementations. Böckeler observed exactly this in the closed beta — nondeterminism persisting *despite* precise specs.

Unpack why that is fatal rather than merely annoying:

1. **A compiler's contract is determinism.** `gcc` on the same input gives the same output; that is what lets you trust that a spec change caused a behaviour change. An LLM breaks the invariant, so every regeneration is a fresh, unreviewed codebase.
2. **Diff review dies.** Under spec-as-source, the human reviews the spec diff. But the code diff between regeneration N and N+1 contains changes the spec diff does not explain — refactors, renames, different algorithm choices. You cannot review the spec and be done, and you cannot review the code because it is "generated".
3. **The spec must grow until it is the code.** Every non-determinism you need to pin down becomes another clause. The endpoint of "make the spec precise enough to determine the implementation" is a spec isomorphic to source code, written in a worse language. This is the MDA failure of the 2000s, re-run with a stochastic generator instead of a deterministic one.
4. **Regeneration destroys the artifacts around code.** Tests, comments, git blame, bisect, hotfixes — all of it assumes code is edited, not replaced. Nine months of closed beta, JavaScript only, and it still could not leave the lab.
5. **The adjacent problem was tractable and sellable.** Skills governance — inventory, security scanning, eval scoring, policy gates — is a real enterprise pain with a named buyer (CISOs, platform teams, eng leadership) and no non-determinism problem to solve. The pivot moved from "invent a new compiler" to "sell a package manager", which is the move Podjarny already knows how to run from Snyk.

**Important honesty caveat:** Tessl has never published a post saying "the Framework is deprecated" or "the LLM is a non-deterministic compiler, so we stopped." The 2026-01-29 announcement is silent about the old product. The non-determinism diagnosis is **Böckeler's (2025-10-15) and the commentary that followed it**, not Tessl's own statement. What is *directly* evidenced is the disappearance: no Framework docs, no `tessl build`, no Spec Registry, a 0.x CLI, and an entirely reframed company. Treat the mechanism above as a well-supported inference, not a confession.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | tessl.io homepage | https://tessl.io/ | Tagline "Skills are the new code. Treat them that way."; three pillars; nav = Platform / Agent / Registry / Pricing / Docs / Status. **Zero occurrences** of spec, spec-driven, Framework, tessl build, Spec Registry | 2026-08-03 |
| 2 | Announcing skills on Tessl | https://tessl.io/blog/skills-are-software-and-they-need-a-lifecycle-introducing-skills-on-tessl/ | The pivot post. Guy Podjarny, **published 2026-01-29**. Package manager, 2,000+ evaluated skills, review + task evals, lifecycle. No mention of the Framework or any deprecation | 2026-08-03 |
| 3 | docs.tessl.io full index | https://docs.tessl.io/llms.txt | Complete 70+ page doc map. Sections: registry & package manager, governance, evals, observability, inventory, Tessl Agent, projects, CLI reference. **No page for `tessl build`, `.spec.md`, spec compilation, or the Framework** | 2026-08-03 |
| 4 | Spec-Driven Development with Tessl | https://docs.tessl.io/use/spec-driven-development-with-tessl.md | The one surviving "SDD" page. It is a plugin install + a four-step prompt workflow. Spec-first, not spec-as-source | 2026-08-03 |
| 5 | Tessl Registry | https://tessl.io/registry | Heading: "Skills Registry — Find skills that make AI agents work correctly." Quality scores, impact multipliers, security status. No specs of any kind | 2026-08-03 |
| 6 | tessl.io/blog index | https://tessl.io/blog | 13 most recent posts, 2026-06-23 → 2026-07-30, all agents/skills/evals/governance. Nothing about specs | 2026-08-03 |
| 7 | npm `tessl` | https://registry.npmjs.org/tessl | 0.94.0 @ 2026-07-31; first publish 2025-08-12; never 1.0 | 2026-08-03 |
| 8 | Böckeler, *Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl* | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | **Published 2025-10-15.** Hands-on with the Framework; observed non-determinism from identical specs; the spec-first / spec-anchored / spec-as-source ladder; MDA parallel | 2026-08-03 (secondary retrieval) |
| 9 | GitHub API `/orgs/tessl`, `/orgs/tessl-io` | https://api.github.com/orgs/tessl | 404 both. No public source, no public issue tracker | 2026-08-03 |
| 10 | Snyk × Tessl partnership | https://snyk.io/blog/snyk-tessl-partnership/ | Securing the Agent Skills Registry — confirms the skills-governance positioning from a second party | 2026-08-03 |
| 11 | TechCrunch / Fortune funding coverage | https://techcrunch.com/2024/11/14/tessl-raises-125m-at-at-500m-valuation-to-build-ai-that-writes-and-maintains-code/ | **2024-11-14**, $125M at $500M, original thesis | 2026-08-03 (secondary) |

## What to borrow for faion

Nothing from the product. Four things from the post-mortem:

1. **Name our rung and stay on it.** Böckeler's ladder — spec-first / spec-anchored / **spec-as-source** — is a genuinely useful axis and belongs in our SDD corpus. Our `project-spec/` + same-PR delta rule is squarely **spec-anchored**: the spec is kept alive and enforced as the system evolves, and the code is still hand-maintained. That is the rung that works. Write it down explicitly so nobody in a future planning session drifts upward "for consistency."

2. **The falsifiable line: a spec is a contract, never a build input.** Concretely, for us: `project-spec/` and `spec.md` are read by humans and agents to *decide* and to *check*; they are never the sole input to a regeneration that overwrites hand-written code. Any future proposal to generate a module from a methodology file, or to regenerate `faion-cli` internals from `.aidocs/`, hits this rule.

3. **Non-determinism is the reason our validators must be deterministic.** If the *generator* is stochastic, the *gate* must not be. This is a direct argument for the Go validator over an LLM-judge for structural SDD checks: parse-and-compare gives the same verdict twice, an LLM does not. Same logic already applies to our content quality-gate stack (LT/Vale/Hunspell deterministic, LLM-judge advisory).

4. **Watch for the same failure shape in our own product.** Faion sells 2,622 methodologies as *context*, not as a compiler. The Tessl trap would be a future "faion generates your project from a methodology" feature. The lesson is that the market rewarded the boring adjacent product — packaging, distribution, quality scoring, governance of the context layer — and punished the ambitious one. That is uncomfortably close to a description of what Faion already is. Read it as validation of positioning, and as a warning about the one direction not to expand.

## What NOT to borrow — and why

1. **Spec-as-source / regenerate-forever.** The whole thesis. Nine months of closed beta, JS-only, never GA, then silently dropped by the best-funded team in the category. If they could not make it work, we are not going to make it work as a side effect of an SDD methodology.

2. **Generated-code markers (`// GENERATED FROM SPEC - DO NOT EDIT`) over hand-written modules.** They are a promise that the generator is authoritative. With a non-deterministic generator that promise is false, and the marker just blocks the fix.

3. **Any dependency on the Tessl platform.** Proprietary, closed-source, no public repo, 0.x CLI, and a company that has already reframed its product once inside twelve months. For a solopreneur — especially a non-technical one — that is a rug-pull surface with a signup wall in front of it.

4. **Their skills registry as a distribution channel for Faion content.** Superficially tempting: we have 2,622 methodologies and 455 playbooks; they have a package manager for exactly that shape of artifact. Don't. It hands our differentiator to a third-party registry that scores, ranks, and gates it, and it directly contradicts the sealed-content model `faion-cli` is built on. Note the strategic read, though: Tessl's pivot is a competitor moving into the *context-distribution* layer we occupy.

5. **"Spec-driven development" as a marketing phrase.** Tessl has now used it to mean two incompatible things eighteen months apart. When we write about SDD, say which rung.

## Mapping to our corpus

- **Direct conflict: none.** No methodology in `skills/faion/knowledge/sdd/` proposes generating code from a spec. `spec-structure`, `spec-requirements`, `writing-specifications`, `plan-md-structure`, `project-spec-structure` all treat the spec as a contract for humans and agents. We were never on the failed rung.
- **`project-spec-structure` is vindicated, specifically its rebuild test.** `content/02-rebuild-test.xml` sets the bar at *"a mid-level dev should rebuild the project in two weeks"* from `project-spec/` + `ui-ux-design.md` + `constitution.md`. That is precisely the spec-anchored bar: complete enough to reconstruct intent, deliberately **not** complete enough to be a compiler input. Tessl's failure is the empirical case for why the bar sits there and not higher. Worth adding as a `<rationale>` note in that methodology.
- **Corpus gap: the SDD ladder itself.** `sdd/INDEX.xml` (274 lines) has no methodology naming spec-first / spec-anchored / spec-as-source, and no methodology on the limits of spec-driven generation. Candidate new file: `sdd/spec-driven-development-rungs` — cites Böckeler 2025-10-15 and the Tessl case as the worked failure. This is exactly the kind of dated, receipted content the corpus sells well.
- **Cross-layer note:** Tessl's *current* product (skills inventory, review scoring, eval-backed improvement, policy gating in CI) is a Layer 3/4 concern — orchestration and reliability — not decomposition. If the landscape doc wants Tessl assessed as a live tool rather than a post-mortem, it belongs in `layer4-reliability/`, evaluated against our own quality-gate stack. As a Layer 2 decomposition tool it no longer exists.

## Open questions / staleness risk

**The correction, stated plainly.** The landscape doc's claim that Tessl's Framework is *"about nine months in closed/private beta"* and that the live product is *"a Spec Registry of 10,000+ usage specs"* is **wrong as of 2026-08-03, on both halves**:

- The nine-months-in-beta figure was accurate around Böckeler's October 2025 assessment. It is now ~stale by a product generation: the Framework never reached GA and is absent from tessl.io, docs.tessl.io (verified against the complete `llms.txt` index), and every 2026 blog post.
- The Spec Registry of usage specs no longer exists as the live product. tessl.io/registry is a **Skills Registry** ("Find skills that make AI agents work correctly"), launched 2026-01-29 with 2,000+ evaluated *skills*.

**The prior research pass was right.** The pivot is real, dated **2026-01-29**, and the direction is exactly as reported: away from "spec is the artifact, code is build output" toward agent-skills governance under the banner "Skills are the new code." `tessl build` is gone from the documentation. The Framework never shipped GA.

**One qualification on the prior pass.** It attributes the *reason* — "the LLM is a non-deterministic compiler" — as the cited cause. That framing is correct in substance and well-supported, but its **source is Birgitta Böckeler's 2025-10-15 martinfowler.com analysis and downstream commentary, not a statement by Tessl.** Tessl has published no post-mortem, no deprecation notice, and no explanation. Cite it as the analyst diagnosis, and cite the pivot itself as company-evidenced-by-absence. Do not put the phrase in Tessl's mouth.

**Residual uncertainty:**

- Whether the Framework is formally dead or merely dormant behind the beta wall. No deprecation notice exists; existing private-beta users may still have it. Absence from docs is strong evidence, not proof of shutdown.
- Whether the Spec Registry's 10,000+ usage specs were archived, folded into the skills registry, or deleted. Not answerable from public sources today.
- **Staleness horizon: ~3 months.** The company has reframed once in twelve months and has $125M to reframe again. The *lesson* recorded here does not go stale; the product description will.
- Not fetched: the Sept-2025 posts *"Announcing Tessl's Products…"* and *"How Tessl's Products Pioneer Spec-Driven Development"* (linked from the pivot post's footer). Worth pulling if we ever want the original claims quoted verbatim rather than characterized.
