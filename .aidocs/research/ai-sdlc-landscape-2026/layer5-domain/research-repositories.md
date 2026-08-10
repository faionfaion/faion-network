# Layer 5 — Domain: Research Repositories (Dovetail, Marvin, Condens, Looppanel, Notably)

**Cluster verdict:** the repository category is real and the underlying capability (tag → highlight → insight → evidence, queryable across studies) is not something a markdown folder replicates for free. But the *vendors* have split hard on solopreneur-friendliness in 2026: Dovetail quietly killed self-serve pricing and is now Free-or-Enterprise-only (bad for one person), Looppanel is team-priced with no free tier at all (bad for one person), while Marvin and Condens both ship a genuinely usable single-person entry point at $0 and ~€15/mo respectively. Notably sits in the middle but its own pricing page was unreachable for direct verification (persistent TLS failure from the fetch tool — flagged below), so treat its numbers as secondary-sourced. Net: for a non-technical solopreneur, **Marvin (free) or Condens (Lite)** are the only two of the five that make sense to actually install; the other three are "borrow the mental model, skip the checkout page."

---

# Dovetail
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea not the tool · **Verified:** 2026-08-03

## What it is
A cloud UX research repository: import interview transcripts/calls/surveys, tag quotes into themes, aggregate themes into "Insights," attach evidence (linked quotes) to each insight, and search/report across the whole corpus. Historically the category-defining product referenced in most UX-research playbooks and courses.

## Current state
**This is the load-bearing fact of this dossier.** As of 2026-08-03, `dovetail.com/pricing/` (redirected from the legacy `dovetailapp.com/pricing/`) shows exactly **two** plans, no self-serve mid-tier at all:

- **Free** — "$0, no card required." Per the page, 1 channel, 1 project, basic chat/summarization, no AI Dashboards, no AI Agents. Framed as "for individuals to make sense of calls, documents, and surveys."
- **Enterprise** — "Custom pricing available," invoiced only, sales-quoted "based on your team size, usage needs, and selected add-ons." Unlimited channels/projects/agents/dashboards.

Dovetail's own help docs make the history explicit — `docs.dovetail.com/help/purchase-a-paid-plan`: *"Dovetail offers a Free plan and an Enterprise plan. We no longer offer self-serve paid plans."* And `docs.dovetail.com/help/changes-to-legacy-plans`: legacy self-serve plans were named **"Pro, Personal Pro, Starter, Team"** — those customers are being migrated to Free or a new "Professional" (Enterprise-adjacent) plan on renewal, losing workspace tags/fields, templates, and access control unless they move to Enterprise.

**Resolution of the conflict tasked:**
- Pass A ("~$99/seat/mo, ≈$12k/yr team") — this is a stale reference to the discontinued **Team** plan's per-seat rate, extrapolated to a small team's annual spend. Not purchasable today.
- Pass B ("$30-39/user/mo Pro, $50 Team") — stale reference to the discontinued **Pro**/legacy-**Team** self-serve tiers, likely from an even earlier price point before the last self-serve increase.
- The playbook in our corpus (`user-interviews-at-scale/playbook.md`, `last_verified: 2026-05-02`) — "Starter plan, $29/mo" for tagging/synthesis, later "Team plan ($99/mo)" for multi-researcher tagging — is the same category of stale reference, one generation behind: **Starter** and **Team** are two of the four names Dovetail's own docs list as discontinued legacy plans.

**None of the three claims is "current."** All three are internally-consistent snapshots of a self-serve tier ladder (Starter → Pro/Personal Pro → Team) that existed at different points before Dovetail collapsed everything to Free/Enterprise. The **settled number as of 2026-08-03 is: Free ($0, 1 project cap) or Enterprise (custom, sales-only, invoiced)** — there is no fixed dollar figure for a single seat anymore because Dovetail no longer sells single seats without a sales conversation. Maintainer: Dovetail Pty Ltd (dovetail.com). Free tier: 1 project, 1 channel — enough for exactly one active study at a time, nothing "at scale."

