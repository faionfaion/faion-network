# Agent Integration — Audience Segmentation

## When to use
- Pre-launch positioning when the team is debating which buyer to target first.
- Post-launch when "everyone is our customer" assumptions are eroding paid-acquisition efficiency or message-resonance metrics.
- Pricing-tier design that needs distinct buying behaviours and willingness-to-pay levels.
- Pivoting into a new market, where the prior segmentation no longer maps.
- Product-tier or product-line decisions (free vs pro vs enterprise; consumer vs SMB vs mid-market).

## When NOT to use
- Pre-traction MVPs with < 50 customers — go for one persona, not segment matrices.
- Strict niche businesses where the entire ICP fits in one segment by design (e.g., tax software for US dentists).
- For account-based sales motions where named accounts replace segmentation.
- For ephemeral campaigns — A/B-test creatives instead.

## Where it fails / limitations
- Segment definitions decay; behavioural segments especially shift in 6-12 months as products and competitors evolve.
- 2x2 matrices give clean visuals but oversimplify multi-dimensional reality; don't over-trust them.
- Demographic-only segmentation is the most common failure mode — yields lookalikes that don't predict purchase.
- Segments that are not addressable (no channel reaches them economically) are worthless regardless of theoretical size.
- Mutually exclusive segmentation in B2B is hard: a contact may be both "decision maker" and "user".

## Agentic workflow
Use agents to ingest CRM, analytics, and survey data; propose candidate segmentation dimensions; score segments against attractiveness criteria from `README.md`; emit profile cards. Decisions about which segment to pursue belong to humans (commercial trade-offs). Agents should never propose a target without addressability evidence and a sizing range. Maintain segments as a structured artefact (YAML/JSON) so re-scoring is reproducible quarter-over-quarter.

### Recommended subagents
- `faion-persona-builder-agent` — produces persona-grade detail per chosen segment.
- A `dimension-finder` subagent: runs feature-importance / variance analysis on CRM/analytics features to surface the two most differentiating axes.
- `faion-brainstorm` — diverges on candidate segment names + needs framings, converges on at most four mutually exclusive segments.
- A `scorer` subagent: applies the weighted criteria (Size 20, Growth 15, Reachability 20, Profitability 20, Fit 15, Competition 10) consistently across segments.
- `faion-improver` — quarterly refresh against fresh data.

### Prompt pattern
"Given the attached CRM export (`crm.csv`) with fields `[plan, mrr, signup_source, employee_count, industry, churn_30, feature_use_score]`, propose two candidate dimensions that maximise inter-segment variance and minimise intra-segment variance. Show a confusion matrix for each. Output as `dimensions.json`."

"Given segments `[A, B, C]` and the attractiveness rubric below, score each 1-5 per criterion with one-line justification. Compute weighted total. Flag any score with no evidence."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| dbt | Cohort and segment SQL pipelines | https://docs.getdbt.com |
| Posthog / Amplitude / Mixpanel APIs | Behavioural-segment cohorts | https://posthog.com / https://amplitude.com/docs/apis |
| HubSpot / Salesforce CLI | CRM segment ops | https://developers.hubspot.com / https://developer.salesforce.com |
| Segment / RudderStack | CDP routing per segment | https://segment.com / https://www.rudderstack.com |
| `pandas` + `scikit-learn` | k-means / hierarchical clustering for segmentation | `pip install pandas scikit-learn` |
| `kmodes` | Categorical-variable clustering | `pip install kmodes` |
| Notion / Airtable API | Segment library | https://developers.notion.com |
| Census / Hightouch | Reverse-ETL segments to ad/email tools | https://www.getcensus.com / https://hightouch.com |
| Crayon / Klue (if exposed) | Competitive intel per segment | https://www.crayon.co / https://klue.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Segment / RudderStack | SaaS / OSS | Yes (REST + SDK) | CDP for segment-driven activation |
| Census / Hightouch | SaaS | Yes (REST) | Reverse-ETL to ad platforms |
| HubSpot / Salesforce | SaaS | Yes (REST) | CRM as segment ground truth |
| Posthog / Amplitude / Mixpanel | SaaS | Yes (REST) | Behavioural data |
| Apollo.io / ZoomInfo | SaaS | Yes (REST) | B2B firmographic enrichment |
| Clearbit (now HubSpot) | SaaS | Yes (REST) | Firmographic data on sign-ups |
| SurveyMonkey / Typeform | SaaS | Yes (REST) | Psychographic survey delivery |
| Forsta / Qualtrics | SaaS | Yes (REST) | Enterprise segmentation studies |
| Productboard | SaaS | Yes (REST) | Segment ↔ feature roadmap link |
| Crayon / Klue | SaaS | Yes (REST) | Competitive density per segment |

