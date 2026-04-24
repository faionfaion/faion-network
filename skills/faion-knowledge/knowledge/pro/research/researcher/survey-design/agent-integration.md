# Agent Integration — Survey Design

How to drive the survey-design methodology with Claude subagents and external survey tooling. Pairs with `README.md` (methodology), `templates.md`, `examples.md`.

## When to use

- Quantifying patterns already surfaced in 10+ qualitative interviews (use Continuous Discovery first).
- Pricing sensitivity studies (Van Westendorp, Gabor-Granger) where N >= 100 is realistic.
- Feature prioritization on an installed user base (MaxDiff, Kano, importance/satisfaction matrix).
- Periodic NPS/CSAT tracking against a stable cohort, automated by an agent on a cron.
- Screener-driven recruitment funnels for follow-up interviews.

## When NOT to use

- Discovery of unknown problems: interviews and observation reveal what surveys cannot ask about.
- Sample sizes below ~30: stick to interviews; quant claims are not defensible.
- Predicting future behavior ("would you pay X?"): use price-anchored conjoint or pre-orders, not stated intent.
- B2B segments where access to the named buyer is gated: 1:1 outreach beats panel surveys.
- Internal stakeholder "alignment" (use a workshop, not a survey).

## Where it fails / limitations

- Stated-preference bias: respondents over-report willingness to pay and adoption intent by 2-5x.
- Self-selection on social/email channels distorts demographics and attitudes (the angry and the loyal answer; the indifferent do not).
- Question ordering effects: a satisfaction grid before NPS shifts NPS by 5-15 points.
- LLM-generated questions drift toward double-barrel ("How easy and intuitive...") and leading framings unless explicitly checked.
- Open-ended fields in agent-driven analyses are often skimmed; nuance is lost without theme-coding.
- Panel fraud: paid panels return 5-30% bot/satisficer responses; attention checks are mandatory.

## Agentic workflow

Drive survey design as a four-stage pipeline executed by `faion-research-agent`. Stage 1 (objective + audience) is opus — it turns a vague decision into a researchable question. Stage 2 (drafting) is sonnet — generate 1.5x more questions than needed, then prune. Stage 3 (bias review) is sonnet but run as an adversarial second pass with a fresh context window so it does not anchor on its own draft. Stage 4 (analysis) is opus on the cleaned dataset; haiku is acceptable only for tabulation and quote extraction.

### Recommended subagents

- `faion-research-agent (mode: validate)` — orchestrates objective definition and drafts the survey design doc per `templates.md`.
- `faion-research-agent (mode: pricing)` — owns Van Westendorp / Gabor-Granger blocks; cross-checks scale anchoring.
- `faion-research-agent (mode: personas)` — feeds segmentation logic so demographics map to existing user-personas.md.
- `faion-domain-checker-agent` — irrelevant here; do not invoke.
- Generic `general-purpose` reviewer agent (sonnet, fresh context) — second-pass bias and double-barrel detector.

### Prompt pattern

Drafting:
```
You are designing a survey per skills/faion-knowledge/knowledge/pro/research/researcher/survey-design/README.md.
Objective: <1 sentence>. Decision it informs: <1 sentence>. Audience: <segment>. Target N: <number>.
Output the full survey using the "Survey Design Document" template. Cap length at 7 minutes (use README length table). Include screener, attention check at Q5, demographics last, one open-ended at end. Return only the markdown document.
```

