# Agent Integration — Competitive Intelligence (Market Researcher)

> **Scope:** Market-researcher angle on CI. Sister doc
> `pro/research/researcher/competitive-intelligence/agent-integration.md`
> covers the general agentic CI loop (collector → classifier → synthesizer →
> battlecard). This file focuses on the three market-research deliverables
> the researcher orchestrator does NOT cover: **win/loss analysis**,
> **pricing intelligence**, and **market-positioning signals**.

## When to use
- Deal review backlog has > 20 closed-lost / closed-won opps in the last 60 days and CRM stage notes are unstructured.
- Pricing committee meets quarterly and needs a defensible benchmark (model, list, discounting band, packaging) per segment.
- Inbound positioning brief is stalling because category language ("API platform" vs "iPaaS" vs "agent runtime") is contested.
- Repositioning, rebrand, or new-segment launch where messaging needs evidence from buyer language, not exec opinions.
- Pre-Series-B/C: investors will ask for a defensible win-rate trend with reasons-coded loss data.

## When NOT to use
- < 10 closed deals/quarter — sample too small; n=10 win/loss is anecdote, not analysis. Use customer interviews instead.
- Self-serve / PLG product with no sales conversations — there is no "loss reason" to extract; switch to churn analytics + cancel-survey.
- Pricing locked by enterprise contract (multi-year MSAs) for the next 12 months — pricing intel has no decision to inform.
- Single-product, single-segment startup — positioning emerges from PMF interviews, not CI synthesis.
- Where buyer interviews are blocked by NDA or Procurement — synthesize from public review sites, do not fabricate.

## Where it fails / limitations
- **Win/loss self-report bias:** sales reps over-attribute losses to "price"; buyers cite price ~30% of the time but actually leave for product fit, integration risk, or relationship gaps. Always run buyer-side interviews for ≥30% of losses; never rely solely on rep notes.
- **Pricing page theater:** posted list price ≠ closed price. Discounting averages 15–35% in B2B SaaS; published intel without realized-ACV grounding is misleading. Cross-check with G2 reviewer-disclosed spend, Vendr/Tropic benchmarks, and ex-customer interviews.
- **Packaging fog:** competitors hide tiers behind "Contact Sales" or rotate AB-tested pages; a single scrape lies. Require ≥3 independent fetches over 14 days before declaring a pricing change.
- **Positioning language drift:** category labels mutate (e.g., "AI workflow" → "agent" → "agentic"). LLM clustering will collapse distinct positions. Always extract verbatim quotes from buyers and competitors before LLM summarization.
- **Anchoring on the loudest competitor:** market-share leaders dominate review-site volume; emerging threats are invisible until they take a deal. Stratify by segment and deal-size, not raw mention count.
- **Survivorship bias in win-rate uplift:** the 16%→45% Crayon case study conflates CI rollout with new pricing, new battlecards, and new sales hires. Do not promise this number to leadership.

## Agentic workflow
A `wl-extractor` agent ingests CRM closed-deal records (Salesforce/HubSpot exports, Gong/Chorus transcripts) and emits a normalized `loss_reason` and `competitor_won` field with cited evidence per deal. A `pricing-tracker` agent runs the general CI collector but writes to a separate pricing event store with packaging diffs (tier name, included quotas, add-ons, contract length) and triangulates against G2 spend disclosures + Vendr indexes. A `positioning-extractor` agent pulls competitor homepage hero, G2 review headlines, and analyst-report mentions; clusters them by job-to-be-done; and outputs a positioning map. A weekly `market-synth` agent produces a single doc that joins all three streams into the `competitive-analysis.md` deliverable in `.aidocs/product_docs/`. Humans approve loss-reason coding for every deal > $100k ACV and any pricing change > 10%.

