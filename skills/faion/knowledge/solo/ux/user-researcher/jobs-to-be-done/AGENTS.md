# Jobs to Be Done (JTBD)

## Summary

JTBD is a framework for understanding why customers "hire" products to make progress. It produces a job statement ("When [situation], I want to [action], so I can [outcome]") covering functional, emotional, and social dimensions, plus a forces analysis (push/pull/habit/fear) that explains switching behavior. Jobs are stable over time; solutions evolve. The framework also produces an 8-stage job map (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude) that reveals where the job breaks down.

## Why

Product teams focused on features and demographics miss the underlying motivation. JTBD interviews with recent switchers — people who recently purchased, switched, or started using a category — reconstruct the decision timeline and reveal the real competition (often non-obvious: a task manager competes with sticky notes and email, not just Trello). Without JTBD, positioning copy speaks to features; with it, it speaks to the progress customers are trying to make.

## When To Use

- Repositioning a product that has low conversion despite apparent feature completeness
- Designing a new product category where obvious competitors don't exist yet
- Understanding why customers churn when they "should" be satisfied
- Rewriting positioning copy to speak to motivation, not features
- Planning a switching campaign by mapping forces of progress for a competitor's customers

## When NOT To Use

- Usability testing: JTBD explains why someone hired the product; usability testing explains why the product failed on the job
- Quantitative feature prioritization: JTBD is qualitative and requires synthesis, not voting
- When you have fewer than 5 recent switcher interviews — the framework needs pattern recognition across cases
- When a LLM-generated job statement hasn't been validated with actual customers — synthetic JTBD is fiction

## Content

| File | What's inside |
|------|---------------|
| `content/01-jtbd-framework.xml` | Core concepts: job vs. solution, three dimensions, hiring/firing, four forces of progress |
| `content/02-interview-and-mapping.xml` | Switcher interview method, timeline reconstruction, job mapping, examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/job-statement.md` | Job statement canvas with functional, emotional, and social dimensions |
| `templates/jtbd-interview.md` | Interview guide for recent switchers with forces analysis section |
| `templates/job-map.md` | 8-stage job map template (goals, pain, opportunity per stage) |
| `templates/prompt-extract-statement.txt` | LLM prompt to extract JTBD statement from an interview transcript |
| `templates/prompt-job-map.txt` | LLM prompt to map a job statement into 8-stage framework |
| `templates/jtbd-parser.py` | Regex extractor for When/I want/So I can from raw interview notes |
