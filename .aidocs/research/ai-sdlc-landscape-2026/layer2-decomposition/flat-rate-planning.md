# Flat-Rate Planning (moving the planning phase off metered tokens)
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

An **economic pattern**, not a product. The claim: the most token-expensive part of AI-assisted work is long planning conversations carrying large context, and you can move exactly that phase onto a flat-rate consumer subscription (ChatGPT Plus/Pro, Gemini AI Pro, Claude Pro) instead of metered API tokens or a metered IDE — then bring the resulting markdown back into the repo and do implementation where the code is.

BMAD shipped a concrete instance of it. Their own words, from `web-bundles/README.md` (fetched 2026-08-03):

> "**Cost.** Web LLM subscriptions are flat-rate. Run brainstorming, briefs, PRDs, and research there instead of burning IDE tokens."

and from the concept doc:

> "Planning work and implementation work want different tools. Web bundles let each use the right one." … "A PRFAQ pass and three rounds of research in a Gem cost zero marginal dollars; the same work in an IDE is real spend."

This dossier is about whether that survives scrutiny. Short answer up front: **the tool-fit argument is sound, the token-savings argument is largely wrong, and for us specifically the dollar arbitrage is dead on arrival — what survives is quota-pool diversification.**

### Adjudicating the landscape-doc claim #3

> *"Web Bundles (v1.0, May 2026) — package the planning skills as a Gemini Gem or ChatGPT Custom GPT, moving the planning phase onto a FLAT SUBSCRIPTION instead of metered IDE tokens."* 🟢

**The factual half is confirmed.** From `web-bundles/bundles.json` (fetched 2026-08-03): `"schemaVersion": "1.0"`, `"releaseTag": "web-bundles-v1.0.0"`, `"releasedAt": "2026-05-25"`. Six bundles ship: Brainstorming Coach, Product Brief Coach, PRFAQ Coach, PRD Coach, UX Coach, Market & Industry Research. The stated rationale is verbatim the flat-rate argument. v6.8.0 (2026-05-25) records "Launched Web Bundles v6 for Gemini Gems and ChatGPT Custom GPTs."

**The 🟢 is where I disagree.** The mechanism is real; the economic claim underneath it is only true for a specific workload shape, and it isn't the shape we run. Downgrading to 🟡. Reasons below.

## Current state

### The flat-rate options (prices as of 2026-08-03)

| Provider | Tier | Price/mo | Skill-bundle surface | Trains on your input by default? |
|---|---|---|---|---|
| OpenAI | Free | $0 | — | Yes (unless Data Controls off) |
| OpenAI | Go | $8 | — | Yes |
| OpenAI | **Plus** | **$20** | **Custom GPTs** | Yes (unless Data Controls off) |
| OpenAI | Pro | $100 (launched 2026-04-09) / $200 | Custom GPTs | Yes |
| OpenAI | **Business** | **$25/user** | Custom GPTs | **No — no-train is the default** |
| Google | Free | $0 | — | Yes + human review |
| Google | AI Plus | $4.99 | Gems | Yes + human review |
| Google | **AI Pro** | **$19.99** | **Gems** | Yes + human review |
| Google | AI Ultra | $99.99 / $199.99 (cut from $249.99 at I/O 2026) | Gems | Yes + human review |
| Google | Workspace / Cloud | varies | Gems | **No — enterprise data not used for training** |
| Anthropic | Free | $0 | Projects (no shareable bundle) | Opt-out available |
| Anthropic | **Pro** | **$17 annual / $20 monthly** | Projects | Opt-out available |
| Anthropic | Max 5x | from $100 | Projects | Opt-out available |
| Anthropic | Max 20x | ~$200 | Projects | Opt-out available |

**Sourcing discipline:** Anthropic figures are **primary** — `claude.com/pricing`, fetched 2026-08-03 (the page renders Max 20x's price in a shared block that read as "From $100/month" to the fetcher; secondary sources consistently give $200, and I've marked it `~`). OpenAI and Google figures are **secondary** — `openai.com/chatgpt/pricing` returned HTTP 403 and `one.google.com/about/google-ai-plans/` rendered without prices, so these come from search summaries of cloudzero, aipricing.guru, felloai, pricepertoken, and blog.google, all consulted 2026-08-03. Treat OpenAI/Google numbers as ±one tier-restructure.

