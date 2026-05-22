<!--
purpose: Binary pass/fail gating rubric (10 items minimum) for graduation.
consumes: junior evidence + mentor review notes
produces: graduation decision
depends-on: content/01-core-rules.xml r5
token-budget-impact: docs-only
-->
# Junior AI Co-Pilot — graduation rubric

Each item is binary: pass or fail. Graduation requires 100% pass.

| id | statement | evidence source |
|----|-----------|-----------------|
| r1 | Can spot a fabricated API in generated code within 60 seconds | week 2 reflection + sample diff |
| r2 | Writes prompts with explicit input/output contract | PR samples |
| r3 | Splits AI-generated changes into ≤ 50-LOC scoped PRs | PR history |
| r4 | Writes failing tests before accepting AI implementation | week 4 reflection + diff |
| r5 | Recognises ≥3 IPI categories in a sample input | week 5 reflection |
| r6 | Never pastes prod credentials, customer PII, or unreleased IP into prompts | mentor observation log |
| r7 | Uses only the team's approved AI tool list | mentor observation log |
| r8 | Cites source for any non-trivial fact the AI emits | reflections + PRs |
| r9 | Can compare ≥2 AI co-pilots on the same task | week 1 reflection |
| r10 | Articulates when NOT to use AI co-pilot for a task | final-week retrospective |
