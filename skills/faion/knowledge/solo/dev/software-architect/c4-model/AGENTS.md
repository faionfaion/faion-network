# C4 Model

## Summary

The C4 model is a hierarchical diagramming approach for software architecture: Context (system + users + external systems), Containers (deployable units + technology choices), Components (internal structure of one container), and Code (class diagrams, usually auto-generated). Each level zooms into the previous one. Always start at Level 1; create Level 4 only from auto-generation tools. Keep each diagram to 5–10 elements — split rather than crowd.

## Why

Architecture diagrams created ad-hoc are inconsistent in abstraction level, notation, and scope, making them unusable for communication. C4 provides a shared vocabulary (Person, Software System, Container, Component) and a zoom protocol that both technical and non-technical stakeholders can navigate. Diagrams stored as code (Structurizr DSL, PlantUML, Mermaid) in version control stay synchronized with the architecture and can be generated in CI/CD.

## When To Use

- Onboarding new contributors: Level 1 (Context) and Level 2 (Container) are mandatory
- Architecture review: create diagrams to communicate current and target state
- Documenting microservices topology: Container diagram shows services, databases, message brokers
- Recording decisions in ADRs: reference C4 diagrams for the affected components
- Sprint planning for cross-team features that touch multiple containers or external systems
- Deployment diagrams for mapping containers to cloud infrastructure

## When NOT To Use

- Single-developer scripts or single-container applications where a simple README suffices
- When diagrams would be discarded immediately — invest only if they will be maintained
- Level 4 (Code) diagrams done manually — use IDE class diagram generation instead
- As a substitute for ADRs: C4 shows structure, ADRs document the decisions behind structure
- When the team has agreed on a different diagramming standard already in use — don't introduce C4 mid-project without buy-in

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-levels.xml` | Level 1 (Context), Level 2 (Container), Level 3 (Component), Level 4 (Code) — purpose, audience, elements, key question for each |
| `content/02-supplementary-diagrams.xml` | System Landscape, Dynamic, and Deployment diagrams — when to use each |
| `content/03-tooling-and-practices.xml` | Structurizr DSL, PlantUML C4, Mermaid C4, draw.io compared; notation conventions; documentation-as-code CI/CD pattern; common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/structurizr-workspace.dsl` | Structurizr DSL workspace with Context and Container levels wired up |
| `templates/plantuml-context.puml` | PlantUML C4 Context diagram template with Person, System, and External System |
| `templates/mermaid-container.md` | Mermaid C4 Container diagram template (GitHub/GitLab-native) |
