# C4 Model for Software Architecture Visualization

The C4 model is a lean, hierarchical approach to software architecture diagramming created by Simon Brown. It provides a standardized way to visualize software systems at different levels of abstraction, making architecture accessible to both technical and non-technical stakeholders.

## Overview

C4 stands for **Context, Containers, Components, and Code** - four levels of abstraction that allow you to "zoom in" on a software system like Google Maps.

```
Level 0: System Landscape (optional)
         └─ All systems in the organization

Level 1: System Context
         └─ Your system + users + external systems

Level 2: Container
         └─ High-level technology choices (apps, DBs, queues)

Level 3: Component
         └─ Internal structure of a container

Level 4: Code (optional)
         └─ Class/module diagrams (usually auto-generated)
```

## The Four Core Levels

### Level 1: System Context Diagram

**Purpose:** Show the system in its environment - the "big picture"

**Audience:** Everyone (technical and non-technical)

**Elements:**
- Your software system (single box)
- Users/personas interacting with the system
- External systems your system depends on or integrates with

**Key Question:** "What is this system and who uses it?"

### Level 2: Container Diagram

**Purpose:** Show high-level technology decisions and how containers communicate

**Audience:** Software architects, developers

**Containers** are separately deployable/runnable units:
- Web applications (React, Angular, Vue)
- API services (REST, GraphQL, gRPC)
- Databases (PostgreSQL, MongoDB, Redis)
- Message brokers (Kafka, RabbitMQ)
- File storage (S3, GCS)
- Mobile apps (iOS, Android)

**Key Question:** "What are the main technology building blocks?"

### Level 3: Component Diagram

**Purpose:** Show internal structure within a single container

**Audience:** Developers working on that container

**Components** are major structural building blocks:
- Controllers/Handlers
- Services/Use Cases
- Repositories/Gateways
- Domain models

**Key Question:** "How is this container organized internally?"

### Level 4: Code Diagram

**Purpose:** UML class diagrams showing implementation details

**Audience:** Developers

**Recommendation:** Usually auto-generated from code (IDEs, reverse engineering tools). Manual creation rarely adds value.

## Supplementary Diagrams

Beyond the four core levels, C4 supports three supplementary diagram types:

### System Landscape Diagram (Level 0)

Shows all software systems within an enterprise/organization. Useful for:
- Portfolio views
- Enterprise architecture
- Understanding system dependencies across teams

### Dynamic Diagram

Shows how elements collaborate at runtime for specific use cases:
- Request flows
- Sequence of interactions
- Event propagation

### Deployment Diagram

Maps containers to infrastructure:
- Cloud regions/zones
- Kubernetes clusters
- Server instances
- Network boundaries

## Notation

### Element Types

| Element | Symbol | Description |
|---------|--------|-------------|
| Person | Stick figure or box | Human user |
| Software System | Box | System boundary |
| Container | Box with tech label | Deployable unit |
| Component | Box | Logical grouping |
| External System | Gray box | System outside scope |

### Relationship Arrows

| Arrow | Meaning |
|-------|---------|
| Solid arrow | Uses, calls, depends on |
| Labeled arrow | Protocol, technology, or purpose |

### Labels and Descriptions

Every element should have:
- **Name:** Clear, descriptive identifier
- **Technology:** Stack/framework (for containers/components)
- **Description:** Brief explanation of responsibility

```
[Container: API Service]
Technology: Python/FastAPI
Description: Handles authentication and user management
```

## Tooling Comparison

| Tool | Type | Best For | Pros | Cons |
|------|------|----------|------|------|
| **Structurizr DSL** | Text-based | Large teams, CI/CD | Model-based, versioned | Learning curve |
| **PlantUML C4** | Text-based | Quick diagrams | Familiar syntax | Limited styling |
| **Mermaid C4** | Text-based | Documentation | GitHub/GitLab native | Experimental |
| **draw.io** | Visual | One-off diagrams | Free, intuitive | Manual updates |
| **IcePanel** | Collaborative | Team modeling | Real-time, interactive | SaaS pricing |

### Structurizr DSL

The recommended tool by Simon Brown. Key features:
- Single model, multiple views
- Export to PlantUML, Mermaid, PNG, SVG
- Architecture decision records (ADRs)
- Documentation generation

### PlantUML C4 Extension

Community-maintained extension with:
- Pre-built C4 macros
- Sprite support
- Multiple layout options
- VS Code integration

### Mermaid C4 (Experimental)

Native support in:
- GitHub README/Wiki
- GitLab
- Notion
- Documentation tools

### draw.io

Visual editor with:
- C4 shape libraries
- Multi-page diagrams
- Export options
- Confluence integration

## Best Practices

### General Guidelines

1. **Start with Context** - Always begin at Level 1
2. **Zoom incrementally** - Don't skip levels
3. **One diagram per level** - Don't mix abstraction levels
4. **5-10 elements max** - Keep diagrams readable
5. **Label everything** - Names, technologies, descriptions
6. **Update regularly** - Treat diagrams as living documents

