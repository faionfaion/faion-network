---
name: competitor-analysis
description: Identify 5-8 competitors (direct + adjacent), score them on 8 axes, and produce a 1-page client-ready deliverable.
tier: pro
group: market-research
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a structured competitor matrix covering 5-8 players across 8 scoring axes, plus a condensed 1-page deliverable you can hand to a client or paste into a strategy deck — using B2B onboarding tools (Userflow, Appcues, Pendo, Chameleon, WalkMe, Intercom, Stonly) as the worked example throughout.

## Prerequisites

- A defined product category and target buyer segment (e.g., "B2B onboarding tool for SaaS teams under 50 seats").
- Access to G2, Capterra, Product Hunt, LinkedIn, SimilarWeb (free tier), Crunchbase (free tier).
- A spreadsheet or Notion table to build the matrix.
- Familiarity with basic pricing research (public pricing pages + sales inquiry).
- Completed `scope-creep-management` if you are delivering this as a client engagement add-on.

## Steps

1. **Define the competitive scope.** Write one sentence: "We are a [product type] for [buyer segment], solving [core problem]." For the worked example: "Userflow is an in-app onboarding tool for SaaS product teams who need to build interactive product tours without engineers."

2. **Source 5-8 competitors across two layers.** Direct competitors share the same product type and buyer. Adjacent competitors solve the same problem with a different approach:
   - Direct (same tool category): search G2 → category "User Onboarding" → "Highest Rated". Pull: Userflow, Appcues, Pendo, Chameleon, WalkMe.
   - Adjacent (related category or substitute): Intercom (onboarding via in-app messages), Stonly (knowledge-base-led onboarding). Also check Product Hunt "onboarding" tag for emerging players.
   - Cap the list at 8 to keep the matrix client-readable. Drop duplicates or tools clearly out of the target segment.

3. **Build the 8-axis matrix.** Open a spreadsheet with competitors as rows and the axes below as columns. Fill each cell with a short factual note (1-2 lines max), not opinion:

   | Axis | What to capture | Source |
   |------|----------------|--------|
   | **Price** | Starting plan cost / billing model | Public pricing page or sales inquiry |
   | **Target segment** | ICP: company size, team, use case | G2 profile, homepage headline |
   | **USP** | Primary differentiation claim | Homepage H1 / G2 "What I like most" reviews |
   | **Weakness** | Most cited complaint | G2/Capterra negative reviews (sort by lowest rating) |
   | **Traction signal** | Customer count, G2 review count, or self-reported ARR | G2 profile, press releases |
   | **Growth rate** | Hiring pace (LinkedIn "Jobs"), new review velocity (G2 "Recent" tab) | LinkedIn, G2 |
   | **Funding** | Total raised, last round, investor tier | Crunchbase free tier |
   | **Threat level** | H / M / L — your assessment based on the above | Synthesis |

   Example row (Pendo): Price: $7k-35k/yr (sales-led, no self-serve) | Target: mid-market SaaS, 100-1000 seats | USP: product analytics + in-app guides in one platform | Weakness: expensive, complex setup, overkill for small teams | Traction: 10k+ customers (self-reported) | Growth: 50+ open roles on LinkedIn | Funding: $348M raised (Series F) | Threat: High (enterprise expansion risk).

4. **Classify threat level for each competitor.** Use a 3-point scale:
   - **High** — well-funded, growing fast, overlapping ICP, investing in features that erode your differentiation.
   - **Medium** — overlapping ICP but slower growth, different pricing tier, or narrower feature set.
   - **Low** — adjacent only, different buyer, stagnant hiring, no recent funding.

   For the worked example: WalkMe = High (enterprise, owned by SAP); Appcues = Medium (similar ICP but slower growth); Stonly = Low (knowledge-base-first, different motion).

