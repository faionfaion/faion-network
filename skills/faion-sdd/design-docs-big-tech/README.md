# Design Docs at Big Tech Companies

Comprehensive guide to design document practices at Google, Amazon, Meta, Uber, Stripe, Spotify, Netflix, Microsoft, and other leading tech companies.

**Last Updated:** 2026-01-25
**Sources:** Pragmatic Engineer, Industrial Empathy, company engineering blogs, open source projects

---

## Overview

Design documents (also called RFCs, ERDs, or design reviews) are the cornerstone of engineering culture at major tech companies. They serve as:

1. **Early issue identification** - Catch design issues when changes are still cheap
2. **Consensus building** - Achieve agreement across teams and stakeholders
3. **Knowledge sharing** - Document decisions for future team members
4. **Onboarding tool** - Help new engineers understand systems quickly

> "Our job is not to produce code per se, but rather to solve problems. Unstructured text may be the better tool for solving problems early when changes are still cheap." - Google Engineering

---

## Company Comparison

| Company | Document Name | Format | Review Style | Key Feature |
|---------|---------------|--------|--------------|-------------|
| **Google** | Design Doc | Informal, collaborative | Inline comments in Google Docs | Emphasis on trade-offs and "why" |
| **Amazon** | 6-Pager / PR-FAQ | Narrative prose, no bullets | Silent reading 20-25 min | "Working backwards" from customer |
| **Uber** | RFC/ERD | Formal with approvers | Mailing lists + doc comments | Tiered by impact scope |
| **Spotify** | RFC + ADR | Two-stage process | Open for weeks, async | RFC for alignment, ADR for record |
| **Stripe** | RFC | Written culture | Async, bias toward documentation | Strong mentorship integration |
| **Netflix** | ADR | Lightweight | Team-based | Focus on architectural decisions |
| **Microsoft** | Design Doc/TDD | SDL-integrated | Security-focused code review | SDL lifecycle integration |
| **Airbnb** | Spec + Design Doc | Separate product/engineering | Cross-functional | Product and engineering alignment |
| **Shopify** | RFC | GitHub-based | Async with deadline | Deadline-driven consensus |
| **Atlassian** | RFC | Confluence-based | Triad model (eng/PM/design) | Architecture principles validation |

---

## Detailed Practices by Company

### Google Design Docs

**Philosophy:** Informal but structured documents created before coding begins. Focus on high-level strategy and trade-offs.

**Key Characteristics:**
- Written in Google Docs with heavy use of collaboration features
- No strict format, but common structure has emerged
- Emphasis on documenting "why" decisions were made
- Reviewers add inline comments, not separate feedback documents
- Formal review meeting for complex projects

**Process:**
1. Author writes initial design doc
2. Shares with close collaborators for early feedback
3. Circulates to wider audience for review
4. Review meeting (optional, for complex projects)
5. Document becomes historical artifact

**Best Practice:** Always include "do nothing" as a baseline alternative. Sometimes the best decision is to not build anything.

### Amazon 6-Pager and PR-FAQ

**Philosophy:** "Working backwards" from the customer. Start with the end result and work towards minimum requirements.

**6-Pager Format:**
- Maximum 6 pages of narrative prose (no bullet points)
- Supporting data in unlimited appendix
- Sections: Introduction, Goals, Tenets, State of Business, Lessons Learned, Strategic Priorities
- Written densely - every word must count

**PR-FAQ Format:**
- Starts with hypothetical press release announcing finished product
- Followed by FAQ document adding detail
- Forces customer-centric thinking from day one

**Meeting Process:**
1. Printed copies distributed at meeting start
2. 20-25 minutes of silent reading
3. Discussion and feedback
4. Printouts with handwritten notes returned to author
5. Author revises based on all feedback

**Best Practice:** Write as if explaining to someone unfamiliar with the subject. No jargon, no assumptions.

### Uber RFC/ERD Process

**Philosophy:** Evolved from lightweight RFCs to tiered Engineering Requirements Documents based on impact scope.

**Evolution:**
- Early days: Simple RFCs circulated via mailing lists
- At scale (2000+ engineers): Formal ERD process with tool support
- Now: Tiered templates based on change scope

**Tiered Approach:**
| Tier | Scope | Template | Approvers |
|------|-------|----------|-----------|
| Lightweight | Team-only changes | Mini RFC | Team lead |
| Standard | Cross-team impact | Full RFC | Multiple teams |
| Heavyweight | Org/company-wide | Detailed ERD | Principal engineers |

**Process:**
1. Author writes document using appropriate template
2. Circulates to relevant mailing lists
3. Collects feedback via inline comments
4. Approvers sign off or raise objections
5. Development starts only after approval

**Best Practice:** Use lightweight templates for simple changes. Don't over-engineer the process.

### Spotify RFC + ADR

**Philosophy:** Two-stage process - RFCs for reaching consensus, ADRs for recording decisions.

**RFC Process:**
- Written in shared Google Docs for easy collaboration
- Open for review for 1-3 weeks
- Participants depend on problem type
- Large problems broken into big-picture RFC + smaller focused RFCs

**ADR Process:**
- Created after RFC process completes
- Captures the decision, context, and consequences
- Serves as permanent record
- Used for onboarding and project handovers

**Benefits Observed:**
- Improved onboarding for new developers
- Better agility during org changes
- Alignment across teams on best practices

**Best Practice:** Break large RFCs into multiple smaller, focused documents. Start with a big-picture RFC, then dive deep.

### Stripe RFC Process

**Philosophy:** Strong written culture with bias toward async decision-making.

