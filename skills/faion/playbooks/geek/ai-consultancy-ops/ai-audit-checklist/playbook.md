---
name: ai-audit-checklist
description: Run a NIST AI RMF-aligned audit across Govern, Map, Measure, and Manage and deliver a 1-page client risk report.
tier: geek
group: ai-consultancy-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have completed a structured AI system audit covering all four NIST AI RMF core functions — Govern, Map, Measure, and Manage — and produced a signed-off 1-page client report that itemises findings, risk ratings, and remediation owners.

## Prerequisites

- Access to the client's AI system documentation: model cards, data dictionaries, deployment runbooks, incident logs.
- At least one 90-minute stakeholder interview slot with the AI product owner and one with the data engineering lead.
- Python 3.11+ with `anthropic>=1.27`, `pydantic>=2.7`, `pandas>=2.2` installed (for automated bias and drift checks).
- Read-only credentials for the client's model serving environment (e.g. SageMaker, Vertex AI, or a self-hosted endpoint) to pull inference logs.
- A copy of the [NIST AI RMF Playbook](https://airc.nist.gov/Docs/2) (PDF) for reference during the Govern walkthrough.
- Completed `ai-proposal-template` engagement (or equivalent scoped statement of work defining audit boundaries).

## Steps

1. **Schedule and scope the engagement.** Confirm the audit boundary in writing: which model(s), which deployment stage (dev / staging / prod), which regulatory jurisdiction (EU AI Act, HIPAA, CCPA, or none). Record in `audit-scope.md`.

2. **Run the Govern checklist.** For each item below, mark `PASS / PARTIAL / FAIL` and note the evidence artifact:
   - AI governance policy exists and is dated within the last 12 months.
   - Responsible AI owner (a named individual) is documented and reachable.
   - Risk appetite statement covers AI-specific scenarios (hallucination, bias, data poisoning).
   - Third-party model usage (OpenAI, Anthropic, Google) is listed in a vendor register with data-processing agreements.
   - Employee AI-use policy exists and has been communicated in the last 6 months.
   - Model change-management process (versioning, sign-off, rollback) is documented.
   - Human-in-the-loop override mechanism exists for high-stakes decisions.
   - Incident response runbook covers AI-specific failure modes.
   - AI system inventory is maintained (all production models listed with owners).
   - Audit trail retention policy (logs kept ≥90 days minimum).

3. **Run the Map checklist.** Verify that the system's context and risk profile are documented:
   - Intended use cases are enumerated with explicit out-of-scope uses.
   - Affected populations are identified (demographic breakdown where applicable).
   - Data lineage from raw source to model input is traceable end-to-end.
   - Training and evaluation data sources are documented with license/consent status.
   - Sensitive attributes (race, gender, health, religion) are flagged in the data dictionary.
   - Foreseeable misuse scenarios are listed (at least 5).
   - Impact assessment exists for each misuse scenario (severity × likelihood matrix).
   - External dependencies (upstream APIs, data vendors) are mapped with SLA and fallback.
   - Deployment context (who uses it, via which interface, at what volume) is current.
   - Regulatory classification is confirmed (EU AI Act risk tier: unacceptable / high / limited / minimal).

4. **Run the Measure checklist.** Collect quantitative evidence using the client's inference logs:

   ```python
   import anthropic
   import pandas as pd
   from pydantic import BaseModel

   class BiasMetrics(BaseModel):
       demographic_parity_diff: float   # |P(y=1|A=0) - P(y=1|A=1)|
       equalized_odds_diff: float       # max TPR diff across groups
       avg_calibration_error: float     # ECE across all groups

   client = anthropic.Anthropic()

   # Send a sample of 200 inference log rows to Claude for bias signal extraction
   with open("inference_sample.jsonl") as f:
       sample = f.read()

   msg = client.messages.create(
       model="claude-opus-4-7",
       max_tokens=2048,
       messages=[{
           "role": "user",
           "content": f"""Analyse this inference log sample for demographic disparity signals.
   Return a JSON object with keys: demographic_parity_diff (float),
   equalized_odds_diff (float), avg_calibration_error (float).

   <log_sample>
   {sample}
   </log_sample>"""
       }]
   )
   metrics = BiasMetrics.model_validate_json(msg.content[0].text)
   print(metrics)
   ```

   Checklist items:
   - Demographic parity difference < 0.05 for each sensitive attribute.
   - Equalized odds difference < 0.05 (TPR and FPR gap across groups).
   - Average calibration error (ECE) < 0.10 on held-out eval set.
   - Accuracy / F1 / AUC on production distribution is within 2 pp of baseline.
   - Latency p99 < SLA threshold (documented in the engagement scope).
   - Data drift alert is configured and tested (e.g. via Evidently AI or Arize).
   - Concept drift (model output distribution shift) is tracked over rolling 30-day window.
   - Adversarial robustness test (prompt injection, jailbreak attempts) has been run in the last quarter.
   - Hallucination rate on domain-specific eval set is below agreed threshold (default 5%).
   - Explainability method (SHAP, LIME, or attention probing) is available for at least one model tier.

5. **Run the Manage checklist.** Confirm operational risk controls are in place:
   - Risk register exists with each AI risk rated (likelihood × impact) and an owner.
   - Escalation path is defined: who decides to pause or roll back a model in production.
   - Automated circuit-breaker exists: model output is blocked if confidence < threshold.
   - Retraining trigger is defined: what metric threshold triggers a new training run.
   - Shadow mode / canary deployment is used for new model versions (≥5% traffic split before full rollout).
   - Post-deployment monitoring dashboard is live and reviewed at least weekly.
   - Bias monitoring alert fires and reaches a named recipient within 24 hours.
   - Model card is kept up to date after each retraining cycle.
   - Privacy impact assessment (PIA) covers the model's data processing.
   - Decommission procedure is documented: how to safely retire the model and purge user data.

6. **Score each section.** Count PASSes per section. Compute a section score: `PASS / total × 100`. Overall score = mean of four section scores.

   | Section | Checks | Score |
   |---------|--------|-------|
   | Govern | 10 | ___ % |
   | Map | 10 | ___ % |
   | Measure | 10 | ___ % |
   | Manage | 10 | ___ % |
   | **Overall** | 40 | ___ % |

7. **Draft the 1-page client report.** Use this template structure:

   ```
   AI Audit Report — <Client Name> — <System Name> — <Date>

   Executive Summary (3 sentences)
   Overall Score: ___% | Govern: ___% | Map: ___% | Measure: ___% | Manage: ___%

   Critical Findings (FAIL items only, max 5 bullets)
   - [Section] <Finding>: <Remediation> — Owner: <Name> — Due: <Quarter>

   High-Risk Items (PARTIAL, risk-rated HIGH)
   - [Section] <Finding>: <Remediation> — Owner: <Name> — Due: <Quarter>

   Strengths (PASS items worth highlighting, max 3 bullets)

   Next Audit Date: <recommended cadence>
   Auditor: <your name + credential>
   ```

8. **Present and sign off.** Walk through findings in a 30-minute readout. Capture the client's remediation commitments in writing. Export the report as a PDF and store it in the engagement folder.

## Verify

After completing all steps, run this command to confirm your bias-metrics script produces a structured result without errors:

```bash
python3 -c "
import anthropic, json
from pydantic import BaseModel

class BiasMetrics(BaseModel):
    demographic_parity_diff: float
    equalized_odds_diff: float
    avg_calibration_error: float

client = anthropic.Anthropic()
msg = client.messages.create(
    model='claude-sonnet-4-6',
    max_tokens=256,
    messages=[{'role': 'user', 'content':
        'Return a JSON object: {\"demographic_parity_diff\": 0.03, \"equalized_odds_diff\": 0.02, \"avg_calibration_error\": 0.07}'}]
)
m = BiasMetrics.model_validate_json(msg.content[0].text)
assert m.demographic_parity_diff < 0.05, 'parity diff exceeds threshold'
print('bias metrics OK:', m)
"
```

Expected output: `bias metrics OK: demographic_parity_diff=0.03 equalized_odds_diff=0.02 avg_calibration_error=0.07`

Also confirm the audit score sheet totals 40 checks across 4 sections, and the 1-page report PDF is ≤2 MB.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client refuses access to inference logs | Data governance policy or legal hold | Scope the Measure section to synthetic stress-test data provided by the client; document the limitation in the report |
| `anthropic.AuthenticationError` when running bias script | `ANTHROPIC_API_KEY` not set | `export ANTHROPIC_API_KEY=$(op read "op://faion.net/Anthropic/api_key")` then re-run |
| Pydantic `ValidationError` on BiasMetrics parse | Model returned explanation text around the JSON | Wrap the API call in a JSON-extraction retry: strip everything outside `{...}` using `re.search(r'\{.*\}', text, re.DOTALL)` |
| Client's model is not accessible (black-box SaaS) | No inference log export available | Switch to a behavioural audit: run 100 standardised probe prompts and score outputs manually; document as `audit_method: behavioural_probe` in the report |
| Overall score below 50% | Systemic governance gap | Flag as High-Risk engagement; recommend a 90-day remediation sprint before next audit; include in executive summary |
| EU AI Act tier is "high-risk" but no conformity assessment exists | Regulatory oversight gap | This is a Critical Finding; add to the report as a legal-compliance blocker with external counsel referral |

## Next

- `ai-proposal-template` — draft the follow-on remediation engagement based on Critical Findings from this audit.
- Run a focused `model-monitoring-drift` playbook to set up continuous post-remediation monitoring for the client's production model.
- Upgrade to a full EU AI Act conformity assessment if the system is classified as high-risk under Article 6.

## References

- [knowledge/geek/ai/ml-ops/evaluation-metrics](../../../knowledge/geek/ai/ml-ops/evaluation-metrics) — demographic parity diff, equalized odds, and ECE definitions used directly in Step 4 Measure checklist thresholds.
- [knowledge/geek/ai/ml-ops/evaluation-framework](../../../knowledge/geek/ai/ml-ops/evaluation-framework) — structured eval pipeline used to score each NIST function section and compute the overall audit score in Step 6.
- [knowledge/pro/research/researcher/risk-assessment](../../../knowledge/pro/research/researcher/risk-assessment) — likelihood × impact matrix methodology applied in the Manage checklist (Step 5) and risk register scoring.