## Mechanics
1. Create a project per study, import transcripts/recordings as "Notes."
2. Build a tag taxonomy (tag groups + tags), highlight quotes, apply tags.
3. Aggregate tagged highlights by theme (chart view) to spot the highest-signal clusters.
4. Create an "Insight" object per theme: one-sentence finding + linked evidence (the actual tagged quote highlights, not copy-pasted text) + a recommendation field.
5. Export/share the insight report (PDF) with evidence links intact for stakeholder review.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Dovetail Pricing | https://dovetail.com/pricing/ | Current Free/Enterprise-only tier structure, "no self-serve" note | 2026-08-03 |
| 2 | Purchase a Paid Plan | https://docs.dovetail.com/help/purchase-a-paid-plan | Explicit "we no longer offer self-serve paid plans" statement | 2026-08-03 |
| 3 | Changes to Legacy Plans | https://docs.dovetail.com/help/changes-to-legacy-plans | Names of the four discontinued self-serve plans (Pro, Personal Pro, Starter, Team) and migration mechanics | 2026-08-03 |
| 4 | koji.so — Dovetail Pricing 2026 blog post (snippet only) | www.koji.so/blog/dovetail-pricing-2026 | Third-party confirmation: "Dovetail no longer publishes per-seat pricing" | 2026-08-03 (search snippet, not fetched in full) |

## What to borrow for faion
- The **Insight → Evidence link** data model: an insight is not prose, it's a claim object with a pointer array into tagged source quotes. This is the actual mechanism that makes "groundedness verifiable" — worth teaching as a *pattern* in `research-repository-setup`/`research-repository-ops`, independent of any vendor.
- The tag-group taxonomy convention (theme tags + orthogonal sentiment tags) is vendor-neutral and already partly reflected in `templates/taxonomy-seed.yaml`.

## What NOT to borrow — and why
- Do not reference Dovetail as the default recommended tool in solopreneur-tier content anymore. It is structurally hostile to solo buyers: no fixed self-serve price exists to quote, "contact sales" is the only paid path, and the free tier's 1-project cap makes "at scale" (the existing playbook's own title) actively false for Dovetail specifically.
- Do not carry forward the $29/$99 figures anywhere in the corpus — they are dead prices for a dead tier structure.

## Mapping to our corpus
`skills/faion/playbooks/pro/ux-research/user-interviews-at-scale/playbook.md` (tier: pro, `last_verified: 2026-05-02`) names Dovetail with literal UI steps across Phase 5–6 (project creation, tag groups, Insight + evidence linking, PDF export) and Prerequisites/Next sections with the two stale prices above. **This playbook needs a correction pass**: either (a) swap the tool reference to Marvin or Condens (both still self-serve-priced and mechanically near-identical: project → import → tag → insight → evidence → export), or (b) keep Dovetail as the UI reference but strip the dollar figures and replace with "contact sales; no published self-serve price as of 2026." Recommendation: (a) — a solopreneur audience should not be pointed at a tool that requires a sales call to get a price.

## Open questions / staleness risk
- Exact date Dovetail discontinued self-serve plans is not stated on any page I could reach — only that migration to Free/Professional happens "at the end of your billing period" for remaining legacy accounts. Re-check in 3-6 months; this is a fast-moving fact.
- Could not fetch `docs.dovetail.com/help/changes-to-legacy-plans` in full (only a synthesized excerpt); if a future pass needs the exact migration deadline dates, re-fetch directly.

---

# Marvin
**Layer:** 5 — Domain · **Verdict:** 🟢 take · **Verified:** 2026-08-03

## What it is
heyMarvin.com's "Marvin" — a UX/product research repository with AI-native ingestion (calls, uploads), an AI Notetaker, tagging, insight synthesis, and an "Ask AI" layer over the tagged corpus. **Confirmed correct product**: this is not the to-do app "Amazing Marvin" nor the Prefect AI-agent-framework "Marvin" — the pricing page's feature set (Insight reports & library, video clips & playlists, AI Interviewer credits, virtual observation room, Marvin MCP/API) is unambiguously a UX-research-repository product.

## Current state
Per `heymarvin.com/pricing`, checked 2026-08-03:

