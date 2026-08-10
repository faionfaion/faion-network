# Concept & Prototype Tools — Figma Make, UX Pilot, Magic Patterns, v0, Uizard

**Cluster verdict:** all five tools are real and shipping in August 2026, but they split cleanly into two groups that our corpus already treats differently. Figma Make and v0 are **developer-adjacent code generators bolted onto a paid platform** ($16-$100+/month once you need anything beyond a toy) — take the idea (fast divergent-option generation, design-token-aware prompting) but keep the tool itself out of a non-technical solopreneur's default stack. UX Pilot, Magic Patterns, and Uizard are **closer to genuinely non-technical**, with usable low-cost or free tiers, but none of them ships built-in accessibility or design-system-consistency enforcement — that judgment layer is still 100% human, which is exactly the gap our three geek-tier methodologies (`generative-ui-design`, `ai-generated-layout-review-checklist`, `figma-ai-ecosystem`) are built to fill. None of the five tools independently justifies moving those methodologies off geek tier; see the re-tiering section below for the arithmetic.

---

# Figma Make
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
A prompt-to-app generator embedded inside the Figma product suite. Positioned in Figma's own marketing as "Prompt to code anything you can imagine" — it takes a text prompt (optionally seeded with copied Figma frames, components, and variables) and produces an interactive, code-backed prototype inside the Figma canvas.