BMAD's own stated requirement: *"Requires Gemini Advanced (for Gems) or ChatGPT Plus / Pro / Business / Enterprise (for Custom GPTs). Deep Research has its own plan limits."* So the entry ticket is ~$20/mo either way.

### Can a Custom GPT / Gem actually hold a large skill bundle?

**A skill bundle: comfortably yes. A knowledge corpus: no.**

Hard limits (secondary sources, 2026-08-03):
- **ChatGPT Custom GPT:** 20 knowledge files, each up to 512 MB and 2,000,000 tokens; only text is extracted from files containing images.
- **Gemini Gem:** 10 knowledge files. Gemini's compensating advantage is live Drive links rather than static uploads.

What BMAD actually ships per bundle — measured from the repo, 2026-08-03:

| Bundle | Knowledge files | Size |
|---|---|---|
| PRFAQ Coach | `SKILL.md` | 11,223 B |
| PRFAQ Coach | `INSTRUCTIONS.md` (pasted into settings, not uploaded) | 5,023 B |
| Brainstorming Coach | `SKILL.md` + `brain-methods.csv` | — |

So a bundle is **1–2 uploaded files totalling ~11 KB**, against a ceiling of 10–20 files. BMAD is using ~10% of the file budget and a rounding error of the token budget. The architecture is deliberate and documented: *"The persona resides in instructions while the protocol lives in the knowledge file, allowing persona changes without altering the underlying protocol."*

**Now scale that to us.** Our corpus is 2,622 methodologies across 23 domains, 3,070 manifest entries, ~330 MB on disk. 20 files × 2M tokens is nominally 40M tokens of headroom, so the *limit* is not the blocker. Three other things are:

1. **Retrieval.** Uploading 20 concatenated blobs replaces our two-level routing (`knowledge/domains.xml` + `playbooks/taxonomy.xml` → ≤3 candidate buckets → only those `INDEX.xml` → leaf) with opaque vendor RAG we cannot tune, test, or debug. We would trade a designed retrieval path for a black box.
2. **Content sealing.** D-001 is explicit: the methodology base "must not be trivially extractable"; Go embeds a gzipped blob and only `get-content <hash>` prints bodies. Uploading the corpus to a consumer chat account hands the product to a surface with a download button. This is a non-negotiable USP, not a preference.
3. **Tier gating.** `tier-manifest.json` v8 gates 3,070 entries across free/solo/pro/geek. A Custom GPT has one access level: whoever has the link.

**Conclusion:** the bundle pattern is for *protocols* — a few KB of instructions that tell a model how to run a conversation. It is structurally the wrong container for a knowledge corpus, and that is fine, because a protocol is exactly what a PRFAQ or brief coach is.

## Mechanics

### The BMAD instance, end to end

1. **Author.** Bundles are generated from BMAD skills by the `bmad-os-skill-to-bundle` utility skill (in `bmad-code-org/bmad-utility-skills`). Point it at a skill folder; it emits `SKILL.md`, `INSTRUCTIONS.md`, and required data files, with persona inheritance from the owning agent.
2. **Package.** `tools/bundle-web-bundles.js` zips each bundle directory and attaches it to a tagged GitHub Release. `bundles.json` carries per-bundle metadata: `slug`, `name`, `tagline`, `description`, `defaultPersona` / `swapPersona` (each with `name`, `title`, `lineage`), `accentColor`, `motif`, `knowledgeFiles`, `needsWebBrowsing`, `needsDeepResearch`, `stitchIntegration`.
3. **Distribute.** One front door: `bmadcode.com/web-bundles`. The README is blunt that this is deliberate — *"That is the only supported install path"* — for three reasons: install steps stay current as Gemini and ChatGPT evolve; every shelf update is a tagged release and the site points at the newest tag; one signup captures the mailing list.
4. **Install.** "Download, unzip, create the Gem or GPT, follow the inline steps." Stated setup cost: *"a few minutes per bundle."* Upload `SKILL.md` (+ data files) as Knowledge; paste `INSTRUCTIONS.md` into the instructions box.
5. **Run.** Conversation happens in the flat-rate surface, with Canvas, image generation, and Deep Research available.
6. **Hand off.** BMAD's own words: *"Sessions produce Canvas documents exportable as files, pasteable into repositories, or feedable into IDE-based BMad skills for subsequent phases."*

