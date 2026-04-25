# Agent Integration — Survey Design

## When to use
- Quantify a hypothesis already shaped by 10+ qualitative interviews (Mom Test or otherwise).
- Measure satisfaction (CSAT, NPS, CES), feature priority (MaxDiff, Kano), or pricing (Van Westendorp, Gabor-Granger) over a defined population.
- Track a metric over time (quarterly NPS, post-release CSAT) where comparability across waves matters more than depth.
- Screen a panel before booking interviews — short qualifier surveys to reach the right segment.

## When NOT to use
- Discovery of unknown problems — interviews and analytics outperform surveys here.
- N below ~30 in any segment you intend to report on (CIs explode; agent-summarized "findings" become noise).
- Predicting future behavior ("would you pay $X?") — past behavior questions only.
- When the audience cannot self-report accurately (children, expert tasks, sensitive topics without anonymity).

## Where it fails / limitations
- LLM-generated questions skew leading or double-barreled by default (the model wants to be helpful, helpfulness reads as bias).
- Free-text responses look themable to an agent even when they are not — small-N noise read as signal.
- Likert/NPS analysis with N<100 produces unstable scores; agents will report "5% NPS drop" that is inside the CI.
- Translation/localization changes scale interpretation (e.g. East-Asian respondents underuse extreme scale ends — Western agents miss this).
- Distribution channel bias compounds silently: one Slack post → response set looks "engaged users" not "users".

## Agentic workflow
Drive survey design as a four-stage chain: (1) objective + decision framing, (2) instrument drafting, (3) bias review pass, (4) analysis-plan-before-distribution. Always run a separate critic agent over the question list — the drafting agent will not catch its own leading wording. Keep humans in the loop for translation, screener gates, and any incentive/compensation structure. After fielding, agents are good at descriptive stats and theme coding open-ends; they are bad at causal claims and significance testing without explicit stats tools.

### Recommended subagents
- `faion-market-researcher-agent` — primary author for the instrument; best at JTBD-aligned phrasing.
- `faion-ux-researcher-agent` — secondary for usability of the survey itself (length, mobile UX, drop-off prediction).
- `faion-ba-modeling-agent` — quantitative analysis pass (cross-tabs, segmentation, Van Westendorp curve fitting).
- A fresh-context critic instance (same model, no priors) — bias/leading-question review of the drafted instrument.

### Prompt pattern
```
Role: survey methodologist.
Objective: <single decision the survey will inform>.
Audience: <segment + size>.
Constraints: <=7 min, ≤12 questions, mobile-first, neutral wording.
Forbidden: hypotheticals, double-barreled, leading, "would you", absolute time bins.
Deliver: screener (1-2 Q) → easy openers (2) → core (5-8) → demographics (3) → 1 open-end. JSON.
```

```
Role: bias auditor. Input: survey JSON.
For each question, flag: leading, double-barreled, hypothetical, vague scale, missing "prefer not to say", reverse-coded inconsistency. Return list of {qid, issue, suggested_rewrite}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `surveyjs-cli` | Convert JSON spec → renderable survey JSON for SurveyJS / form runtimes | `npm i -g survey-creator-cli` |
| `pandas` + `pingouin` | Cross-tabs, chi-square, ANOVA, effect sizes from CSV exports | `pip install pandas pingouin` |
| `bertopic` / `top2vec` | Theme-cluster open-ended responses at scale | `pip install bertopic` |
| `qsf-tools` | Parse/diff Qualtrics .qsf survey definitions for version control | github.com/erikriverson/qsf-tools |
| `r-cmdr` (`psych` pkg) | Cronbach alpha, factor analysis, scale reliability | `install.packages("psych")` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qualtrics | SaaS | Yes — REST API + Python SDK | Enterprise; full panel + advanced logic |
| Typeform | SaaS | Yes — REST API, webhooks | Best UX, weak for matrix questions |
| SurveyMonkey | SaaS | Yes — REST API | OK API, branching reasonable |
| Tally | SaaS (free tier) | Partial — webhook only | Cheap; no programmatic creation |
| Formbricks | OSS, self-host | Yes — REST + JS SDK | Open-source alternative; in-product surveys |
| LimeSurvey | OSS, self-host | Yes — RemoteControl 2 JSON-RPC API | Heavy but full-featured |
| Pollfish / Prolific | SaaS panel | Yes — REST API | Paid panels; agents can spec audience |
| Google Forms | SaaS (free) | Limited — Apps Script | OK for internal; no real logic |
| MaxDiff via Sawtooth/Conjointly | SaaS | Yes — API on Conjointly | Required for proper MaxDiff; Sawtooth is desktop-bound |

## Templates & scripts
See `templates.md` for survey design document and question banks (pricing, satisfaction, feature prioritization). Inline helper for Van Westendorp price-sensitivity analysis from a CSV export:

```python
# vw_pricing.py — usage: python vw_pricing.py responses.csv
# expects columns: too_cheap, cheap, expensive, too_expensive
import sys, pandas as pd
import numpy as np
df = pd.read_csv(sys.argv[1])
prices = np.linspace(df[["too_cheap","cheap","expensive","too_expensive"]].min().min(),
                     df[["too_cheap","cheap","expensive","too_expensive"]].max().max(), 200)
