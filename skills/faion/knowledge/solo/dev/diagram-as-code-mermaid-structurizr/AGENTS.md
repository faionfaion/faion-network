---
slug: diagram-as-code-mermaid-structurizr
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pattern for keeping architecture diagrams in version control as text (Mermaid for inline docs, Structurizr DSL for C4 models); produces a diagrams directory with a render script, a lint pass, and a doc-link policy preventing drift."
content_id: "ab6daed372e7fccd"
complexity: medium
produces: code
est_tokens: 4900
tags: ["dev", "solo", "diagrams", "mermaid", "structurizr", "documentation"]
---
# Diagram-as-Code with Mermaid / Structurizr

## Summary

**One-sentence:** Pattern for keeping architecture diagrams in version control as text (Mermaid for inline docs, Structurizr DSL for C4 models); produces a diagrams directory with a render script, a lint pass, and a doc-link policy preventing drift.

**One-paragraph:** Pattern for keeping architecture diagrams in version control as text (Mermaid for inline docs, Structurizr DSL for C4 models); produces a diagrams directory with a render script, a lint pass, and a doc-link policy preventing drift. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- C4-style system context and container diagrams for distributed services.
- Sequence diagrams for tricky auth flows or webhook handshakes.
- Entity-relationship diagrams alongside schema files.
- Solo founders who cannot maintain a parallel design tool.

## Applies If (ALL must hold)

- Project has ≥1 architecture diagram currently maintained as PNG / Figma / Lucid that drifts from code.
- Authors can read+write Markdown.
- CI can run a small renderer (mermaid-cli, structurizr-cli) without proprietary licenses.
- Diagrams are referenced from prose docs that live in the same repo.

## Skip If (ANY kills it)

- Diagrams are throw-away brainstorm artefacts — overhead exceeds value.
- Visual fidelity (logos, screenshots, animations) is the deliverable — DSLs cannot match.
- Org mandates a specific diagramming tool incompatible with text formats (e.g. tied to Visio).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[diagram-as-code-mermaid-structurizr]] | upstream context this methodology builds on |
| [[changelog-automation-conventional-commits]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-diagram-as-code-mermaid-structurizr-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-diagram-as-code-mermaid-structurizr.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-diagram-as-code-mermaid-structurizr.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[diagram-as-code-mermaid-structurizr]]
- [[changelog-automation-conventional-commits]]
- [[ci-quality-gate-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
