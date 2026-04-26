# STAR Interview Method

## Summary

Behavioral-interview framework (Situation-Task-Action-Result) for extracting evidence
of past performance and structuring post-interview analysis. The testable rule: every
STAR question must use past-tense behavioral framing ("Tell me about a time...") — never
hypothetical framing ("How would you..."); hypothetical answers have near-zero predictive
validity and must be blocked with a prescribed probe.

## Why

McDaniel et al. (1994) meta-analysis shows structured behavioral interviews are ~2x more
predictive of job performance than unstructured interviews. The STAR frame forces
candidates to produce observable, verifiable evidence rather than values statements.
Pronoun-shift detection ("we" vs. "I") and mandatory result quantification close the
two most common inflation paths (team re-attribution and "R" fabrication).

## When To Use

- Behavioral interview rounds for any role where past behavior is the dominant
  performance predictor: managerial, cross-functional, customer-facing roles.
- Calibrating an interviewer team that drifts into hypothetical questions.
- Generating tailored STAR question banks per competency from a JD or leveling rubric.
- Post-interview transcript analysis: STAR-component tagging and missing-component flagging.
- Coaching internal candidates preparing for promotion panels.

## When NOT To Use

- Pure technical screens where the signal lives in code, system design, or work samples —
  STAR adds noise, not signal.
- Roles with fewer than 2 years of experience: candidates lack a STAR repertoire; use
  situational + work-sample combinations.
- Cultures where narrative storytelling style is unfamiliar without controlling for it
  in scoring (some EU/EE/JP contexts).
- Crisis or urgency screens where only real-time problem-solving is a valid signal.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | STAR component definitions, interview flow, follow-up question types, complete vs. incomplete response patterns. |
| `content/02-question-bank.xml` | Question bank by competency (leadership, problem-solving, communication, collaboration, adaptability) with probes. |
| `content/03-rules-and-gotchas.xml` | Hypothetical-block rule, pronoun-shift detection, result quantification, agent scoring prohibition. |

## Templates

| File | Purpose |
|------|---------|
| `templates/star-scorecard.md` | Per-question S/T/A/R component scoring sheet with competency evidence and hire recommendation. |
| `templates/hiring-manager-guide.md` | Before/during/after interview checklist for hiring managers using STAR. |
| `templates/star-completeness.py` | Deterministic STAR completeness checker: flags missing components and "we"-only answers before LLM analysis. |
