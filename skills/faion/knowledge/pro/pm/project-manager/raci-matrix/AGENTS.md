# RACI Matrix

## Summary

Assign one of four roles — Responsible (does the work), Accountable (single decision owner), Consulted (provides input), Informed (notified after) — to each role for each task or deliverable. The rule: exactly one Accountable per task, no exceptions. Multiple Accountables collapse the escalation path and hide conflicts that only sponsors can resolve.

## Why

"I thought you were handling that" and "who approves this?" are symptoms of undefined accountability. RACI makes implicit role assumptions explicit before work begins, so disputes surface in a kickoff meeting rather than at a missed deadline. The Consulted count is a bottleneck detector: more than 3-4 Consulted per task signals that decisions will be slow.

## When To Use

- New project kickoff with multiple roles (PM, dev lead, QA, DevOps, BA, sponsor) and recurring "who decides?" friction
- Cross-team features where SDD task ownership is ambiguous (backend + frontend + data + ops)
- Vendor/contractor engagements: clarify what client owns vs what contractor delivers
- Audit/compliance projects (SOC2, ISO 27001) requiring a named Accountable per control
- Solopreneur engagements with designer, developer, and VA mix

## When NOT To Use

- One-person solo task with no external stakeholders — overhead with zero return
- Pure agile teams with collective code ownership and one PO — RACI flattens to "PO=A, team=R" everywhere; use DACI for decisions instead
- Highly emergent work where roles shift weekly — matrix decays faster than it is updated

## Content

| File | What's inside |
|------|---------------|
| `content/01-raci-rules.xml` | Four roles defined, four validation rules, common violations and resolutions |
| `content/02-raci-examples.xml` | Feature development RACI example, solopreneur example, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/raci-matrix.md` | Blank RACI grid template with role columns and task rows |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/raci-validate.py` | Check RACI CSV for rule violations: no-A, multi-A, no-R, C inflation, empty rows |