- **Free** — $0, no card required. **2 full seats, 3 collaborator seats**, viewer seats included. Includes: 5 file uploads/month, **Marvin AI Notetaker, project-wide Ask AI, Insight reports & library, video clips & playlists** — all present on the free tier, not gated as "upgrade to unlock."
- **Starter** — price not published (contact sales). 2 full seats, 10 collaborator, 50 viewer, 100 AI-Interviewer credits/yr. Adds unlimited data ingestion, repository-wide Ask AI, cloud storage/collaboration, GTM integrations, virtual observation room, AI-assisted analysis, custom topic subscriptions.
- **Pro** (marked "Most popular") — price not published. 5 full/15 collaborator/100 viewer seats, 250 AI-Interviewer credits/yr. Adds agentic Ask AI, survey/research/support integrations, Deep Research (thematic+emotion analysis), custom branding, MCP/API access, 40+ language translation.
- **Enterprise** — custom. 5 full/unlimited collaborator/unlimited viewer, 500 AI-Interviewer credits/yr, SSO/SAML, HIPAA, dedicated CSM.

**The claim to verify holds up**: the free tier genuinely includes AI summaries (via the AI Notetaker) and project-wide "Ask AI" at $0 with no card and no seat-count trap for a solo user (2 full seats is enough for one person plus one collaborator). The 5-uploads/month cap is the real constraint — fine for someone running one or two small studies a month, a bottleneck past that. Maintainer: Marvin (heyMarvin), commercial UX-research SaaS.

## Mechanics
1. Free account, no card. Upload up to 5 recordings/files per month or connect a live call for AI Notetaker capture.
2. AI auto-generates a note + summary per session; tag manually or let AI-assisted analysis propose themes (paid tiers).
3. Ask project-wide questions against the tagged corpus ("Ask AI") — grounded Q&A over your own data, free tier included.
4. Build an insight report from the library; free tier includes "Insight reports & library" as a named feature, not a paywalled add-on.
5. Upgrade path is purely about volume (uploads, seats, AI-Interviewer credits) and enterprise controls (SSO, HIPAA) — not about gating the core repository mechanic.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Marvin Pricing | https://www.heymarvin.com/pricing | Full 4-tier table, exact free-tier feature list and seat counts | 2026-08-03 |

## What to borrow for faion
- The free-tier structure itself is a template for how we should describe "layer 5 entry cost" in our own content: $0, no card, core mechanic (tag→insight→AI-grounded-Q&A) fully present, only volume/seats gated. This is the honest "$0 entry into layer 5" claim — use Marvin, not Dovetail, as the reference tool in free/solo-tier content.
- "Ask AI" scoped to project vs. repository-wide (Starter/Pro) is a clean illustration of the buy-vs-build tradeoff worth citing in `research-repository-setup`'s platform-scorecard criteria (AI tagging maturity).

## What NOT to borrow — and why
- Don't quote Starter/Pro/Enterprise dollar prices anywhere — Marvin doesn't publish them; any number attributed to those tiers in future research would be a hallucination risk, not a stale-data risk.
- Don't assume the 5-uploads/month cap scales to "solopreneur running weekly interviews" — it doesn't; that use case tips into Starter (unpriced, sales-gated) quickly.

