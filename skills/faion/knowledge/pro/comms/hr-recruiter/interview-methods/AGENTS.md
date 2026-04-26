# Interview Methods

## Summary

Bundle of structured-interview methodologies covering competency definition, STAR
behavioral questions, scorecards, technical assessments, culture-fit assessment,
reference checks, and hiring-committee debrief. The testable rule: cap competencies at
4-6 with weights summing to 100% — more dilutes predictive signal; behavioral anchors
must be observable verbs, never traits ("driven", "strong").

## Why

Unstructured interviews have near-zero predictive validity. Schmidt and Hunter (1998)
show structured behavioral interviews are roughly twice as predictive as unstructured
ones. Forcing independent scorecard submission before the debrief channel opens prevents
the loudest-voice-wins dynamic. Inter-rater reliability (Cohen's kappa) below 0.4 on
any competency signals recalibration is needed before a hire decision.

## When To Use

- Standing up an interview process from scratch for a new role family: competencies →
  questions → scorecards → debrief flow.
- Auditing an existing process whose interview-to-offer rate falls outside the 15-25% band.
- Calibrating interviewers across geographies where in-person calibration is impractical.
- Rolling out structured interviews after a hiring-manager change before legacy bias
  re-anchors.

## When NOT To Use

- Single-hire one-off (founder hiring a co-founder, exec search) — overhead exceeds
  benefit; use a 2-step trust-and-reference loop.
- Roles where the only valid signal is portfolio review (illustrators, cinematographers).
- Volume retail or hourly hiring at scale — use realistic job previews, not panel interviews.
- Statutorily-fixed questionnaires (clinical, legal regulated roles).

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-overview.xml` | Five-stage pipeline: competency definition, question generation, scorecard, calibration pack, debrief synthesis. |
| `content/02-method-catalog.xml` | Structured interview design, behavioral questions, scorecard, technical assessment, reference check, debrief. |
| `content/03-rules-and-gotchas.xml` | Competency cap rule, bias/legal review pass, auto-score block, FCRA/GDPR constraints. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-scorecard.md` | Competency-by-competency scoring template with behavioral anchors and hire/no-hire field. |
| `templates/irr-check.py` | Cohen's kappa inter-rater agreement check; gates debrief when kappa &lt; 0.4 per competency. |