def cum(col, ascending): 
    s = df[col].dropna().sort_values(ascending=ascending).reset_index(drop=True)
    return [(s <= p).mean() if ascending else (s >= p).mean() for p in prices]
tc = cum("too_cheap", False); ch = cum("cheap", False)
ex = cum("expensive", True); te = cum("too_expensive", True)
def cross(a, b): 
    diff = np.array(a) - np.array(b); i = np.argmin(np.abs(diff)); return prices[i]
print(f"Point of Marginal Cheapness (PMC): {cross(tc, ex):.2f}")
print(f"Point of Marginal Expensiveness (PME): {cross(ch, te):.2f}")
print(f"Optimal Price Point (OPP): {cross(tc, te):.2f}")
print(f"Indifference Price Point (IPP): {cross(ch, ex):.2f}")
```

## Best practices
- Decide the analysis plan and segment cuts BEFORE fielding — surveys without a pre-registered analysis become fishing expeditions.
- Always include "Prefer not to say" / "Don't know" — forcing a choice corrupts data more than missing it.
- Pilot with 5-10 humans, time them, then cut 25% of questions you thought were essential.
- Randomize answer order on multi-choice (eliminates primacy/recency) but keep ordinal scales fixed.
- For MaxDiff, use a tool that runs proper experimental design (balanced incomplete block) — agent-generated MaxDiff is almost always unbalanced.
- Embed an attention check ("select 'agree' for this row") in any survey >5 minutes; reject responders who fail.
- Report margin of error explicitly per segment, not just overall N.

## AI-agent gotchas
- Agents propose Likert 5 by default; use 7-point for attitudes when you need nuance, binary for behavioral self-report.
- Agents skip translation review — re-prompt explicitly per locale; never assume the bias auditor caught localization issues.
- When summarizing results, agents pattern-match top-line themes from open-ends and drop disconfirming responses; require quote-with-respondent-id grounding for every claim.
- Agents generate plausible "insights" from N=20 segments. Hard rule: any segment with N<30 gets descriptives only, no recommendations.
- For NPS, agents commonly report "score went up 3 points" without acknowledging the ±5-7 band — gate any NPS reporting through a stats checker tool, not LLM-only.
- Human-in-loop checkpoints: question list approval, screener logic, incentive amount, audience targeting in panels (cost overruns), and final results summary before sharing externally.

## References
- Dillman et al., *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method* (Wiley, 4th ed.)
- Fowler, *Survey Research Methods* (SAGE)
- Sawtooth Software whitepapers on MaxDiff and CBC: https://sawtoothsoftware.com/resources
- Van Westendorp Price Sensitivity Meter — https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter
- NN/g, *Surveys: 5 Common Mistakes* — https://www.nngroup.com/articles/survey-mistakes/
- Pew Research methodology hub — https://www.pewresearch.org/methods/