### Recommended subagents
- `faion-research-agent` (mode `competitors`) — orchestrator entry; calls the four specialists below and assembles `competitive-analysis.md`.
- `wl-extractor` — Sonnet. Parses CRM stage notes + call transcripts; emits structured `{deal_id, stage, amount, competitor_won, primary_loss_reason, secondary_reasons[], evidence_quotes[]}`. Reject deals lacking ≥1 buyer-side quote.
- `pricing-tracker` — Haiku for fetch + Sonnet for diff. Polls pricing pages on a 24h cadence, normalizes to a canonical schema (per-seat / per-usage / flat / hybrid), flags packaging changes, cross-references Vendr/Tropic when available.
- `positioning-extractor` — Sonnet. Extracts hero copy, "compare to" pages, third-party analyst language (Gartner, Forrester, IDC summaries on AlphaSense). Outputs `{competitor, claimed_category, ICP_signal, JTBD_extracted}`.
- `pricing-fact-checker` — Sonnet. HEADs every URL claim, recomputes effective annual cost from raw page text, blocks digest publication if math fails.
- `wl-interviewer-prepper` — Sonnet. Generates buyer-interview discussion guide per closed-lost deal (uses JTBD interview protocol, not feature checklist); humans run the interview.

### Prompt pattern
Win/loss extractor (XML, structured output, evidence-first):
```
<role>win/loss analyst</role>
<task>code one closed deal</task>
<deal_id>{{ id }}</deal_id>
<crm_notes>{{ stage_history_md }}</crm_notes>
<call_transcripts>{{ gong_excerpts }}</call_transcripts>
<output_schema>{outcome: won|lost|no_decision, competitor_won?: str, primary_reason: enum[price|product_fit|integration|relationship|timing|incumbent|other], secondary_reasons: list, evidence_quotes: list[{speaker, quote, source}], confidence: 1-5}</output_schema>
<rules>If no buyer-side quote, set confidence <= 2 and flag for interview. Never infer reason from rep speculation alone.</rules>
```

Pricing diff (XML):
```
<role>pricing analyst</role>
<previous>{{ snapshot_t0 }}</previous>
<current>{{ snapshot_t1 }}</current>
<output_schema>{change_type: enum[price|tier|packaging|none], magnitude_pct: number, what_changed: str, effective_annual_cost_delta_usd: number, evidence_urls: list, confidence: 1-5}</output_schema>
<constraint>Recompute effective cost from raw text. If the page is unchanged but JS-rendered, return INSUFFICIENT_DATA.</constraint>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gong` API | Call transcripts, deal-room stage history | gong.io/api |
| `chorus` (ZoomInfo) API | Same-class call intel | chorus.ai/developers |
| `salesforce` REST / Bulk API | Closed-deal export, custom loss-reason fields | developer.salesforce.com |
| `hubspot` API | SMB CRM equivalent | developers.hubspot.com |
| `vendr` data | Realized SaaS pricing benchmarks | vendr.com (gated; scrape ToS-restricted) |
| `tropic` benchmarks | Negotiation/realized-price index | tropicapp.com (partner API) |
| `g2` Buyer Intent + Reviews API | Reviewer-disclosed spend, sentiment, win signals | g2.com/products/api |
| `capterra` / `softwareadvice` scrape | Buyer reviews with workflow context | apify.com actors |
| `alphasense` | Analyst notes, earnings transcripts (pricing commentary) | alpha-sense.com/api |
| `crunchbase` API | Funding-stage → pricing-power inference | data.crunchbase.com |
| `klue` win/loss module | Structured win/loss workflow + battlecards | klue.com/win-loss |
| `clozd` | Outsourced + DIY buyer-interview platform | clozd.com |
| `primary intelligence` | Win/loss interview SaaS | primary-intel.com |
| `firecrawl` / `r.jina.ai` | LLM-ready pricing-page extract | firecrawl.dev, r.jina.ai |
| `playwright` | Render JS pricing pages with calculator widgets | playwright.dev |
| `dbt` + `duckdb` | Local warehouse for win/loss + pricing facts | duckdb.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Klue Win-Loss | SaaS | Partial — REST API | Tight Salesforce integration; closed taxonomy. |
| Clozd | SaaS + services | Limited API | Best-in-class buyer interviews; human-in-the-loop. |
| Primary Intelligence | SaaS | API + Slack | Programmatic interview dispatch; structured loss reasons. |
| Crayon | CI suite (with W/L module) | REST API | Battlecards + win/loss roll-up. |
| Vendr | Pricing benchmark | Partner API only | Realized-price truth source for B2B SaaS. |
| Tropic | Pricing/negotiation | Partner API | Similar to Vendr; complements. |
| Gong | Call intel | REST + webhooks | Source of truth for buyer quotes. |
| Chorus | Call intel | REST | ZoomInfo-owned; equivalent. |
| AlphaSense | Analyst & filings | REST + summaries | Pricing commentary in earnings calls. |
| G2 | Reviews + intent | REST | Reviewer-disclosed deal size and renewal status. |
| TrustRadius | Reviews | Limited API | Smaller volume; B2B-only. |
| Owler / Crunchbase | Firmographic + funding | REST | Pricing-power signal (funding stage). |
| ProfitWell / Paddle Price Intelligently | Willingness-to-pay studies | API + reports | Survey-based; complements scrape. |
| Maxio (SaaSOptics) | Realized ACV in your stack | REST | Internal benchmark, not competitive — but needed for delta math. |