## Mapping to our corpus
Not currently named anywhere in the corpus (grep of `research-repository-setup` content and the one playbook that names a repository tool shows only Dovetail). Recommend adding Marvin as the named free-tier example in `research-repository-setup/templates/platform-scorecard.md` and as the replacement tool reference in `user-interviews-at-scale/playbook.md` (see Dovetail's "Mapping to our corpus" above).

## Open questions / staleness risk
- Contact-sales pricing for Starter/Pro means the real cost a solopreneur would pay past the free tier is unknown and unverifiable without a sales call — re-check by requesting a quote if this tool becomes a hard recommendation.
- Product is young enough that seat/upload caps on the free tier could tighten; re-verify at next audit.

---

# Condens
**Layer:** 5 — Domain · **Verdict:** 🟢 take · **Verified:** 2026-08-03

## What it is
A UX research repository (condens.io) built around transcription, tagging, and a searchable insight/quote repository, with an explicit low-end single-contributor tier aimed at freelancers/small teams.

## Current state
Per `condens.io/pricing/`, checked 2026-08-03:

- **Lite** — **€15/month** (or €165/year, effectively one month free on annual). 1 contributor included; additional contributors €15/mo each. 15-day free trial, no card required. Includes unlimited transcription, unlimited projects, basic analysis; AI features limited to small datasets.
- **Business** — **€500/month billed yearly (€6,000/year)**. 5 contributors included; additional contributors €85/mo each. Unlimited viewers. Adds unlimited AI search, 3 customizable repositories, ChatGPT/Claude integration, advanced integrations, basic anonymization.
- **Enterprise** — custom/contact sales. Minimum 5 contributors. Adds unlimited repositories, API access, advanced anonymization/redaction, custom LLM integration, dedicated support.

For **one person**: Lite at €15/mo (~$16-17 at 2026 exchange rates) is the relevant number — a real, checkout-able, single-contributor price, not a sales-gated quote. Free education/nonprofit discounts exist per the pricing page. Maintainer: Condens GmbH.

## Mechanics
1. Sign up, 15-day trial with full feature access; workspace goes read-only (not deleted) if you don't convert to paid.
2. Import/transcribe recordings (unlimited on every paid tier, including Lite).
3. Tag quotes into a repository; on Lite, AI analysis works but is capped to small datasets — the tagging/search mechanic itself is not artificially crippled, just throughput-limited.
4. On Business+, "unlimited AI search" and multi-repository structuring become available — this is the tier where a small agency, not a solopreneur, actually lives.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Condens Pricing | https://condens.io/pricing/ | Full 3-tier table, trial terms, per-contributor add-on pricing | 2026-08-03 |

## What to borrow for faion
- Condens' Lite tier is the cleanest existing proof that a real, transparently-priced single-contributor research repository exists at solopreneur budget (€15/mo, cheaper than a Zoom Pro seat). Use it as the anchor "cheapest real repository" figure in any pricing comparison we publish.
- The read-only-on-lapse (rather than delete-on-lapse) trial-to-paid conversion pattern is worth noting as a UX pattern in any SaaS-selection guidance we write for solopreneurs (data isn't held hostage).

## What NOT to borrow — and why
- Business tier's per-org €6,000/yr minimum (5 contributors) confirms this vendor, like the others, treats "team" as the real target market — don't imply Condens itself is built for a solopreneur beyond Lite; Lite is intentionally feature-capped on AI.

## Mapping to our corpus
Not currently named in the corpus. Best candidate to cite as the "under $20/mo" reference point in `research-repository-setup`'s `templates/platform-scorecard.md` cost-per-user criterion.

## Open questions / staleness risk
- EUR pricing not converted/pinned to USD in our corpus — if we quote a USD figure later, convert at the review date, don't reuse today's rate indefinitely.

---

# Looppanel
**Layer:** 5 — Domain · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
A UX research repository (looppanel.com) centered on auto-recording, AI note-taking, and video-clip-based insight sharing, explicitly team-workspace-first (SSO, admin/billing controls even on its base paid plan).

## Current state
Per `looppanel.com/pricing` (also `www.looppanel.com/pricing`), checked 2026-08-03:

- **Pro** — **$395/month or $4,200/year** (one month free annually, i.e. ~$350/mo effective). **5 editors minimum** included, unlimited viewers, 30 transcription hours/month, 360 uploads/month, AI notes, auto-analysis (3 runs/project), video highlight reels, team workspace, SSO (Microsoft/Google), SOC 2 + standard DPA. Additional editors $75/mo each, up to 10 total.
- **Enterprise** — custom/"Talk to Us," 10-editor minimum, unlimited transcription/uploads, PII redaction, custom SSO, translation (96 languages), API access, SLAs.

**No free tier and no trial were found on the pricing page.** There is no plan priced or scoped for a single editor — the cheapest possible spend is $395/mo for 5 editor seats regardless of how many you actually use.

## Mechanics
1. Auto-record calls (Zoom/Meet integration implied by "auto-record") into the workspace.
2. AI generates notes automatically per session; auto-analysis runs (capped at 3/project on Pro) surface themes.
3. Clip/share video highlights directly rather than only text quotes — this tool's differentiator is video-first evidence, not text-quote evidence.
4. Global smart search across the team workspace.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Looppanel Pricing | https://www.looppanel.com/pricing | Full 2-tier table, per-seat add-on cost, no free tier confirmed | 2026-08-03 |

## What to borrow for faion
- Video-clip-as-evidence (rather than only text quotes) is a legitimate alternative evidence format worth mentioning in `research-repository-setup` as a platform-scorecard dimension — some studies (usability tests) are better cited as a clip than a transcript quote.

## What NOT to borrow — and why
- Everything about the pricing model: $395/mo floor with a 5-seat minimum makes this the least solopreneur-compatible tool in the cluster — you pay for four seats you will never fill. Do not recommend anywhere in solo/free-tier content; not even worth listing as an "upgrade path" since Marvin/Condens cover the same mechanic at 4-25x lower entry cost.

## Mapping to our corpus
Not named in the corpus; recommend explicitly excluding it from any solopreneur-facing tool list we publish, with a one-line note in `research-repository-setup` under "cost-per-user" scoring criteria as the negative example (team-minimum pricing floor).

## Open questions / staleness risk
- Could not confirm whether a free trial exists elsewhere (e.g. gated behind a demo call) — pricing page shows none; if Looppanel adds one later, re-check before hard-excluding it from free-tier guidance.

---

# Notably
**Layer:** 5 — Domain · **Verdict:** 🟡 take the idea not the tool (pricing unverified against primary source) · **Verified:** 2026-08-03

## What it is
notably.ai — an AI-native research repository/canvas: transcription, AI-generated summaries/insights, and tagging, marketed similarly to Condens/Marvin.

## Current state
**Verification caveat, stated plainly**: `notably.ai` and `www.notably.ai` returned a persistent TLS handshake failure to the fetch tool used in this research pass (`OPENSSL_internal:TLSV1_ALERT_INTERNAL_ERROR`, reproduced across https/http and a reader-proxy retry) — almost certainly bot/anti-scraping protection on their edge, not a sign the site is down. **I could not verify Notably's pricing directly against its own page** and had to rely on secondary sources, which disagree:

- **aichief.com** (review site, checked 2026-08-03): Free trial ($0, "limited access... individual use and initial exploration"); **Pro $50/month** (AI-generated summaries/insights, 50 AI credits/month, 10 transcription hours); **Teams $400/month**; Enterprise custom. This shape (transcription hours + AI-credit metering + Teams tier priced near Looppanel's) is consistent with a UX-research-repository product.
- **toolfi.ai** (review site, checked 2026-08-03): Free ($0, "up to 100 notes," single user); Pro **$8/month** ("unlimited notes," "advanced AI," collaboration). This shape (a flat note-count cap, no transcription/AI-credit language) reads like a **generic note-taking app**, not a research repository — likely either a data-quality error on the review site or evidence of a name collision with a different "Notably" product, structurally the same risk flagged for Marvin in this task but not resolved with the same confidence here.

Given the domain mismatch (transcription hours and AI-credit metering only appear in the aichief figures, and Teams-at-$400 sits in the same band as Looppanel's team-priced competitor), **aichief's figures are the more credible read for the UX-research-repository "Notably,"** but this is a secondary-source judgment call, not a primary-source fact — flagged explicitly rather than stated as settled.

## Mechanics (per secondary sources, unverified against primary)
1. Free trial: limited-feature individual exploration, no stated hard cap besides "limited access."
2. Pro ($50/mo per aichief): AI summaries/insights, metered AI credits (50/mo) and transcription hours (10/mo) — a usage-metered single-contributor tier, structurally similar to Marvin's credit system.
3. Teams ($400/mo): scale tier, details not surfaced by either secondary source.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|---------------|---------|
| 1 | Notably homepage/pricing (primary) | https://www.notably.ai/pricing | **Not fetchable** — persistent TLS error from fetch tool | Attempted 2026-08-03, failed |
| 2 | AIChief — Notably review | https://aichief.com/ai-productivity-tools/notably/ | Secondary-sourced 4-tier pricing (Free/Pro $50/Teams $400/Enterprise) | 2026-08-03 |
| 3 | ToolFi — Notably pricing | https://www.toolfi.ai/pricing/notably-2a92692b | Conflicting secondary-sourced pricing ($0/$8), likely wrong product or stale scrape | 2026-08-03 |

## What to borrow for faion
- If aichief's numbers are right, Notably's AI-credit + transcription-hour metering is a third data point (alongside Marvin) for "usage-metered AI repository pricing" as a category norm worth naming in our platform-scorecard cost criteria.

## What NOT to borrow — and why
- Do not cite a specific Notably price anywhere in shipped faion content until someone re-verifies directly against `notably.ai` from a browser (not an automated fetcher) — the $8 vs $50 spread is a 6x discrepancy, too large to responsibly publish either number as fact.

## Mapping to our corpus
Not named in the corpus. Do not add it to `research-repository-setup` templates until the pricing conflict above is resolved by a direct, browser-based check.

## Open questions / staleness risk
- **Highest staleness/verification risk in this dossier.** Re-run this check with a real browser session (not an automated HTTP fetch) before using any Notably number in customer-facing content. The TLS failure pattern (consistent across protocol/proxy retries) suggests active bot-blocking, which review sites' own scrapers may also be fighting — explaining why they disagree with each other.

---

## Strategic verdict: does a repository tool make the methodology more or less valuable?

**Yes — but conditionally, and the condition is exactly the one our own methodology already encodes.** The mechanics found across these five tools converge on one real, non-markdown-cheap capability: an **Insight object that holds a pointer array into tagged source quotes**, not a copy-pasted string. Dovetail's "Add evidence" link, Marvin's repository-wide "Ask AI," and Condens'/Notably's AI search all depend on this same structure — a corpus that is *indexed and taggable*, not just written. That buys you two things a markdown folder cannot cheaply replicate:

1. **Aggregation-by-tag across the whole corpus** ("which theme has the most highlights across 40 studies") — in markdown this requires either grep-and-count discipline that degrades linearly with volume, or building your own indexer, which is exactly the buy-vs-build tradeoff layer 5 exists to short-circuit.
2. **Grounded semantic Q&A over your own tagged data** (Marvin's/Notably's "Ask AI," scoped to project or repository) — replicating this in markdown means building a bespoke RAG pipeline, which is a geek-tier engineering project, not a research-ops task.

Markdown *can* replicate the citation mechanic itself cheaply (a quote block under an `## Insight` heading with a footnote back to the source transcript file) — what it cannot replicate cheaply is the **query surface**: aggregation, cross-study search, and cheap re-tagging without hand-editing every file that references a changed tag.

So: **a repository tool makes the methodology more valuable, but only past the scale threshold where aggregation and cross-study query start paying for themselves** — which is precisely the population our own methodology's `Skip If` clause excludes: *"Single-researcher solo workflow with <50 studies/year"* and *"Throwaway research without ongoing reuse."* Below that threshold, a disciplined markdown convention (one file per study, one quote block per insight claim, YAML frontmatter tags) delivers the same evidentiary honesty — "there is something to point at" — at zero tool cost, because at low volume a human can still hold the whole corpus in their head and grep it. Above that threshold (multi-researcher, compliance audit trail, ongoing reuse across quarters) the query surface starts mattering and a repository tool stops being optional.

**On the re-tiering recommendation ("move `research-repository-setup` down because the tools are cheap"): this is wrong, and the actual prices found make that clearer, not murkier.** It's true that Marvin (free) and Condens Lite (€15/mo) are affordable at solo-tier budgets — if "can a solopreneur afford the tool" were the only gate, a re-tier would be defensible. But the methodology's own `Skip If` list already excludes the population that would use the tool at its cheapest tier: single-researcher, <50 studies/year, throwaway research. What the methodology actually produces — a tag taxonomy authored for reuse, an access matrix (admin/researcher/read-only), an audit trail, ingestion wiring from multiple upstream sources, a 90-day historical backfill — are **multi-researcher and compliance concerns**, not "can I afford Dovetail" concerns. A true solopreneur running one study a quarter doesn't need an access matrix (there's only one access level: them) and doesn't need ingestion wiring (they import by hand). Cost of the cheapest tool and applicability of the methodology are two different axes; the prior pass conflated them. **Pro is the correct tier — keep it there.**

## Cluster-level "which of these five should a solopreneur actually use" verdict

- **Marvin — 🟢 take.** Real $0 entry, free tier includes AI summaries + Ask AI, not just a crippled trial; correct product identity confirmed.
- **Condens — 🟢 take.** €15/mo Lite is a genuine, checkout-able single-contributor price with unlimited transcription/projects — the cheapest "real" (non-freemium-capped) paid repository in the cluster.
- **Dovetail — 🟡 take the idea, not the tool.** Self-serve pricing is gone; Free caps at 1 project, Enterprise requires a sales call with no published number — bad fit for a non-technical solopreneur who wants to see a price before signing up.
- **Notably — 🟡 take the idea, not the tool (low confidence).** Plausible ~$50/mo Pro tier per secondary sources, but primary pricing page unreachable and secondary sources disagree 6x — don't recommend a number until re-verified.
- **Looppanel — 🔴 skip.** $395/mo floor with a 5-editor minimum and no free tier; you pay for team seats you don't have.
