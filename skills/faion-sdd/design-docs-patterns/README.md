# Design Docs Patterns

Comprehensive guide to design document patterns used by leading tech companies. This methodology covers Google Design Docs, Amazon 6-Pagers/PR-FAQ, Uber RFCs, Spotify DIBB, and integration with Architecture Decision Records (ADRs).

## Overview

Design docs are lightweight planning documents written before implementing code to:

1. **Identify issues early** - Catch design flaws when changes are cheap
2. **Build consensus** - Achieve alignment across teams and stakeholders
3. **Share knowledge** - Document decisions for future team members
4. **Enable onboarding** - Help new engineers understand systems

> "Our job is not to produce code per se, but rather to solve problems. Unstructured text may be the better tool for solving problems early when changes are still cheap."

## Company Approaches

| Company | Format | Key Characteristics |
|---------|--------|---------------------|
| **Google** | Design Doc | Informal, collaborative, emphasizes "why" over "what" |
| **Amazon** | 6-Pager / PR-FAQ | Narrative format, silent reading, SMART goals |
| **Uber** | RFC/ERD | Formal approvers, service SLAs, tiered process |
| **Spotify** | DIBB | Data-driven, hypothesis-based, company bets |
| **Oxide/Joyent** | RFD | Request for Discussion, Git-based, state machine |
| **Rust/OSS** | RFC | Community feedback, explicit process, long-term |

## When to Write a Design Doc

### Write a design doc when:

| Trigger | Rationale |
|---------|-----------|
| Feature takes > 1 engineering week | Significant investment needs validation |
| Change is cross-cutting or multi-PR | Coordination required across boundaries |
| High security implications | Risk mitigation needs documentation |
| API changes affecting multiple teams | Stakeholder alignment essential |
| New service or system | Architecture decisions need consensus |
| Requirements are unclear | Writing clarifies thinking |

### Skip the design doc when:

| Scenario | Alternative |
|----------|-------------|
| Small, well-defined feature | Ticket/issue description |
| Bug fix with obvious solution | PR description |
| < 1 day of work | Quick sync meeting |
| Internal refactor, same behavior | Code review only |
| Prototype or spike | Spike summary in ticket |

### Decision rule

> If in doubt, start writing. It's cheap, and you can stop if unnecessary. The mere act of contemplating a design doc suggests you have unstructured thoughts that need clarity.

## Lightweight vs Heavyweight Approaches

### Lightweight Design Docs

- **When:** Internal changes, small teams, rapid iteration
- **Format:** 1-2 pages, informal tone, async review
- **Review:** Email to team list, comment threads
- **Timeline:** 1-3 days from draft to approval
- **Example:** Google's informal design docs for team-scoped changes

### Heavyweight Design Docs

- **When:** Cross-org changes, external APIs, infrastructure
- **Format:** 5-10+ pages, formal sections, required approvers
- **Review:** Scheduled meeting, senior audience, formal sign-off
- **Timeline:** 1-2 weeks with multiple revision cycles
- **Example:** Uber's ERD with mandatory approvers and SLAs

### Spectrum of formality

```
Quick RFC    Light Design Doc    Full Design Doc    ERD/6-Pager
   |              |                    |                |
1 page       2-3 pages            5-10 pages       10+ pages
Async        Mixed                Meeting          Silent reading
Team         Org                  Cross-org        Executive
```

## Design Doc Lifecycle

```
DRAFT → REVIEW → APPROVED → IMPLEMENTING → IMPLEMENTED → ARCHIVED
         |          |
       Iterate   Sign-off
```

| Phase | Activities |
|-------|------------|
| **Draft** | Author writes initial version, may share informally |
| **Review** | Circulate to stakeholders, collect feedback, iterate |
| **Approved** | Required approvers sign off, doc becomes authoritative |
| **Implementing** | Reference during development, update if design changes |
| **Implemented** | Feature shipped, doc becomes historical record |
| **Archived** | Doc superseded or system deprecated |

## Integration with ADRs

Architecture Decision Records (ADRs) complement design docs:

| Aspect | Design Doc | ADR |
|--------|------------|-----|
| **Scope** | Full system/feature design | Single architectural decision |
| **Length** | 5-20+ pages | 1-2 pages |
| **Audience** | Engineers, PMs, stakeholders | Engineers, architects |
| **Lifecycle** | One-time, project duration | Permanent record |
| **Location** | Wiki/docs system | Code repository |
| **Updates** | Evolves during design | Immutable once accepted |

### Integration patterns