### Naming Conventions

```
System: "{Name} System" (e.g., "Banking System")
Container: "{Name}" + Technology (e.g., "Web App [React]")
Component: "{Name}" + Type (e.g., "User Service [Service]")
Person: Role-based name (e.g., "Customer", "Admin")
```

### Common Mistakes

| Mistake | Solution |
|---------|----------|
| Too many elements | Split into multiple diagrams |
| Missing technologies | Always specify tech stack |
| Vague descriptions | Use active verbs (handles, stores, sends) |
| Mixing levels | One abstraction level per diagram |
| Outdated diagrams | Integrate into CI/CD |

### When to Create Each Level

| Diagram | When to Create |
|---------|----------------|
| System Context | Always (mandatory) |
| Container | Always for non-trivial systems |
| Component | For complex containers or onboarding |
| Code | Only if auto-generated; skip otherwise |
| Deployment | For production systems |
| Dynamic | For complex workflows |

## LLM Usage Tips

### Generating Diagrams with AI

LLMs can assist with C4 diagram creation, but require careful prompting:

**Effective Approach:**
1. Provide clear system description
2. Specify desired output format (Structurizr DSL, PlantUML, Mermaid)
3. Request one level at a time
4. Validate against actual architecture

**Limitations:**
- LLMs may hallucinate APIs or patterns
- Over-recommend complex architectures (microservices) for simple systems
- Output quality varies significantly with prompt wording

**Best LLMs for C4 (2025):**
- Claude performs well for Structurizr DSL and PlantUML syntax
- GPT-4 handles Mermaid syntax effectively
- All major LLMs can generate reasonable Level 1-2 diagrams

### Prompting Patterns

**System-first pattern:**
```
Given this system description: [description]
Generate a C4 [level] diagram in [format] showing:
- Main elements and their technologies
- Relationships with protocols/purposes
- Brief descriptions for each element
```

**Iterative refinement:**
```
Current diagram: [paste diagram code]
Improve by: [specific feedback]
Keep the same format and style.
```

See [llm-prompts.md](llm-prompts.md) for complete prompt templates.

## Documentation as Code

### Git Workflow

```
repository/
├── docs/
│   └── architecture/
│       ├── workspace.dsl      # Structurizr model
│       ├── diagrams/          # Generated images
│       └── decisions/         # ADRs
├── .github/
│   └── workflows/
│       └── diagrams.yml       # Auto-generation
```

### CI/CD Integration

1. Store diagram source in version control
2. Generate images on commit/PR
3. Publish to documentation site
4. Validate syntax in CI

### Living Documentation

- Link diagrams in README/documentation
- Reference in ADRs
- Update during architecture reviews
- Include in onboarding materials

## Files in This Directory

| File | Description |
|------|-------------|
| [README.md](README.md) | This overview document |
| [checklist.md](checklist.md) | Step-by-step checklist for creating C4 diagrams |
| [examples.md](examples.md) | Real-world case studies and diagram examples |
| [templates.md](templates.md) | Copy-paste templates (Structurizr, PlantUML, Mermaid) |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for AI-assisted diagram creation |

## External Resources

### Official

- [C4 Model Official Site](https://c4model.com/) - Simon Brown's authoritative guide
- [Structurizr](https://structurizr.com/) - Official tooling by Simon Brown
- [Structurizr DSL Documentation](https://docs.structurizr.com/dsl)

### Tools

- [C4-PlantUML GitHub](https://github.com/plantuml-stdlib/C4-PlantUML) - PlantUML extension
- [Mermaid C4 Docs](https://mermaid.js.org/syntax/c4.html) - Mermaid syntax reference
- [draw.io C4 Blog](https://www.drawio.com/blog/c4-modelling) - Visual editor guide

### Learning

- [The C4 Model Book (O'Reilly, 2026)](https://www.oreilly.com/library/view/the-c4-model/9798341660113/) - Upcoming book by Simon Brown
- [IcePanel C4 E-book](https://icepanel.io/blog/2025-11-26-ebook-communicating-architecture-with-the-c4-model) - Free downloadable guide
- [FreeCodeCamp C4 Tutorial](https://www.freecodecamp.org/news/how-to-create-software-architecture-diagrams-using-the-c4-model/) - Step-by-step guide

### GitHub Examples

- [c4-structurizr-llm-assistant](https://github.com/michaeltschreiber/c4-structurizr-llm-assistant) - LLM assistant for C4
- [GoDataDriven C4 Example](https://github.com/godatadriven/c4-model-example) - Complete Structurizr example
- [c4-draw.io Templates](https://github.com/kaminzo/c4-draw.io) - draw.io shape libraries

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [Architecture Decision Records](../architecture-decision-records.md) | Document decisions referenced in diagrams |
| [System Design Process](../system-design-process/) | Use C4 during design |
| [Microservices Architecture](../microservices-architecture/) | Container diagrams for services |
| [Event-Driven Architecture](../event-driven-architecture/) | Dynamic diagrams for events |