**Key Characteristics:**
- "Write everything down" culture
- High-bar code reviews complement design reviews
- Strong mentorship programs integrated with RFC process
- Clear promotion framework tied to documentation skills

**Best Practice:** Use RFCs not just for technical decisions but for any decision that needs cross-team alignment.

### Meta/Facebook Approach

**Philosophy:** Notably less emphasis on formal documentation compared to other Big Tech.

**Reality:**
- No formal company-wide RFC process
- Some teams use 1-pager documents
- High autonomy for individuals and teams
- Compensates with: high talent bar, long tenures, internal systems

**Why it works for Meta:**
- Historical culture of "move fast"
- Engineers expected to handle ambiguity
- Systems built to counter lack of documentation
- High hiring bar ensures capable engineers

**Caution:** This approach is not recommended for most companies, especially with remote/async work.

### Microsoft Design Docs

**Philosophy:** Integrated with Security Development Lifecycle (SDL). Security and quality are non-negotiable.

**Document Types:**
- **FDD (Functional Design Document):** Business perspective, processes, use cases
- **TDD (Technical Design Document):** Implementation details, architecture

**SDL Integration:**
1. Requirements phase: Define with security in mind
2. Design phase: Create FDD and TDD
3. Implementation: Manual code review by separate reviewer
4. Verification: Security tooling and penetration testing
5. Release: Final security and privacy review

**Best Practice:** Treat security as a first-class citizen in design documents, not an afterthought.

---

## When to Write Design Docs

| Change Type | Document Needed | Scope |
|-------------|-----------------|-------|
| Bug fix | No | - |
| Small feature (1-2 days) | Optional mini-doc | Team only |
| Medium feature (1-2 weeks) | Standard design doc | Team + stakeholders |
| Large feature (1+ month) | Detailed RFC | Cross-team review |
| Architecture change | RFC + ADR | Company-wide |
| New service/system | Full design doc | Architecture review |

---

## LLM-Assisted Design Doc Writing

### When LLMs Help

| Task | LLM Effectiveness | Notes |
|------|-------------------|-------|
| Initial structure | High | Generate outline from requirements |
| Alternative analysis | High | Brainstorm options systematically |
| Risk identification | Medium-High | Surface edge cases |
| Prose refinement | High | Improve clarity and flow |
| Technical accuracy | Low-Medium | Requires expert validation |
| Trade-off analysis | Medium | Needs domain context |

### When LLMs Don't Help

- **Organizational context:** LLMs don't know your team's history or politics
- **System-specific details:** Your architecture is unique
- **Stakeholder preferences:** Review culture varies by company
- **Proprietary technology:** Internal tools and systems

### Best Practices for LLM-Assisted Writing

1. **Start with context:** Provide system overview, constraints, existing architecture
2. **Iterate in sections:** Don't generate entire document at once
3. **Validate technically:** Every technical claim needs human review
4. **Preserve voice:** Edit LLM output to match your team's style
5. **Use for brainstorming:** LLMs excel at generating alternatives to consider

See [llm-prompts.md](llm-prompts.md) for effective prompts.

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Design doc as spec | Confuses "why" with "what" | Keep separate: design doc (why/how), spec (what) |
| No alternatives section | Reviewers question judgment | Always document 2-3 alternatives considered |
| Writing after implementation | Defeats purpose | Write before coding; changes are cheap |
| Too many approvers | Process gridlock | Keep under 10 participants |
| Too long for scope | Wastes reviewer time | Match document length to change scope |
| No "do nothing" option | Missing baseline | Always include status quo as alternative |
| Skipping trade-offs | Hides decision rationale | Explicitly state pros/cons of chosen approach |

---

## Files in This Directory

| File | Description |
|------|-------------|
| [README.md](README.md) | This file - overview and best practices |
| [checklist.md](checklist.md) | Step-by-step checklist for writing design docs |
| [examples.md](examples.md) | Real examples from Google, Amazon, Uber, etc. |
| [templates.md](templates.md) | Copy-paste templates from various companies |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted writing |

---

## External Resources

### Primary Sources

- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) - Malte Ubl's comprehensive guide
- [Pragmatic Engineer: RFCs and Design Docs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs) - Gergely Orosz
- [RFC and Design Doc Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design) - Templates and examples
- [Design Docs Library](https://www.designdocs.dev/) - 1000+ examples from 40+ companies

### Company Engineering Blogs

- [Uber Engineering Blog](https://eng.uber.com/)
- [Spotify Engineering](https://engineering.atspotify.com/)
- [Meta Engineering](https://engineering.fb.com/)
- [Shopify Engineering](https://shopify.engineering/)
- [Atlassian Engineering](https://www.atlassian.com/blog/atlassian-engineering)

### Templates and Frameworks

- [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template)
- [Uber H3 RFC Template](https://github.com/uber/h3/blob/master/dev-docs/RFCs/rfc-template.md)
- [Squarespace RFC Template](https://slab.com/library/templates/squarespace-rfc-template/)
- [ADR GitHub](https://adr.github.io/) - Architecture Decision Records
- [InnerSource RFC Patterns](https://patterns.innersourcecommons.org/p/transparent-cross-team-decision-making-using-rfcs)

### Books

- "The Staff Engineer's Path" by Tanya Reilly - includes RFC template
- "Software Engineering at Google" - O'Reilly book with design doc chapter

---

## Metadata

| Field | Value |
|-------|-------|
| **ID** | design-docs-big-tech |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #design-docs, #rfc, #google, #amazon, #uber, #spotify |
| **Domain Skill** | faion-sdd |
| **Version** | 2.0 |

---

*Reference Document | Design Docs at Big Tech | Version 2.0*
