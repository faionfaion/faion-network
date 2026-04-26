# Elicitation Techniques

## Summary

Elicitation is the process of drawing out information from stakeholders about their needs, wants, and constraints — not just asking questions but using structured techniques to uncover stated and unstated requirements. Core techniques are: interviews (depth), workshops (consensus), observation (actual behavior), document analysis (existing state), surveys (breadth), prototyping (validation), focus groups (user perspective), and brainstorming (ideation). Each session produces a typed artifact committed to version control; a synthesis step extracts REQ stubs that cite at least two distinct technique sessions per requirement.

## Why

Stakeholders cannot reliably articulate what they need in the abstract. Interviews surface stated needs; observation surfaces actual behavior — the gap between them is where the most valuable requirements live. Single-technique programs miss requirements; triangulation across at least two techniques per area is the empirical fix. Without a documented elicitation record, requirements lack the source attribution needed for impact analysis, regulated-industry audits, and conflict resolution.

## When To Use

- Kickoff of a new initiative where stakeholder needs are vague, contradictory, or undocumented.
- Migration or replatforming projects where knowledge lives in a few senior employees' heads.
- Regulated domains (medical, fintech, gov) where elicitation evidence is part of the audit trail.
- Discovery sprints where the BA must triangulate a process within one week using mixed techniques.
- Distributed or async teams where surveys, recorded interviews, and async observation are the only feasible channels.

## When NOT To Use

- Solo founder or 2-person team where direct conversation is faster than scheduling formal sessions.
- Backlog refinement on a stable product — DoR conversations and slice discussions cover it.
- The answer is already in a spec, ADR, or RFC — read first, elicit only the gaps.
- Bug triage or incident postmortems — those have their own templates (5-whys, blameless retro).
- Stakeholders are unwilling or unavailable — surveys to non-responsive groups produce noise; escalate sponsorship instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-techniques.xml` | Eight elicitation techniques with when-to-use, preparation steps, and execution guidance. Technique selection guide by information type. |
| `content/02-examples.xml` | Requirements discovery interview example and process mapping workshop example; common antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Interview guide with objectives, background questions, main questions, closing questions, and action items. |
| `templates/workshop-agenda.md` | Workshop agenda with time slots, activities, owners, materials, and expected outputs. |
| `templates/session-check.py` | Pre-commit validator for elicitation session artifacts: checks frontmatter, consent, PII-redaction status. |
