# Resource Management

## Summary

Plan to 70% utilisation (not 100%), map skills to tasks from a YAML roster in git, level resource load using critical-path analysis, and track allocations weekly against actuals. Agents propose reassignments; resource managers and individuals confirm. Rate cards live in a secrets store, not in the repo.

## Why

100% allocation is a planning fiction that ignores meetings, support, ramp time, and unplanned work. Real available time is 60–70% of nominal hours. Planning to full capacity means any unplanned event causes a miss. Resource leveling resolves the over-allocation math but must respect morale — the same person reassigned three times in two months will burn out; the algorithm does not know this.

## When To Use

- Multi-team programs sharing scarce specialists (security, ML, SRE, designers) where allocation conflicts cause schedule slips
- Agency / consulting environments billing by utilisation with hard hourly budgets
- Programs spanning external contractors with rate cards and SOW linkage to deliverables
- Capacity planning across quarters when demand forecasts must align with hiring pipelines
- Workforce planning during reorgs where role mapping is non-trivial

## When NOT To Use

- Stable single-team product squad with a tech lead doing capacity by feel — kanban WIP limits are sufficient
- Solopreneurs — calendar blocking covers it; resource matrices waste time
- Pre-PMF startups optimising for learning velocity — 100% of one engineer beats 60% of three
- Fixed-bid contracts where resource visibility is internal-only and not a deliverable

## Content

| File | What's inside |
|------|---------------|
| `content/01-planning.xml` | Roster schema, utilisation rules, skill matrix, ramp time, vacation handling |
| `content/02-leveling.xml` | Resource leveling techniques, morale constraints, contractor linkage, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-check.py` | Flags overloaded resources per ISO week from roster + allocations YAML |
