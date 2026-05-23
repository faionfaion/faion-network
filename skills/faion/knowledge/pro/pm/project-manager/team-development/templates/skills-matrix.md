<!-- purpose: Skills matrix role x skill (1-4 scale; ? for unknown) with Gap-Action column. -->
<!-- consumes: team roster + skills taxonomy + role expectations -->
<!-- produces: skills_gap_plan entries for TeamDevelopmentReport -->
<!-- depends-on: content/01-core-rules.xml#training-before-hire -->
<!-- token-budget-impact: ~200 tokens when loaded as context -->

# Skills Matrix — [Team Name]

Scale: 1=Beginner | 2=Basic | 3=Intermediate | 4=Expert | ?=Unknown (never guess)

| Skill | [Role 1] | [Role 2] | [Role 3] | Gap Action |
|-------|-----------|-----------|-----------|------------|
| [Skill A] | ? | 3 | 2 | [Training / Pair / Hire] |
| [Skill B] | 4 | 1 | ? | [Pair: Role 1 leads workshop] |
| [Skill C] | 2 | 2 | 4 | [Cross-train: Role 3 leads] |

## Gap Summary
| Gap | Severity | Options Evaluated | Chosen | Owner Role | Deadline Sprint |
|-----|----------|-------------------|--------|------------|-----------------|
| [Skill B — Role 2] | High | training/pairing/contracting/hiring | pairing | [PM] | S14 |

<!-- Rules:
- ALWAYS evaluate all four options (training, pairing, contracting, hiring) before choosing.
- ? for unknown — never guess a 3.
- Severity: High (blocks delivery), Medium (slows delivery), Low (nice to have).
- Deadline must be S-numbered sprint (e.g. S14), never "next" or "soon".
-->