Bias review (fresh context, do not show the draft's rationale):
```
Audit this survey for: leading wording, double-barreled items, hypotheticals presented as fact, missing screener, scale-anchor mismatch, order effects, missing attention check. For each issue: quote the offending line, name the defect, propose a one-line fix. Refuse to comment on anything else.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `surveyjs-cli` | Local validation/preview of SurveyJS JSON schemas | `npm i -g survey-creator-cli` · surveyjs.io |
| `formbricks` CLI | Self-host OSS surveys, programmatic survey CRUD | `npx formbricks@latest` · formbricks.com/docs |
| `limesurvey-cli` (RemoteControl 2 over JSON-RPC) | Drive LimeSurvey via API from agents | manual.limesurvey.org/RemoteControl_2_API |
| `qualtrics-mcp` / Qualtrics API v3 | Create/distribute/export surveys | api.qualtrics.com |
| `typeform` API + `@typeform/api-client` | Create forms, fetch responses as JSON | developer.typeform.com |
| `pollster` (R) / `pyreadstat` + `pandas` | Weighted analysis, SPSS/Stata import | CRAN; pypi.org/project/pyreadstat |
| `numpy` + `scipy.stats` | Significance tests, confidence intervals | pypi |
| `lime` (CLI) | Run MaxDiff designs locally | github.com/sawtoothsoftware (Lighthouse) |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qualtrics | SaaS | Yes (REST v3 + webhook on response) | Industry default for academic/enterprise; expensive. |
| SurveyMonkey / Momentive | SaaS | Yes (REST API, OAuth) | Mature panels (SurveyMonkey Audience). |
| Typeform | SaaS | Yes (REST + webhooks) | Good for short consumer surveys; weak for matrix items. |
| Google Forms | SaaS | Partial (Apps Script only) | Free, but no proper screener routing or quotas. |
| Tally | SaaS | Yes (webhook + REST) | Free tier, decent logic; favored for solo founders. |
| Formbricks | OSS / SaaS | Yes (REST + webhook + SDK) | Self-host; in-product micro-surveys. |
| LimeSurvey | OSS | Yes (RemoteControl 2 JSON-RPC) | Most flexible OSS; complex to operate. |
| SurveyJS | OSS lib + SaaS service | Yes (JSON schema, embeddable) | Best when survey is an artifact in your repo. |
| Prolific | SaaS panel | Yes (REST API) | Academic-grade respondents; clean quality. |
| Pollfish | SaaS panel | Yes (REST API) | Mobile, fast, lower quality controls. |
| CloudResearch Connect | SaaS panel | Yes (REST API) | Successor to vetted MTurk pools. |
| Maze | SaaS | Yes (REST) | Mixes surveys + usability; agent can publish runs. |
| Sprig | SaaS | Yes (SDK + REST) | In-product surveys with AI summarization. |

Agent-friendliness rule: prefer services with a documented REST API plus response webhook. Polling export endpoints wastes tokens.

## Templates & scripts

See `templates.md` for the survey-design document template and per-research-type question banks (already in `README.md`).

Inline helper — bias linter for an agent's draft (run before sending to the bias-review pass):

```python
# bias_linter.py — quick deterministic checks before LLM review
import re, sys, json

LEADING = re.compile(r"\b(don't you (think|agree)|isn't it|wouldn't you say|how amazing|how awful)\b", re.I)
DOUBLE  = re.compile(r"\b\w+\s+(and|or)\s+\w+\b.*\?")  # crude
HYPO    = re.compile(r"\b(would you|will you|do you plan to|how often will)\b", re.I)
ABS     = re.compile(r"\b(always|never|every time|all of the time)\b", re.I)

def lint(items):
    out = []
    for i, q in enumerate(items, 1):
        text = q.get("text", "")
        flags = []
        if LEADING.search(text): flags.append("leading")
        if HYPO.search(text):    flags.append("hypothetical")
        if ABS.search(text):     flags.append("absolutist-anchor")
        if "?" in text and " and " in text and "satisf" in text.lower():
            flags.append("possible-double-barrel")
        if len(text.split()) > 28: flags.append("too-long")
        if flags:
            out.append({"q": i, "text": text, "flags": flags})
    return out

if __name__ == "__main__":
    data = json.load(sys.stdin)  # [{"text": "..."}]
    json.dump(lint(data), sys.stdout, indent=2)
```

Pipe survey question JSON in → fix flagged items → only then invoke the LLM bias review. Cheap pre-filter, ~10 lines of agent code.

## Best practices

- Anchor sample size to the decision, not vanity. For a directional preference split, n=100/segment with 95% CI gives +/- ~10pp; tighter requires n=400.
- Always add one verifiable attention check ("Select 'Somewhat agree' to confirm you are reading"). Drop respondents who fail; report drop rate.
- Randomize answer-option order on every multi-choice and matrix item (except scales, where order is meaningful).
- Use a dual-coded screener: behavioral ("In the last 30 days, did you...") plus declarative ("What is your role?"). Behavioral wins on conflict.
- For pricing, never ask "would you pay X". Use Van Westendorp + a real price anchor or a pre-order page.
- Segment in the analysis plan before fielding. If a segment is not in the plan, do not slice on it post-hoc without flagging it as exploratory.
- Pilot with 5-10 respondents from the actual audience and time them. Above 7 minutes median → cut.
- For LLM-summarized open-ends, give the model the full corpus, force theme codes with counts, and require verbatim quotes per theme to prevent hallucinated synthesis.
- Version-control the survey JSON (SurveyJS / Formbricks export) alongside the analysis notebook. Surveys are code.

## AI-agent gotchas

- LLMs drift toward Likert-5 for everything; force the agent to justify scale choice per question (binary vs 5 vs 7 vs 10) using the README scale table.
- Models will silently merge concepts ("How easy and useful is..."). Run `bias_linter.py` before any human review; the regex catches what the LLM rationalizes away.
- Agent-generated demographics often duplicate or omit segments tracked in `user-personas.md`. Always pass the personas doc as context; require demographic options to be a strict subset.
- Open-ended analysis: an agent will summarize 1,000 responses without asking how many it actually read. Force `len(responses)` echo + sample-size disclosure in the analysis prompt.
- Panel data has bot infill — never let an agent draw conclusions before deduplication on (IP, device fingerprint, completion time < 30% of median).
- Human-in-the-loop checkpoints (mandatory): (1) sign-off on objective + decision before drafting, (2) human approval after bias-review pass, (3) human review of significance/CI claims before any business decision is published.
- When using paid panels, an agent must not auto-launch fielding — cost spikes and ethics review require a human button.

## References

- Dillman, D. et al. — "Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method" (4th ed.).
- Pew Research Center — "Writing Survey Questions" (pewresearch.org/our-methods/u-s-surveys/writing-survey-questions).
- Sawtooth Software — MaxDiff and CBC technical papers (sawtoothsoftware.com/resources).
- Van Westendorp price-sensitivity meter — original 1976 ESOMAR paper, summarized at conjointly.com/guides/price-sensitivity-meter.
- AAPOR Code of Professional Ethics — aapor.org/standards-ethics/aapor-code-of-ethics.
- SurveyJS docs — surveyjs.io/documentation.
- Formbricks docs — formbricks.com/docs.
- Internal: `skills/faion-knowledge/knowledge/pro/research/researcher/agent-invocation/README.md` (mode dispatch).
- Internal: `skills/faion-knowledge/knowledge/pro/ux/user-researcher/survey-design/README.md` (UX-side counterpart).
