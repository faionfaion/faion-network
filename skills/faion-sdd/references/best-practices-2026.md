# SDD Best Practices 2026

Research compilation on Specification-Driven Development and documentation best practices for 2025-2026.

**Research Date:** 2026-01-19
**Sources:** Thoughtworks, Martin Fowler, AWS, Google Cloud, Microsoft, Red Hat, Pragmatic Engineer

---

## Table of Contents

1. [M-SDD-013: AI-Assisted Specification Writing](#m-sdd-013-ai-assisted-specification-writing)
2. [M-SDD-014: Living Documentation (Docs-as-Code)](#m-sdd-014-living-documentation-docs-as-code)
3. [M-SDD-015: Architecture Decision Records (ADR)](#m-sdd-015-architecture-decision-records-adr)
4. [M-SDD-016: API-First Development](#m-sdd-016-api-first-development)
5. [M-SDD-017: Design Docs Patterns (Big Tech)](#m-sdd-017-design-docs-patterns-big-tech)
6. [Key Trends Summary](#key-trends-summary)
7. [Sources](#sources)

---

## M-SDD-013: AI-Assisted Specification Writing

### Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-013 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #ai, #specifications, #llm |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

### Problem

Traditional specification writing is slow, inconsistent, and often neglected. Developers struggle to articulate requirements clearly, leading to:
- Ambiguous requirements causing implementation delays
- Inconsistent spec formats across teams
- Specifications that become outdated immediately
- Bottleneck shifted from implementation to specification

**Key insight from 2025:** "AI can handle much of the implementation, and suddenly the bottleneck has shifted upstream" - specification skills have atrophied.

---

### Framework

#### The SDD-AI Workflow (2025)

```
INTENT → SPEC → PLAN → EXECUTION → REVIEW
   ↓        ↓       ↓         ↓          ↓
 human    AI+human  AI      AI agent   human
 input   collab   generate  execute    verify
```

#### Core Principles

1. **Specification First** - Expected behaviors, edge cases, and constraints captured upfront
2. **One Source of Truth** - Spec anchors entire project (tests, docs, design trace back)
3. **Built-in Testability** - Spec defines "what done looks like"
4. **Iterative by Design** - Specs evolve with feedback, maintaining traceability

#### AI-Assisted Spec Writing Process

| Phase | Human Role | AI Role |
|-------|------------|---------|
| Intent capture | Describe problem, constraints | Structure and clarify |
| Requirement extraction | Validate completeness | Generate from context |
| Edge case identification | Confirm relevance | Enumerate possibilities |
| Acceptance criteria | Approve criteria | Draft testable conditions |
| Format standardization | Choose format | Apply template consistently |

#### Supported Formats

- **Natural language** (most common)
- **Structured formats** (YAML, JSON, Markdown)
- **Formal specifications** (OpenAPI, JSON Schema for APIs)
- **BDD format** (Given-When-Then)

---

### Templates

#### AI Prompt for Spec Generation

```markdown
Generate a specification for [FEATURE_NAME]:

**Context:**
- Product: [product description]
- Target users: [user personas]
- Constraints: [technical/business constraints]

**Requirements:**
1. Generate functional requirements (FR-X format)
2. Identify edge cases
3. Write acceptance criteria
4. Note dependencies
5. Flag potential risks

**Format:** Use standard spec.md template
```

#### Spec Review Checklist (AI-Assisted)

```markdown
## AI Spec Review

- [ ] All functional requirements have acceptance criteria
- [ ] Edge cases identified and documented
- [ ] Dependencies explicitly listed
- [ ] Constraints are testable/measurable
- [ ] Scope is clearly bounded (what's NOT included)
- [ ] User stories follow format: As [user], I want [action], so that [benefit]
```

---

### Best Practices

| Practice | Description |
|----------|-------------|
| **Tight scoping** | Keep specs focused; use multiple specs for different concerns (arch, docs, testing) |
| **Lessons learned file** | Maintain file AI learns from past hiccups |
| **Sprint integration** | Include spec requirements in user stories; schedule spec writing in sprint planning |
| **Iterative refinement** | Start with rough spec, refine through AI dialogue |
| **Human approval gates** | All AI-generated specs require human review before implementation |

---

### Tools (2025-2026)

| Tool | Type | Key Features |
|------|------|--------------|
| **AWS Kiro** | Enterprise IDE | 3-phase: Specify → Plan → Execute; AWS integration |
| **Claude Code** | CLI Agent | Long context, autonomous coding, Git integration |
| **GitHub Spec-Kit** | Extension | GitHub-native spec workflow |
| **Cursor** | AI IDE | Inline spec editing |
| **Windsurf** | AI IDE | Multi-file spec awareness |

---

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting AI spec without review | Always verify AI-generated specs against domain knowledge |
| Over-relying on AI for domain context | Provide rich context; AI lacks your business knowledge |
| Specs too large for context window | Break into focused, modular specs |
| Ignoring AI suggestions | Review all suggestions; AI catches edge cases humans miss |

---

## M-SDD-014: Living Documentation (Docs-as-Code)

### Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-014 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #documentation, #automation, #ci-cd |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

### Problem

Documentation becomes outdated immediately after creation:
- 4-week average time to manually create technical documents
- Documentation diverges from actual implementation
- "Documentation debt" accumulates rapidly
- Static docs in wikis become graveyard of outdated info

---

### Framework

#### Docs-as-Code Principles

1. **Treat docs like code** - Same systems, processes, workflows
2. **Version control** - Store in Git alongside source code
3. **CI/CD integration** - Auto-build, lint, validate on every commit
4. **Single source of truth** - Generate from code where possible

#### Living Documentation Types

```
GENERATED FROM CODE          MAINTAINED MANUALLY
─────────────────────        ──────────────────
API reference (OpenAPI)      Architecture decisions
Code comments → docs         Design rationale
Test specs → examples        User guides
Type definitions             Tutorials
Changelogs (from commits)    Onboarding docs
```

#### Automation Pipeline

```
Code Change
    ↓
┌──────────────────────────────────────┐
│ CI/CD Pipeline                       │
│ ├── Lint docs (Spectral, Vale)       │
│ ├── Validate links                   │
│ ├── Generate API docs                │
│ ├── Build documentation site         │
│ ├── Run doc tests                    │
│ └── Deploy to hosting                │
└──────────────────────────────────────┘
    ↓
Updated Documentation
```

---

### Templates

#### Documentation CI Pipeline (.github/workflows/docs.yml)

```yaml
name: Documentation CI

on:
  push:
    paths:
      - 'docs/**'
      - 'src/**'
      - 'openapi.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        uses: stoplightio/spectral-action@v0.8
        with:
          file_glob: 'openapi.yaml'

      - name: Check broken links
        uses: gaurav-nelson/github-action-markdown-link-check@v1

      - name: Build docs
        run: npm run docs:build

      - name: Deploy to Backstage
        if: github.ref == 'refs/heads/main'
        run: npm run docs:deploy
```

#### LLM-Ready Documentation Structure

```markdown
# [Component Name]

## Summary
[1-2 sentence description for LLM context]

## Quick Start
[Code example that works immediately]

## API Reference
[Auto-generated from OpenAPI/code]

## Architecture
[Human-maintained design decisions]

## Changelog
[Auto-generated from commits]

---
*Last updated: [AUTO-DATE]*
*Generated from: [SOURCE_FILE]*
```

---

### Best Practices

| Practice | Description |
|----------|-------------|
| **Build artifacts** | Treat docs as build artifacts requiring CI/CD discipline |
| **Centralized storage** | Store in Backstage, GitBook, or similar developer portal |
| **Auto-rebuild** | Rebuild on code changes (ReadTheDocs, GitHub Actions) |
| **LLM-optimized** | Provide markdown versions for AI assistants (Cursor, Copilot) |
| **Test your docs** | Validate code examples actually run |

---

### Tools (2025-2026)

| Category | Tools |
|----------|-------|
| **Generators** | Doxygen 1.15, Sphinx 8.2, JSDoc, TypeDoc |
| **Platforms** | Mintlify, GitBook, ReadTheDocs, Backstage |
| **Linters** | Spectral (API), Vale (prose), markdownlint |
| **AI-assisted** | doc-comments-ai, ai-doc-gen, Mintlify AI |

---

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Docs separate from code | Co-locate documentation with source code |
| Manual API doc updates | Generate from OpenAPI spec automatically |
| No link validation | Add link checker to CI pipeline |
| Docs not searchable | Index in developer portal with full-text search |

---

## M-SDD-015: Architecture Decision Records (ADR)

### Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-015 |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #architecture, #adr, #decisions |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

### Problem

Architecture decisions are lost over time:
- New team members don't understand "why" of existing design
- Same discussions repeated without historical context
- Production incidents lack design context
- Decisions seem "puzzling" without knowing when/why they were made

---

### Framework

#### What is an ADR?

A document capturing an important architectural decision along with its context and consequences.

#### ADR Structure (Nygard Format)

```
┌─────────────────────────────────────┐
│ TITLE: Short decision description   │
├─────────────────────────────────────┤
│ STATUS: Proposed│Accepted│Deprecated│
├─────────────────────────────────────┤
│ CONTEXT: What is the situation?     │
├─────────────────────────────────────┤
│ DECISION: What did we decide?       │
├─────────────────────────────────────┤
│ CONSEQUENCES: What results from it? │
└─────────────────────────────────────┘
```

#### ADR Lifecycle

```
PROPOSED → ACCEPTED → [DEPRECATED | SUPERSEDED]
    ↓          ↓              ↓
  Review    Active        Link to new ADR
  period    decision
```

#### Status Types

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion, gathering feedback |
| **Accepted** | Approved, active decision |
| **Deprecated** | No longer relevant, kept for history |
| **Superseded** | Replaced by newer ADR (link required) |

---

### Templates

#### ADR Template (docs/adr/NNN-title.md)

```markdown
# ADR-NNN: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Deciders:** [List of people involved]

## Context

[What is the issue? What forces are at play?
Include technical, business, and team constraints.]

## Decision

[What is the change being proposed/made?
State in full sentences with active voice: "We will..."]

## Alternatives Considered

### Alternative 1: [Name]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why rejected:** [reason]

### Alternative 2: [Name]
...

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Risk to mitigate]

### Neutral
- [Implication neither good nor bad]

## Related Decisions

- ADR-NNN: [Related decision]
- ADR-NNN: [Supersedes this if applicable]

## Notes

[Any additional context, meeting notes, or future considerations]
```

#### ADR Review Meeting Template

```markdown
# ADR Review: ADR-NNN

**Date:** YYYY-MM-DD
**Duration:** 30 min (10 min silent read, 20 min discussion)
**Attendees:** [Keep under 10 people]

## Reading Period (10 min)
- Read the ADR silently
- Add inline comments to specific sections

## Discussion Points
1. [Comment/question from review]
2. [Comment/question from review]

## Decision
- [ ] Approved as-is
- [ ] Approved with changes: [list changes]
- [ ] Needs revision: [list concerns]
- [ ] Rejected: [reason]

## Action Items
- [ ] [Action] - @owner - due date
```

---

### Best Practices

| Practice | Description |
|----------|-------------|
| **Co-locate with code** | Store in `docs/adr/` in same repo |
| **Sequential numbering** | Use NNN format (001, 002...) |
| **Immutable by default** | Prefer new ADR over editing existing |
| **Timestamp everything** | Include date and system version |
| **Keep pithy** | Focus on decision, not design guide |
| **Single decision focus** | One ADR = one decision |
| **Cross-functional review** | Involve affected teams (under 10 people) |
| **Silent reading** | Amazon-style: 10 min read, then discuss |

---

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| ADR as design guide | Keep focused on decision, not implementation details |
| Not updating status | Mark superseded ADRs, link to replacement |
| Missing alternatives | Always document what you considered and rejected |
| No timestamps | Include date for historical context |
| Hidden in wiki | Store in version control with code |

---

### Sources

- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Google Cloud ADR Overview](https://cloud.google.com/architecture/architecture-decision-records)
- [Microsoft Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [adr.github.io](https://adr.github.io/)

---

## M-SDD-016: API-First Development

### Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-016 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #api, #openapi, #contract-testing |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

### Problem

APIs designed after implementation lead to:
- Inconsistent API designs across services
- Breaking changes for consumers
- Documentation that doesn't match reality
- Delayed frontend/mobile development waiting for backend

---

### Framework

#### API-First Principles

1. **Design before code** - API contract is first artifact
2. **Contract as source of truth** - Generate code, tests, docs from spec
3. **Consumer-driven** - Design for API consumers, not implementation convenience
4. **Shift-left testing** - Mock servers enable parallel development

#### API-First Workflow

```
DESIGN → VALIDATE → MOCK → IMPLEMENT → TEST → DEPLOY
   ↓         ↓        ↓         ↓         ↓
OpenAPI   Spectral  Prism    codegen   contract
  spec     linting  server   from spec   tests
```

#### OpenAPI 3.1 Key Features (2021+)

| Feature | Description |
|---------|-------------|
| **JSON Schema alignment** | Full JSON Schema vocabularies support |
| **Webhooks** | New top-level element for event-driven APIs |
| **$ref improvements** | Better reference handling |
| **Nullable simplification** | Use `type: ['string', 'null']` |

---

### Templates

#### OpenAPI 3.1 Specification Template

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: |
    [Brief API description]

    ## Authentication
    [Auth method description]

    ## Rate Limiting
    [Rate limit details]
  contact:
    name: [Team Name]
    email: [team@example.com]

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      tags:
        - Resources
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Resource:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 100
        createdAt:
          type: string
          format: date-time

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

#### CI/CD Pipeline for API-First

```yaml
name: API Contract CI

on:
  push:
    paths:
      - 'openapi.yaml'
      - 'src/api/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        run: npx @stoplight/spectral-cli lint openapi.yaml

      - name: Generate mock server
        run: npx @stoplight/prism-cli mock openapi.yaml &

      - name: Run contract tests
        run: npm run test:contract

      - name: Generate SDK
        run: npx openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o sdk/
```

---

### Best Practices

| Practice | Description |
|----------|-------------|
| **Spectral linting** | Validate specs with industry-standard rules |
| **Mock server deployment** | Generate temporary servers for frontend testing |
| **Contract testing** | Ensure backend matches API contract |
| **Security scanning** | Integrate OWASP ZAP in pipeline |
| **SDK generation** | Auto-generate client libraries from spec |
| **Version in URL** | Use `/v1/`, `/v2/` for breaking changes |

---

### Tools (2025-2026)

| Category | Tools |
|----------|-------|
| **Specification** | OpenAPI 3.1, AsyncAPI (events) |
| **Linting** | Spectral, Redocly |
| **Mocking** | Prism, WireMock |
| **Documentation** | Swagger UI, Redoc, Stoplight |
| **Code generation** | openapi-generator, openapi-stack |
| **Contract testing** | Pact, Dredd |

---

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Spec written after code | Design spec first, generate code from it |
| No versioning strategy | Plan for v1, v2 from the start |
| Missing error schemas | Define all error response formats |
| No examples | Include request/response examples in spec |

---

## M-SDD-017: Design Docs Patterns (Big Tech)

### Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-017 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #design-docs, #rfc, #google, #uber |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

### Problem

Design docs written without structure lead to:
- Inconsistent quality across teams
- Missing critical considerations
- Difficult cross-team review
- No clear approval process

---

### Framework

#### Design Doc Purpose

"Our job is not to produce code per se, but rather to solve problems. Unstructured text may be the better tool for solving problems early when changes are still cheap."

#### Design Doc Functions

1. **Early issue identification** - Catch design issues when changes are cheap
2. **Consensus building** - Achieve agreement across organization
3. **Knowledge sharing** - Document decisions for future team members
4. **Onboarding** - Help new engineers understand system

#### Company Approaches

| Company | Name | Key Features |
|---------|------|--------------|
| **Google** | Design Doc | Informal, collaborative, focuses on "why" |
| **Uber** | ERD (Engineering Review Doc) | Formal approvers, service SLAs required |
| **Amazon** | 6-pager | Narrative format, silent reading |
| **Rust/OSS** | RFC | Community feedback, explicit process |

#### Uber RFC/ERD Process

```
AUTHOR WRITES → CIRCULATE → COLLECT FEEDBACK → APPROVE → IMPLEMENT
                    ↓              ↓               ↓
               Mailing list   Comments in doc   Approvers sign
               (segmented)    Add objections    or object
```

---

### Templates

#### Design Doc Template (Google-style)

```markdown
# Design Doc: [Project Name]

**Author:** [Name]
**Reviewers:** [Names]
**Status:** Draft | In Review | Approved | Implemented
**Last Updated:** YYYY-MM-DD

---

## Overview

[1-2 paragraphs describing what this doc covers and why it exists]

## Context and Scope

### Background
[What led to this design being needed?]

### Goals
- [Goal 1]
- [Goal 2]

### Non-Goals
- [Explicitly what this design does NOT address]

## Design

### System Overview
[High-level architecture diagram and description]

### Detailed Design

#### Component A
[Details about component A]

#### Component B
[Details about component B]

### Data Model
[Database schema, data structures]

### API
[API endpoints, contracts]

## Alternatives Considered

### Alternative 1: [Name]
[Description]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why not chosen:** [reason]

### Alternative 2: [Name]
...

## Cross-cutting Concerns

### Security
[Security implications and mitigations]

### Privacy
[Data privacy considerations]

### Scalability
[How design handles growth]

### Monitoring
[Observability, alerting]

## Timeline and Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Design approval | YYYY-MM-DD | [ ] |
| Phase 1 complete | YYYY-MM-DD | [ ] |
| Launch | YYYY-MM-DD | [ ] |

## Open Questions

1. [Unresolved question 1]
2. [Unresolved question 2]

## References

- [Link to related docs]
- [Link to ADRs]
```

#### RFC Template (Uber-style)

```markdown
# RFC: [Title]

**RFC Number:** RFC-NNN
**Author:** [Name]
**Status:** Draft | Review | Approved | Rejected
**Created:** YYYY-MM-DD
**Approvers:** [List of required approvers]

---

## Summary

[One paragraph summary of the proposal]

## Motivation

[Why are we doing this? What problem does it solve?]

## Proposal

### Overview
[High-level description of proposed solution]

### Detailed Design
[Technical details of the implementation]

### Service SLAs (if applicable)
| Metric | Target |
|--------|--------|
| Availability | 99.9% |
| P99 Latency | <100ms |
| Throughput | 1000 RPS |

### Dependencies
- [External service/library 1]
- [External service/library 2]

### Rollout Plan
1. [Phase 1]
2. [Phase 2]
3. [Phase 3]

## Alternatives

### Alternative 1
[Description and why rejected]

## Security Considerations

[Security analysis]

## Operational Considerations

[Deployment, monitoring, rollback]

## Timeline

| Phase | Description | Target |
|-------|-------------|--------|
| 1 | [Description] | Q1 2026 |
| 2 | [Description] | Q2 2026 |

## Approvals

| Approver | Team | Status | Date |
|----------|------|--------|------|
| [Name] | [Team] | [ ] | |
| [Name] | [Team] | [ ] | |
```

---

### Best Practices

| Practice | Description |
|----------|-------------|
| **Silent reading** | Start review meetings with 10-15 min reading |
| **Inline comments** | Comment on specific sections, not general feedback |
| **Explicit approvers** | Define who must sign off |
| **Segmented distribution** | Send to relevant mailing lists only |
| **Templates by type** | Different templates for services, libraries, policies |
| **Keep it short** | 2-5 pages typically; longer needs justification |

---

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Design doc as spec | Keep separate: design doc (why/how), spec (what) |
| No alternatives section | Always document what you considered |
| Writing after implementation | Write before coding; cheap to change |
| Too many approvers | Keep under 10 participants |

---

## Key Trends Summary

### 2025-2026 Specification-Driven Development

1. **AI as specification partner** - LLMs help structure and complete specs, but humans remain accountable
2. **Bottleneck shift** - Implementation is commoditized; specification skills are premium
3. **Tool explosion** - 15+ major SDD platforms launched 2024-2025
4. **Workflow standardization** - Intent → Spec → Plan → Execute → Review pattern universal

### Living Documentation

1. **Docs-as-Code mainstream** - Version control, CI/CD for documentation
2. **LLM-optimized docs** - Markdown for AI assistants (Cursor, Copilot)
3. **Auto-generation mature** - API docs, code docs generated from source
4. **Developer portals** - Backstage, GitBook as central hubs

### Architecture Decisions

1. **ADRs standard practice** - Adopted across AWS, Google Cloud, Microsoft
2. **Immutability preferred** - New ADRs over editing existing
3. **Co-location with code** - Store in `docs/adr/` in repo
4. **Amazon-style reviews** - Silent reading before discussion

### API Development

1. **API-First mandatory** - Design before implementation
2. **OpenAPI 3.1** - JSON Schema alignment, webhooks support
3. **Contract testing** - Automated verification against spec
4. **Mock-first frontend** - Parallel development enabled

---

## Sources

### Specification-Driven Development
- [Thoughtworks: Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: SDD Tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Microsoft: Spec-Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [JetBrains: Spec-Driven Approach](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/)
- [Red Hat: SDD Quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Scott Logic: Specification Renaissance](https://blog.scottlogic.com/2025/12/15/the-specification-renaissance-skills-and-mindset-for-spec-driven-development.html)

### Living Documentation
- [Augment Code: Auto Document](https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices)
- [Squarespace: Docs-as-Code Journey](https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey)
- [Mintlify](https://www.mintlify.com/)
- [GitBook: LLM-Ready Docs](https://gitbook.com/docs/publishing-documentation/llm-ready-docs)
- [Medium: Living Documentation](https://medium.com/@rasmus-haapaniemi/living-documentation-how-to-let-your-documentation-grow-naturally-and-be-self-sustainable-24feac57a041)

### Architecture Decision Records
- [AWS Architecture Blog: ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Google Cloud: ADR Overview](https://cloud.google.com/architecture/architecture-decision-records)
- [Microsoft: Azure ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub](https://adr.github.io/)
- [UK GOV: ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)

### API-First Development
- [Baeldung: API First with Spring Boot](https://www.baeldung.com/spring-boot-openapi-api-first-development)
- [DevGuide: Contract-First](https://devguide.dev/blog/contract-first-api-development)
- [OpenAPI Specification 3.1](https://swagger.io/specification/)
- [openapi-stack](https://github.com/openapistack)
- [Fern: API-First Platforms](https://buildwithfern.com/post/api-first-development-platforms)

### Design Docs & RFCs
- [Pragmatic Engineer: RFCs and Design Docs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
- [Pragmatic Engineer: RFC Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)
- [Industrial Empathy: Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [Uber H3 RFC Template](https://github.com/uber/h3/blob/master/dev-docs/RFCs/rfc-template.md)
- [InnerSource: RFC Patterns](https://patterns.innersourcecommons.org/p/transparent-cross-team-decision-making-using-rfcs)

---

*Reference Document | SDD Best Practices 2026 | Version 1.0*