1. **Design doc references ADRs** - Link to relevant past decisions
2. **Design doc spawns ADRs** - Extract key decisions into ADRs
3. **ADR references design doc** - Link to full context
4. **Parallel creation** - Write both simultaneously

### Recommended workflow

```
Design Doc (why + how)
    |
    +→ ADR-001: Database choice
    +→ ADR-002: API versioning strategy
    +→ ADR-003: Authentication mechanism
```

## Review Process Best Practices

### Preparation

1. Gather all design materials before review
2. Share doc 24-48 hours in advance for pre-reading
3. Create structured agenda with time allocations
4. Identify required vs optional reviewers

### During review

1. **Silent reading start** - 10-20 minutes of focused reading
2. **Inline comments** - Specific feedback on sections, not general
3. **Structured discussion** - Follow agenda, timebox sections
4. **Decision capture** - Document outcomes in real-time

### Post-review

1. Consolidate feedback centrally (avoid email/Slack fragmentation)
2. Address all comments, mark resolved
3. Schedule follow-up if needed
4. Obtain explicit sign-off from approvers

### Common review anti-patterns

| Anti-pattern | Solution |
|--------------|----------|
| Review by committee (too many reviewers) | Cap at 5-7 required reviewers |
| Bike-shedding on minor details | Timebox and move on |
| Missing key stakeholders | Identify approvers upfront |
| Feedback via multiple channels | Centralize in doc comments |
| Never-ending review cycle | Set review deadline |

## LLM Usage Tips

### When LLMs help

- **Drafting initial structure** - Generate outline from requirements
- **Expanding sections** - Flesh out bullet points into prose
- **Identifying gaps** - Ask "what's missing in this design?"
- **Alternative analysis** - Generate pros/cons for options
- **Technical writing** - Improve clarity and conciseness

### When LLMs struggle

- **Context-specific decisions** - Lacks your system knowledge
- **Trade-off evaluation** - Can't weigh your constraints
- **Political navigation** - Unaware of organizational dynamics
- **Novel architecture** - Limited to training data patterns
- **Security review** - May miss domain-specific vulnerabilities

### Effective LLM workflow

1. **Start human** - Define problem, goals, constraints
2. **LLM assist** - Generate structure, expand sections
3. **Human review** - Add context, fix inaccuracies
4. **LLM refine** - Improve prose, check consistency
5. **Human finalize** - Verify accuracy, add judgment calls

### Prompt strategies

See [llm-prompts.md](llm-prompts.md) for specific prompts covering:
- Design doc structure generation
- Alternative analysis
- Risk identification
- Technical writing improvement
- Cross-cutting concerns checklist

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step checklist for writing design docs |
| [examples.md](examples.md) | Real design doc examples from open source |
| [templates.md](templates.md) | Copy-paste templates for different styles |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted writing |

## External Resources

### Guides and Articles

- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) - Malte Ubl's definitive guide
- [Engineering Planning with RFCs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs) - Gergely Orosz's comprehensive overview
- [Scaling Teams via Writing](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/) - Why written culture matters
- [Amazon 6-Pager Guide](https://writingcooperative.com/the-anatomy-of-an-amazon-6-pager-fc79f31a41c9) - Anatomy of Amazon's format
- [Oxide RFD Process](https://oxide.computer/blog/rfd-1-requests-for-discussion) - Git-based design docs

### Example Libraries

- [designdocs.dev](https://www.designdocs.dev/) - 1000+ design docs from 40+ companies
- [ADR GitHub](https://adr.github.io/) - Architecture Decision Record resources
- [Rust RFC Repository](https://github.com/rust-lang/rfcs) - Canonical RFC process
- [Kubernetes Proposals](https://github.com/kubernetes/community/tree/master/contributors/design-proposals) - Large-scale OSS design docs

### Tools

- [ADR Tools](https://github.com/npryce/adr-tools) - CLI for managing ADRs
- [Backstage ADR Plugin](https://backstage.io/docs/architecture-decisions/) - ADR integration
- [Google Docs](https://docs.google.com) - Most common authoring tool
- [Notion](https://notion.so) - Alternative with templates

## Related Methodologies

- [writing-design-documents.md](../methodologies/writing-design-documents.md) - Core SDD design doc methodology
- [writing-specifications.md](../methodologies/writing-specifications.md) - Spec writing patterns
- [adr-template.md](../../faion-software-architect/methodologies/adr-template.md) - ADR methodology

---

*Part of the faion-sdd skill. For SDD workflow overview, see [../CLAUDE.md](../CLAUDE.md).*
