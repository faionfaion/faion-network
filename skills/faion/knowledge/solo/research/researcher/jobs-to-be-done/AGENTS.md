# Jobs to Be Done (JTBD)

## Summary

A framework for understanding what progress customers are trying to make so products can be designed around stable motivations rather than shifting feature requests. Core rule: interview recent switchers (within 60-90 days), tag each response as Push / Pull / Habit / Fear, synthesize 1-3 candidate job statements in "When... I want... So I can..." form, and always capture functional, emotional, and social job dimensions.

## Why

Feature-based thinking produces roadmaps that match stated wants but miss underlying motivations. Jobs are stable over decades (communicate with family, capture thoughts, get from A to B) while solutions change. Identifying the real job reveals non-obvious competition and prevents building features that satisfy surface requests while failing the deeper progress the customer needs.

## When To Use

- Re-framing an idea or feature in customer-progress terms before building.
- Diagnosing why a feature flopped: was the job mismatched or just the solution?
- Understanding switching: interview recent switchers using the Forces of Progress framework.
- Mapping a complex job into stages to find the highest-pain stage.

## When NOT To Use

- Optimizing an already-validated product on a known job — use A/B tests, retention analysis, and growth experiments.
- B2C impulse purchases (snacks, fashion) where the job is simply "feel good now."
- Pure infrastructure or API tooling where the job is technical and persona/feature thinking is faster.
- No recent switchers available to interview — JTBD without switching data is hypothesis-spinning.

## Content

| File | What's inside |
|------|---------------|
| `content/01-jtbd-concepts.xml` | Core concepts: job vs. solution, functional/emotional/social dimensions, hiring and firing, Forces of Progress model. |
| `content/02-interview-and-job-map.xml` | Switcher interview method, timeline reconstruction questions, job-map 8-stage template, and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/job-statement.md` | Template for documenting a core job with functional, emotional, and social dimensions plus competitive set. |
| `templates/jtbd-interview.md` | Full interview guide: context fields, timeline questions, forces analysis, draft job statement. |
| `templates/job-map.md` | 8-stage job map (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude) with pain + opportunity fields. |
| `templates/force-aggregator.py` | Python script: reads tagged-transcript JSON files, aggregates Push/Pull/Habit/Fear counts and severities. |
