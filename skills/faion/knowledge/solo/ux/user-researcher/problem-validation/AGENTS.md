# Problem Validation

## Summary

Evidence-based process for deciding whether a problem is worth solving: collect evidence across a validation hierarchy (paid &gt; committed &gt; engaged &gt; stated &gt; anecdote), apply Mom Test question rewrites to avoid leading/hypothetical framing, and output a PROCEED / PIVOT / KILL decision with a scored evidence log. Define a kill threshold before collecting any evidence.

## Why

Building products for unvalidated problems is the leading cause of startup failure. The validation hierarchy forces the researcher to distinguish between weak evidence (someone said they have the problem) and strong evidence (someone pre-paid to solve it). Without a pre-defined kill threshold, researchers rationalize weak evidence as sufficient and continue building.

## When To Use

- Before committing engineering resources to a solution
- After pain point research has identified candidate problems — which are worth solving?
- Quarterly review of assumed problems in an existing product backlog
- Pre-pivot: does the proposed direction have enough validated demand?
- When a founder or PM has a strong hypothesis and needs structured pushback

## When NOT To Use

- When real users have already been paying for the solution — validation complete, move to retention
- As a substitute for usability testing (problem validation answers "does this problem exist?", not "does this UI work?")
- When n &lt; 5 data points — a single frustrated user is anecdote, not signal
- When all evidence is compliments and hypotheticals — that is negative validation, stop and pivot

## Content

| File | What's inside |
|------|---------------|
| `content/01-validation-framework.xml` | Hierarchy, Mom Test rewrites, commitment signals, red flags |
| `content/02-process-and-antipatterns.xml` | 5-step process, evidence scorer logic, agent limitations |

## Templates

| File | Purpose |
|------|---------|
| `templates/validation-report.md` | Problem Validation Report with evidence table and PROCEED/PIVOT/KILL decision |
| `templates/prompt-evaluate.txt` | LLM prompt to score evidence and recommend proceed/pivot/kill |
| `templates/prompt-rewrite-questions.txt` | LLM prompt to rewrite questions using Mom Test principles |
| `templates/evidence-scorer.py` | Score evidence items by hierarchy level and print validation percentage |
