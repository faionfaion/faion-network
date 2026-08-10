# Desk Research Tools (Perplexity, Elicit, Consensus, Scite, OpenAI/Gemini Deep Research)
**Layer:** 5 — Domain · **Cluster verdict:** 🟡 take the idea, not most of the tools · **Verified:** 2026-08-03

Cluster read: one general web-search tool (Perplexity) is worth a solopreneur's money outright; the two academic-corpus tools (Elicit, Consensus) and the citation-graph tool (Scite) are narrow-scope specialists that are usually the wrong tool for a business question, not defective ones; and the two vendor "Deep Research" agents (OpenAI, Gemini) have now automated the exact decompose→search→synthesize loop our `perplexity-ai-research` methodology hand-rolls — which does not make the methodology obsolete, it moves its value up one layer, from "how to decompose a query" to "which tool, when, and how to verify what it hands back." The empirical anchor for that verification requirement: the best-performing AI search tool in the only rigorous third-party citation-accuracy audit found still got more than 1 in 3 answers wrong. Per-tool detail and the two closing arguments (partial-substitute, re-tiering) follow.

---

# Perplexity
**Layer:** 5 — Domain · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

An AI-native search engine: user asks a question in natural language, Perplexity runs live web retrieval, and returns a synthesized answer with inline numbered citations to the sources it used. It is the only tool in this cluster designed as a general-purpose research front-end rather than a scoped academic index, and it is the tool our own `perplexity-ai-research` methodology is built directly around.

## Current state

- **Maintainer:** Perplexity AI, Inc. (San Francisco; founded August 2022 by Aravind Srinivas, Denis Yarats, Johnny Ho, Andy Konwinski) — per Wikipedia, checked 2026-08-03.
- **Price for one person:** Perplexity Pro is widely and consistently reported at **$20/month** (or ~$200/year annual). The live `perplexity.ai/pro` pricing page returned HTTP 403 to automated fetch at time of writing (Cloudflare bot protection blocks the fetch tool on the whole `perplexity.ai` app domain) — **this figure is not independently re-confirmed from the primary page today and should be manually re-checked before quoting to a customer.**
- **API pricing (confirmed primary source, `docs.perplexity.ai`, checked 2026-08-03):** Sonar (standard) $1/1M input + $1/1M output tokens plus $5–12 per 1,000 requests by context size; Sonar Pro $3/1M in + $15/1M out; Sonar Deep Research $2/1M input + $8/1M output + **$2/1M citation tokens + $3/1M reasoning tokens + $5 per 1,000 search queries** — billed as separate line items. This confirms Perplexity's Deep Research model is not a single generation pass: it meters searches, reasoning, and citations as distinct cost centers, which is direct structural evidence of an internal multi-step pipeline (see Mechanics).
- **2026 change:** per Wikipedia, "In February 2026, Perplexity transitioned to a subscription-first model by discontinuing its AI-integrated advertising strategy" — worth re-checking for a Pro-price change at the next audit, since ad-revenue removal often precedes a price move.
- **Free tier:** unlimited basic search; Deep Research is capped. Perplexity's own launch announcement states **"Up to 5 queries per day for non-subscribers and 500 queries per day for Pro users"** (Perplexity AI official LinkedIn post announcing Deep Research; corroborated by Tom's Guide and secondary trackers, checked 2026-08-03). These are the launch-era caps and were the most recent published figures retrievable today — the live help-centre page 403'd, so treat them as directionally right rather than freshly reconfirmed.
- **Pro consumer price cross-check:** two independent price trackers (costbench.com, aipromptshub.co, both checked 2026-08-03) agree on **$20/month or $200/year**, and both list "600 daily Pro queries" plus model choice (GPT-5.5 / Claude Opus / Grok / Sonar / Gemini 3.x class) as what Pro unlocks. Higher tiers exist: Max $200/mo, Education $10/mo, Enterprise $40–325/mo.

## Mechanics