## Current state
- **Plan gating (per figma.com/pricing, fetched 2026-08-03):** the pricing comparison table has a dedicated "Figma Make" row-set. Quoting the fetch: *"Prompt the model" — Available on all paid tiers (Professional, Organization, Enterprise)* and *"The Starter (free) plan does **not** include access to Figma Make. All Make features require at least a Professional paid subscription."*
- **Conflicting third-party read:** mantlr.com's "Figma Make Pricing 2026: Plans, AI Credits, and Real Costs" (fetched 2026-08-03) instead claims *"All four Figma plans include Make access"*, listing Starter/free at *"500 AI credits/month with a 150/day cap"*. This directly contradicts Figma's own pricing-page table above. Flagged as an open discrepancy, not resolved — see staleness section.
- **Price for one person (Professional plan, the tier both sources agree is the real entry point):** **$16/month** (full seat, billed annually) per figma.com/pricing, fetched 2026-08-03. Professional includes **3,000 AI credits/month**, shared across all Figma AI features (Make, Draw AI, image tools), not a Make-specific allowance.
- **Credit burn (mantlr.com, fetched 2026-08-03):** simple edits 10-30 credits, single-screen generation 50-150 credits, full app / multi-component builds 200-340+ credits; *"a representative prototype project consumes 500-1,500 credits across the full build and iteration cycle"* — i.e., 2-3 real prototypes/month on the $16 Professional seat before hitting the wall.
- **Model:** launched on Claude 3.7 Sonnet (Figma's own 2025 announcement blog); by mid-2026 Figma has added a model picker — release notes (fetched via search 2026-08-03) confirm GPT-5.6 is now selectable inside Figma Make, so it is now multi-model, not Claude-exclusive.
- **Maintainer:** Figma, Inc. (part of the core product, not a separate acquisition).

## Mechanics
1. Designer opens Figma Make from inside a file, optionally copies existing frames in ("Bring in design systems using Make kits and npm packages, or attach Figma frames, PDFs, and more" — figma.com/make, fetched 2026-08-03).
2. Writes a natural-language prompt describing the interaction/feature ("add a checkout flow," "make this card draggable").
3. Make reads the file's context — component hierarchy, styles, and named Variables — and generates a working, code-backed canvas object: *"Everything you build is code-backed and visually editable, so you can easily jump between code and canvas."*
4. Output can be refined by further prompting, or by hand-editing the generated code/canvas directly (bidirectional).
5. Higher tiers unlock backend wiring, mobile-responsive Make, "Plan mode" (multi-step agentic planning), and publishing to a live URL — all gated to Organization/Enterprise per the pricing table.
6. This is squarely a **Figma-seat-holder's tool**: it lives inside the design app, assumes an existing Figma file/library, and its most valuable output (code-backed canvas) still needs a human to decide what ships. It is not a standalone product a non-technical founder can use without already paying for and knowing Figma.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Figma Pricing | https://www.figma.com/pricing/ | Seat prices, AI-credit allocations per plan, Make feature-gating table | 2026-08-03 |
| 2 | Figma Make product page | https://www.figma.com/make/ | Make-kits, design-context ingestion, code-backed/visually-editable claim | 2026-08-03 |
| 3 | Introducing Figma Make (blog) | https://www.figma.com/blog/introducing-figma-make/ | Original mechanics: copy frames in, preserve design-system hierarchy, Claude 3.7 Sonnet at launch | 2026-08-03 |
| 4 | Figma Make Pricing 2026 (third-party) | https://mantlr.com/blog/figma-make-pricing-2026 | Credit-burn-per-operation breakdown, conflicting claim that free tier includes Make | 2026-08-03 |
| 5 | Figma release notes (GPT-5.6 in Make) | www.figma.com/release-notes/ | Confirms multi-model picker inside Make in 2026 | 2026-08-03 (via search snippet) |

## What to borrow for faion
- The **"prompt the model with pinned design tokens or it defaults to generic aesthetics"** insight (echoed almost verbatim in our own `figma-ai-ecosystem` rule r8: "Audit Figma Variables before running Figma Make... poorly named variables produce generic AI output") is confirmed by the tool's own mechanics: Make literally uses variable *names* as prompt context, so sloppy naming degrades output. Worth a concrete example in the methodology.
- The multi-variant discipline in `generative-ui-design` rule r1 ("generate 3-5 variants, not 1") maps directly onto Figma's own r5 in our `figma-ai-ecosystem` methodology about generating 3 image-expand variations — this is a pattern Figma itself nudges toward operationally (probabilistic outputs, pick-the-best UX), not just a best practice we invented.

## What NOT to borrow — and why
- Do not borrow the "it's embedded in your design tool so it's low-friction" framing for our non-technical solopreneur audience — Make requires an existing paid Figma seat ($16+/month) and an existing Figma file with a maintained library. A solopreneur with no design background and no Figma habit gets zero value from Make; it's additive to an existing design practice, not a replacement for one.
- Do not adopt Make's "Publish"/"backend support" gating structure as a model for how our own tier gates should work — that's Figma's seat-monetization logic, unrelated to how methodology value scales.

## Mapping to our corpus
- `skills/faion/knowledge/ux/figma-ai-ecosystem/` (geek tier) is explicitly a **Figma-first** report methodology and already encodes the plan-gating reality (rule r6: "All AI features require Figma Professional/Organization plans") and the anti-hallucination rule (r7: "Do not build workflows that assume Figma Make, Draw, or Sites have agent-callable APIs. They do not exist as of 2026.") — this is confirmed live: Make has no public API for agents, only a UI-driven canvas experience.
- Note the duplicate-slug situation: `figma-ai-ecosystem` and `figma-ai-ecosystem-ui-design` share `content_id: 6885a4c5c2cc788e` in the manifest — same underlying content served under two slugs/tiers of retrieval, both geek. Any re-tiering decision has to apply to both slugs since they're the same body.
- `ai-generated-layout-review-checklist` (geek) names Figma Make explicitly in its Applies-If clause ("mockup generated by an AI tool (v0.dev, Galileo, Figma Make, Magician, Uizard, Visily)") — this dossier's findings support keeping that citation current in 2026.

## Open questions / staleness risk
- **Unresolved conflict:** Figma's own pricing page (fetched directly) says Make requires Professional+; a third-party 2026 blog says all four tiers including free include Make with a 500-credit/month allowance. Both were fetched the same day (2026-08-03). This may reflect a mid-2026 loosening of the gate that Figma's marketing copy hasn't fully caught up to, or the third-party source may be wrong/stale. Re-verify against a live Figma account before publishing anything definitive about free-tier Make access.
- Figma's AI-credit pricing model is volatile — Figma has changed seat/credit structure multiple times since AI features launched in 2025; any specific number here should be treated as a 2026-08 snapshot, not a stable fact.
- GPT-5.6 availability inside Make means the underlying model is no longer Claude-only, which changes any assumption our methodology makes about Make's behavioral quirks being Claude-specific.

---

# UX Pilot
**Layer:** 5 — Domain · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
A standalone, browser-based AI UX/UI design tool: text prompt → wireframes → higher-fidelity mockups, aimed at product managers, founders, and designers who want to "ideate, design and hand-off web applications in one place" (uxpilot.ai, fetched 2026-08-03).

## Current state
- **Free tier:** *"80 daily credits," "no credit card needed"* — confirmed directly from uxpilot.ai and uxpilot.ai/pricing, fetched 2026-08-03.
- **Paid tiers:** the pricing page is a JS-rendered single-page app; repeated direct WebFetch attempts (including a dedicated background research pass) returned only the free-tier line, never the paid-plan numbers. The most concrete figures found came from a third-party review snippet surfaced via DuckDuckGo search (not independently confirmed against the primary site): *"UX Pilot offers a free plan with 45 credits, a Standard plan at $19/month with 420 credits, a Pro plan at $29/month with 1,200 credits, and a Teams option for $39/month/user."* Note this **45-credit** free-tier figure conflicts with the official site's own **80 daily credits** claim — likely the reviewer described a different (older or monthly-framed) free allotment. Treat all UX Pilot paid-tier numbers as **unconfirmed** pending a primary-source re-check.
- If the $19-$39/month figures hold, UX Pilot sits in the same $12-$40/month band as Uizard and pre-2026 Magic Patterns — i.e., materially cheaper than a Figma Professional seat and far cheaper than geek tier.
- **Maintainer:** no registered legal entity name found on the public site. Founders per uxpilot.ai/about (fetched 2026-08-03): Adam (Founder & CEO), Naveed (Co-founder & CTO), Renato (CMO). No public founding date found.

## Mechanics
1. User types a product/feature description in plain English (no design skill assumed).
2. UX Pilot generates wireframes/mockups directly from the prompt — the tool markets this as *"Smarter Product Design With AI, done in seconds"*.
3. No confirmed code-export or Figma-round-trip capability was found in any fetched page — the tool positions itself as covering "ideate → design → hand-off" internally rather than exporting to a separate design tool.
4. No accessibility-check or design-system-token-compliance feature is advertised anywhere in the fetched marketing copy. Quality control is left entirely to the human reviewer.
5. Target audience is explicitly non-technical-friendly: a featured testimonial is from a "Project Manager" praising the tool as "intuitive and user-friendly," not from an engineer.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | UX Pilot homepage | https://uxpilot.ai | Workflow positioning, "Trusted by 1M+ Users," free-credit claim | 2026-08-03 |
| 2 | UX Pilot pricing | https://uxpilot.ai/pricing | Free-tier credits only; paid tiers not rendered in static fetch | 2026-08-03 |
| 3 | UX Pilot about | https://uxpilot.ai/about | Founder names, "Birth of UX Pilot" narrative, no explicit founding date | 2026-08-03 |
| 4 | Third-party review (unnamed, surfaced via DDG snippet) | not directly resolved | Claimed Standard $19/mo (420 credits), Pro $29/mo (1,200 credits), Teams $39/mo/user | 2026-08-03, unconfirmed |

## What to borrow for faion
- The framing "ideate, design, and hand-off in one place" targeted at non-designers is a useful north star for how our own playbooks should describe a solopreneur's realistic UX workflow: one tool, no separate design-to-dev handoff ceremony, because there's no dedicated designer on the team.
- The complete absence of any accessibility or token-compliance feature in UX Pilot's own marketing is a strong, concrete data point supporting why `ai-generated-layout-review-checklist` (our ten-check human review gate) remains necessary even for the most non-technical-friendly tool in this cluster.

## What NOT to borrow — and why
- Do not recommend UX Pilot as a design-system-of-record tool — it has no confirmed component-library or token-import mechanism, unlike Figma Make (which explicitly reads Figma Variables) or Magic Patterns (which explicitly imports "styles and design-system rules").
- Do not cite the $19/$29/$39 figures as confirmed pricing in any customer-facing material — they are third-party, unconfirmed, and conflict with the vendor's own free-tier credit claim.

## Mapping to our corpus
- Named explicitly in `ai-generated-layout-review-checklist`'s Applies-If clause is not the case for UX Pilot by name (that list cites "v0.dev, Galileo, Figma Make, Magician, Uizard, Visily" — UX Pilot is not named). Given UX Pilot's growing "1M+ users" claim, it's a candidate to add to that Applies-If tool list in a future revision, but that's a content edit, not a re-tiering question.
- `generative-ui-design`'s r2 ("treat generated UI as a zero-cost rough draft. Critique aggressively") applies cleanly here — UX Pilot generates fast, unvalidated layouts with zero built-in critique loop.

## Open questions / staleness risk
- Paid-tier pricing for UX Pilot could not be confirmed from primary sources despite multiple fetch attempts (WebFetch on `/pricing`, `/pricing/`, `www.` and bare-domain variants, plus a dedicated background research pass) — the pricing page is entirely client-rendered and returns no server-side content. This is the single weakest data point in this dossier; do not treat the $19/$29/$39 figures as settled.
- No legal entity name or funding/founding date found — makes it hard to assess company longevity risk for a "should I depend on this tool" recommendation.

---

# Magic Patterns
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
A prompt-to-UI-code generator built by North Park Labs, Inc., aimed at turning "a prompt, product requirement, or feature idea into high-fidelity UI in minutes" (magicpatterns.com, fetched 2026-08-03), with an explicit design-system-import feature.

## Current state
- **Maintainer:** North Park Labs, Inc. — confirmed via site footer and AlternativeTo's listing, both fetched 2026-08-03.
- **Pricing restructure mid-2026:** official blog post *"New Plans, Credits, and On-Demand Usage"* (magicpatterns.com/blog/new-plans-and-pricing, published 2026-03-01, fetched 2026-08-03) confirms a plan rename and price increase:
  - Plans renamed **Hobby → Starter**, **Pro → Business**, **Enterprise** unchanged.
  - Quoting the post directly: grandfathered monthly subscribers kept **"$19"** (Starter) or **"$75"** (Business) *"until June 30, 2026,"* after which prices moved to **"$20"** and **"$100"** respectively.
  - As of the 2026-08-03 check date, the June 30 cutover has already passed — meaning the live prices for anyone on a monthly plan are now **$20/month (Starter)** and **$100/month (Business)**.
  - Existing credit balances were multiplied 10x, and the credit-cost model changed from "one prompt, one credit" to complexity-scaled credits ("change this color" costs less than "build me a full prototype with 10 pages"); visual edits and "Fix with AI" cost zero credits per the same post.
  - The live JS-rendered `/pricing` page could not be scraped directly (repeated WebFetch attempts returned only the page title) — figures above come from the dated blog post, not the current pricing table, so exact current credit allotments per tier are unconfirmed.
  - A free entry point exists ("Get Started for Free" CTA on the homepage) but no specific free-tier credit/generation limit could be confirmed from any fetched page — AlternativeTo describes it only as "a limited free tier" within a stated overall subscription range of "$15 to $800 per month" (third-party, approximate, fetched 2026-08-03).
- **Recent model update:** GPT-5.6 added to Magic Patterns per a July 9, 2026 blog post, alongside credit-efficiency framing — confirms active 2026 development.

## Mechanics
1. User writes a prompt, product requirement, or feature description.
2. Optionally imports "existing screenshots, components, styles, and design-system rules" (magicpatterns.com, fetched 2026-08-03) so generated screens match an established visual language — this is a stronger design-system-awareness claim than UX Pilot or Uizard make.
3. Output is high-fidelity UI, explicitly marketed via a case study (Vanta) as producing *"prototypes that look like real Vanta features, not mockups"* — i.e., positioned as closer to shippable fidelity than a wireframe tool.
4. No code stack (React/Tailwind vs. something else) was confirmed from marketing copy in this pass, though the tool's target audience explicitly spans "frontend engineers and product leads," implying developer-consumable code output is part of the value proposition even if the exact framework isn't stated on the marketing page.
5. No accessibility-checking or automated design-token-compliance feature is advertised — "applies your established visual language" is a generative-consistency claim, not a validation/QA claim.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Magic Patterns homepage | https://www.magicpatterns.com | Workflow claim, design-system import claim, target-audience testimonials | 2026-08-03 |
| 2 | New Plans, Credits, and On-Demand Usage (blog) | https://www.magicpatterns.com/blog/new-plans-and-pricing | Grandfathered $19→$20 / $75→$100 pricing, 10x credit multiplier, complexity-scaled credit model | 2026-08-03 (post dated 2026-03-01) |
| 3 | AlternativeTo listing | https://alternativeto.net/software/magic-patterns/about/ | Third-party confirmation of maintainer (North Park Labs) and rough "$15-$800/month" range | 2026-08-03 |
| 4 | GPT-5.6 announcement (blog) | https://www.magicpatterns.com/blog/introducing-gpt-5-6 | Confirms active mid-2026 model updates | 2026-08-03 |

## What to borrow for faion
- The design-system-import mechanic ("bring your existing screenshots, components, styles, and design-system rules") is the most concrete confirmation in this whole cluster that at least one tool tries to solve the token-drift problem our `ai-generated-layout-review-checklist` rule c02 (token-compliance) exists to catch — but note it's still a best-effort *generation-time* nudge, not a *verification* step. The methodology's review gate remains the only place that actually checks compliance after the fact.
- The zero-cost "visual edits and Fix with AI" credit model is a useful pattern to reference when explaining to solopreneurs why iterative refinement inside these tools is cheap but full generations are not — maps to our own r2 in `generative-ui-design` ("treat generated UI as a zero-cost rough draft").

## What NOT to borrow — and why
- Do not recommend Magic Patterns' Business tier ($100/month, current per the 2026-03-01 blog with cutover already passed) as a "cheap AI prototyping tool" in any solopreneur-facing material — at $100/month it now costs more than our own geek tier ($99/month) and is squarely in "small-team SaaS budget" territory, not solopreneur-casual spend.
- Even the Starter tier at $20/month is a real recurring cost for a tool whose main output (marketing calls it "not mockups" but doesn't confirm accessibility/consistency validation) still needs the same human review discipline as a free tool — the price increase doesn't buy quality assurance.

## Mapping to our corpus
- Not currently named in any of the three geek-tier methodology Applies-If/tool lists (`ai-generated-layout-review-checklist` names "v0.dev, Galileo, Figma Make, Magician, Uizard, Visily" — no Magic Patterns). Given its design-system-import feature and real 2026 traction (active blog, model updates, pricing overhaul), it's a reasonable candidate to add by name in a future content revision.
- `figma-ai-ecosystem`'s scope is Figma-specific and explicitly out-of-scope for a "single-surface" or non-Figma tool per its own Skip-If clause — Magic Patterns is not a Figma surface, so it stays out of that methodology's remit and belongs instead under `generative-ui-design` / `ai-generated-layout-review-checklist`, which are tool-agnostic.

## Open questions / staleness risk
- The live current-tier pricing (post-cutover $20/$100, or any further 2026 changes since March) could not be confirmed against the actual `/pricing` page — it is JS-rendered and returned empty content on every fetch attempt in this pass. The blog post is dated and explicit, but pricing pages can move faster than blog announcements; re-verify before publishing exact current numbers.
- Exact credit allotment per tier under the new complexity-scaled model is not published anywhere found in this pass — meaning "how many real prototypes per month does $20 buy" cannot be answered with confidence, unlike Figma Make where a third party at least attempted a credit-per-operation breakdown.

---

# v0 (Vercel)
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
Vercel's prompt-to-full-stack-app generator: "Prompt. Build. Publish." — text prompt in, deployed live website out, with GitHub sync for developers who want to keep working on the generated code (v0.app, fetched 2026-08-03).

## Current state
- **Free tier:** **$0/month** — *"$5 of included monthly credits"* and a *"7 message/day limit"* (v0.app/pricing, fetched 2026-08-03).
- **Plus tier:** **$30/user/month** — *"$30 of included monthly credits per user"* plus *"$2 of free daily credits on login per user"*; unlocks all models, visual design editing, GitHub sync, team collaboration.
- **Business tier:** **$100/user/month** — same credit allowance as Plus, adds training-opt-out-by-default, priority performance access, no queues.
- **Enterprise:** custom pricing, adds no-training guarantee, SAML SSO, RBAC, SLA-backed support.
- Separate **model-based/token pricing** exists for v0 Mini/Pro/Max/Max Fast, ranging **$1-$50 per million tokens** — i.e., v0 is usage-metered underneath the credit wrapper, and heavy generation sessions can burn through the included credit allotment fast regardless of the flat subscription price.
- **Maintainer:** Vercel Inc.

## Mechanics
1. User describes the app/feature in natural language.
2. v0 generates a working application — context clues on the marketing page (Next.js integration, shadcn/ui templates, Tailwind styling examples) strongly imply a **React/Next.js/Tailwind** output stack, though the fetched page never states the stack in so many words.
3. The generated app **deploys immediately as a live website** ("Deploy to Vercel," "live websites in seconds") — this is real production deployment infrastructure, not just a code export.
4. "Edit with design mode" gives a visual/live-preview refinement loop without writing code.
5. "Sync with a repo" / "Connect to GitHub and push code directly to your repository" is the explicit developer on-ramp — v0 assumes a developer will eventually take custody of the generated codebase for anything beyond a disposable prototype.
6. Target audience is explicitly dual per the fetched page: non-technical users get an iOS app and pure-prompt generation; developers get GitHub sync, design systems for reusable tokens, and code-level control. But the deepest value (repo sync, design-system authoring, model selection) is developer-facing — a non-technical solopreneur can get a live demo page from v0, but anything durable needs an engineer to own the exported repo.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | v0 pricing | https://v0.app/pricing | Free/Plus/Business/Enterprise tiers, credit allotments, per-model token rates | 2026-08-03 |
| 2 | v0 homepage | https://v0.app | Prompt→build→publish workflow, GitHub sync, design mode, target-audience framing | 2026-08-03 |

## What to borrow for faion
- v0's "Prompt. Build. Publish." three-step framing is a clean, portable structure for how our own playbooks could narrate a generative-UI workflow end-to-end, independent of any specific tool.
- The explicit credit-metering-under-a-subscription model (flat monthly fee + burnable credit pool + separate token-rate schedule) is a useful cautionary pattern to flag for solopreneurs: the advertised $30/month Plus price is not a ceiling on real cost if usage runs hot — worth a line in any playbook that recommends v0.

## What NOT to borrow — and why
- Do not recommend v0 as a non-technical solopreneur's primary tool. Its most durable value (GitHub-synced, developer-owned codebase) requires a developer to consume the output; the free/Plus tiers are for demos and exploration, not for someone who will never touch the exported repo. This is the clearest "developer-adjacent" tool in the cluster alongside Figma Make.
- Do not treat the $30/month Plus price as the real cost of "using v0 seriously" — the credit-burn model plus separate per-model token pricing means a solopreneur experimenting heavily could pay meaningfully more; don't understate this in customer-facing material.

## Mapping to our corpus
- `generative-ui-design` (geek) names v0 directly in its own summary: *"generating 5-10 layout variants (v0, Claude Artifacts, Galileo, Uizard, Relume)"* — this dossier confirms v0's mechanics (multi-variant generation via re-prompting, not a built-in "generate 5 variants" button) match the methodology's framing of v0 as a *raw* option-generator that the methodology's r1 (generate 3-5 variants) has to be imposed on manually, since v0 doesn't produce a variant set natively.
- `ai-generated-layout-review-checklist` names "v0.dev" explicitly in its Applies-If tool list — still accurate; v0's own marketing confirms zero built-in accessibility or design-token-compliance checking, which is exactly the gap rules c02/c03 in that methodology exist to close.

## Open questions / staleness risk
- v0's pricing structure (flat fee + credit pool + per-model token rates) is exactly the kind of layered pricing that changes frequently at fast-moving AI-tool companies; re-verify the $30/$100 figures and the $1-$50/million-token range before using them in anything long-lived.
- The exact output stack (React/Next.js/Tailwind) was inferred from contextual page elements, not a direct statement on the fetched page — worth a direct confirmation from v0's own docs before citing it as a hard fact in customer-facing copy.

---

# Uizard
**Layer:** 5 — Domain · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
A standalone AI UI/UX design tool from Uizard Technologies (Copenhagen, Denmark; company traces to a 2017 research project called pix2code, incorporated 2018 — uizard.io/about, fetched 2026-08-03). Its "Autodesigner" engine generates multi-screen, editable mockups from a text prompt, a screenshot, or a hand-drawn sketch.

## Current state
- **Free tier:** **$0** — *"3 AI generations per month," "2 projects," "10 free templates," "400 components per organization,"* up to 5 custom templates (uizard.io/pricing, fetched 2026-08-03). This is the most restrictive free tier of the five tools — 3 generations/month is a trial, not a working allotment.
- **Pro tier:** **$12/month** (billed annually) — *"500 AI generations per month,"* "AI engine: Autodesigner 2.0," developer handoff to React/CSS, up to 100 projects, private projects, access to all templates, unlimited free viewers/commenters.
- **Business tier:** **$39/month** — everything in Pro plus 5,000 AI generations/month, faster generation, custom brand kit, unlimited projects, priority support.
- **Enterprise:** custom pricing — unlimited AI generations, unlimited teams, design-system setup, AI data SLA, white-label/custom solutions.
- **Maintainer:** Uizard Technologies.

## Mechanics
1. **Text-to-mockup (Autodesigner):** user describes an app concept in plain English; Uizard generates a multi-screen, editable prototype directly — the marketing page shows a literal example prompt ("an app that is a community platform...") mapped to a generated result.
2. **Screenshot-to-design (Screenshot Scanner):** converts a screenshot of an existing app/site into an editable Uizard mockup within seconds — a workflow none of the other four tools in this cluster advertise.
3. **Hand-drawn-to-digital (Wireframe Scanner):** digitizes a photographed paper sketch into a production-ready design — again unique to Uizard among the five.
4. **Theme generation:** users can reskin an entire project by generating a new visual theme, rather than manually restyling each screen.
5. **Developer handoff:** Pro tier explicitly ships "Developer handoff React CSS" — meaning Uizard does produce a defined code-export format (React + CSS), confirmed directly from the pricing page, unlike Magic Patterns or UX Pilot where the exact export format was not confirmed.
6. Marketing copy leans hard into non-technical accessibility: *"No code. No design. No effort,"* explicitly naming product managers, founders, and marketers (not designers/engineers) as the target buyer.
7. No accessibility-checking or design-token-compliance feature was found in any fetched page — Theme Generation controls visual consistency across screens generated by Uizard itself, but nothing validates the output against WCAG or an external design system's rules.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Uizard homepage | https://uizard.io | Autodesigner, Screenshot Scanner, Wireframe Scanner, Theme Generation, target-audience framing | 2026-08-03 |
| 2 | Uizard pricing | https://uizard.io/pricing/ | Free/Pro/Business/Enterprise tiers, exact generation counts, React/CSS handoff on Pro | 2026-08-03 |
| 3 | Uizard about | https://uizard.io/about/ | Company history (pix2code, 2017 research → 2018 incorporation), Copenhagen HQ | 2026-08-03 |

## What to borrow for faion
- Uizard is the only tool in this cluster with a confirmed, named code-export format (React/CSS) at an affordable tier ($12/month) — a concrete, current example worth naming in `generative-ui-design`'s examples file for solopreneurs who eventually need a developer to pick up the output.
- The Screenshot Scanner / Wireframe Scanner workflows (image-to-editable-design) are a distinct mechanic none of our current methodology content addresses — "AI-generated layout from a photo of a napkin sketch" is a real, cheap, non-technical workflow worth a mention in a future revision of `generative-ui-design`'s procedure file.

## What NOT to borrow — and why
- Do not treat the free tier as usable for real work — 3 generations/month is a demo, not a workflow; any solopreneur recommendation should be explicit that Uizard's real floor is the $12/month Pro tier, not "free."
- Do not imply Uizard's Theme Generation or Autodesigner substitutes for a design-system audit — it produces internal visual consistency across its own generated screens, not conformance to an existing external brand/design system the way Magic Patterns' import feature claims to.

## Mapping to our corpus
- Named directly in both `generative-ui-design`'s summary ("v0, Claude Artifacts, Galileo, Uizard, Relume") and `ai-generated-layout-review-checklist`'s Applies-If tool list ("v0.dev, Galileo, Figma Make, Magician, Uizard, Visily") — Uizard is the one tool in this cluster the corpus already cites in *both* methodologies, and this dossier confirms both citations are still current in 2026.
- At $12/month Pro, Uizard is the cheapest tool in this entire cluster with a real, usable paid tier — the strongest single data point for the re-tiering question below.

## Open questions / staleness risk
- Pro-tier price ($12/month annual) versus month-to-month price was not separately confirmed — the fetched page states the annual-billed figure with a "save 40%" note, implying a materially higher month-to-month price that wasn't captured in this pass.
- No 2026-specific pricing-change announcement was found for Uizard (unlike Magic Patterns' well-documented March 2026 restructure) — absence of evidence isn't evidence of stability; re-check before treating $12/$39 as durable.

---

## Re-tiering assessment

**The manifest, confirmed by direct read (2026-08-03):** `solo` = **$19/month**, `pro` = **$35/month**, `geek` = **$99/month** (`skills/tier-manifest.json`, `pricing` block). The prior re-tiering recommendation argued the tools these three methodologies describe cost $12-$22/month, making geek's $99/month a mismatch. Doing the arithmetic per tool with what this dossier actually found:

| Tool | Real single-person price found | vs. geek ($99/mo) |
|---|---|---|
| Uizard | **$12/month** (Pro, annual) | well under |
| UX Pilot | **unconfirmed** (free tier only confirmed; third-party unconfirmed figures cluster $19-$39/month) | likely under, not proven |
| Figma Make | **$16/month** Figma Professional seat minimum — but that $16 buys a shared AI-credit pool good for only ~2-3 real prototypes/month, and the credit-consuming feature set (backend, publish, mobile Make) requires **Organization ($55/seat) or Enterprise ($90/seat)** | entry price under geek; realistic-use price approaches or exceeds it |
| v0 | **$30/month** (Plus) minimum for anything beyond a 7-message/day free trial, with a separately metered $1-$50/million-token layer underneath | under geek, but not "$12-22" and not a hard ceiling |
| Magic Patterns | **$20/month** Starter (post-cutover, confirmed dated blog post) but **$100/month** Business (post-cutover) — Business now **exceeds** geek tier outright | Starter under; Business over |

**The prior recommendation's premise does not hold as stated.** Only one tool (Uizard) actually sits cleanly in the claimed $12-$22/month band with a usable paid tier. UX Pilot's real paid price could not be confirmed at all. Figma Make's *nominal* per-seat price ($16) is misleadingly low because Make competes for a shared credit pool that a solo user burns through in 2-3 projects — the realistic cost of using Make "for real" pushes toward the $55-$90/seat Organization/Enterprise tiers, i.e., toward or past geek. Magic Patterns' own numbers now straddle geek tier exactly — Starter under it, Business over it, following a documented mid-2026 price increase the prior recommendation predates. v0 (Plus, $30/month) is closer to $30-$100 territory than $12-$22, before even counting metered token overage.

**Recommendation: keep `generative-ui-design`, `ai-generated-layout-review-checklist`, and `figma-ai-ecosystem` (and their twin slugs) at geek tier.** The re-tiering case rested on a "these are all $12-22/month tools" premise that is only true for one of the five tools this dossier checked; two of the five (Figma Make at realistic usage, Magic Patterns Business) now cost as much as or more than geek tier itself, and one (UX Pilot) has no confirmed paid price at all. A user who can afford $55-$100/month for Figma Organization or Magic Patterns Business — or who is running Figma Make workflows seriously enough to need Plan mode and Publish — is exactly the geek-tier "agent builder" persona the manifest already targets, not the $19 solo or $35 pro persona. If anything, this dossier's numbers argue geek is correctly priced *relative to the tool costs it references*, not overpriced.

---

## Strategic verdict: do prompt-to-prototype tools make UX/product methodology MORE or LESS valuable

**More valuable — and every tool's own mechanics prove it by omission.** Across all five tools checked, not one advertises a built-in accessibility check, a design-token-compliance validator, or a research-grounding requirement. Figma Make reads component names and Variables for *styling* context but performs no WCAG contrast/focus-order check — that's still the job of `ai-generated-layout-review-checklist` rule c03. Magic Patterns imports "design-system rules" to *generate* consistent-looking screens but has no confirmed verification step to catch drift after the fact — exactly the gap rule c02 (token-compliance) exists to close, and its own case-study language ("prototypes that look like real Vanta features, not mockups") is precisely the kind of confident-looking-but-unvalidated output the checklist's ten checks were written to catch before it reaches engineering. Uizard's Theme Generation enforces internal consistency across its own outputs but nothing external. v0 and UX Pilot show zero accessibility or provenance tooling in any fetched page. None of the five tools tracks which output percentage is AI-generated vs. human-edited (rule c10's attestation requirement) or requires a cited research artifact (rule c01) — these tools make it *faster* to produce a plausible-looking screen, which is precisely why the volume of unvalidated, confident-looking output entering review pipelines is rising, not falling. The tools compress ideation time; they do not encode judgment. A solo founder using any of these five tools alone gets speed and zero built-in quality gate — the methodology is the only thing standing between "AI generated something that looks done" and something that is actually done. Faster garbage-generation raises, not lowers, the value of a fast, cheap human-judgment layer.
