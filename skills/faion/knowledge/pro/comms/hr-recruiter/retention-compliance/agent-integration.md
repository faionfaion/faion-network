# Agent Integration — Retention & Compliance

How to drive the retention + compliance bundle (employee retention, stay interviews, exit analysis, talent reviews / 9-box, hiring compliance, DEI hiring, recruitment process audit) with Claude subagents and HRIS / analytics tooling. Pairs with `README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Sustained voluntary attrition above the role-family benchmark (>15% knowledge work, >25% sales, >40% support) for two consecutive quarters.
- Pre-emptive stay interviews on top performers and flight-risk segments (post-acquisition, post-restructure, post-comp-cycle).
- Annual or bi-annual talent reviews with succession planning needs.
- Compliance audits before / after a regulatory event (NYC AEDT, EU AI Act enforcement, EEOC charge, GDPR audit).
- DEI hiring reviews when the funnel produces homogeneous slates and a slate-diversity intervention is being designed.
- Process audits when KPIs (time-to-fill, cost-per-hire, candidate NPS) drift without a clear cause.

## When NOT to use

- Companies under ~25 people where stay-interview / talent-review formality outweighs benefit; informal manager 1:1s suffice.
- Crisis layoff cycles — running stay interviews during a RIF is dishonest and worsens trust.
- Single-country, single-jurisdiction startups doing ad-hoc hiring — heavy compliance frameworks add overhead without proportional risk reduction.
- DEI-as-PR exercises without leadership commitment to act on findings; data collection without action erodes trust.

## Where it fails / limitations

- Stay-interview answers are systematically optimistic in low-trust environments; turnover follows even after "all green" interviews.
- Exit-interview themes coded by an agent under-weight low-volume but high-impact departures (a single high-performer leaving with concrete reasons matters more than 10 average departures).
- 9-box grids encode current-bias: "potential" is highly subjective and inherits managerial halo effects.
- Compliance checklists are jurisdiction-specific (US/EU/UK/Canada/India differ on protected classes, retention periods, consent rules); generic LLM advice is unreliable.
- DEI hiring interventions can backfire if framed as quotas; agents drafting outreach risk producing tokenizing language.
- Recruitment-process audits surface symptoms (stage drop-off) but not root-cause organizational dysfunction (bad management, broken comp).
- Disparate-impact analysis requires demographic data that may legally not be collectible in a given jurisdiction; agents must not infer demographics.

## Agentic workflow

Drive retention + compliance as a five-track program owned by `faion-recruiter-agent` plus `faion-people-analytics-agent` (specialization). Track A — stay interviews: opus designs the question set + frequency per segment; humans run the conversations; sonnet codes themes from notes. Track B — exit analysis: sonnet codes exit interviews into a controlled vocabulary; opus does quarterly trend synthesis with statistical thresholds. Track C — talent review: sonnet drafts 9-box pre-reads from performance + manager input; opus produces succession-gap analysis; the rating itself is human, calibrated in a session. Track D — compliance audit: sonnet checklists against jurisdictional rules (with explicit jurisdiction parameter); opus interprets findings; legal sign-off mandatory before any action. Track E — DEI hiring audit: sonnet computes disparate-impact ratios on legitimately-collected demographic data; opus produces intervention designs; bias review by `general-purpose` reviewer with fresh context.

### Recommended subagents

- `faion-recruiter-agent` — primary; owns retention + compliance + audit work.
- `faion-research-agent (mode: market)` — comp-benchmarking when retention data points to comp.
- `general-purpose` reviewer (sonnet, fresh context) — adversarial pass on DEI language, compliance interpretations, exit-interview theme coding.
- `faion-employer-brand-agent` — drafts retention-program comms.
- Legal counsel (human) — non-optional reviewer for any compliance or DEI intervention.

### Prompt pattern

Stay-interview design (segment-aware):
```
Design a stay-interview question set per skills/faion/knowledge/pro/comms/hr-recruiter/retention-compliance/README.md.
Segment: <e.g. senior engineers, tenure 18-36 months, post comp-cycle>. Known concerns from last pulse: <pasted>. Cadence: quarterly.
Output 8-10 questions max, mixing: engagement drivers, risk factors, growth, recognition, manager support. Each question must elicit a behavior or fact, not an opinion. Forbidden: "Are you happy?", "How is everything?". Provide a follow-up probe per question.
```

Exit-interview thematic coding:
```
Given N exit-interview transcripts (attached) and the controlled vocabulary (attached), code each transcript with: primary reason, secondary reason(s), departure pattern (push / pull / personal), retention-recoverable (Y/N with evidence), key quote (verbatim, single sentence). Do not invent codes; use only the supplied vocabulary. If a transcript does not fit, mark "uncoded" with explanation. No aggregate statistics yet.
```

Disparate-impact computation:
```
Inputs: stage-by-stage candidate data with demographic flags collected per <jurisdiction> rules (attached). Compute four-fifths-rule pass ratios per protected class per stage. Flag stages where any class is below 80% of the highest-class rate. Output: pass-rate table + flagged stages + minimum sample size needed for significance. Do not interpret; do not recommend; do not infer demographics from names.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandas` + `scipy.stats` | Disparate-impact, four-fifths rule, kappa for rater agreement | pypi |
| BambooHR / Rippling / HiBob / Workday API | HRIS pulls for tenure, comp, manager chain | each provider |
| Lattice / 15Five / Culture Amp API | Engagement / pulse / stay-interview data | each provider |
| Greenhouse / Lever / Ashby API | Hiring funnel demographics for DEI audits | each provider |
| `dbt` + `duckdb` | Cohort retention warehousing | getdbt.com, duckdb.org |
| `pyreadstat` | Survey data import (SPSS/Stata/SAS) for legacy datasets | pypi |
| `gh` + GitHub Pages | Audit report version control | cli.github.com |
| `op` (1Password CLI) | Pull HRIS API tokens without committing secrets | developer.1password.com/docs/cli |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BambooHR / Rippling / HiBob | SaaS HRIS | Yes (REST) | Tenure, comp, manager hierarchy. |
| Workday / SAP SuccessFactors | SaaS HRIS (enterprise) | Partial | Heavy auth + audit logging. |
| Lattice / 15Five / Culture Amp / Peakon | SaaS engagement | Yes (REST) | Engagement + stay-interview workflows. |
| Glint (LinkedIn) | SaaS engagement | Limited | Strong analytics, weak API. |
| Visier / One Model | SaaS people analytics | Yes (REST) | Cohort retention, predictive turnover. |
| ChartHop / Pave | SaaS comp + people | Yes (REST) | Comp equity audits, banding. |
| Pyn | SaaS lifecycle nudges | Yes (REST) | Manager-as-coach automation. |
| Workhuman / Bonusly | SaaS recognition | Yes (REST) | Recognition data feeds retention models. |
| Eightfold / Findem / SeekOut | SaaS sourcing AI | Partial | Bias audits required (disparate impact). |
| HireRight / Checkr | SaaS background | Yes (REST) | Compliance-heavy; consent flow stays human. |
| OneTrust / TrustArc | SaaS privacy/GDPR | Yes (REST) | Data inventory + DSAR automation. |
| Holistic AI / Arthur / Fiddler | SaaS AI audits | Yes (REST) | Algorithmic bias monitoring (NYC AEDT, EU AI Act). |

## Templates & scripts

See `templates.md` for: stay-interview script, exit-interview script, 9-box, hiring compliance checklist, DEI dashboard. The README's 9-box grid and questions are starter material.

Inline helper — four-fifths rule disparate-impact check (deterministic gate before LLM interpretation):

```python
# four_fifths.py — flag stages failing 80% rule
import sys, json

