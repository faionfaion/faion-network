# Agent Integration — Surveys and Questionnaires

## When to use
- Quantifying findings from qualitative research at scale (validation surveys after interviews/diaries).
- Tracking standardized UX metrics over time: NPS, CSAT, SUS, SEQ, CES — quarterly cohorts vs baseline.
- Triaging large user bases: which features matter, which segments are unhappy, where to invest research.
- Post-task micro-surveys (1-2 questions) embedded in product after key flows.
- Pre-research segmentation: screener surveys to recruit qualified participants for deeper qualitative work.

## When NOT to use
- "Why" questions — surveys give "what" and "how much", interviews give "why".
- Sample <100 — confidence intervals too wide; do interviews instead.
- Highly emotional or sensitive topics — self-report bias and social desirability skew responses.
- Concept testing where context matters — closed survey questions can't substitute for showing the artifact.
- When you cannot act on results — running a survey you'll ignore burns trust with respondents.

## Where it fails / limitations
- Self-report ≠ behavior. NPS predicts loyalty weakly; SUS scores don't correlate strongly with measured task success.
- Question wording dominates results. Two well-meaning researchers writing the same survey produce statistically different scores.
- Response bias: power users and angry users over-respond; casual users under-respond. Without weighting, signal skews.
- LLM-coded open-ended responses cluster aggressively, hiding nuanced minority views. Always sample-check coding manually.
- Long surveys (>5 min) have steep dropoff; the last questions get fewer, lower-quality answers.
- Standardized metrics (NPS, SUS) require strict question wording and order; "almost-NPS" is not benchmarkable against industry data.

## Agentic workflow
Agents excel at the operational and analytical bookends. Pre-launch: a research agent drafts the survey from objectives, validates against bias heuristics (leading, double-barreled, vague), assembles standardized scales correctly, and runs a pilot-test simulation. Post-launch: an analysis agent computes per-segment statistics, codes open-ended responses with a fixed taxonomy, runs sentiment + theme analysis, generates the report draft. Humans approve the survey before launch and review the analysis before circulating.

### Recommended subagents
- `faion-ux-researcher-agent` — drafts questions, designs scales, performs synthesis.
- `faion-market-researcher` (from `pro/research/market-researcher`) — sampling design, weighting, statistical confidence.
- `faion-product-manager` — translates results into roadmap signals.
- `faion-conversion-optimizer` — designs in-product micro-surveys timed to key moments.
- `faion-data-analyst` style subagent — segmentation cuts, cross-tabs, longitudinal tracking.

### Prompt pattern
Bias check (run on every drafted question):
```
Question: "{q}"
Options: {options}
Score for: leading (does it suggest an answer?), double-barreled (two concepts?), vague (undefined terms?), loaded (emotive language?), missing options (exhaustive + mutually exclusive?). Output JSON with score 0-3 per dimension and rewrite_suggestion if any score >0.
```
Open-ended coding (apply to each response):
```
Response: "{text}"
Taxonomy: {fixed_codes}
Assign 1-3 codes from taxonomy. If response is off-topic, code as OFFTOPIC. If new theme not in taxonomy, code as NEW with proposed_label. Return JSON.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Typeform API | Create surveys + fetch responses programmatically | https://www.typeform.com/developers/ |
| SurveyMonkey API | Same | https://api.surveymonkey.com |
| Qualtrics API | Enterprise survey platform | https://api.qualtrics.com |
| Google Forms + Apps Script | Free DIY surveys with API access | https://developers.google.com/apps-script |
| `pandas` + `scipy.stats` | Cross-tabs, t-tests, chi-square, confidence intervals | `pip install pandas scipy` |
| `pingouin` | Friendly stats library (effect sizes, ANOVA) | `pip install pingouin` |
| `statsmodels` | Regression, weighting, longitudinal models | `pip install statsmodels` |
| `nps-calc` (or any 3-line function) | Standardized NPS computation | inline |
| Anthropic SDK | Open-ended coding + theme synthesis | `pip install anthropic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Typeform | SaaS | Yes — full API | Strong UX, conversational forms |
| SurveyMonkey | SaaS | Yes — API | Largest panel marketplace |
| Qualtrics | SaaS | Yes — full API | Enterprise; advanced logic + weighting |
| Google Forms | SaaS | Partial — Apps Script | Free baseline, limited logic |
| Hotjar Surveys | SaaS | Yes — API | In-product micro-surveys; pairs with session recordings |
| Sprig (formerly UserLeap) | SaaS | Yes — API | In-product event-triggered surveys |
| Refiner | SaaS | Yes — API | SaaS-product NPS/CSAT focused |
| Delighted | SaaS | Yes — API | Lightweight NPS/CES/CSAT specialized |
| Pendo + Pendo Feedback | SaaS | Yes — API | In-product surveys tied to behavior data |
| LimeSurvey | OSS | Yes — REST API | Self-hosted; full control over data residency |
| Formbricks | OSS | Yes — REST API | Open-source Typeform alternative |
| Prolific / Respondent / User Interviews | SaaS | Yes — APIs | Recruitment panels with quality controls |

