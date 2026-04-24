# Agent Integration — Audience Segmentation

## When to use
- Pre-launch: deciding which one segment a solopreneur ships their MVP to.
- Post-launch with mixed signals (e.g. churn high in 30% of cohort, NPS high in 50%) — segment to find the actual ICP.
- Repositioning a stalled product where messaging tests against "everyone" failed.
- Pricing tier design when usage data shows two or more behavioral clusters.
- Channel allocation: when paid spend gets diffused across LinkedIn, Reddit, X, YouTube without a clear winner.
- B2B GTM: when sales calls reveal three buyer personas with different objections.

## When NOT to use
- TAM under ~5k addressable accounts — segment further and you starve every segment of evidence.
- First 10 paying customers — too few datapoints; do `pain-points` and `problem-validation` instead.
- Pure infra/dev tools where the buyer is "any engineer with this stack" — use `niche-evaluation`.
- When dimensions are picked from gut alone with zero interview/CRM/analytics data feeding them.
- For one-off campaigns where the segment is already given by the brief.

## Where it fails / limitations
- LLM-driven segmentation hallucinates plausible-sounding personas that don't exist in the data — always anchor on real interview transcripts or analytics rows.
- Static segmentation rots within 6–12 months as the market shifts; without a refresh cadence the deck becomes lore.
- Demographic-only segments (age, role, company size) consistently underperform behavior-and-needs segments for messaging work.
- Two-by-two matrices over-collapse: real markets often have 5–7 meaningful clusters that the matrix forces into four boxes.
- Score weighting is subjective; agents tend to score every segment 3–4 (regression to the mean) unless forced into rank-ordering.
- Segment size estimates from public sources (LinkedIn filters, Statista) compound error — validate with at least one bottom-up count.

## Agentic workflow
Drive segmentation as a multi-step pipeline: (1) data-collection agents hit CRM/analytics/transcripts, (2) clustering agent proposes 5–8 candidate segments, (3) `faion-research-agent` (mode `personas`) and `faion-persona-builder-agent` build profiles, (4) human ranks/eliminates before agents score the survivors. Never let one agent run end-to-end without a human checkpoint between candidate generation and scoring — that is where hallucinated segments slip through.

