# Design Doc Examples

Real design document examples from open source projects and tech companies. Study these to understand what good design docs look like in practice.

## Open Source Design Docs

### Rust RFCs

The Rust programming language has one of the most influential RFC processes in open source. Many projects cite Rust's process as their inspiration.

**Repository:** [github.com/rust-lang/rfcs](https://github.com/rust-lang/rfcs)

**Notable Examples:**

| RFC | Title | Why It's Good |
|-----|-------|---------------|
| [RFC 2005](https://github.com/rust-lang/rfcs/blob/master/text/2005-match-ergonomics.md) | Match Ergonomics | Clear problem statement, detailed alternatives |
| [RFC 2094](https://github.com/rust-lang/rfcs/blob/master/text/2094-nll.md) | Non-lexical Lifetimes | Complex topic explained clearly |
| [RFC 2700](https://github.com/rust-lang/rfcs/blob/master/text/2700-associated-constants-on-ints.md) | Associated Constants | Concise, focused scope |
| [RFC 3107](https://github.com/rust-lang/rfcs/blob/master/text/3107-derive-default-enum.md) | Derive Default for Enums | Good motivation section |

**Format highlights:**
- Summary, motivation, detailed design, drawbacks, rationale, alternatives
- Tracking issue for implementation
- Community discussion via GitHub PRs

---

### Kubernetes Enhancement Proposals (KEPs)

Kubernetes uses KEPs for significant changes. These are comprehensive and heavily reviewed.

**Repository:** [github.com/kubernetes/enhancements](https://github.com/kubernetes/enhancements/tree/master/keps)

**Notable Examples:**

| KEP | Title | Why It's Good |
|-----|-------|---------------|
| [KEP-1040](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1040-priority-and-fairness) | Priority and Fairness | Excellent problem framing |
| [KEP-2170](https://github.com/kubernetes/enhancements/tree/master/keps/sig-network/2170-multi-network) | Multi-network | Clear phases and milestones |
| [KEP-1287](https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/1287-in-place-pod-vertical-scaling) | In-place Pod Vertical Scaling | Thorough alternatives analysis |

**Format highlights:**
- Metadata YAML header
- Summary, motivation, proposal, design details
- Production readiness checklist
- Graduation criteria (alpha → beta → stable)
- Test plans and rollout strategy

---

### React RFCs

React's RFC process is community-driven and focuses on API design.

**Repository:** [github.com/reactjs/rfcs](https://github.com/reactjs/rfcs)

**Notable Examples:**

| RFC | Title | Why It's Good |
|-----|-------|---------------|
| [RFC 0068](https://github.com/reactjs/rfcs/blob/main/text/0068-react-hooks.md) | React Hooks | Landmark RFC, thorough motivation |
| [RFC 0188](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md) | Server Components | Complex topic, clear explanation |
| [RFC 0229](https://github.com/reactjs/rfcs/blob/main/text/0229-use.md) | use() Hook | Good prior art section |

**Format highlights:**
- Summary, basic example, motivation
- Detailed design, drawbacks, alternatives
- Adoption strategy, unresolved questions

---

### Go Proposals

Go uses a proposal process for language and standard library changes.

**Repository:** [github.com/golang/proposal](https://github.com/golang/proposal/tree/master/design)

**Notable Examples:**

| Proposal | Title | Why It's Good |
|----------|-------|---------------|
| [Generics](https://github.com/golang/proposal/blob/master/design/43651-type-parameters.md) | Type Parameters | Years of iteration, comprehensive |
| [Fuzzing](https://github.com/golang/proposal/blob/master/design/draft-fuzzing.md) | Native Fuzzing | Clear use cases |
| [Modules](https://github.com/golang/proposal/blob/master/design/24301-versioned-go.md) | Versioned Go Modules | Addresses real pain points |

---

### Oxide RFDs

Oxide Computer Company uses a unique "Request for Discussion" format stored in Git.

**Repository:** [rfd.shared.oxide.computer](https://rfd.shared.oxide.computer/)

**Notable Examples:**

| RFD | Title | Why It's Good |
|-----|-------|---------------|
| [RFD 1](https://rfd.shared.oxide.computer/rfd/0001) | Requests for Discussion | Meta-RFD explaining the process |
| [RFD 68](https://rfd.shared.oxide.computer/rfd/0068) | Rack Network Topology | Clear technical diagrams |

**Format highlights:**
- State machine (prediscussion → discussion → published → committed)
- AsciiDoc format with metadata headers
- Stored in Git, reviewed via PRs
- Labels for categorization

---

### FoundationDB Design Docs

Apple's distributed database has excellent design documentation.

**Repository:** [github.com/apple/foundationdb/tree/main/design](https://github.com/apple/foundationdb/tree/main/design)

**Notable for:**
- Deep technical content
- Performance analysis
- Failure mode documentation

---

## Company-Specific Examples

### Google (via Public Sources)

Google doesn't publish internal design docs, but these public resources reflect their style:

- [Google API Design Guide](https://cloud.google.com/apis/design) - API design principles
- [Bigtable Paper](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) - Academic paper style
- [Site Reliability Engineering Book](https://sre.google/sre-book/table-of-contents/) - Operational design thinking

**Inferred Google format:**
```
Title
Author, Reviewers
Status, Last Updated

Overview (1-2 paragraphs)
Context and Scope
  - Background
  - Goals
  - Non-Goals
Design
  - System Overview
  - Detailed Design
  - Data Model
  - API
Alternatives Considered
Cross-cutting Concerns
  - Security, Privacy, Scalability, Monitoring
Timeline and Milestones
Open Questions
References
```

---

### Amazon (6-Pager Style)

Amazon's 6-pagers are internal, but the format is well-documented:

**Public resources explaining the format:**
- [The Anatomy of an Amazon 6-pager](https://writingcooperative.com/the-anatomy-of-an-amazon-6-pager-fc79f31a41c9)
- [Amazon's Peculiar Meeting Culture](https://www.sec.gov/Archives/edgar/data/1018724/000119312521091890/d168744dex991.htm) (Bezos letters)

**Reconstructed format:**
```
[NARRATIVE FORMAT - NO BULLET POINTS]

Introduction (1/2 page)
- Hook the reader
- State the problem

Goals (1/2 page)
- SMART goals
- Success metrics

Tenets (1/2 page)
- Guiding principles
- Priority order

State of the Business (1-2 pages)
- Current situation
- Data and metrics
- Customer insights

Lessons Learned (1/2 page)
- What we've tried
- What worked/didn't

Strategic Priorities (1-2 pages)
- Proposed solution
- Implementation approach
- Resource requirements

[APPENDIX - NO PAGE LIMIT]
- Supporting data
- Graphs and charts
- Detailed analysis
```

---

### Uber (RFC/ERD Style)

Uber evolved from "DUCK" documents to a tiered RFC system.

**Public resources:**
- [Scaling Engineering Teams via Writing](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/)

**Reconstructed format:**
```
RFC: [Title]
RFC Number: RFC-NNN
Author: [Name]
Status: Draft | Review | Approved | Rejected
Created: YYYY-MM-DD
Approvers: [Required sign-offs]

Summary (1 paragraph)

Motivation
- Problem statement
- Business impact

Proposal
- Overview
- Detailed Design
- Service SLAs (availability, latency, throughput)
- Dependencies

Alternatives (with rejection rationale)

Security Considerations

Operational Considerations
- Deployment
- Monitoring
- Rollback

Timeline

Approvals Table
| Approver | Team | Status | Date |
```

---

## Design Doc Libraries

### designdocs.dev

**URL:** [designdocs.dev/library](https://www.designdocs.dev/library)

Curated collection of 1000+ design docs from 40+ companies including:
- Hasura (GraphQL)
- AWS EKS Anywhere
- AWS SAM CLI
- Envoy Proxy
- HashiCorp tools
- And many more

**How to use:**
1. Browse by company or topic
2. Study structure and depth
3. Adapt patterns to your context

---

### GitHub Collections

**Search queries for finding design docs:**

```
# Rust-style RFCs
path:rfcs filename:*.md "# Summary"

# Kubernetes-style KEPs
path:keps filename:kep.yaml

# Design proposals
filename:design*.md "## Motivation"

# Architecture decisions
filename:adr*.md "## Decision"
```

---

## Example Analysis

### What Makes a Good Design Doc

Study these common patterns from successful design docs:

#### Strong Problem Statement

**Good (Rust RFC 2005):**
> "Match ergonomics aims to make matching more ergonomic by automatically inserting references in some cases."

**Why it works:** Specific, actionable, states the benefit.

#### Clear Non-Goals

**Good (Kubernetes KEP):**
> "Non-goals: This KEP does not attempt to solve multi-cluster networking."

**Why it works:** Explicitly bounds scope, prevents scope creep.

#### Thorough Alternatives

**Good pattern:**
```
### Alternative 1: Use existing library X
- Pros: Mature, well-tested
- Cons: Doesn't support Y, performance overhead
- Rejected because: Performance is critical for our use case

### Alternative 2: Build custom solution
- Pros: Tailored to our needs
- Cons: Maintenance burden
- Rejected because: Team lacks expertise in Z

### Chosen approach: Fork and modify library X
- Pros: Starting point + customization
- Cons: Ongoing merge complexity
- Why chosen: Best balance of effort vs. benefit
```

#### Data-Driven Decisions

**Good pattern:**
> "Based on analysis of 10,000 production queries, 73% would benefit from this optimization, with an estimated P99 latency reduction of 45ms."

**Why it works:** Specific numbers, clear impact.

---

## Quick Reference

### By Format Type

| Format | Best Examples |
|--------|---------------|
| RFC | Rust, React, Ember.js |
| KEP | Kubernetes |
| RFD | Oxide, Joyent |
| Design Doc | Go proposals, FoundationDB |
| 6-Pager | Amazon (internal) |

### By Complexity

| Complexity | Example Source |
|------------|----------------|
| Small feature | React minor RFCs |
| Medium feature | Go proposals |
| Large system | Kubernetes KEPs |
| Platform change | Rust major RFCs |

### By Industry

| Domain | Example Source |
|--------|----------------|
| Frontend | React, Vue RFCs |
| Backend | Go, Rust proposals |
| Infrastructure | Kubernetes, Envoy |
| Database | FoundationDB, CockroachDB |
| Distributed systems | Oxide RFDs |

---

*For templates based on these examples, see [templates.md](templates.md).*
