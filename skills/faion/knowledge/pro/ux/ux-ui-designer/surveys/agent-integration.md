# Agent Integration — Surveys and Questionnaires

## When to use
- You need quantitative validation of qualitative findings (interviews, diary studies) at N>=100.
- Tracking standard UX metrics over time: NPS, SUS, CSAT, SEQ.
- Segmenting users (new vs power, free vs paid) and measuring satisfaction or feature value across segments.
- Pre/post launch comparison of perceived ease, trust, or specific feature impact.

## When NOT to use
- You don't yet know which questions to ask — run interviews first; a survey of ill-formed questions is worse than no data.
- Sample <30 — descriptive stats are noisy and infer nothing useful; do qualitative with that audience.
- You need behavioral data (clicks, time on task) — analytics or usability tests are correct, not self-reported surveys.
- High-stakes decisions where social-desirability bias dominates (e.g. "would you pay for X?" — surveys overstate willingness 2-4x).

## Where it fails / limitations
- Self-report bias: stated preferences differ from revealed behavior; survey results need triangulation.
- Survey fatigue: long surveys collapse response rate and inflate straight-lining (same answer all the way down).
- Sampling bias: who answers is rarely who you mean. Voluntary samples skew engaged + dissatisfied.
- Open-ended fields produce lots of text but little actionable signal unless coded properly — coding is expensive.
- Translation pitfalls: SUS in particular is sensitive to wording; a sloppy localization invalidates benchmarks.

## Agentic workflow
Agents are most useful in three places: question drafting from research goals (with bias linting), pilot review, and open-ended response coding. Keep humans in the loop at instrument approval and at thematic-coding sign-off — LLM coding looks confident but invents themes when noise is high.

### Recommended subagents
- `survey-question-drafter` — converts objectives into question candidates with type and bias notes.
- `survey-bias-linter` — flags double-barreled, leading, vague, and double-negative items.
- `open-ended-coder` — proposes themes, codes responses, flags low-confidence items for human review.
- `nps-sus-calculator` — computes standard metrics from raw CSV; deterministic, run as code not LLM.

### Prompt pattern
```
For each survey question, return JSON: {question, type, options?, bias_flags[]}.
Bias flags: leading, double-barreled, double-negative, vague, jargon, loaded.
If any flag fires, also return a rewritten neutral version. Do not invent options;
respect the provided answer scale (Likert-5, NPS-0-10, binary).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandas` | Tabulate CSV exports, compute NPS/CSAT | `pip install pandas` |
| `pingouin` / `scipy.stats` | Significance tests across segments | `pip install pingouin` |
| `bertopic` | Topic modeling on open-ended responses | `pip install bertopic` |
| `litellm` | Batch open-ended coding via LLM | `pip install litellm` |
| `qualtrics-api-py` | Pull responses from Qualtrics | `pip install qualtrics-api` |
| `gh` + Google Forms scripts | Pull responses from Google Forms via Apps Script | https://developers.google.com/apps-script |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qualtrics | SaaS | Yes (REST API) | Enterprise standard, full programmatic control. |
| SurveyMonkey | SaaS | Yes (API) | Mature, decent API limits. |
| Typeform | SaaS | Yes (API + webhooks) | Strong UX, good API for results. |
| Tally | SaaS | Yes (API) | Cheaper, simpler, GDPR-friendly EU host. |
| Google Forms | SaaS (free) | Limited | OK for one-off; weak segmentation. |
| LimeSurvey | OSS | Yes (REST API) | Self-host for sensitive data. |
| Formbricks | OSS | Yes (REST API) | Open-source product-survey platform with in-app triggers. |

## Templates & scripts
Inline NPS + SUS calculator (≤45 lines).

```python
# survey_metrics.py
import pandas as pd, sys

def nps(series: pd.Series) -> float:
    s = series.dropna().astype(int)
    promoters = (s >= 9).mean() * 100
    detractors = (s <= 6).mean() * 100
    return round(promoters - detractors, 1)

# SUS: 10 items, alternating positive/negative, scale 1-5
SUS_POS = [0, 2, 4, 6, 8]   # 0-indexed
SUS_NEG = [1, 3, 5, 7, 9]
def sus(row: list[int]) -> float:
    pos = sum(row[i] - 1 for i in SUS_POS)
    neg = sum(5 - row[i] for i in SUS_NEG)
    return (pos + neg) * 2.5

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    if "nps" in df: print("NPS:", nps(df["nps"]))
    sus_cols = [c for c in df.columns if c.startswith("sus_")]
    if len(sus_cols) == 10:
        df["sus_score"] = df[sus_cols].apply(lambda r: sus(list(r)), axis=1)
        print("SUS mean:", round(df["sus_score"].mean(), 1))
```

## Best practices
- Pilot with N=10 minimum and time the median respondent — kill any survey >5 minutes.
- Randomize answer-order on attitudinal items and Likert blocks to neutralize order/anchoring bias.
- Always pair an attitudinal item ("how easy?") with a behavioral observation when possible — discrepancies are insight goldmines.
- Use validated instruments (SUS, UEQ, NPS, CSAT) verbatim; do not "improve" wording or you lose benchmark comparability.
- Track and report response and completion rates explicitly — silent dropoffs change interpretation.

## AI-agent gotchas
- LLMs invent plausible answer scales (e.g. 7-point when you specified 5). Constrain and validate.
- Open-ended coding with LLMs hallucinates themes when responses are short ("ok", "no", emoji); enforce minimum word count before LLM coding.
- Models conflate NPS with CSAT/SUS calculations. Implement metrics in deterministic code, not LLM completions.
- Bias linters miss culturally specific loaded language; native-speaker review still required for non-English surveys.
- Human checkpoint: instrument review by a researcher before launch + theme-coding spot check on at least 10% of LLM-coded responses.

## References
- Sauro & Lewis, "Quantifying the User Experience" (definitive UX survey statistics reference).
- NN/g, "Survey design 101": https://www.nngroup.com/articles/qualitative-surveys/
- Brooke, "SUS: A quick and dirty usability scale": original 1996 paper.
- Reichheld, "The One Number You Need to Grow" (NPS origin).
- MeasuringU benchmarks: https://measuringu.com/sus/
