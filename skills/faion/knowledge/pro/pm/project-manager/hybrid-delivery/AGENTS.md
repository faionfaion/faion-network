# Hybrid Delivery

## Summary

A framework for programs that combine predictive (waterfall) and agile delivery modes when neither alone fits. The boundary between modes is defined explicitly in a program.yaml work-graph: top-level milestones (predictive arm) decompose into epics, which decompose into team backlogs (agile arm). Both arms use their own vocabulary and rituals; a translation layer converts between them for steering-committee reporting.

## Why

Pure agile or pure waterfall rarely fits real programs. Hardware + software combinations, regulated environments, and enterprise rollouts all have components with different risk profiles and cadence needs. Hybrid works when the boundary is explicit; it fails — degenerating into incoherence — when the boundary is undefined or driven by politics rather than risk profile. The translation layer prevents vocabulary collisions from breaking executive trust.

## When To Use

- Programs with hardware + software components where physical-world milestones are predictive and digital iteration is agile.
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates on top of agile execution.
- Enterprise transformation rollouts: portfolio-level milestones + budget cycles with Scrum/Kanban delivery teams.
- Vendor + internal team mixes where vendor contracts are fixed-bid and internal teams iterate.
- DevOps + Agile delivery with monthly/quarterly ops/finance/security governance reviews.

## When NOT To Use

- Pure software-only product teams with autonomous backlog and no compliance gates — full Scrum or Kanban is simpler.
- Tiny teams (under 10) where ceremony overhead exceeds coordination value — pick one mode.
- Pure fixed-scope delivery where iteration adds risk without value — stay predictive.
- "We do hybrid" without explicit boundaries — that is incoherence, not hybrid; refuse and force a real method choice.

## Content

| File | What's inside |
|------|---------------|
| `content/01-boundary-and-patterns.xml` | Decision framework, five hybrid patterns, boundary-definition rules, tool count rule. |
| `content/02-translation-and-governance.xml` | Translation table, gate cadence rules, EVM gotcha, alignment script reference. |

## Templates

none
