# Feature Prioritization (MoSCoW)

## Summary

MoSCoW categorizes requirements into Must Have, Should Have, Could Have, and Won't Have buckets for a fixed-timebox release. The core rule: every Must Have must pass the fail-test — "if we don't have this, does the product work?" — and Must + Should must not exceed 80% of capacity.

## Why

Without a shared priority vocabulary, every requirement becomes "high priority" and scope creep is uncontrollable. MoSCoW forces explicit trade-off decisions and, critically, requires documenting exclusions (Won't Have), which prevents scope re-entry mid-sprint.

## When To Use

- Fixed-timebox release (sprint, milestone, MVP, contractual deadline) where capacity is the constraint
- Stakeholder workshop where the goal is shared vocabulary, not numerical optimization
- Scoping a vendor or contractor engagement: M/S/C/W maps cleanly to contract obligations
- Compliance and legal-driven work where "Must" carries a non-negotiable definition

## When NOT To Use

- Cross-feature ROI comparison — MoSCoW does not encode effort or impact magnitude; use RICE
- Long-horizon roadmaps (>1 quarter) — categories drift; rerun MoSCoW per release
- Many candidates (>30 items) — categories collapse into "Must" by stakeholder pressure; use a numeric framework
- Strategic bets — MoSCoW cannot capture "this is a moat play, not viability"

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Category definitions (Must/Should/Could/Won't), effort allocation rules, fail-test |
| `content/02-process.xml` | 6-step MoSCoW process from listing requirements to locking categories |
| `content/03-antipatterns.xml` | Common failure modes: Must inflation, missing Won't, no timebox |

## Templates

| File | Purpose |
|------|---------|
| `templates/moscow-matrix.md` | Prioritization matrix with effort tracking and summary table |
| `templates/moscow-capacity-validator.sh` | Bash script to validate Must+Should <= 80% of capacity from CSV |