def four_fifths(stage):
    # stage = {class_label: {"applied": int, "passed": int}}
    rates = {c: (v["passed"] / v["applied"]) if v["applied"] else 0
             for c, v in stage.items()}
    if not rates: return {"flag": False, "rates": {}}
    top = max(rates.values())
    if top == 0: return {"flag": False, "rates": rates}
    ratios = {c: round(r / top, 3) for c, r in rates.items()}
    failing = [c for c, r in ratios.items() if r < 0.8]
    return {"top_rate": round(top, 3), "rates": rates, "ratios": ratios,
            "failing_classes": failing, "flag": bool(failing)}

if __name__ == "__main__":
    data = json.load(sys.stdin)  # {stage_name: {class: {applied, passed}}}
    out = {s: four_fifths(d) for s, d in data.items()}
    json.dump(out, sys.stdout, indent=2)
```

Pipe stage-level demographic data in. Flagged stages route to legal + DEI lead before any LLM interpretation. Always verify min sample (>= 30 per group) before treating ratios as meaningful.

## Best practices

- Stay interviews are about action, not measurement. If you have no intent or budget to act on findings, do not run them.
- Run exit interviews via a neutral party (HR Ops, not the manager). Departing employees mute candor with their direct chain.
- Code exit data with a tight controlled vocabulary (15-25 codes max). Free-text aggregation is unreliable, even with LLMs.
- 9-box ratings calibrate in a live cross-functional session; pre-reads are pre-reads, not the rating.
- Compliance: maintain a jurisdictional matrix (US-state, EU-country, UK, Canada-province) covering: protected classes, retention periods, consent for screening, AEDT/AI-Act requirements. Refresh annually with counsel.
- DEI: focus on systemic interventions (slate diversity, structured interviews, blind resume review, comp equity audits) not individual decisions.
- Run a disparate-impact audit on every new screening tool *before* turning it on, then quarterly.
- Always preserve the demographic data and the model decision together for audit; AEDT requires bias-audit publication for many tools.
- Track retention by cohort (start year + role family) not company-wide; mask hides everything.
- Avoid "engagement" vanity metrics divorced from action; pulse fatigue is real and reduces signal.

## AI-agent gotchas

- Demographic inference from names / emails / photos is illegal in many jurisdictions and unreliable everywhere. Never let an agent infer; only operate on legitimately-collected, consented data.
- LLMs over-summarize exit-interview free text; high-impact unique reasons get smoothed into popular themes. Force "show every quote that appears only once" alongside themes.
- "Compliance advice" from an LLM is not legal advice; agents must always defer to counsel and cite jurisdiction explicitly.
- DEI language drift: agents reach for buzzwords ("diverse perspectives", "lived experience") that vary in reception. Adversarial review with a fresh-context reviewer is mandatory.
- Disparate-impact ratios computed on n < 30 per group are meaningless; agents will report them anyway. Add a sample-size gate.
- Stay-interview questions auto-generated by an agent gravitate toward "engagement" theatre; force behavior + fact-eliciting questions.
- 9-box "potential" ratings encoded by an agent inherit historical bias; never let an agent pre-fill potential. Performance, yes; potential, never.
- Auto-emailed retention surveys / stay-interview invites violate CASL / CAN-SPAM / GDPR if there's no internal-comms-consent basis; route through internal newsletters infrastructure, not transactional email.
- Mandatory human-in-loop: (1) every compliance interpretation (counsel), (2) every DEI intervention (DEI lead), (3) every 9-box rating (manager + HRBP), (4) any disparate-impact-flagged stage (counsel + DEI), (5) any retention action affecting comp / role / manager assignment.

## References

- SHRM — "Talent Management" + "HR Compliance" toolkits (shrm.org).
- EEOC — Uniform Guidelines on Employee Selection Procedures (29 CFR 1607); four-fifths rule.
- US DOL — employment law guides (dol.gov).
- NYC Local Law 144 (AEDT) — automated employment decision tool bias-audit requirements.
- EU AI Act — high-risk AI in employment (recruitment, performance evaluation, allocation of work).
- GDPR Art. 22 — automated decision-making restrictions; UK GDPR equivalent.
- Information Commissioner's Office (ICO) — AI and data protection guidance (ico.org.uk).
- Bersin / Deloitte — "High-Impact Talent Management" research.
- Edmondson, A. — "The Fearless Organization" (psychological safety as retention driver).
- McKinsey — "Diversity Wins" series (intervention efficacy literature).
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization/agent-integration.md`.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/onboarding/agent-integration.md`.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/recruiting-process/agent-integration.md`.