5. **Identify one strategic insight per quadrant.** After filling the matrix, group competitors by threat level and write one sentence per group:
   - High-threat insight: "WalkMe/Pendo occupy the enterprise tier; competing there requires a platform investment or a clear 'simple alternative' narrative."
   - Medium-threat insight: "Appcues and Chameleon are the most direct price-comparable rivals; product-led trial conversion is the primary battleground."
   - Low-threat insight: "Adjacent tools (Intercom, Stonly) are churn risks if the buyer discovers them post-sale; differentiation must be in-product, not just in marketing."

6. **Condense to a 1-page client deliverable.** Structure:
   - Header: market name, date, analyst name.
   - Table: all 8 columns, max 8 rows, each cell ≤15 words.
   - Below the table: 3 bullet "Strategic Observations" (one per threat tier).
   - Footer: "Sources: G2, Crunchbase, LinkedIn — data as of [date]. Prices and funding may change."

   Export the spreadsheet tab as PDF or copy the Notion table into a client doc. Keep the full working spreadsheet as the source of truth; the 1-pager is a summary only.

7. **Review for staleness and gaps.** Before sending:
   - Re-check any funding figure older than 6 months on Crunchbase.
   - Confirm pricing pages still exist (companies remove pricing when going sales-led).
   - Verify you have ≥1 G2/Capterra review source for each competitor's weakness; do not derive weaknesses from product docs alone.

## Verify

Open the finished matrix and confirm all of the following are true:

- Exactly 5-8 competitor rows, no empty rows.
- All 8 axis columns filled (no "N/A" without a note explaining why data is unavailable).
- Each "Threat level" cell is one of: High, Medium, or Low.
- The 1-page deliverable fits on a single printed page (test: File → Print → 1 page).
- At least one competitor per threat tier (High / Medium / Low) is present.

If any check fails, return to Step 3 or Step 4 and fill the gap before delivering.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cannot find pricing for a competitor | Sales-led pricing, no public page | Note "sales-led, contact for pricing" in the Price cell; use G2 reviewer comments like "costs ~$X/mo" as a proxy and cite the review URL |
| Two competitors look nearly identical in the matrix | Axes are too coarse or you have a duplicate | Check target segment closely — if ICP differs (SMB vs. mid-market), add a "Min seats" sub-column. If truly identical, remove the weaker one. |
| Crunchbase shows no funding data | Company is bootstrapped or data not public | Note "bootstrapped (no public funding)" — this is itself a strategic signal (no VC pressure to expand) |
| Matrix has 9+ competitors and feels unwieldy | Scope too broad | Cut to direct-only for the 1-pager; move adjacent competitors to an appendix table with only 3 axes (Price, Target, Threat) |
| Client disputes a "Weakness" entry | Sourcing is anecdotal | Link to ≥2 G2/Capterra reviews (date + reviewer role) for each weakness. If you can't find 2 sources, downgrade the claim to "reported by some users" |
| Growth rate is ambiguous — one tool is hiring but another has more reviews | Hiring and review velocity measure different things | Report both signals separately in the Growth column; write "hiring: 40 open roles (LinkedIn); review velocity: +120 reviews in 90 days (G2)" |

## Next

- Run `scope-creep-management` before presenting this matrix to a client as a standalone deliverable — framing research as a deliverable requires clear scope boundaries.
- Use the High-threat competitors as input to a positioning workshop: take the USP column of all High-threat players and identify the claim your product can own that none of them make.
- Revisit the matrix quarterly: set a calendar reminder to re-run Steps 3-4 for the High-threat group only; Low/Medium can be reviewed semi-annually.

## References

- [knowledge/pro/research/market-researcher/competitor-analysis](../../../knowledge/pro/research/market-researcher/competitor-analysis) — provides the SWOT-grid + market-share estimation framework that underpins Steps 3-5; the 8-axis matrix in this playbook is a condensed client-facing adaptation of that methodology's portfolio scorecard output.
- [knowledge/pro/research/market-researcher/competitive-intelligence-methods](../../../knowledge/pro/research/market-researcher/competitive-intelligence-methods) — the four-type competitor taxonomy (direct/indirect/substitute/potential) drives Step 2's sourcing logic; the gap-validation critic principle informs the "adjacents as churn risk" observation in Step 5.
