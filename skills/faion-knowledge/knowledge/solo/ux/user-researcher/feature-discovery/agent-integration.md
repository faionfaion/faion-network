# Agent Integration — Feature Discovery

## When to use
- Quarterly roadmap planning when the backlog is full but priorities are unclear
- Post-launch analysis: identifying which features to build next based on usage data and support tickets
- Competitive gap analysis: discovering features that rivals have but your product lacks (and vice versa)
- Before running a user survey: generate a candidate feature list to score via Opportunity Scoring or Kano
- Synthesizing a large feature request log (50+ items) into actionable clusters

## When NOT to use
- When the core product is not yet working — feature discovery before product-market fit is premature optimization
- Replacing direct customer conversations: analytics and ticket logs supplement but do not replace qualitative insight
- When only one vocal customer is requesting a feature — frequency matters; one loud voice is not signal
- When the team has already committed to a roadmap for the current quarter — discovery is for next cycle

## Where it fails / limitations
- Agents cannot query your analytics platform directly without tool integration (Amplitude, Mixpanel, etc.)
- RICE scoring and Kano categorization are heuristic; numbers suggest precision that does not exist
- Feature requests often describe symptoms, not jobs; an agent will synthesize what customers said, not what they need
- Opportunity score math (importance + importance - satisfaction) produces misleading results for poorly-worded surveys
- Agents have no way to assess implementation effort without engineering input — effort estimates must come from humans

## Agentic workflow
A well-structured feature discovery pipeline uses three agent passes: (1) collection — agent processes raw input (support tickets, interview notes, review exports) and produces a candidate feature list; (2) categorization — agent classifies each feature by Kano type and drafts opportunity scores from stated importance/satisfaction pairs; (3) prioritization — agent computes RICE scores using human-provided effort and reach estimates. The human's role is to supply data, validate categorization, and make the final prioritization call.

### Recommended subagents
- `faion-sdd-executor-agent` — run discovery tasks within an SDD feature plan
- Any general Claude subagent — process support ticket exports, generate candidate feature list, compute RICE scores

### Prompt pattern
```
You are a product analyst. Given the following support tickets and feature requests, extract:
1. A deduplicated feature candidate list (name + problem it solves)
2. Kano category for each (Must-have / Performance / Delight / Indifferent)
3. Frequency count across tickets

Input: <paste ticket export>
```

```
Given the following feature list with Importance (1-10) and Satisfaction (1-10) scores from a survey,
compute Opportunity Score = Importance + max(Importance - Satisfaction, 0).
Sort descending. Flag any score > 10 as high priority.
Data: <paste table>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Amplitude CLI (API) | Query feature usage and drop-off data | developers.amplitude.com |
| Mixpanel API | Feature adoption funnel data | developer.mixpanel.com |
| Canny CLI (API) | Feature request management | developers.canny.io |
| ProductBoard API | Structured feature backlog + scoring | developer.productboard.com |
| Linear API | Engineering effort estimation integration | linear.app/developers |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Canny | SaaS | Yes (REST API) | Read feature requests, votes, comments; create posts |
| ProductBoard | SaaS | Yes (REST API) | Manage feature backlog; score features; push to roadmap |
| Amplitude | SaaS | Yes (API) | Query cohort adoption of specific features |
| Mixpanel | SaaS | Yes (API) | Funnel analysis per feature; identify drop-off |
| Linear | SaaS | Yes (GraphQL API) | Link feature candidates to engineering issues |
| Notion | SaaS | Yes (API) | Maintain feature discovery board as database |
| Airtable | SaaS | Yes (REST API) | Feature scoring tables with formula columns |

## Templates & scripts
See `templates.md` for Feature Discovery Board and Feature Request Log templates.

Inline script — RICE scorer:
```python
# rice_scorer.py — compute RICE scores for feature candidates
features = [
    {"name": "Customizable dashboard", "reach": 1000, "impact": 2, "confidence": 0.8, "effort": 3},
    {"name": "CSV export",             "reach": 500,  "impact": 1, "confidence": 1.0, "effort": 1},
    {"name": "AI suggestions",         "reach": 800,  "impact": 3, "confidence": 0.5, "effort": 8},
    {"name": "Dark mode",              "reach": 1200, "impact": 0.5, "confidence": 0.8, "effort": 2},
]

for f in features:
    rice = (f["reach"] * f["impact"] * f["confidence"]) / f["effort"]
    f["rice"] = round(rice, 1)

for f in sorted(features, key=lambda x: -x["rice"]):
    print(f"{f['rice']:7.1f}  {f['name']}")
```

## Best practices
- Collect from at least 4 sources (interviews + support tickets + analytics + competitor reviews) before scoring
- Cap the candidate list at 20 items per discovery cycle — scoring 50+ features creates decision paralysis
- Separate "what customers ask for" from "what job they need done" — request: "export to Excel"; job: "share data with my finance team"
- Validate the top 3 RICE-scored features with a fake door test or prototype before committing to build
- Keep a "not this cycle" list visible to the team — rejected features must have a recorded rationale
- Revisit effort estimates after the first sprint; discovery effort is often 2× the initial engineer estimate

## AI-agent gotchas
- Agent-generated Kano categorization is opinion-based without actual customer survey data; treat it as a starting hypothesis
- LLMs will over-represent features requested in their training data (e.g., dark mode, mobile app) — cross-check against your actual ticket log
- RICE confidence scores must come from humans; an agent cannot assess how solid the evidence base is
- Human checkpoint: engineering lead must validate all effort estimates before RICE scores drive roadmap decisions
- Agents conflate feature requests into overly broad categories; instruct to preserve specific, distinct items ("bulk actions" vs. "batch email send")

## References
- https://www.intercom.com/blog/product-prioritization-framework/ (Intercom RICE framework original post)
- Noriaki Kano, "Attractive Quality and Must-be Quality" (1984) — foundational Kano model paper
- Anthony Ulwick, "Jobs to Be Done: Theory to Practice" — Outcome Driven Innovation + Opportunity Scoring
- https://www.producttalk.org/ — Teresa Torres continuous discovery framework
- Marty Cagan, "Inspired: How to Create Tech Products Customers Love"
