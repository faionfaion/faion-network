# Hybrid Delivery

## Summary

A delivery model that combines predictive (waterfall/stage-gate) and agile methods within a single program, assigning each by component risk profile. The canonical pattern: use predictive for planning, contracting, regulatory submissions, and hardware; use agile for software execution, testing, and iteration. The boundary must be drawn in writing — boundary ambiguity is the dominant failure mode.

## Why

Pure agile and pure waterfall each fail in mixed-reality programs. Hardware/software products need physical milestones alongside iterative firmware; regulated industries need gate evidence alongside fast cycles; enterprise portfolios need quarterly budget cycles alongside two-week sprints. Hybrid is not a compromise — it is an explicit, architected two-cadence model with a defined translation layer between them.

## When To Use

- Programs with hardware and software components (medical device, automotive, IoT).
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates and V-model evidence.
- Enterprise transformation rollouts: portfolio level uses milestones, delivery teams use Scrum/Kanban.
- Vendor plus internal team mixes where vendor work is fixed-bid (predictive) and internal is iterative.
- Cloud platforms running DevOps + Agile for delivery while ops/finance/security gate quarterly.

## When NOT To Use

- Pure software product team with autonomous backlog and no compliance — full Scrum or Kanban is simpler.
- Startup with fewer than 10 people — ceremony overhead exceeds coordination value.
- Pure fixed-scope construction build where iteration adds risk without value — stay predictive.
- "We do hybrid" with no explicit written boundary — that is incoherence, not a method.

## Content

| File | What's inside |
|------|---------------|
| `content/01-hybrid-patterns.xml` | Five hybrid patterns (Water-Scrum-Fall, Agile-with-Gates, Phased Agile, Selective Agile, DevOps+Agile); decision framework for method selection; boundary rules and translation-layer requirements. |
| `content/02-antipatterns.xml` | Six hybrid failure modes: boundary ambiguity, dual definitions of done, tool sprawl, governance drift, political compromise disguised as method, EVM on agile arm. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid-alignment.py` | Script that flags milestone/epic misalignment in a program.yaml (past due, at risk, orphan epics). |
