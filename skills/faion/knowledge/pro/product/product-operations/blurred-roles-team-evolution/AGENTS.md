# Blurred Roles and Team Evolution

## Summary

Modern AI-era product teams operate as overlapping Venn diagrams rather than relay-race handoffs.
Each role (PM, designer, engineer, data) is expected to hold fluency in adjacent disciplines.
The ratio shifts toward more PMs relative to engineers as discovery, evals, and prioritization
become the bottleneck — not coding. Every overlap zone must have one human DRI; agents fill the
zone but do not own the decision.

## Why

Handoff-based structures slow AI-era development. When models can code at scale, the bottleneck
moves upstream to discovery, evaluation, and judgment calls. Cross-functional fluency — not
specialization in isolation — is what allows a small team to out-learn a large one. Andrew Ng's
"2 PMs : 1 Engineer" inversion captures the ratio shift; the Venn metaphor captures the operating
model shift.

## When To Use

- Designing or auditing role splits for an AI-augmented product team
- Migrating a relay-race workflow (spec → design → eng → QA) into overlapping ownership
- Framing solopreneur staffing: which roles to absorb, delegate to agents, or keep as a human hire
- Calibrating PM:Engineer ratios when agent throughput shifts the bottleneck to discovery
- Writing role descriptions or hiring scorecards that assume cross-disciplinary fluency

## When NOT To Use

- Heavily regulated environments (medical devices, aerospace, SOX, IEC 62304) where role
  separation is a compliance requirement — blurring violates the audit trail
- Large-scale orgs (>50 engineers) with established RACI — this is a future-state model, not
  a refactor playbook
- Performance-management decisions — this is an operating-model lens, not a competency framework
- Day-to-day task assignment within a single sprint — use a normal queue/board

## Content

| File | What's inside |
|------|---------------|
| `content/01-model.xml` | Venn-diagram team model, skill table, PM:Engineer ratio insight |
| `content/02-agent-usage.xml` | Agentic workflow, role-persona subagent pattern, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/role-overlap.sh` | Bash script: emit per-author file-area distribution from git history |

## Scripts

none
