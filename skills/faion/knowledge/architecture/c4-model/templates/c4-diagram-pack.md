<!--
purpose: C4 diagram-pack spec.
consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
produces: a c4-model artefact validating against scripts/validate-c4-model.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400-1500 tokens once filled
variables:
  - name: system_name
    type: string
    required: true
    description: The system this pack describes, kebab-case. Use the name the deploy manifest uses - the CI check compares the L2 container list against that manifest and a different spelling means it silently matches nothing.
  - name: owner
    type: string
    required: true
    description: The person accountable for keeping these diagrams true. C4 diagrams rot within weeks of a deploy; an unowned pack is a screenshot of a system that has since changed shape.
  - name: email
    type: string
    required: true
    description: The owner's email, reachable after they change teams. This is the address the next engineer writes to before undoing what this document decided.
  - name: date
    type: string
    required: true
    description: The day this was agreed, ISO - not the day it was typed up. Downstream reviews are scheduled off it, so a placeholder date silently disables the review.
  - name: toolchain
    type: enum
    required: true
    options: [structurizr, mermaid, plantuml]
    description: Which source format the team will actually maintain, not the prettiest. mermaid renders in GitHub with no build step; structurizr gives one model and four views but needs a workspace file; plantuml needs a renderer in CI.
  - name: diagram_ext
    type: string
    required: true
    default: "mmd"
    description: File extension for the diagram sources - mmd for mermaid, dsl for structurizr, puml for plantuml. It must match the toolchain or the lint step finds no diagrams and passes silently.
  - name: container_manifest
    type: path
    required: true
    description: Path to the deploy manifest the CI lint compares the Level 2 container list against. Without a real path the sync policy below is a promise instead of a gate.
-->
---
artefact_id: c4-pack-{{system_name}}-{{date}}
owner: {{owner}} <{{email}}>
version: 1.0.0
last_reviewed: {{date}}
toolchain: {{toolchain}}
---

## Level 1 — System Context

- Path: `docs/architecture/c4/01-context.{{diagram_ext}}`
- Audience: non-technical stakeholders, leadership.
- Includes: system, users, external systems.

## Level 2 — Containers

- Path: `docs/architecture/c4/02-containers.{{diagram_ext}}`
- Audience: engineers, ops.
- Includes: deployable units + their technology stack + relationships.

## Level 3 — Components (per container)

- Path: `docs/architecture/c4/03-components-[container].{{diagram_ext}}`
- Audience: engineers working on this container.
- Includes: components inside one container + relationships.

## Sync policy

- Diagrams live in `docs/architecture/c4/` and ship in every PR that adds/removes a container or external system.
- CI lint compares the container list in L2 against `{{container_manifest}}`; mismatch blocks merge.
