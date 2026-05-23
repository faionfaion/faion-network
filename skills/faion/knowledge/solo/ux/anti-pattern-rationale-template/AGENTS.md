---
slug: anti-pattern-rationale-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Records every UX anti-pattern discovery as a versioned artefact with named owner, evidence, and re-occurrence triggers so the same anti-pattern is not re-litigated in the next sprint.
content_id: "5376be92c89c5f2a"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: ["ux", "anti-pattern", "pattern-bank", "design-decision", "rationale"]
---
# Anti-Pattern Rationale Template

## Summary

**One-sentence:** Records every UX anti-pattern discovery as a versioned artefact with named owner, evidence, and re-occurrence triggers so the same anti-pattern is not re-litigated in the next sprint.

**One-paragraph:** Codified template that turns the recurring inspiration / patterns capture loop into a decision-record artefact: each anti-pattern carries its UI surface, observed user behaviour, evidence link, hypothesis-for-cause, and a named owner. The rationale section forces a sourced explanation grounded in inputs; the version + last_reviewed pair keeps the bank fresh.

**Ефективно для:**

- Solo founder running periodic competitive scans who needs a stable artefact shape per finding.
- Design-review rituals where the same anti-pattern keeps surfacing and nobody remembers the prior verdict.
- Onboarding handoff to a new agent or designer that needs the bank as ground truth.
- AI-generated UI reviews where the agent must cite an artefact rather than free-prose.

## Applies If (ALL must hold)

- Designer or agent has at least 1 anti-pattern instance captured in the last 30 days.
- Bank is stored in a single source-of-truth repository (repo, Notion, Figma sidekick).
- A named owner exists who can be cited as the artefact maintainer.
- Downstream consumer (review agent, design ticket, audit) needs to read the artefacts.

## Skip If (ANY kills it)

- No bank exists and there is no plan to maintain one — start with inspiration capture playbook first.
- Single-pattern bug is being fixed inline and will not be revisited.
- Compliance-grade audit shape is required; use formal accessibility review process instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Anti-pattern instance + screenshot | image + caption | Figma comments / screen capture |
| UI surface name + route | string | App URL or design canvas |
| Evidence link to user behaviour | URL | Session replay / research notes |
| Owner handle | string | Designer / agent registry |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/prototyping` | Prototype context that surfaced the anti-pattern. |
| `solo/ux/heuristic-eval-severity-rubric` | Severity scoring used to triage the anti-pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-anti-pattern-record` | sonnet | Per-instance judgement on UI surface, evidence, hypothesis. |
| `bank-dedupe-pass` | haiku | Deterministic similarity check against existing artefacts. |
| `cross-pattern-rationale-audit` | opus | Spot systemic patterns across 20+ entries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/anti-pattern-rationale-template.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/anti-pattern-rationale-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-pattern-rationale-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[pattern-bank-tagging-schema]]
- [[heuristic-eval-severity-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