## Templates & scripts
Inline win/loss → competitive-analysis joiner (Python, ≤ 50 lines):

```python
# wl_join.py — join win/loss + pricing + positioning into one doc
import json, pathlib, collections, statistics, datetime
WL = [json.loads(l) for l in open("wl_events.ndjson")]
PRICE = [json.loads(l) for l in open("pricing_events.ndjson")]
POS = [json.loads(l) for l in open("positioning_events.ndjson")]

# win-rate per competitor, last 90d
cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()
recent = [d for d in WL if d["closed_at"] >= cutoff]
by_comp = collections.defaultdict(lambda: {"won": 0, "lost": 0, "reasons": []})
for d in recent:
    if d.get("confidence", 0) < 3:  # drop low-confidence
        continue
    c = d.get("competitor_won") or "no-competitor"
    if d["outcome"] == "won": by_comp[c]["won"] += 1
    elif d["outcome"] == "lost":
        by_comp[c]["lost"] += 1
        by_comp[c]["reasons"].append(d["primary_reason"])

rows = []
for c, s in by_comp.items():
    n = s["won"] + s["lost"]
    if n < 5: continue  # n>=5 minimum
    wr = s["won"] / n
    top_reason = collections.Counter(s["reasons"]).most_common(1)
    price_delta = next((p["effective_annual_cost_delta_usd"] for p in PRICE if p["competitor"] == c), None)
    pos = next((p["claimed_category"] for p in POS if p["competitor"] == c), "?")
    rows.append((c, n, wr, top_reason[0][0] if top_reason else "?", price_delta, pos))

rows.sort(key=lambda r: r[2])  # worst win-rate first = highest threat
out = pathlib.Path(".aidocs/product_docs/competitive-analysis.md")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w") as f:
    f.write(f"# Competitive Analysis ({datetime.date.today()})\n\n")
    f.write("| Competitor | n | Win-rate | Top loss reason | Price delta (USD/yr) | Position |\n")
    f.write("|---|---|---|---|---|---|\n")
    for c, n, wr, r, pd, pos in rows:
        f.write(f"| {c} | {n} | {wr:.0%} | {r} | {pd or '?'} | {pos} |\n")
```

The orchestrator (`faion-research-agent`) shells out to this after the three collectors complete. Drop the doc into `.aidocs/product_docs/competitive-analysis.md` per the researcher contract.