### Recommended subagents
- `faion-research-agent` — orchestrator with mode `personas` / `pains` / `validate`; outputs `user-personas.md`, `pain-points.md` to `.aidocs/product_docs/`.
- `faion-persona-builder-agent` — listed in this methodology's frontmatter; takes raw interview/CRM rows and produces segment profile cards using the template in `templates.md`.
- `faion-domain-checker-agent` — for naming the segments once shortlisted (verifies name candidates aren't already taken as brand handles).
- `faion-sdd-executor-agent` — to encode the chosen target segment as a constitution decision and propagate it into product specs.

### Prompt pattern
```
You are running mode=segmentation on the product described in <product>.
Inputs: <CRM_export.csv>, <interview_transcripts/>, <analytics_rollup.json>.
Step 1: extract dimensions only from observed variation in inputs. No inferred dimensions.
Step 2: propose 4–8 candidate segments with cited row counts.
Step 3: STOP. Return JSON {dimensions, candidates[]} for human review.
```

```
Given approved segments <segments.json>, score each on Size/Growth/Reach/Profit/Fit/Competition (1–5) using ONLY evidence from <evidence_pack/>. For any criterion lacking evidence, return "unknown" — do not guess. Output the table from templates.md verbatim.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Materialize segment definitions as warehouse models so segments are queryable, not deck-trapped | https://docs.getdbt.com |
| `duckdb` CLI | Local clustering / segment counts over CSV exports without a warehouse | https://duckdb.org |
| `posthog-cli` | Pull cohort definitions, behavioral events, feature-flag rollouts per segment | https://posthog.com/docs/cli |
| `mixpanel` Query API + `httpie` | Behavioral-segment counts and funnels via JQL | https://developer.mixpanel.com |
| `gh` + Discussions | Pull public user discussions/tags as qualitative segment signal | https://cli.github.com |
| `jq` | Slice JSON exports from Stripe/HubSpot/Pipedrive into per-segment files | https://jqlang.github.io |
| `pandas` + `scikit-learn` (`KMeans`, `silhouette_score`) | Automated cluster discovery on numeric/behavioral matrices | https://scikit-learn.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS + SaaS | Yes — REST + cohort API | Cohorts map 1:1 to behavioral segments; can be created/read by agents |
| Mixpanel | SaaS | Yes — JQL + Cohorts API | Best for behavioral segmentation on event streams |
| Amplitude | SaaS | Partial — paid tier for API | Behavioral cohorts; UI-heavy |
| HubSpot | SaaS | Yes — Lists API | Demographic + lifecycle segmentation; B2B CRM |
| Segment (Twilio) | SaaS | Yes — Personas/Computed Traits API | Identity resolution across sources before segmentation |
| Census / Hightouch | SaaS (reverse ETL) | Yes — API + dbt models | Sync warehouse segments to ad/email platforms |
| Dovetail | SaaS | Partial — REST API | Tag interview transcripts; export themes for psychographic segmentation |
| Notably / Marvin | SaaS | Yes — auto-tagging | AI tagging of qualitative data into segment dimensions |
| Statista / SimilarWeb / IBISWorld | SaaS | Limited (paid API) | Top-down market sizing per segment; require human verification |
| LinkedIn Sales Navigator | SaaS | No public API for segment counts | Use the filter UI to estimate B2B TAM by firmographic segment |

## Templates & scripts

See `templates.md` for the segmentation analysis and segment profile card templates. Inline below: a small clustering harness that turns a CSV of users into candidate behavioral segments — useful as the "Step 2" data step before agents propose names.

```python
# segment_candidates.py — emit candidate behavioral clusters from a usage CSV
# Usage: python segment_candidates.py users.csv 5 > candidates.json
import sys, json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

path, k_max = sys.argv[1], int(sys.argv[2])
df = pd.read_csv(path)
num = df.select_dtypes(include="number").fillna(0)
X = StandardScaler().fit_transform(num)

best = {"k": None, "score": -1, "labels": None}
for k in range(2, k_max + 1):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    s = silhouette_score(X, km.labels_)
    if s > best["score"]:
        best = {"k": k, "score": float(s), "labels": km.labels_.tolist(), "centers": km.cluster_centers_.tolist()}

df["segment"] = best["labels"]
profiles = []
for seg_id, group in df.groupby("segment"):
    profiles.append({
        "segment_id": int(seg_id),
        "n": int(len(group)),
        "share": round(len(group) / len(df), 3),
        "means": {c: float(group[c].mean()) for c in num.columns},
    })

print(json.dumps({"k": best["k"], "silhouette": best["score"], "profiles": profiles}, indent=2))
```

## Best practices
- Pick dimensions from observed variance, not from a textbook list — if every customer is the same on a dimension, drop it.
- Force mutually-exclusive, collectively-exhaustive (MECE) segments; agents tend to write overlapping ones unless prompted.
- Quantify each segment with two independent estimates (top-down market-sizing + bottom-up CRM count); flag any segment where they disagree by 3x+.
- Name segments after their job-to-be-done (e.g. "The Overwhelmed Solo PM"), not their demographics — names drive messaging.
- Score on rank-order first (1st, 2nd, 3rd most attractive), then assign 1–5 weights, to defeat the regression-to-the-middle problem.
- Refresh quarterly; archive prior versions so segment-drift is visible.
- For solopreneurs: commit to ONE segment until $10K MRR (per README); resist agent suggestions to "differentiate" early.
- Encode the chosen target as a constitution-level decision in `.aidocs/` so downstream specs/marketing/pricing inherit it.

## AI-agent gotchas
- Hallucinated segments: agents invent plausible personas with no evidence. Mitigation: require row-citations (CRM ID, transcript filename) for every claim; reject segments with zero citations.
- Score inflation: LLMs default to 3–4 across all criteria. Mitigation: force rank-ordering before scoring, or require evidence-or-"unknown" per criterion.
- Dimension drift: agents pick "innovative" dimensions like "growth mindset" that can't be measured. Mitigation: constrain dimensions to a whitelist tied to data sources you actually have.
- Recency bias from interview windows: if all transcripts are from one quarter, segments will overfit. Mitigation: stratify input data over ≥2 quarters before clustering.
- Confusing personas with segments: the agent produces one fictional person instead of a sized cluster. Mitigation: require `n=` and `% of base` on every segment.
- Locking in too early: agents will run scoring even on weak data. Human-in-the-loop checkpoints: (1) approve dimensions, (2) approve candidate segments, (3) approve scoring inputs.
- Ignoring negative segments (who NOT to serve): explicitly prompt for the anti-segment; otherwise agents skip it.
- B2B vs B2C confusion: same prompt yields very different outputs — set `audience_type` upfront.

## References
- Philip Kotler, *Marketing Management*, segmentation chapters (STP framework).
- Christensen, Cook, Hall — "Marketing Malpractice: The Cause and the Cure" (HBR, 2005) — Jobs-to-be-Done as a segmentation lens.
- Mark Ritson — "How brands grow: segmentation by behavior, not demographics" (Marketing Week columns).
- Bob Moesta, *Demand-Side Sales 101* — switch interviews feeding segmentation.
- April Dunford, *Obviously Awesome* — choosing one segment for positioning.
- PostHog docs — Cohorts: https://posthog.com/docs/data/cohorts
- Mixpanel — Behavioral cohorts: https://docs.mixpanel.com/docs/users/cohorts
- Segment Personas — Computed Traits: https://segment.com/docs/personas/
- scikit-learn KMeans + silhouette: https://scikit-learn.org/stable/modules/clustering.html
- Sibling methodologies in this skill: `niche-evaluation`, `market-research-tam-sam-som`, `persona-building`, `mvp-scoping`, `gtm-strategy`.
