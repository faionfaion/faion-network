# Architecture Decision Records (ADR)

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision along with its context and consequences. ADRs provide a historical record of why architectural choices were made, enabling future team members to understand the reasoning behind the current system design.

The concept was popularized by Michael Nygard in his [2011 blog post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and has since become a standard practice in software engineering.

## Why Write ADRs?

### Problems ADRs Solve

| Problem | How ADRs Help |
|---------|---------------|
| **Lost context** | New team members don't understand "why" of existing design | Decisions documented with full context |
| **Repeated discussions** | Same debates happen without historical context | Previous analysis preserved and referenced |
| **Production incidents** | Lack design context during troubleshooting | Decision rationale aids debugging |
| **Puzzling code** | Design choices seem arbitrary | "Why" is documented alongside "what" |
| **Tribal knowledge** | Decisions live only in people's heads | Persistent, searchable documentation |

### Benefits

- **Onboarding acceleration**: New developers understand system evolution
- **Decision transparency**: All stakeholders see the reasoning
- **Accountability**: Decisions have documented ownership
- **Learning from history**: Both successes and failures are preserved
- **Avoiding decision reversal**: Prevents undoing good decisions due to forgotten context

## When to Write an ADR

### Write an ADR When

- **Large impact decisions**: Choices affecting system structure, scalability, or maintainability
- **Breaking changes**: API changes requiring consumer migration
- **Technology selection**: Choosing frameworks, databases, or major dependencies
- **Pattern adoption**: Deciding on architectural patterns (microservices, event-driven, etc.)
- **Quality attribute tradeoffs**: Balancing security vs. performance, consistency vs. availability
- **Undocumented existing decisions**: Implicit standards that should be explicit
- **Cross-team decisions**: Choices affecting multiple teams or services

### When NOT to Write an ADR

- **Small, reversible decisions**: Low-risk choices easily changed later
- **Implementation details**: How code is written (unless it sets a pattern)
- **Changelog items**: Individual bug fixes or minor features
- **Already documented elsewhere**: Covered by standards, policies, or other docs
- **Single-developer decisions**: Tiny, self-contained, minimal-risk choices

### The Spotify Rule

From [Spotify Engineering](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record):

> "An ADR should be written whenever a decision of significant impact is made; it is up to each team to align on what defines a significant impact."

## ADR Lifecycle

```
PROPOSED → ACCEPTED → [DEPRECATED | SUPERSEDED]
    │          │              │
  Review     Active       Link to new ADR
  period    decision      or mark obsolete
```

### Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **Proposed** | Under discussion, gathering feedback | Review and discuss |
| **Accepted** | Approved, active decision | Implement and follow |
| **Rejected** | Not approved (keep for reference) | Document why rejected |
| **Deprecated** | No longer relevant due to context change | Keep for history |
| **Superseded** | Replaced by newer ADR | Link to replacement |

### Immutability Principle

Once accepted, ADRs should be treated as **immutable**:
- Don't alter existing information
- Add amendments as new sections
- Create new ADR to supersede if decision changes
- Update only the status field

## ADR Storage and Organization

### Where to Store ADRs

**Best practice**: Co-locate with code in version control.

```
project/
├── docs/
│   └── adr/                    # or decisions/, architecture/
│       ├── 0001-use-react.md
│       ├── 0002-postgresql-database.md
│       └── 0003-rest-api-design.md
└── src/
```

### Naming Convention

```
NNNN-short-title.md
```

Examples:
- `0001-use-react-for-frontend.md`
- `0002-adopt-event-sourcing.md`
- `0003-api-versioning-strategy.md`

### Organization Tips

- **Sequential numbering**: Use 4-digit format (0001, 0002...)
- **Numbers never reused**: Superseded ADRs keep their numbers
- **Chronological order**: Tells the story of system evolution
- **Single decision per file**: Easier to track and reference

## ADR Formats

### Available Templates

| Format | Best For | Complexity |
|--------|----------|------------|
| **Nygard** | Simple, quick decisions | Low |
| **MADR** | Comprehensive decisions with alternatives | Medium |
| **Y-statements** | One-liner decisions with tradeoffs | Low |
| **Extended** | Enterprise, compliance-heavy environments | High |

See [templates.md](templates.md) for copy-paste templates.

## ADRs in Agile Teams

### Integration with Agile

- ADRs fit the agile principle: "Just enough documentation"
- Create ADRs during sprint planning when major decisions arise
- Review ADRs in architecture review meetings
- Link ADRs to user stories/epics they affect

### Meeting Format (Amazon-style)

1. **Silent reading** (10 minutes): Everyone reads the ADR
2. **Q&A** (15 minutes): Clarifying questions
3. **Discussion** (15 minutes): Debate alternatives
4. **Decision** (5 minutes): Accept, reject, or defer

### Tips for Agile Teams

- Keep ADRs short (1-2 pages)
- Write ADRs as you make decisions, not after
- Any team member can propose an ADR
- Use pull requests for ADR review
- Include ADRs in Definition of Done for architectural stories

## Tools

### Command-Line Tools

| Tool | Description | Install |
|------|-------------|---------|
| [adr-tools](https://github.com/npryce/adr-tools) | Bash scripts for ADR management | `brew install adr-tools` |
| [adr-tools-python](https://pypi.org/project/adr-tools-python/) | Python port of adr-tools | `pip install adr-tools-python` |
| [dotnet-adr](https://github.com/endjin/dotnet-adr) | .NET Global Tool for ADRs | `dotnet tool install -g adr` |

### Static Site Generators

| Tool | Description | URL |
|------|-------------|-----|
| [Log4brains](https://github.com/thomvaill/log4brains) | ADR management + static site generation | npm package |
| [adr-viewer](https://github.com/mrwilson/adr-viewer) | Renders ADRs as HTML | Python package |
| [ADR Manager](https://github.com/adr/adr-manager) | Web-based ADR management | GitHub integration |

### IDE Integration

- VS Code: Markdown preview, templates via snippets
- IntelliJ: Markdown support, ADR templates
- Vim/Neovim: Markdown plugins + custom templates

## LLM Usage Tips

### When to Use LLMs for ADRs

| Task | LLM Helpful? | Why |
|------|--------------|-----|
| Drafting initial structure | Yes | Speeds up boilerplate |
| Identifying alternatives | Yes | Brainstorms options you might miss |
| Pros/cons analysis | Yes | Systematic evaluation |
| Writing consequences | Yes | Thinks through implications |
| Context gathering | Somewhat | Can summarize, but needs your input |
| Final decision | No | Requires human judgment and accountability |

### Best Practices with LLMs

1. **Provide context**: Give LLM project background, constraints, team size
2. **Iterate**: Use LLM for first draft, refine with domain knowledge
3. **Verify facts**: LLMs may hallucinate technical details
4. **Add team input**: LLM output is starting point, not final answer
5. **Human decision**: Always have humans make and own the final decision

See [llm-prompts.md](llm-prompts.md) for effective prompts.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **ADR as design guide** | Keep focused on decision, not implementation details |
| **Not updating status** | Mark superseded ADRs, link to replacement |
| **Missing alternatives** | Always document what you considered and rejected |
| **No timestamps** | Include date for historical context |
| **Hidden in wiki** | Store in version control with code |
| **Too long** | Keep to 1-2 pages; create separate ADR if needed |
| **No ownership** | Always list deciders/authors |
| **Writing after the fact** | Write ADRs as decisions are made |

## Resources

### Official Resources

- [ADR GitHub Organization](https://adr.github.io/) - Central hub for ADR resources
- [MADR Project](https://adr.github.io/madr/) - Markdown Any Decision Records
- [ADR Templates](https://adr.github.io/adr-templates/) - Template collection

### Articles and Guides

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Michael Nygard's original article
- [When Should I Write an ADR](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record) - Spotify Engineering
- [AWS ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/) - AWS Architecture Blog
- [Microsoft Azure ADR Guide](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record) - Azure Well-Architected Framework
- [UK Government ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework) - December 2025

### Repositories with ADR Examples

- [joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record) - Comprehensive examples
- [adr/madr](https://github.com/adr/madr/tree/develop/docs/decisions) - MADR's own decisions
- [JabRef/jabref](https://github.com/JabRef/jabref) - Real-world ADRs

### Books

- "Documenting Software Architectures" by Clements et al.
- "Software Architecture in Practice" by Bass, Clements, and Kazman
- "Design It!" by Michael Keeling

## Related Files

- [checklist.md](checklist.md) - Step-by-step checklist for writing ADRs
- [templates.md](templates.md) - Copy-paste ADR templates
- [examples.md](examples.md) - Real ADR examples from open-source projects
- [llm-prompts.md](llm-prompts.md) - Effective prompts for LLM-assisted ADR writing
