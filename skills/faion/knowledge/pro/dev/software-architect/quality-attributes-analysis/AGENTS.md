# Quality Attributes Analysis

## Summary

Quality Attributes Analysis (QAA) is the systematic process of identifying, prioritizing, and binding non-functional requirements (NFRs) to architectural decisions using ISO/IEC 25010:2023 characteristics, 6-part quality attribute scenarios, utility trees with (Importance, Difficulty) scoring, and ATAM-style trade-off analysis. The concrete rule: every (H,H) scenario must have an executable fitness function (load test, chaos drill, security scan) wired into CI/CD — a scenario without a test is decoration.

## Why

80% of architectural decisions are driven by quality attributes, not features. When NFRs are treated as informal statements ("must be fast", "must be secure"), teams optimize one attribute and inadvertently sacrifice another without making the trade explicit. Quality issues found in design cost 10-100x less to fix than in production. The utility tree surfaces hidden conflicts between competing quality goals and creates stakeholder alignment before code is written.

## When To Use

- Pre-architecture phase of a non-trivial system — surface NFRs that will drive structural decisions
- Major architectural pivot (monolith → microservices, on-prem → cloud, sync → async)
- Investor / customer due diligence requiring evidence the architecture meets SLA / compliance promises
- Postmortem after a performance, security, or availability incident that the original architecture did not anticipate
- Multi-tenant or regulated domain (healthcare, finance, public sector) requiring ISO/IEC 25010 traceability
- New team onboarding — utility tree + scenarios align priorities faster than any wiki page

## When NOT To Use

- Idea / prototype stage with fewer than 5 paying customers — quality attributes are imagined; bottleneck is product-market fit
- Tactical sprint planning — utility trees are not a substitute for backlogs
- Single-developer side project with no SLA — overhead exceeds value
- Team will not revisit the artifact after the workshop — a one-shot ATAM is theater
- Trade-offs are already political, not technical — no analysis method survives a pre-decided executive choice

## Content

| File | What's inside |
|------|---------------|
| `content/01-scenario-structure.xml` | 6-part scenario anatomy (Source/Stimulus/Environment/Artifact/Response/Measure), worked examples |
| `content/02-utility-tree.xml` | Utility tree structure, (H,H) priority notation, ATAM 9-step overview, ATAM outputs |
| `content/03-tactics.xml` | Performance, availability, security, modifiability, scalability tactics with examples |
| `content/04-tradeoffs.xml` | Common quality attribute conflicts, CAP theorem, stakeholder concern matrix |
| `content/05-antipatterns.xml` | Hallucinated SLAs, qualitative measures, symmetric (H,H) tree, scenario inflation |

## Templates

| File | Purpose |
|------|---------|
| `templates/scenario-lint.py` | CI script: rejects scenarios missing any of 6 parts or lacking numeric thresholds |
| `templates/scenario-template.md` | 6-part scenario template with prompts for each field |
| `templates/utility-tree.md` | Utility tree skeleton with (Importance, Difficulty) legend |