## Templates & scripts
See `templates.md` and `examples.md` for the full segmentation analysis and segment profile-card templates.

Inline behavioural-segment k-means (deterministic seed for reproducibility):

```python
# segment.py — k-means on usage features, emits segments.json
import json, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv("usage.csv")  # cols: customer_id, mrr, dau_w, feat_score, seats
features = ["mrr", "dau_w", "feat_score", "seats"]
X = StandardScaler().fit_transform(df[features])

km = KMeans(n_clusters=4, n_init=20, random_state=42).fit(X)
df["segment"] = km.labels_

profile = (
    df.groupby("segment")[features]
      .agg(["mean", "median", "count"])
      .round(2)
      .to_dict()
)
out = {
    "n_segments": 4,
    "feature_importance": dict(zip(features, km.cluster_centers_.var(axis=0).tolist())),
    "profile": profile,
}
with open("segments.json", "w") as f:
    json.dump(out, f, indent=2)
```

## Best practices
- Pick two dimensions, not five — anything denser is unreadable in stakeholder conversations.
- Combine quantitative (firmographics, behavioural) and qualitative (needs, attitudes); pure quant misses messaging insights.
- Validate segment size against an addressable population (LinkedIn audience, paid-ads reach, list rentals); theoretical size means nothing.
- Always include a "do-not-target" segment with explicit reasoning (low LTV, high CAC, support-cost-heavy).
- Pair the top segment with one channel and one message; if you can't pick one, the segment is too broad.
- Re-score quarterly using the same rubric weights; weight changes must be flagged as a methodology change.
- Sanity-check exclusivity: every customer should fit one and only one segment after rules apply; orphans signal definition gaps.
- Map segments to existing personas explicitly; the two artefacts must agree.

## AI-agent gotchas
- Agents asked to "find segments" without constraints often output 8 micro-segments by demographics; force a 2-3 dimension cap.
- LLMs invent segment sizes ("estimated 200K SMBs in NYC") that are decorative; demand a source for any quantitative claim.
- Behavioural-clustering agents over-fit to noisy features (e.g., one outlier whale); require feature standardisation and scree-plot evidence for `k`.
- B2B segmentation generated from B2C tropes (lifestyle, age) misses fit/firmographics; force `industry, employee_count, role` as priors.
- Reverse-ETL bots syncing segments to ad tools without a kill switch can blow ad budgets; require approval gating in production.
- Agents merging "current solution" responses across surveys conflate competitors with substitutes; clarify in the prompt.
- When proposing the final target, agents tend to pick the largest segment; force a weighted-score table so reachability and fit aren't ignored.

## References
- Tony Ulwick — *Jobs To Be Done* (needs-based segmentation)
- Mark Ritson — *Mini MBA in Marketing* (segmentation lectures)
- Philip Kotler — *Marketing Management* (classical demographic / psychographic / behavioural)
- April Dunford — *Obviously Awesome* (positioning per segment)
- Bain & Company — *Customer Segmentation* primer — https://www.bain.com/insights/management-tools-customer-segmentation/
- Christensen, Cook, Hall — *Marketing Malpractice* (HBR), the JTBD critique of segmentation