## Templates & scripts
See `templates.md` for the survey planning and standard-question templates. Minimal NPS + segment cut:

```python
# nps_segments.py
import pandas as pd
df = pd.read_csv("responses.csv")
def nps(scores):
    s = pd.Series(scores).dropna()
    if len(s) < 30: return None
    promoters = (s >= 9).mean()
    detractors = (s <= 6).mean()
    return round((promoters - detractors) * 100, 1)
print("Overall NPS:", nps(df["recommend_0_10"]))
for seg, g in df.groupby("plan"):
    print(f"  {seg} (n={len(g)}): NPS = {nps(g['recommend_0_10'])}")
# Open-ended themes via LLM coding (separate step) joined here
```

## Best practices
- Lock the question wording for any standardized metric (NPS, SUS, SEQ, CES) — change a word and the benchmark comparison is invalid.
- Pilot every survey with 5-10 representative users before launch; agents can simulate this with synthetic respondents but a real pilot catches genuine confusion.
- Keep surveys under 5 minutes / 10-15 questions for general audiences; under 2 minutes for in-product micro-surveys.
- Demographics at the END, not the start. Start with low-effort, high-relevance questions to build investment.
- Always include at least one open-ended question — the gold for product insight comes from open-text comments, not Likert means.
- Report confidence intervals, not just point estimates. "NPS = 42 ± 6" tells stakeholders far more than "NPS = 42".
- Segment before interpreting — overall scores hide divergent experiences (new vs experienced, plan tier, geo).
- Run the same survey periodically (quarterly) so you can track movement, not just absolute level.

## AI-agent gotchas
- LLM-drafted questions over-use jargon and double-barreled phrasing. The bias-check pass is mandatory; expect to rewrite ~30% of LLM-generated questions.
- LLM coding of open-ended responses converges on majority themes and silences outliers. Always look at the OFFTOPIC/NEW buckets manually — that's where surprises live.
- Sentiment classification on short product feedback ("works fine") is unreliable; require the LLM to extract specific praise/issue rather than a polarity score.
- Fake-respondent / bot fraud is common on cheap general panels; require attention checks and validate response patterns (straightlining, suspicious speed).
- Prompt caching: when coding thousands of open-ended responses, cache the taxonomy + few-shot examples as a system prompt; cuts cost ~80%.
- Don't let an agent autonomously translate standardized scales to other languages — translated SUS/NPS need formal cross-cultural validation, not LLM translation.
- Cross-tabs over many segments inflate false positives (multiple-comparisons problem). Apply a Bonferroni or FDR correction before reporting any "significant" segment difference.
- Privacy: survey responses often contain PII in free text. Redact before sending to a third-party LLM, or run coding on a local model for sensitive populations.

## References
- Sauro, Jeff & Lewis, James — *Quantifying the User Experience* (definitive UX-stats reference)
- Tullis, Tom & Albert, Bill — *Measuring the User Experience*
- Oppenheim, A.N. — *Questionnaire Design, Interviewing and Attitude Measurement*
- Nielsen Norman Group — Qualitative Surveys: https://www.nngroup.com/articles/qualitative-surveys/
- MeasuringU — UX metrics & NPS guidance: https://measuringu.com/
- SUS reference — System Usability Scale: https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html
- Anthropic — Prompt caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