1. User submits a question via web/app/API.
2. Base "Search" mode runs a small number of retrieval passes and synthesizes a short cited answer — this is roughly one decompose-search-synthesize cycle done for you.
3. **Pro Search / Sonar Deep Research** goes further. Perplexity's own launch post describes the mode verbatim as one that **"performs dozens of searches, reads hundreds of sources, and reasons through the material to autonomously deliver a comprehensive report"** (`perplexity.ai/hub/blog/introducing-perplexity-deep-research`; the page itself 403s to automated fetch, this exact sentence was recovered as the indexed snippet of that URL and independently repeated verbatim by ZDNET's write-up, both checked 2026-08-03). The API docs corroborate with "Expert-level research model conducting exhaustive searches and generating comprehensive reports" (`docs.perplexity.ai`, checked 2026-08-03). Third-party testing puts a typical run at **2–4 minutes** (secondtalent.com review, 2026). Concretely it it plans a research approach, runs a series of searches (billed per 1,000 searches, confirming this is genuinely plural), reasons over what it finds (billed as separate "reasoning tokens"), and produces a longer cited report. Perplexity does not publish a user-facing "edit the plan first" step the way Gemini does (see below) — it appears close to fully autonomous per query, not plan-then-approve.
4. Output is inline-cited; there is no built-in per-claim confidence rating or mandatory human-verification gate — that is exactly the layer our methodology adds (see `01-core-rules.xml`: `recency-filter-when-market-data`, `citation-source-link-required`, `compare-two-tools-on-stakes-questions`).

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Sonar Deep Research model page | docs.perplexity.ai/getting-started/models | One-line mechanics description: "exhaustive searches and generating comprehensive reports" | 2026-08-03 |
| 2 | Perplexity API pricing | docs.perplexity.ai/getting-started/pricing | Exact per-model token + per-request + per-search-query pricing | 2026-08-03 |
| 3 | Perplexity AI — Wikipedia | en.wikipedia.org/wiki/Perplexity_AI | Founding, Feb 2026 ad-model exit, general product description | 2026-08-03 |
| 4 | Tow Center 8-tool citation study | cjr.org/tow_center (see Perplexity's 37% figure below) | Perplexity ranked best-of-8 on citation accuracy, still 37% wrong | 2026-08-03 |
| 5 | Introducing Perplexity Deep Research | perplexity.ai/hub/blog/introducing-perplexity-deep-research | "dozens of searches, reads hundreds of sources, and reasons through the material" — vendor's own mechanics sentence (page 403s; snippet-recovered) | 2026-08-03 |
| 6 | Perplexity AI official Deep Research announcement | linkedin.com/posts/perplexity-ai_introducing-deep-research | 5 queries/day free, 500/day Pro | 2026-08-03 |

## What to borrow for faion

- The billed-separately search/reasoning/citation token split is a good mental model to teach solopreneurs for *why* Deep-Research-style tools cost more than a chat answer — it is doing measurably more retrieval work, not just a longer generation.
- Keep `perplexity-ai-research`'s mandatory `search_recency_filter=year` rule — nothing in Perplexity's own docs auto-applies recency filtering by default, so a stale market figure presenting as current remains a real, un-mitigated failure mode.

## What NOT to borrow — and why

- Do not present Perplexity's Deep Research mode as replacing our decision-tree / tool-selection step. It decomposes and searches well; it does not know when Perplexity itself is the wrong corpus for the question (e.g., a peer-reviewed claim, where Consensus/Scite are more appropriate) — that judgment stays outside the tool.
- Do not carry forward an unverified "$20/mo" price into customer-facing copy without a manual re-check; the live page is unreachable by automated tooling right now, which is itself worth knowing (bot-hardened pricing pages are a recurring pattern across every vendor in this cluster — see Elicit/Consensus/Scite below, all 403'd too).

## Mapping to our corpus

`skills/faion/knowledge/research/perplexity-ai-research` (tier: geek) already encodes atomic sub-queries, recency filters, per-claim H/M/L confidence, and a mandatory `verified_by` gate before downstream use — i.e., it already assumes Perplexity's own decomposition is not enough and bolts a verification layer on top. `ai-research-tools` (tier: geek) is the tool-selection map that routes a question to Perplexity vs. Consensus/Scite/NotebookLM by `evidence_type`. Both are current in substance; the tier assignment is the open question (see Re-tiering, below).

## Open questions / staleness risk

- Perplexity Pro consumer price not reconfirmed from the vendor's own live page today (403); two independent price trackers agree on $20/mo, which is strong but still secondary.
- The 5/day-free, 500/day-Pro Deep Research caps come from Perplexity's own launch announcement, not a currently-fetchable help page — they may have moved since launch.

---

# Elicit
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is

An AI research assistant scoped to peer-reviewed literature: search, summarize, and extract structured data (as spreadsheet-style "columns") across a large academic paper index, with a dedicated systematic-literature-review workflow (paper screening at scale, PRISMA-adjacent). Built by Elicit, Inc. — note: an automated fetch of `elicit.com/pricing` mis-attributed Elicit's maintainer as "Anthropic" (an artifact of the page-summarizing tool conflating an unrelated Claude/SDK mention on the page with the company identity) — **this is corrected here**: Elicit is an independent company, not an Anthropic product.

## Current state

Per `elicit.com/pricing`, fetched 2026-08-03:

- **Basic (free):** "Unlimited search across more than 138 million papers," unlimited summaries, unlimited full-text chat with papers.
- **Pro: $49/month** (billed annually at $588/yr, ~35% discount) — Research Agent + Research Reports + a Systematic Review workflow that screens up to 5,000 papers, 20 extractable table columns, up to 135 data sources, 10 alerts, API access.
- **Scale: $169/month** (billed annually at $2,028/yr, ~39% discount) — 5x core usage, live team collaboration, figure extraction, 200 data sources, 30 columns, admin/usage tracking.
- **Enterprise:** custom pricing — unlimited alerts, 40,000-paper screening, 40 columns, SSO/SAML.

## Mechanics

Retrieval-then-summarize, not free generation: Elicit maintains its own index (claimed 138M+ papers) built substantially from open scholarly metadata sources (overlapping with the Semantic Scholar corpus, which itself claims **214 million papers, 2.49 billion citations, 79 million authors** per Semantic Scholar's own API page, checked 2026-08-03). Every citation Elicit shows resolves to a real indexed paper with real metadata (title/authors/DOI/abstract) before any LLM touches it — the LLM's job is confined to summarizing or extracting from a document that is already known to exist. This structurally forecloses the "invented paper" failure mode that a bare LLM chat has (it can misread or over-summarize a real paper, but it cannot cite one that isn't in the index).

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Elicit pricing page | elicit.com/pricing | Exact tier pricing, corpus size claim, workflow gating | 2026-08-03 |
| 2 | Semantic Scholar API product page | semanticscholar.org/product/api | 214M papers / 2.49B citations / 79M authors — corroborates order-of-magnitude of Elicit's 138M claim | 2026-08-03 |

## What to borrow for faion

- The retrieval-then-summarize architecture is the right mental model to teach as *why* "cannot fabricate references" is true for this category of tool and NOT true for a bare LLM chat — worth stating explicitly in `ai-research-tool-categories`.
- The systematic-review screening workflow (thousands of papers, structured columns) is a good reference shape for a future methodology on *AI-assisted literature triage*, if faion ever serves a research-heavy vertical (health, longevity — see `longlife-faion-net` in our own portfolio).

## What NOT to borrow — and why

- Do not recommend the Elicit subscription itself to a general solopreneur doing market/competitive research. Its entire corpus is peer-reviewed academic literature; a question like "what's our TAM" or "who are our top 5 competitors" has no meaningful peer-reviewed literature to retrieve — the tool will either return nothing on-point or force the question into an academic framing that's usually 1-3+ years stale by publication. This is a scope mismatch, not a quality defect — Elicit is good at what it's built for, and that isn't this.
- Do not carry the $49-169/mo price point into a "cheap tool alternative" argument — it is more expensive than Perplexity Pro and delivers less value for a solopreneur whose research questions are mostly market/business-shaped, not literature-review-shaped.

## Mapping to our corpus

Referenced in `ai-research-tools/content/01-core-rules.xml` (`match-tool-to-evidence-type`: "meta-analysis → Elicit") and in `ai-research-tools` AGENTS.md's applies-if list. The rule is directionally correct: Elicit's `evidence_type` slot is scientific/meta-analytic claims specifically, never market data.

## Open questions / staleness risk

- Elicit's own "138 million papers" figure is the vendor's own claim (not independently cross-verified against a corpus audit) — treat as vendor-reported, not measured.

---

# Consensus
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is

An AI search engine scoped to peer-reviewed scientific literature, built on top of the Semantic Scholar corpus. A user asks a yes/no or claim-shaped question ("does X cause Y") and Consensus returns a synthesized answer with a **consensus meter** (rough distribution of supporting/mixed/against findings) plus direct links to the underlying papers — positioned squarely for scientific/evidence questions, not general search.

## Current state

- `consensus.app/pricing` and `consensus.app` both returned HTTP 403 to automated fetch at time of writing — **pricing and corpus-size figures below could not be independently re-confirmed from the live primary source today** and should be manually re-checked before quoting to a customer.
- Widely and consistently reported (secondary sources, pre-dating today's audit) individual pricing has historically sat in the **~$9-12/month** band for a Premium/Pro individual tier, well below Elicit and Perplexity Pro, with a metered free tier (limited "AI credits"/month).
- Corpus: Consensus is built on the Semantic Scholar Academic Graph, which itself claims 214M papers (semanticscholar.org, checked 2026-08-03) — consistent with, and a plausible source for, a "200M+ papers" claim.

## Mechanics

Same retrieval-then-summarize category as Elicit: Consensus queries a real indexed corpus (Semantic Scholar) and generates its "consensus meter" and summary from retrieved paper abstracts/metadata, rather than free-generating citations. Same structural anti-fabrication property as Elicit follows: it cannot cite a paper that isn't in the Semantic Scholar graph.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Semantic Scholar API product page | semanticscholar.org/product/api | Corpus size (214M papers) that underlies Consensus's claimed 200M+ figure | 2026-08-03 |
| 2 | consensus.app / consensus.app/pricing | — | 403 Forbidden on both fetch attempts — flagged, not independently confirmed today | 2026-08-03 (attempted) |

## What to borrow for faion

- The "consensus meter" (distribution of study findings, not a single synthesized answer) is a genuinely good UX pattern to reference when teaching solopreneurs how to read AI-summarized evidence — it visually signals "this is contested" rather than presenting one confident answer, which is the opposite failure mode of a chat-style tool.

## What NOT to borrow — and why

- Same scope mismatch as Elicit: Consensus is explicitly a science-claim tool. Market/business questions ("is there demand for X," "what's the pricing benchmark for Y SaaS") are not the shape of question it's built to answer, and it will either come back empty or force-fit an unrelated academic paper.
- Do not repeat the "200M+ papers" figure as independently verified — it traces to Semantic Scholar's own claim, one hop removed from Consensus's marketing, not a fetch of Consensus's own page today.

## Mapping to our corpus

Referenced alongside Elicit/Scite in `ai-research-tools`'s `match-tool-to-evidence-type` rule (`scientific_claim → Consensus/Scite`). Correctly scoped in our existing methodology — no change needed to the rule itself, only to tier placement (see closing section).

## Open questions / staleness risk

- Live pricing/marketing pages unreachable today (403) — price band and B2B-use evidence above rest on general/secondary knowledge, not a fresh primary fetch. Flag for re-check at next audit pass.

---

# Scite
**Layer:** 5 — Domain · **Verdict:** 🔴 skip — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

A citation-verification tool, not a discovery tool: its "Smart Citations" feature classifies every citation a paper has received from *later* papers as **supporting**, **contrasting**, or **mentioning**, via an NLP classifier trained on the citing sentence's context (not a raw citation count). The use case is "has this specific claim held up under later scrutiny," which is a materially different job from Elicit/Consensus's "find and summarize relevant papers."

## Current state

- `scite.ai/pricing` returned 403 to automated fetch — **not independently reconfirmed from the live primary page today.**
- Historically and consistently reported (secondary sources) individual pricing has sat around **~$20/month** for an individual plan, with institutional/lab tiers priced separately and considerably higher.
- Maintainer: scite (scite.ai), a citation-analysis company distinct from the unrelated "SciTE" open-source text editor (a namespace collision worth flagging so nobody cites the wrong "Scite" in customer-facing copy).

## Mechanics

Retrieval-then-classify: real citing papers are pulled from publisher-partnership data, and each citation *statement* (the actual sentence doing the citing) is run through a supporting/contrasting/mentioning classifier. Like Elicit/Consensus, citations are always real — the model's job is narrow classification of a real sentence, not generation.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | scite.ai/pricing | scite.ai/pricing | 403 Forbidden — not independently confirmed today | 2026-08-03 (attempted) |

## What to borrow for faion

- The supporting/contrasting/mentioning citation classification is a useful concept to name explicitly in `03-failure-modes.xml` for `ai-research-tools`: "a citation existing is not the same as a citation supporting the claim" — this is exactly the nuance a solopreneur skimming AI search output tends to miss, and it's the sharpest single idea in this whole cluster.

## What NOT to borrow — and why

- This is the clearest 🔴 in the cluster: Scite answers "has this scientific claim been contested by later research," which is almost never the shape of a solopreneur's business question. Recommending a ~$20/mo Scite subscription to a general (non-research-vertical) solopreneur would be pure waste. It only earns a place if faion ever serves a science/health-claims-heavy vertical (again: `longlife-faion-net` is the one portfolio project where this could plausibly matter).

## Mapping to our corpus

Named in `ai-research-tools` AGENTS.md's one-sentence summary and `match-tool-to-evidence-type` alongside Consensus for `scientific_claim`. Fine as a taxonomy entry; should not be elevated into a recommended purchase for a general audience.

## Open questions / staleness risk

- Pricing not independently reconfirmed today (403). Namespace collision with the unrelated SciTE text editor risks a wrong citation in future desk research if someone searches "Scite" without the `.ai` qualifier — worth a standing note in the methodology itself.

---

# OpenAI Deep Research
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is

An agentic mode inside ChatGPT that autonomously browses the web (and can read text/images/PDFs) for an extended period and returns a long, cited report on a user-specified topic — the most direct commercial embodiment of the decompose→search→synthesize loop our own methodology hand-codes.

## Current state

- **Maintainer:** OpenAI.
- **Launch:** February 2025, originally on a specialized o3 model; per Wikipedia (checked 2026-08-03), upgraded to a GPT-5.2-based model in February 2026, with that update adding "better steering, limiting scope to select sites, connecting additional data using MCP servers."
- **Price for one person / access & limits (per Wikipedia, sourced to OpenAI's own figures, dated "as of June 2025" — not independently reconfirmed against a live OpenAI page today; `openai.com` and `help.openai.com` both returned 403 to automated fetch on every attempt):**
  - ChatGPT Pro — **$200/month** — 250 Deep Research queries/month (125 lightweight).
  - ChatGPT Plus/Team/Enterprise — **$20/month** (Plus) — 25 Deep Research queries/month (15 lightweight).
  - Free — 5 "lightweight" queries/month.
  - **These limits are 14 months stale relative to today's date and should be manually re-checked** — OpenAI has a track record of adjusting Deep Research quotas as underlying model costs change.
- **Conflicting 2026 figures — flagged, unresolved:** several independent price trackers (StackSheriff, Prismer.ai, BuyersPrint, all checked 2026-08-03) now report the Plus allowance as **10 full Deep Research runs/month** (down from 25) and the Pro allowance as "unlimited subject to fair use," with an observed practical ceiling around **120 reports/month** (down from a stated 250). Both the June-2025 and the 2026 tracker figures are reported here with their dates because OpenAI's own pages are unreachable to automated fetch and neither figure could be adjudicated today. **Do not quote a specific Deep Research quota to a customer without a manual check on a logged-in account.**

## Mechanics

**Primary source now in hand** — OpenAI's *Deep Research System Card* (PDF, published 2025-02-25, fetched 2026-08-03), which states directly: *"Deep research is a new agentic capability that conducts multi-step research on the internet for complex tasks… Deep research leverages reasoning to search, interpret, and analyze massive amounts of text, images, and PDFs on the internet, **pivoting as needed in reaction to information it encounters**."* The "pivoting as needed" clause is the decisive wording: this is an adaptive loop (search → read → re-plan → search again), not a fixed fan-out of pre-written sub-queries. It can also execute Python for data analysis mid-run. Wikipedia (checked 2026-08-03) adds the wall-clock figure: reports are generated "by autonomously browsing the web for 5 to 30 minutes."

**Does it ask clarifying questions first?** Split by surface, and this distinction matters for our methodology. In the **ChatGPT UI**, Deep Research asks the user one round of clarifying questions before launching — widely documented since the Feb 2025 launch, but I could not re-confirm it from OpenAI's own page today (403). Via the **Responses API**, per OpenAI's developer docs, there is *no* clarification step by default: the agent "generates a research plan internally and starts executing without user interaction." So the human-in-the-loop checkpoint is a product-surface choice, not a property of the model — worth knowing before assuming any Deep Research call will pause to ask.

**Groundedness numbers (system card, Table 11, PersonQA eval):** deep research scored **0.86 accuracy / 0.13 hallucination rate**, against GPT-4o (0.50 / 0.30), o1 (0.55 / 0.20) and o3-mini (0.22 / 0.15). OpenAI's own caveat is that the 0.13 figure "overstates how often deep research hallucinates" because some flagged answers were correct against stale eval data. Two things follow: the agentic-browsing setup measurably *reduces* hallucination versus plain chat models — and it still leaves a double-digit hallucination rate on a vendor's own favourable eval, which is the same order of magnitude as the Tow Center's independent 37% and points the same direction (see Claim 1). Separately, OpenAI's Safety Advisory Group rated deep research **medium risk** — the first model rated medium for cybersecurity — though OpenAI attributed most of that uplift to browsing finding public CTF writeups rather than genuine reasoning gain.

Benchmark note: the original o3-based version scored 26.6% on "Humanity's Last Exam," ahead of DeepSeek R1 (9.4%) and GPT-4o (3.3%), which the vendor uses to argue the model's underlying reasoning (not just its browsing) is a meaningfully different tier from a plain chat model.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | **Deep Research System Card (OpenAI, 2025-02-25)** | cdn.openai.com/deep-research-system-card.pdf | **PRIMARY.** "multi-step research… pivoting as needed"; PersonQA accuracy 0.86 / hallucination 0.13 vs GPT-4o 0.50/0.30; medium-risk safety rating | 2026-08-03 |
| 2 | Deep Research — Wikipedia | en.wikipedia.org/wiki/Deep_research | 5–30 min run time, pricing/limits as of June 2025, Feb 2026 GPT-5.2 model upgrade | 2026-08-03 |
| 3 | OpenAI Responses API deep-research guide | developers.openai.com/api/docs/guides/deep-research | API path has no clarification step; plan generated internally, executes without user interaction | 2026-08-03 (secondary-quoted) |
| 4 | openai.com/index/introducing-deep-research/ | — | 403 Forbidden — primary announcement not directly fetchable today | 2026-08-03 (attempted) |
| 5 | help.openai.com Deep Research FAQ | — | 403 Forbidden on every article-ID attempt | 2026-08-03 (attempted) |

## What to borrow for faion

- The explicit "5 to 30 minutes, autonomously browsing" framing is a good customer-facing way to set expectations for what a Deep-Research-style run costs in wall-clock time, distinct from a normal chat answer.
- The Feb 2026 "limiting scope to select sites" feature is worth tracking: it is OpenAI converging toward exactly the kind of source-scoping/domain-allowlisting our methodology would want to enforce manually (e.g., restrict to primary vendor docs, exclude SEO content farms).

## What NOT to borrow — and why

- Do not recommend a solopreneur maintain a second $20-200/mo ChatGPT subscription purely to get Deep Research, if they are already inside a Claude-based workflow (which is the default assumption for faion customers using Claude Code). The mechanic is worth teaching; the subscription is not worth doubling up on for this feature alone.
- Do not treat OpenAI's own decomposition as a substitute for tool *selection*. Deep Research decides how to search once it's running; it does not know whether ChatGPT's general web index is the right corpus for the question in the first place (a scientific claim is still better served by Consensus/Scite; OpenAI Deep Research will confidently search the general web either way).

## Mapping to our corpus

Not directly named in `ai-research-tools` or `perplexity-ai-research` today — worth a cross-reference addition ("see also: vendor Deep Research agents now automate step 2-3 of this procedure") so the methodology doesn't read as ignorant of commodity Deep Research agents.

## Open questions / staleness risk

- Mechanics and groundedness figures are now anchored to OpenAI's own system card (Feb 2025) — solid, but that card describes the *original o3-based* deep research, while the shipping product moved to a GPT-5.2 base in Feb 2026. The 0.13 hallucination rate should therefore be read as "the best published number for an earlier version," not a current measurement.
- Pricing/quota figures conflict between the June-2025 numbers (25/250 per month) and 2026 tracker numbers (10/~120) with no way to adjudicate today; OpenAI's own live pages 403 on every attempt. High staleness risk on quotas, low on the qualitative mechanics description.
- The ChatGPT-UI clarifying-question step is secondary-sourced only; not primary-confirmed in this pass.

---

# Google Gemini Deep Research
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is

An agentic research mode inside the Gemini app that turns a prompt into an editable multi-step research plan, executes that plan across the web (and optionally the user's own Gmail/Drive/Chat), and produces a multi-page cited report with an optional audio summary.

## Current state

- **Maintainer:** Google.
- **Branding (confirmed live, checked 2026-08-03):** the consumer plan family is now called **Google AI Plus / Google AI Pro / Google AI Ultra** — "Gemini Advanced" as a standalone brand name no longer appears on Google's own live pricing page.
- **Price for one person (per Google's own DE-locale pricing page, `gemini.google/subscriptions/`, checked 2026-08-03 — figures are EUR, not independently cross-confirmed against the USD page, which did not return numeric values to the fetch tool):**
  - Google AI Plus — **€4.99/month** — Deep Research included, limited/"different" access to the top Gemini model, base Gemini Flash access.
  - Google AI Pro — **€21.99/month** — 4x the free tier's usage limits, full Gemini 3.1 Pro access, Deep Research included.
  - Google AI Ultra — **€99.99/month** (5x limits) or **€219.99/month** (20x limits) — priority access to newest features (Deep Think, "Gemini Spark"), maximum Deep Research usage.
  - **These are Euro list prices; a solopreneur should confirm the USD figure directly before quoting** — the automated fetch of the USD page returned template placeholders without numeric values.
- **USD cross-check (price trackers, checked 2026-08-03):** Google AI Pro **$19.99/month** — i.e. the same price point as ChatGPT Plus and Perplexity Pro. The Ultra tier is **unresolved**: one tracker reports a 2026 restructuring introducing a **$99.99/mo** tier alongside **$199.99/mo** (down from an original $249.99), another still lists a flat **$249.99/mo**. Flagged as needing a direct vendor check; it does not affect the solopreneur recommendation, since Deep Research is included from the cheapest paid tier upward.
- **Deep Research is included at all three paid tiers** — confirmed on Google's own plan page (`one.google.com/about/google-ai-plans`, checked 2026-08-03, German locale rendering: "Erweiterter Zugriff auf Gemini 3.1 Pro und Deep Research in Gemini"). There is no separate Deep Research SKU to buy.

## Mechanics

Directly confirmed from Google's own product page (`gemini.google/overview/deep-research/`, checked 2026-08-03), and the single strongest primary-source confirmation of the decompose-execute-synthesize thesis in this whole cluster:

1. **Planning:** "converts user prompts into personalized multi-step research plans that users can review and modify before execution" — i.e., an explicit, user-editable plan step before any searching happens. This is the one vendor in the cluster with a documented human-in-the-loop checkpoint *before* execution (not just after, as our methodology's `human-verification-before-publish` rule does).
2. **Research:** searches the web automatically, and optionally Gmail/Drive/Chat if the user opts in, described as capable of "browsing hundreds of websites." Google's own launch blog (`blog.google/products/gemini/google-gemini-deep-research/`, fetched clean 2026-08-03) is more explicit about the loop being iterative rather than a single fan-out: Gemini **"continuously refines its analysis, browsing the web the way you do: searching, finding interesting pieces of information and then starting a new search based on what it's learned"** — repeated over multiple rounds before it writes anything. The same post confirms the plan step in its own words: it **"creates a multi-step research plan for you to either revise or approve."**
3. **Analysis:** the user can watch reasoning happen incrementally as findings are analyzed and conclusions drawn.
4. **Report generation:** a multi-page report is produced "within minutes," with an optional audio-summary output.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Gemini Deep Research overview | gemini.google/overview/deep-research/ | Full 4-step mechanics description (Planning/Research/Analysis/Report) | 2026-08-03 |
| 1b | **Google's Deep Research launch blog** | blog.google/products/gemini/google-gemini-deep-research/ | **PRIMARY, unblocked.** "creates a multi-step research plan for you to either revise or approve"; "continuously refines… starting a new search based on what it's learned" | 2026-08-03 |
| 2 | Google AI subscription plans (DE) | gemini.google/subscriptions/ (de locale) | EUR pricing for Plus/Pro/Ultra tiers, Deep Research gating | 2026-08-03 |
| 3 | Google One AI plans page | one.google.com/about/google-ai-plans/ | Confirms "Google AI" branding, tier names, feature gating; no numeric USD prices returned | 2026-08-03 |

## What to borrow for faion

- **The editable-plan-before-execution step is the single most valuable idea to borrow from this whole cluster.** It is exactly the missing piece in our own `perplexity-ai-research` procedure, which decomposes into sub-queries but has no explicit "show the plan, let a human edit it before spending the search budget" gate — Gemini ships this natively; we should consider adding an equivalent checkpoint to `04-procedure.xml`.
- The tiered usage-multiplier framing (4x, 5x, 20x limits rather than flat query counts) is a clean way to communicate "how much research can I actually do this month" to a non-technical buyer.

## What NOT to borrow — and why

- Do not recommend Google AI Pro/Ultra purely for Deep Research access if the customer's primary stack is Claude-based — the bundled extras (cloud storage, YouTube Premium) are real value but orthogonal to research workflow, and stacking a third paid AI subscription onto Claude + Perplexity has diminishing returns for a single solopreneur.
- Do not treat "browses hundreds of websites" as a proxy for quality — breadth of retrieval is not the same as correct attribution (see the Tow Center finding below, which did not test Gemini's Deep Research mode specifically, but did test base Gemini's citation accuracy and found it among the worse performers on fabricated/broken URLs).

## Mapping to our corpus

Not currently named in either `ai-research-tools` or `perplexity-ai-research`. The editable-plan-before-execution pattern is the one concrete methodology improvement this whole desk-research audit surfaces — worth a follow-up CR against `perplexity-ai-research/content/04-procedure.xml`.

## Open questions / staleness risk

- EUR pricing not cross-confirmed against USD; Google's product/feature naming ("Deep Think," "Gemini Spark," model version numbers like "Gemini 3.1 Pro" / "Gemini 3.6 Flash") moves fast and should be treated as a snapshot, not a stable reference.

---

## Claim 1 — the Tow Center / Columbia citation-accuracy figure (verified in full)

**Study:** "We Compared Eight AI Search Engines. They're Bad at Citing News." — Tow Center for Digital Journalism / Columbia Journalism Review.
**Authors:** Klaudia Jaźwińska and Aisvarya Chandrasekar.
**Published:** 2025-03-06. Checked 2026-08-03: no confirmed same-methodology follow-up round exists. Later 2026 Tow Center pieces by the same authors ("Your Chatbot's Memory of You Can Shape the Information You See," 2026-04-09; "AI Agents Are Coming for News," 2026-05-14) cover adjacent topics (personalization, agentic publisher access) but are not a re-run of the 8-tool citation-accuracy test — **treat the March-2025 figures as the only data point available, now roughly 17 months old.**

**Methodology:** 8 tools tested — ChatGPT Search, Perplexity, Perplexity Pro, DeepSeek Search, Microsoft Copilot, Grok-2, Grok-3, Google Gemini. 20 news publishers (chosen to vary in their AI-crawler access policy) × 10 articles each × 8 chatbots = **1,600 total queries**. Each response was classified as Correct / Correct but Incomplete / Partially Incorrect / Completely Incorrect / Not Provided / Crawler Blocked, scored against three attributes: correct article identified, correct publisher identified, correct URL provided.

**Exact figures:**
- Overall: chatbots gave incorrect answers to **more than 60% of queries**, across all 8 tools combined.
- **Perplexity (free tier): 37% error rate — the lowest (best) of the 8 tools tested.**
- Grok-3: 94% error rate — the worst.
- DeepSeek: misattributed sources 115 out of 200 times.
- Gemini and Grok-3: more than half of responses cited fabricated or broken URLs; Grok-3 specifically had 154 of 200 citations lead to error pages.
- ChatGPT signaled uncertainty in only 15 of 200 responses despite being wrong on 134 of them — i.e., confident wrongness, not hedged wrongness.
- A separate, non-citation-accuracy finding for **Perplexity Pro specifically**: it "correctly identified nearly one-third of restricted content it shouldn't access" — meaning Perplexity Pro's crawler used and quoted content from publishers who had explicitly blocked it via `robots.txt`/licensing terms. This is a crawler-permission violation, not a citation-accuracy metric, and it means Perplexity's "best of 8" ranking on accuracy sits alongside a real, separate compliance problem — it is not a clean win.

**Verdict on the "37%" claim:** confirmed accurate as stated, with one necessary precision: it is Perplexity's free-tier error rate on the study's combined article/publisher/URL-correctness metric, and it is indeed the lowest (best) among the 8 tools tested — it is not conflating a different tool or a different metric.

**Verdict on the user's interpretation (does "best-in-class still fails >1/3 of the time" argue FOR forced citations + manual verification, regardless of which tool):** **yes, this holds, and I commit to it without hedging.** The instant you have a rigorous audit showing the *best available* tool in a fair 1,600-query test is still wrong more than a third of the time, "pick a better tool" stops being a viable mitigation — there is no tool in the tested set, including the winner, that clears a bar you'd accept for an unreviewed business claim. That converts "always force citations + manual source-checking" from a nice-to-have into the only mitigation that actually generalizes across tool choice and over time (since today's best tool degrading, or a new tool entering the field, doesn't change the policy). This is precisely what `perplexity-ai-research`'s `human-verification-before-publish` rule and `ai-research-tools`'s `citation-source-link-required` rule already encode — the Tow Center number is empirical validation of an existing design decision, not a reason to revisit it.

## Claim 2 — Consensus/Elicit corpus size and B2B uselessness

**Corpus size:** Elicit's own pricing page claims "unlimited search across more than 138 million papers" (elicit.com/pricing, checked 2026-08-03). Consensus is built on the Semantic Scholar Academic Graph, which itself claims **214 million papers, 2.49 billion citations, 79 million authors** (semanticscholar.org/product/api, checked 2026-08-03) — consistent with, and large enough to support, a "200M+ papers" framing for Consensus, though Consensus's own live pricing/marketing pages returned 403 to fetch today and the "200M+" figure specifically attributed to Consensus is not independently reconfirmed from Consensus's own copy at time of writing.

**"Cannot fabricate references" — mechanically verified:** true, and true for a specific structural reason, not because the underlying LLM is more careful. Both Elicit and Consensus are **retrieval-then-summarize** systems: every citation shown resolves to a real, pre-indexed paper (title/authors/DOI/abstract already exist in the database before the LLM is ever invoked). The LLM's role is confined to summarizing, extracting, or scoring a document known to exist — it cannot invent a citation the way an ungrounded chat model can, because there is no generation step that produces the citation itself, only a generation step that describes an already-retrieved one. This is a materially different architecture from a bare LLM chat (which generates text and citations in the same pass, with no database backing the citation), and it is the correct mechanical reason "cannot fabricate references" is a defensible claim rather than marketing.

**B2B/market-question uselessness — verdict:** largely holds, and it holds **by design, not by defect**. Both vendors scope their own marketing explicitly to academic/scientific literature — literature review, meta-analysis, evidence synthesis for researchers and R&D teams. Neither markets toward business/market-research use cases, and structurally there is no peer-reviewed literature corpus to retrieve for questions like "what's our TAM" or "who are the top 5 competitors in category X" — the tools will either return nothing on-point or force-fit an adjacent (and usually stale-by-publication) academic paper. This isn't the tools failing at their job; it's a solopreneur mis-selecting a tool whose corpus was never meant to contain the answer. No credible evidence (positive or negative) of a business/market-research use case succeeding on either tool was found in this pass — the absence of vendor case studies or user reports in that direction is itself consistent with the claim, though it should be read as "no evidence found," not "proven absent."

## Test this prior finding — is our methodology now a partial substitute?

**Verified mechanically, all three vendor agents, each from the vendor's own words:**

| Tool | Vendor's own description of the loop | Plan visible to user? |
|------|--------------------------------------|------------------------|
| Perplexity Deep Research | "performs dozens of searches, reads hundreds of sources, and reasons through the material to autonomously deliver a comprehensive report" (launch blog); API meters searches, reasoning tokens and citation tokens as separate line items — structural proof of a multi-step pipeline | No |
| OpenAI Deep Research | "conducts multi-step research on the internet… **pivoting as needed in reaction to information it encounters**" (Deep Research System Card, 2025-02-25) | ChatGPT UI: one clarifying round, no plan shown. API: no interaction at all |
| Gemini Deep Research | "creates a multi-step research plan for you to either revise or approve"; then "continuously refines its analysis… starting a new search based on what it's learned" (Google launch blog) | **Yes — editable before execution** |

**All three genuinely run an internal decompose-execute-synthesize loop, and two of the three run it adaptively** — OpenAI's "pivoting as needed" and Google's "starting a new search based on what it's learned" both describe re-planning mid-run, which is *stronger* than what our `perplexity-ai-research/content/04-procedure.xml` specifies (a one-shot decomposition into a fixed list of atomic sub-queries, then execute). On the mechanical step alone, the vendors are not merely matching our procedure — they have surpassed it. This is not a marginal or contested finding; it is the vendors' own stated architecture in every case checked.

**Committed answer — what is left for our methodology to add value on:**

1. **Tool/corpus selection is untouched and now more important, not less.** None of the three agents knows when it is the wrong tool for the question — OpenAI and Perplexity's Deep Research will confidently search the general web for a question that actually needs Consensus/Scite's academic corpus, and none of them will decompose "is there a viable market for X" into the market-sizing-specific sub-questions a solopreneur actually needs answered (TAM proxy data, competitor funding history, pricing benchmarks) versus the generic sub-questions a default web-search decomposition produces. This is exactly `ai-research-tools`'s job, and it is a judgment call none of these agents make.
2. **The verification gate is not redundant — Claim 1 proves it's load-bearing, and the vendors' own numbers agree.** A tool that runs its own decomposition and search still produces a report that is wrong at a meaningful rate: 37% on the Tow Center's independent 1,600-query audit for the best of eight tools, and a self-reported **0.13 hallucination rate** for OpenAI Deep Research on OpenAI's own favourable PersonQA eval — the vendor's best case, not a hostile test. Automating the search loop measurably improves groundedness over plain chat (0.13 vs GPT-4o's 0.30) and still does not automate correctness. Every one of these tools emits fluent, confidently-cited prose at those error rates, which is precisely the failure shape a human gate exists to catch.
3. **Structured, reusable output is still missing from every vendor tool.** All three produce a one-off chat transcript or report; none emits a schema-conformant, taggable artifact with per-claim confidence ratings the way our `02-output-contract.xml` does. A Deep Research report that isn't captured into a structured decision record decays the moment the tab closes — it isn't reusable in the next research cycle, and it has no `verified_by` field.
4. **The API-key framing in `perplexity-ai-research` is now actively wrong for our audience and should be rewritten.** The methodology's prerequisites demand `PPLX_API_KEY` and ship a `templates/perplexity_research.py` batch caller — that is a developer workflow, and faion's stated constraint is that a recommendation must work for a solopreneur who won't open a terminal beyond a single `faion` command. Since the vendor UIs now do the decomposition natively, the API path buys almost nothing a non-technical user can use: the correct rewrite is "run this in the Perplexity/Gemini UI, apply these rules to what comes back," with the Python script demoted to an optional appendix for the technical minority. This is the single most concrete corrective the audit produces against our existing content.
5. **The editable-plan-before-execution pattern (Gemini only) is worth reverse-borrowing into our own procedure** — see the Gemini dossier's "What to borrow" — since it is a genuine improvement over our current after-the-fact-only verification gate.

**Bottom line, no hedge:** the *mechanical* step our methodology used to add (splitting a compound question into atomic sub-queries and running them) is now commoditized — vendors do this automatically and better than a manual procedure would. What the methodology still adds is everything the vendors' own agents structurally cannot do for themselves: choosing the right tool for the evidence type, distrusting the output by default, and capturing the result in a form that survives past one chat session. The methodology's center of gravity has moved up a layer, from execution to judgment plus quality control — that is a narrowing of scope, not an obsolescence.

## Re-tiering assessment

Prices found in this pass, against faion's geek tier at $99/month:

| Tool | Individual price | Ratio to geek ($99/mo) |
|------|-------------------|------------------------|
| Perplexity Pro | ~$20/mo (unconfirmed today, see flag above) | 5x cheaper |
| Elicit Pro | $49/mo (confirmed) | ~2x cheaper |
| Elicit Scale | $169/mo (confirmed) | 1.7x *more* than geek |
| Consensus | ~$9-12/mo (unconfirmed today) | 8-11x cheaper |
| Scite | ~$20/mo (unconfirmed today) | 5x cheaper |
| OpenAI Deep Research (entry) | ChatGPT Plus $20/mo — 25 runs/mo (2025 figure) or 10/mo (2026 trackers) | 5x cheaper |
| OpenAI Deep Research (meaningful volume) | ChatGPT Pro $200/mo — 250 runs/mo (2025) / ~120 observed (2026) | geek is *cheaper* than the tier needed for serious use |
| Gemini Deep Research | Google AI Pro $19.99/mo (€21.99 EU) | ~5x cheaper |
| Gemini Deep Research (cheapest paid entry) | Google AI Plus €4.99/mo — Deep Research included | ~20x cheaper |

**The prior pass's reasoning ("tools cost $12-22/mo, geek costs $99/mo, so re-tier down") does not survive scrutiny as stated**, for a structural reason: geek tier is priced against the aggregate value of ~695 geek-only methodologies (the full ai-agent-builder + SDLC-AI stack per `skills/CLAUDE.md`), not against any single tool. Any individual tool-specific methodology in a $99/mo bundle will look "too cheap to justify" by a naive price-ratio test — that argument, taken literally, is a case for dissolving the entire geek tier, not for re-tiering two specific methodologies. Price-ratio is not, by itself, a valid re-tiering signal.

**The re-tiering conclusion is nonetheless correct — for a different, audience-fit reason.** Per `skills/CLAUDE.md`, geek tier is scoped to `ai/` (ml-engineer, ai-agents, rag-engineer, ml-ops, multimodal-ai, llm-integration, claude-code) and `sdlc-ai/` — i.e., *building AI agents and wiring AI into the SDLC*. `ai-research-tools` and `perplexity-ai-research` are not about building agents; they are general research-tool-selection literacy that any solopreneur doing market research, competitor analysis, or evidence-checking needs, technical or not. That is squarely a solo-tier concern, not a geek-tier one — the audience for "which AI search tool should I use for this question" is every solopreneur, not the agent-builder subset who pays for geek.

**Concrete recommendation:** move `ai-research-tools` (the pure selection map — decision-only, no API key, applies to any web-UI tool) to **solo tier**. Move `perplexity-ai-research` (requires `PPLX_API_KEY`, a Python batch-caller script, and JSON-schema output validation) to **pro tier** — it's still a general solopreneur concern, but it's an API/automation workflow one notch more technical than plain tool selection, and geek's agent-building bar is still higher than what this methodology asks of a user.

## Strategic verdict: do these tools make desk-research methodology MORE or LESS valuable

**More valuable, and I commit to this without hedging.** Three findings compound. First, decompose-execute-synthesize — the hard, teachable part of AI-assisted research — is now shipped automatically by three major vendors, two of them adaptively re-planning mid-run. A solopreneur gets it by clicking "Deep Research." That genuinely shrinks the methodology, but only that one step.

Second, the Tow Center's 1,600-query audit found the best of eight tools still wrong 37% of the time, and OpenAI's own system card reports a 0.13 hallucination rate on a favourable eval. Automating the search loop did nothing for correctness, because correctness was never what the loop solved.

Third, the Elicit/Consensus scope finding shows owning a good tool is not knowing when it's the wrong tool. None of the six products audited here knows its own corpus limits; a solopreneur who trusts a fluent, well-cited, wrong-scope answer is worse off than one who never asked.

Together: the tools got good enough at execution that users will now trust default output without knowing they still need a selection layer and a verification gate. That makes owning "how to do desk research well" more valuable precisely because it has become less visible. The risk moved from "the AI can't do this" to "the AI looks like it did this correctly, and didn't" — harder to sell, more necessary to solve. The methodology that survives no longer teaches decomposition; it teaches distrust, tool fit, and structured capture. That is the direction `ai-research-tools` and `perplexity-ai-research` should evolve.
