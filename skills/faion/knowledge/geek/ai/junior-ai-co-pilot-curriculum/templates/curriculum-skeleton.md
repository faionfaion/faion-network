<!--
purpose: 6-week onboarding skeleton with required module headers and exercise stubs.
consumes: tech-stack + tool-name + junior baseline
produces: filled curriculum.json after tailoring
depends-on: content/04-procedure.xml step 2
token-budget-impact: docs-only; never loaded by agent runtime
-->
# Junior AI Co-Pilot Curriculum — {{junior_name}}

Tool: {{tool}}
Mentor: {{mentor_name}}
Duration: 6 weeks, 30-min mentor sync every Friday.

## Week 1 — Prompt anatomy
- Exercise: refactor 3 prompts using explicit input/output contract; commit before/after.
- Reflection: 1 page comparing tokens used and outputs received.

## Week 2 — Hallucination check
- Exercise: review 5 AI-generated code suggestions; cite real library + version for each non-trivial API.
- Reflection: list 5 hallucinations found + how you verified.

## Week 3 — Scoped edits
- Exercise: make 5 changes < 50 LOC each, each gated by `git diff` review with mentor.
- Reflection: 1 page on `change size vs. AI accuracy` observation.

## Week 4 — Test-first AI
- Exercise: write failing tests before AI generates implementation for 3 tasks.
- Reflection: which tests caught hallucinations?

## Week 5 — Security boundaries
- Exercise: run the IPI eval suite against the team's agent; document 3 findings.
- Reflection: which controls were in place, which were missing?

## Week 6 — Mentor review
- Exercise: walk mentor through a complete co-pilot-augmented PR end-to-end.
- Reflection: 1-page retrospective.