**Step 6 is where the whole pattern lives or dies, and it is exactly one sentence long in BMAD's docs.** "Pasteable into repositories" is not a discipline. See the failure mode below.

### Which phases actually dominate token spend?

The landscape doc asserts discovery, decomposition, and long reviews. Let me model it against real prices rather than assert back.

**Prices used** (Anthropic list, from the `claude-api` skill's catalogue cached 2026-06-24): Opus 5 $5/MTok in, $25/MTok out, 1M context. Sonnet 5 $3/$15 ($2/$10 introductory through 2026-08-31). Prompt-cache reads ≈ 0.1× base input; cache writes 1.25× (5-min TTL) or 2× (1-hour TTL). Minimum cacheable prefix 512 tokens on Opus 5.

> These are **modelled** scenarios with stated assumptions, not measured telemetry from our own runs. We do not currently instrument per-phase token spend — see Open questions. Treat the *ratio* as the finding, not the absolute dollars.

**Scenario A — a long planning conversation.** 40 turns, context grows roughly linearly 5K → 100K tokens, ~1.5K output per turn.

| | Tokens | Opus 5 cost |
|---|---|---|
| Input, no caching (40 turns × ~52.5K mean) | 2.10M | $10.50 |
| Output (40 × 1.5K) | 0.06M | $1.50 |
| **Uncached total** | | **~$12.00** |
| Input, with prompt caching (reads at 0.1×, writes on the ~100K delta at 1.25×) | | ~$1.65 |
| **Cached total** | | **~$3.15** |

**Scenario B — one agentic implementation task.** 60 tool-call iterations, context grows 20K → 400K as file reads and test output accumulate, ~2K output per iteration.

| | Tokens | Opus 5 cost |
|---|---|---|
| Input, no caching (60 × ~210K mean) | 12.6M | $63.00 |
| Output (60 × 2K) | 0.12M | $3.00 |
| **Uncached total** | | **~$66.00** |
| **With caching at a realistic ~70% hit rate** | | **~$26.00** |

**The finding, and it inverts the premise:**

> In an agentic-coding workflow, **planning is the cheapest long session you run**, not the most expensive. Scenario B costs roughly **8×** Scenario A after caching.

The reason is caching behaviour, and it is structural rather than incidental:

- A **planning chat** is close to the ideal cache shape. The prefix is stable, each turn appends a small delta, and every turn after the first reads almost the entire context at 0.1×. That's the 4× reduction in Scenario A.
- An **agentic loop** breaks caching in ways a chat does not. Each breakpoint walks back at most **20 content blocks** to find a prior entry; an agentic turn that emits many `tool_use`/`tool_result` pairs blows past that window and silently misses. Compaction and context editing rewrite history, invalidating wholesale. And the raw volume is an order of magnitude larger because tool results — file contents, test output, diffs — are the actual firehose.

**So the landscape doc's premise is true for exactly one workload shape: planning-only work with no implementation loop.** Which, to be fair, is precisely the shape a non-technical solopreneur has. A CX designer, a course author, a services consultant — they run Scenario A repeatedly and never run Scenario B at all. For them, planning *is* 100% of spend, trivially. For us, running an SDD pipeline with agentic executors, it is a minority of it.

**Where "long reviews" land:** with the loop, not the chat. Our multi-language review passes read a full article per reviewer and run per-language — that's Scenario-B-shaped (large per-turn payloads, many parallel agents), not Scenario-A-shaped.

### The constraint that changes the answer for us

**Claude Max is already flat-rate, and the Agent SDK under Max draws the SAME quota as an interactive session** (project memory: `runtime-budget-topology`). We are not paying $5/MTok for our own work. We are spending against a 5-hour window and a weekly ceiling — and hitting the weekly ceiling stops implementation dead.

That single fact rewrites the entire calculation:

| | Metered-API user | Us (Claude Max) |
|---|---|---|
| What planning consumes | dollars | **quota window** |
| What moving planning off Max saves | dollars | **headroom for implementation** |
| Is $20/mo ChatGPT Plus a saving? | yes, vs. ~$12/session | it's a **new $20/mo cost** |
| Is it still worth it? | obviously | **only if the freed headroom is worth $20/mo** |

The only genuinely separate budget pool we already hold is **Codex under OpenAI Max**. So the pattern, for us, is not "escape metered tokens" — it is "add a third pool alongside Claude Max and OpenAI Max, for the class of work that needs no repo access." That is a real and defensible thing to want, given how often the weekly ceiling has actually bitten (project memory: `weekly-quota-throttle`, `sonnet-weekly-limit-separate`). It is just not the thing the landscape doc claims.

**And note the pricing-copy trap.** Our own product rule is that pricing must never be denominated in tokens — we spend zero LLM tokens at runtime on customer work. If we ever write about this pattern publicly, the framing must be "run planning where planning is best; run building where the code is," never "save tokens." The moment we lead with token arithmetic we've re-anchored the reader on tokens as the unit of value, which is the exact anchoring our own positioning forbids.

### The hard failure mode: a second, invisible source of truth

This is the real risk and it is not hypothetical. The chat thread accumulates decisions, caveats, rejected alternatives, and corrections. You export one Canvas document. Everything the export didn't capture now lives in a place that is: not in the repo, not searchable by any agent, not versioned, not reviewable, and — worst — **still open in a browser tab where you will keep editing it.** Two weeks later the repo says one thing, the thread says another, and the thread feels more authoritative because it's where the thinking happened.

BMAD's docs address this with the phrase "pasteable into repositories." That is not enough.

**The discipline that prevents it — seven rules, all enforceable:**

1. **The chat has zero authority.** It is a draft surface. Nothing is decided until it is committed. State this out loud at the start of the session, because the failure is psychological before it is procedural.
2. **One session → one artefact → one commit.** The session ends by writing exactly one markdown file to a declared path (`.product/` per-project, or `.aidocs/` at workspace level), committed in the same change as its CHANGELOG entry. A session that produces no file produced nothing.
3. **Provenance frontmatter is mandatory.** Every imported artefact carries `source: chatgpt-plus | gemini-ai-pro | claude-pro`, `session_date:`, `bundle: <name>@<version>`, `inputs: [...]`, `model:` if known. Without this you cannot later tell whether a claim was researched or invented, and six months on you will not remember.
4. **One-way valve: close the thread.** After export, the thread is dead. Reopening it "just to tweak" is the single act that creates the second source of truth. The next revision starts from the committed file, pasted in fresh, in a new thread.
5. **Repo wins on conflict. Always. No merge.** If the thread and the file disagree, the file is right and the thread is stale — even when you're sure the thread is better. If the thread really is better, that's a new session against the current file.
6. **Gate it.** Our `readiness.md` check refuses to advance a feature whose referenced artefacts have no committed file at the declared path. Make the discipline a gate, not a habit — habits decay under deadline and gates don't.
7. **Prefer retyping to exporting for small artefacts.** A Canvas export carries formatting cruft, no provenance, and the psychological weight of "already finished." Retyping a one-page brief into the repo takes four minutes and is itself a review pass.

Rules 4 and 5 do all the work. The other five are hygiene.

### Data policy: what must never be pasted into a consumer-tier assistant

The vendors' own words, all consulted 2026-08-03:

- **Google (Gemini Apps Privacy Hub):** *"Please don't enter confidential information that you wouldn't want a reviewer to see or Google to use to improve our services, including machine-learning technologies."* Trained human reviewers read, annotate, and process conversations; selected conversations are retained for extended periods **even when activity history is off**. Enterprise (Workspace / Cloud) data is not used for training and stays in the tenant.
- **Anthropic (Consumer Terms update, 2025-08-28):** chats and coding sessions are used to train and improve models **unless you opt out** — Free, Pro, and Max alike; the selection deadline was 2025-10-08. Opted in: up to **5 years** de-identified retention. Opted out: 30-day retention, no training use. Setting is "Help improve Claude" → OFF in Privacy Settings, and it applies only to new or resumed chats.
- **OpenAI:** consumer ChatGPT may use prompts, responses, images, and files to improve model performance depending on settings; opt out at **Settings › Data Controls**. **Business, Enterprise, and API default to no training.** On ownership, the Terms *"assign to you all its right, title, and interest in and to Output"* — commercial use of output is permitted. *(Sourced via search summaries of `terms.law` analysis and OpenAI Help Center articles; `openai.com/policies/row-terms-of-use` returned HTTP 403 to the fetcher — **not read primary**, flagged in Open questions.)*

**The never-paste list:**

| Category | Why |
|---|---|
| Client / customer data of any kind | You have no DPA with a consumer account. Pasting it is a processor-agreement breach before it is anything else. |
| Personal data of third parties | GDPR: no lawful basis, no processor agreement, and human reviewers are in scope. |
| Credentials, API keys, tokens, connection strings | Retained, possibly reviewed, possibly trained on. Rotate anything you've already pasted. |
| Unreleased financials, cap tables, term sheets | Retention windows outlast your embargo. |
| Anything under an NDA or a contract confidentiality clause | The clause does not carve out "but I told a chatbot." |
| Security findings, vulnerability detail, infra topology | Same retention, worse blast radius. |
| **Our methodology bodies** | **This is the product.** 3,070 tier-gated entries. Pasting them into a consumer account is both a sealing breach (D-001) and, plausibly, training data. |

**The operative test is Google's own sentence:** if you would not want a human reviewer to read it, do not type it.

**Two mitigations, ranked:**

1. **Turn training off** on whichever tier you use. Free, immediate, and incomplete — Google still retains selected conversations for review with activity history off, and the setting only binds new sessions.
2. **Pay for the no-train default.** **ChatGPT Business is $25/user/mo against Plus at $20** — five dollars a month to flip the default from "trains unless you opt out" to "no training, ever, by contract." For any solopreneur who touches client work, this is the single highest-leverage line in this dossier. The arbitrage argument that justifies $20 justifies $25 just as easily, and $25 is the version you can put in an NDA.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | `web-bundles/README.md` | `gh api repos/bmad-code-org/BMAD-METHOD/contents/web-bundles/README.md` | The flat-rate rationale verbatim; six-bundle shelf; plan requirements; single-front-door reasoning; `bmad-os-skill-to-bundle` pointer | 2026-08-03 |
| 2 | `web-bundles/bundles.json` | same repo path | `releaseTag: web-bundles-v1.0.0`, `releasedAt: 2026-05-25`, per-bundle `knowledgeFiles` / personas / `needsDeepResearch` | 2026-08-03 |
| 3 | `web-bundles/prfaq-coach/` contents | `gh api .../contents/web-bundles/prfaq-coach` | Measured file sizes: `SKILL.md` 11,223 B, `INSTRUCTIONS.md` 5,023 B | 2026-08-03 |
| 4 | Web Bundles explanation | https://docs.bmad-method.org/explanation/web-bundles/ | Persona-in-instructions / protocol-in-knowledge split; economics; when NOT to use; the one-sentence artefact handoff | 2026-08-03 |
| 5 | BMad Update: Web Bundles for Gemini & ChatGPT, plus BMM v6.8.0 | https://www.bmadcode.com/bmad-update-may-2026-web-bundles-prd-brief-platforms/ | Release date 2026-05-25; six bundles; "planning on a flat-rate Gemini Advanced or ChatGPT Plus subscription, IDE budget reserved for codebase work" | 2026-08-03 |
| 6 | Claude pricing | https://claude.com/pricing | **Primary** — Free $0, Pro $17 annual / $20 monthly, Max 5x from $100, Max 20x (20× Pro usage); Claude Code included from Pro up | 2026-08-03 |
| 7 | Gemini Apps Privacy Hub | https://support.google.com/gemini/answer/13594961 | Human review; the "don't enter confidential information" instruction; retention with activity off *(via search summary)* | 2026-08-03 |
| 8 | Updates to Consumer Terms and Privacy Policy | https://www.anthropic.com/news/updates-to-our-consumer-terms | 2025-08-28 change; opt-out; 5-year vs 30-day retention; 2025-10-08 deadline *(via search summary)* | 2026-08-03 |
| 9 | OpenAI Terms of Use / Data Usage FAQ | https://openai.com/policies/row-terms-of-use/ · https://help.openai.com/en/articles/7039943 | Output assignment; consumer training default; Data Controls opt-out; business/API no-train default — **403 to fetcher, via search summary only** | 2026-08-03 |
| 10 | Custom GPT vs Gem knowledge limits | knowledgebuilderpro.com · learnprompting.org · customgpt.ai | 20 files / 512 MB / 2M tokens (Custom GPT); 10 files (Gem) — **secondary** | 2026-08-03 |
| 11 | Anthropic model catalogue + prompt-caching economics | `claude-api` skill, `shared/prompt-caching.md` | Opus 5 $5/$25, Sonnet 5 $3/$15; cache read 0.1×, write 1.25×/2×; 20-block lookback; 512-token minimum on Opus 5 | cached 2026-06-24, read 2026-08-03 |

## What to borrow for faion

1. **The tool-fit argument, stripped of the token argument.** "Planning wants conversation, Canvas, and Deep Research; implementation wants the codebase and a terminal" is true independent of pricing, and it stays true when every model on earth is flat-rate. Lead with that. Never lead with cost — our own positioning rule forbids token-denominated framing, and the cost claim is the weak half anyway.
2. **The protocol/persona split.** Protocol in the knowledge file, persona in the instructions, so voice changes without touching the method. Our methodologies currently fuse the two. Separating them would let one `working-backwards-prfaq` methodology serve a blunt register and a gentle one from a single source — and it is a cleaner answer to "can I customise this" than forking content.
3. **A tiny, portable protocol export.** BMAD proved a serious coached workflow fits in ~11 KB of markdown. That is a shape worth having: a `faion export --protocol <slug>` that emits a self-contained, runtime-agnostic markdown protocol for a **single free-tier methodology**, runnable anywhere including a Gem. It is a legitimate top-of-funnel artefact and it does not leak the corpus, because one free methodology is already free.
4. **Provenance frontmatter as a corpus-wide convention.** `source` / `session_date` / `bundle` / `inputs`. Costs nothing, and it is the only thing standing between "we researched this" and "an assistant asserted this." Applies to every artefact we import from anywhere, not just chat exports.
5. **The one-way-valve discipline as a shippable methodology.** This is a genuinely reusable operating procedure for solopreneurs working across multiple AI surfaces, and — see the gap analysis below — nobody in our corpus has written it.
6. **The $25 Business-tier insight.** Concrete, actionable, five dollars, flips the data default. This belongs in whatever methodology we write about working with consumer AI tiers.
7. **Quota-pool topology as an explicit planning input.** We already live this (Claude Max + Codex/OpenAI Max, project memory `runtime-budget-topology`) but it exists as tribal knowledge in session memory rather than as a methodology. It should be written down: which pools you hold, which work each pool is allowed to touch, what happens when one hits its ceiling.

## What NOT to borrow — and why

- **Uploading our corpus to a Gem or Custom GPT.** Breaks content sealing (D-001), breaks tier gating (3,070 manifest entries collapse to one access level), and replaces our designed two-level retrieval with vendor RAG we cannot inspect. Non-starter at any scale.
- **"Save tokens" as a marketing frame.** Wrong on the merits (planning is the *cheap* long session once caching is on) and wrong on positioning (we do not price in tokens; we spend zero at runtime on customer work). Using it would anchor buyers on the exact unit our own rules forbid.
- **A hosted install front door.** BMAD centralises on `bmadcode.com/web-bundles` explicitly to keep install steps current and to capture a mailing list. Fine for them. For us it is a new web surface to maintain, on top of `faion.net`, `api.faion.net`, `dev.faion.net`, and `storybook.faion.net`, and our distribution is already a signed single binary.
- **Treating "pasteable into repositories" as sufficient.** It is the one-sentence version of the hardest problem in the pattern. If we ship anything here, the discipline is the deliverable and the export is the trivial part.
- **The pattern for anything needing repo context.** BMAD says this themselves under *When staying in the IDE makes sense*: tasks needing codebase context or file modification, mid-implementation continuity. Honour that boundary exactly.
- **Consumer tiers for client work, at all, without the Business/Workspace upgrade.** Not a preference — a DPA question.
- **Deep Research as a load-bearing dependency.** BMAD flags that *"Deep Research has its own plan limits."* A workflow that assumes it will hit a wall you cannot see coming.

## Mapping to our corpus

Ground truth read 2026-08-03: `tier-manifest.json` v8 (`updated: 2026-05-07`, `last_synced: 2026-05-23`), 3,070 entries — free 129 / solo 841 / pro 1,405 / geek 695.

**Adjacent-but-not-this** (grepped all 22 `INDEX.xml` files for `token|cost|budget|spend|quota|subscription|pricing`, 2026-08-03):

| Our slug | Domain | Why it isn't this |
|---|---|---|
| `inference-cost-unit-economics` | `ai-core` | Your product's inference bill, not your own workflow's |
| `cost-quality-tradeoff-framework`, `cost-quality-pareto-template`, `cost-vs-quality-decision-log` | `ai-core` | Model selection for a shipped feature |
| `cost-slo-per-task-template`, `cost-per-dau-defense-template` | `ai-core` | Production SLOs |
| `weekly-llm-cost-review-template` | `ai-core` | **Closest existing artefact** — a review cadence over LLM spend. Still product-side, not workflow-side. |
| `agent-eval-cost-budget-policy` | `ai-agents` | Eval-harness budgets |
| `agent-reasoning-depth-budget` | `ai-core` | Effort tuning per call |
| `finetune-cost-vs-prompt-decision` | `ai-core` | Build-vs-prompt |
| `ai-coding-agent-handoff-protocol` | `sdlc-ai` | **Closest structural sibling** — handoff between agents. Not handoff between *runtimes and surfaces*. |
| `kb-agents-md-context-pyramid` | `sdlc-ai` | Context layering within a repo |
| `adr-supersession-detection` | `sdlc-ai` | Detects superseded decisions — the *symptom* of a second source of truth, not the prevention |
| `impl-plan-100k-rule` | `sdd` | Plan sizing; the nearest thing we have to context-budget thinking |

**Two real gaps, both worth filling:**

**Gap 1 — `sdlc-ai/multi-surface-planning-handoff`** (proposed). The one-way-valve discipline: chat has zero authority; one session → one artefact → one commit; provenance frontmatter; close the thread; repo wins on conflict; gate on committed file; retype small artefacts. Plus the never-paste list and the Business-tier upgrade. This is a genuinely reusable operating procedure and **nothing in 3,070 entries covers it**. `sdlc-ai` currently has 277 lines of index — it is a thin domain with room.

**Gap 2 — `ai-core/workflow-runtime-budget-topology`** (proposed). Which quota pools you hold, what each is allowed to touch, ceiling behaviour, and the crucial correction that a flat-rate agent SDK is not a free agent SDK. All eleven of our cost methodologies are about the customer's bill; **none is about your own.** This one carries the token math from this dossier — Scenario A vs Scenario B, and the finding that agentic implementation, not planning, is where spend concentrates.

**Tiering both: solo.** Free is deliberately thin (129 of 3,070 = 4.2%). These are operational-discipline pieces — high value to a working solopreneur, low value as a teaser, and the 30% preview carries enough (the never-paste list, the two scenario headlines) to be a real hook.

**On the untracked `skills/bmad-*/`:** delete (full reasoning in `bmad-method.md`). Nothing in the web-bundles pattern needs the vendored skills to survive — the mechanism is documented here, the bundles live in a public repo we can re-read, and everything we'd want to build is our own writing anyway.

## Open questions / staleness risk

- **We have no measured per-phase token telemetry.** Scenarios A and B are modelled from stated assumptions and list prices. The ~8× ratio is the load-bearing claim in this dossier and it is *derived*, not observed. **Instrumenting one real SDD feature end-to-end — planning turns vs. executor turns, with cache-hit rates — would either confirm this or kill it,** and it is a day of work. Until then, treat the direction as sound and the magnitude as soft.
- **OpenAI and Google prices are secondary-sourced.** Both vendor pricing pages defeated the fetcher (403 / price-less render) on 2026-08-03. Numbers are from reputable aggregators consulted the same day. Consumer AI tiers restructured at least twice in 2026 (ChatGPT Pro split into $100/$200 on 2026-04-09; Google Ultra cut $249.99 → $99.99 at I/O 2026). **Re-verify before any of this reaches customer-facing copy.**
- **OpenAI Terms of Use not read primary.** The output-assignment and commercial-use claims come from a legal-analysis site's reading of the terms, not the terms themselves (403). Before we publish anything asserting commercial-use rights on consumer tiers, read the actual document.
- **Anthropic Max 20x price marked `~$200`.** `claude.com/pricing` rendered the Max tiers in a shared block that the fetcher read as "From $100/month" for both. Secondary sources agree on $200.
- **Claude Pro / Projects has no shareable bundle format** comparable to Gems or Custom GPTs, so the BMAD pattern is structurally OpenAI/Google-only today. If Anthropic ships a shareable Project/Skill export, the calculus changes — and for us it would change *badly*, since the whole point is a pool separate from Claude.
- **Web Bundles are five releases old and untouched.** v1.0.0 shipped 2026-05-25 with v6.8.0; the line has since reached v6.10.0 (2026-07-03) with no bundle updates in the CHANGELOG. Either stable or unloved — I cannot tell which from the repo alone.
- **Unverified: does anyone actually keep the discipline?** The seven rules above are derived from reasoning about the failure mode, not from observing teams succeed or fail at it. That is the honest status. If we ship Gap 1 as a methodology, it should say so.

---

## Verdict: does flat-rate planning arbitrage actually work?

**Partly. It survives as one thing and dies as another, and the landscape doc has hold of the wrong half.**

**What dies — the token-savings argument.** Two independent problems. First, prompt caching already collapses the cost of exactly the workload the argument targets: a long planning conversation is the *best-case* cache shape (stable prefix, small deltas, near-total reads at 0.1×), which is why Scenario A drops from ~$12 to ~$3. The expensive thing in an AI-assisted build is the agentic implementation loop, where tool results are the token firehose and the 20-block lookback window, compaction, and context rewrites break caching in ways a chat never does — roughly 8× the planning session, cached. **The pattern moves your cheapest long session off the meter and leaves the expensive one exactly where it was.** Second, for us it is not even arbitrage: Claude Max is already flat-rate and the Agent SDK draws the same quota, so adopting this adds a $20/mo line item rather than removing one.

**What survives — three things, none of them about tokens.**

1. **Tool fit.** Canvas, Deep Research, and image generation are genuinely better planning affordances than a terminal, and a terminal is a genuinely better implementation surface than a chat window. This is true at any price and stays true when everything is flat-rate. It is BMAD's *other* stated rationale and it is the stronger one.
2. **Quota-pool diversification.** For anyone on a flat-rate plan, the scarce resource is not dollars but the 5-hour and weekly windows — and hitting the weekly ceiling stops implementation dead. A $20/mo pool that absorbs context-free planning work buys implementation headroom. That is real, it is exactly the shape of value we already get from Codex under OpenAI Max, and it is worth $20/mo the moment a weekly ceiling costs you a day. Note the honest framing: this is **buying a second bucket, not saving money.**
3. **A forcing function on artefact discipline.** The pattern makes the planning→building handoff a physical boundary you cannot fudge. You must export something, and something you must export is something you must actually decide. Teams that hand off within one runtime skip this constantly.

**Where it breaks, cleanly and predictably: the moment the work needs repo context.** Brownfield analysis, "does this fit our existing architecture," anything reading a spec that lives in the repo, any decomposition grounded in the current codebase — all of it either fails outright or, far worse, succeeds *plausibly* against a codebase the model has never seen. BMAD is honest about this boundary; the risk is that users are not, because a confidently-wrong plan built on imagined architecture is more expensive than any token bill it saved.

**So: is it penny-wise arbitrage that breaks on repo context?** As a cost play, yes — genuinely penny-wise, and it optimises the wrong phase. As a **surface-fit and quota-topology play with a hard artefact gate**, no — it is a sound operating pattern with a well-defined boundary.

**What we should actually do:** take the discipline, take the protocol/persona split, take the quota-pool topology, write both gap methodologies. Do not take the framing, do not take the corpus upload, do not take the marketing line. And if we ever say any of this out loud to a customer, say *"plan where planning is best, build where the code is"* — never *"save tokens."*