## Best practices
- **Code loss reasons in the buyer's words, not yours.** Maintain a 6–8 reason taxonomy max (price / product_fit / integration / relationship / timing / incumbent / other); resist taxonomy bloat — it kills cross-period comparison.
- **Separate "no decision" from "lost".** ~30% of B2B "losses" are stalled deals, not competitive losses. Mixing them poisons win-rate trend.
- **Triangulate price three ways:** posted list, G2 reviewer-disclosed actual, ex-customer or buyer interview. Publish the median and the spread.
- **Track price-per-job-done, not price-per-seat.** A $50/seat tool replacing a $500/seat workflow is cheap. Tag pricing intel with the JTBD it serves.
- **Run buyer-side win/loss interviews on ≥30% of lost deals > $50k ACV.** Outsource to Clozd or use an internal interviewer who never sat on the deal — reps cannot interview their own losses.
- **Stratify everything by segment + deal size.** "We lose 60% of the time" is meaningless; "We lose 80% of mid-market deals against Vendor X when integration matters" is actionable.
- **Positioning extracted from buyers > positioning declared by competitors.** Hero copy is what they wish to be; G2 reviews are what buyers think they are. The gap is your wedge.
- **Re-baseline quarterly.** Pricing, packaging, and positioning shift; a stale market map is worse than no map.
- **Include yourself in every analysis.** Win-rate trend without your own deltas is missing the dependent variable.
- **Publish dated artifacts.** Every output file: `competitive-analysis-YYYY-MM-DD.md`. Sales enablement trusts dates.

## AI-agent gotchas
- **Loss-reason hallucination from rep notes:** notes say "they went with Vendor X" — agent invents a reason. Force the schema to require ≥1 verbatim quote with `speaker` field; reject otherwise.
- **Currency and term ambiguity:** "$10/month" can be USD/EUR, monthly/annually, per-seat/per-org. Schema must pin currency, billing period, unit, and contract length, or downstream math is wrong.
- **Hidden-tier collapse:** if competitor hides Enterprise tier, agent reports "no Enterprise tier exists." Mitigate with G2-disclosed price + LinkedIn job posts mentioning ACV ranges.
- **AB-test flicker:** competitor runs pricing AB tests; daily fetch sees noise. Require persistence across N consecutive fetches before declaring a change (N=3 over 14 days).
- **Reason-taxonomy drift:** model adds new categories every run, breaking trend lines. Pin the enum in the schema; flag deals that don't fit for human triage rather than silently expanding categories.
- **Survivorship in interviews:** only reachable lost-deal contacts get interviewed; reachables are systematically biased (likely happier). Sample randomly within segment, not by who responds first.
- **LLM rep-empathy bias:** model defends sales rep narrative ("buyer was confused"). Adversarial prompt: "Argue the buyer was right to leave; cite evidence."
- **Cross-currency win-rate math:** compute win-rate by deal count AND by ACV; the two often disagree and the gap is the real story.
- **Quote attribution leak:** agent paraphrases buyer quotes losing attribution; downstream report cites "a customer" — useless to leadership. Preserve `{speaker_role, company_size, segment}` end-to-end, never the buyer's name.
- **Positioning category collapse:** model clusters "agent platform" with "automation platform" with "iPaaS"; loses the wedge. Require k-means with manual seed labels per quarter; reject auto-clustering output.
- **Confirmation prompts:** "Why are we losing?" yields a list. Use neutral framing: "Score the closed-lost deals on each of [price, fit, integration, …]; if evidence is absent, return 0."
- **Reasons that aren't:** "no_decision" → "timing" → leadership thinks pipeline is hot. Treat no-decision as its own outcome and report stalled-pipeline rate separately.

## References
- https://www.klue.com/win-loss (Klue win/loss module)
- https://www.clozd.com/blog (buyer-interview methodology)
- https://www.primary-intel.com/resources (interview protocols)
- https://www.vendr.com/blog/saas-pricing (realized-price benchmarks)
- https://www.tropicapp.com/insights (negotiation/realized data)
- https://www.gong.io/blog/sales-call-analysis (transcript mining patterns)
- https://www.priceintelligently.com (willingness-to-pay study design)
- https://www.profitwell.com/recur (SaaS pricing research)
- https://www.april-dunford.com/blog (positioning frameworks: Obviously Awesome / Sales Pitch)
- https://strategyn.com/jobs-to-be-done (JTBD-based positioning)
- https://www.g2.com/products/api/documentation (review + intent + spend data)
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Sister doc: `pro/research/researcher/competitive-intelligence/agent-integration.md` (general CI loop)
