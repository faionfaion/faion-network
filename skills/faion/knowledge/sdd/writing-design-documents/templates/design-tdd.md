# {feature-name}: Technical Design Document

**Status:** Draft / Review / Approved
**Author:** {name}
**Date:** {YYYY-MM-DD}
**Review deadline:** {YYYY-MM-DD}

## Background

{Context: what system this extends, relevant prior decisions, constraints from constitution.md}

## Problem Statement

{Specific technical problem being solved. Reference to spec.md if exists.}

## Requirements

### Functional

| ID | Requirement |
|----|-------------|
| R-1 | {What the system must do} |
| R-2 | {What the system must do} |

### Non-Functional

| ID | Requirement | Metric |
|----|-------------|--------|
| NF-1 | Performance | p99 < {X}ms |
| NF-2 | Availability | {X}% uptime |

## Design

### High-Level Architecture

{Component diagram + brief description}

### Detailed Design

#### {Component or Layer}

{Technical details: interfaces, algorithms, data structures, protocols}

#### {Component or Layer}

{Technical details}

### APIs

{Endpoint specs, message formats, or function signatures as applicable}

### Data Storage

{Schema, indices, data lifecycle, migration approach}

### Error Handling

{How errors propagate, what gets logged, how the system recovers}

### Security

{Auth, authz, encryption, input validation, secrets management}

## Trade-offs

| Decision | Alternative | Why This Was Chosen |
|----------|-------------|---------------------|
| {choice} | {other option} | {rationale} |

## Testing Strategy

| Type | What to test | Tool |
|------|-------------|------|
| Unit | {scope} | pytest / jest |
| Integration | {scope} | pytest |
| E2E | {scope} | playwright |

## Rollout Plan

1. {Phase 1 — e.g. deploy behind feature flag}
2. {Phase 2 — e.g. enable for 5% of users}
3. {Phase 3 — e.g. full rollout, remove flag}

## Open Questions

| # | Question | Owner | Deadline |
|---|----------|-------|----------|
| 1 | {question} | {owner} | {date} |

## References

- Spec: `.aidocs/{status}/{feature}/spec.md`
- Constitution: `.aidocs/constitution.md`
- {External reference}
