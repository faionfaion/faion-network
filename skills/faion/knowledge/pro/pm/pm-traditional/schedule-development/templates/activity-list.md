# Activity List — [Project Name]

| ID | Activity | WBS Ref | Dur (d) | O | M | P | PERT | Predecessors | Resource |
|----|----------|---------|---------|---|---|---|------|--------------|----------|
| A1 | Requirements review | 2.1 | 2 | 1 | 2 | 4 | 2.2 | None | BA |
| A2 | Database design | 3.2 | 3 | 2 | 3 | 6 | 3.3 | A1 | Architect |
| A3 | API design | 3.3 | 2 | 1 | 2 | 4 | 2.2 | A1 | Dev Lead |
| A4 | Frontend wireframes | 3.1 | 4 | 3 | 4 | 7 | 4.2 | A1 | Designer |
| A5 | Database implementation | 4.2 | 5 | 4 | 5 | 9 | 5.5 | A2 | Backend |
| A6 | API development | 4.2 | 8 | 6 | 8 | 14 | 8.7 | A2,A3 | Backend |
| A7 | Frontend development | 4.1 | 10 | 8 | 10 | 16 | 10.7 | A3,A4 | Frontend |
| A8 | Integration | 4.3 | 3 | 2 | 3 | 6 | 3.3 | A6,A7 | Team |
| A9 | Testing | 5.0 | 5 | 4 | 5 | 9 | 5.5 | A8 | QA |
| A10 | Deployment | 6.0 | 2 | 1 | 2 | 4 | 2.2 | A9 | DevOps |

**PERT formula:** (O + 4M + P) / 6
**Required for activities > 5 days:** use three-point estimation (O/M/P columns)
**Buffer:** add Project Buffer at the end = 15-25% of Critical Path duration
