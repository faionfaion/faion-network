---
slug: structural-patterns
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structural patterns define how classes and objects are composed into larger structures using inheritance and object composition.
content_id: "b80b33513b53382e"
tags: [design-patterns, structural-patterns, adapter, decorator, facade, proxy]
---
# Structural Design Patterns

## Summary

**One-sentence:** Structural patterns define how classes and objects are composed into larger structures using inheritance and object composition.

**One-paragraph:** Structural patterns define how classes and objects are composed into larger structures using inheritance and object composition. The seven GoF structural patterns are Adapter, Bridge, Composite, Decorator, Facade, Proxy, and Flyweight. All four "wrapping" patterns (Adapter, Proxy, Decorator, Bridge) involve surrounding an object but serve distinct purposes: Adapter converts an interface, Proxy controls access, Decorator adds behavior, Bridge separates abstraction from implementation. Select by problem, not by name recognition.

## Applies If (ALL must hold)

- Adapter: integrating third-party library, legacy API, or protocol with an incompatible interface
- Bridge: needing independent variation in both abstraction and implementation dimensions (designed up-front)
- Composite: representing hierarchical/tree structures (file systems, UI component trees, org charts)
- Decorator: adding cross-cutting behavior (logging, caching, auth) without subclassing; building middleware chains
- Facade: simplifying a complex subsystem for callers; library entry points; API gateway behavior in-process
- Proxy: lazy loading expensive objects; access control; caching; remote object representation; audit logging
- Flyweight: very large numbers of similar objects where most state is shared (text rendering, game particles)

## Skip If (ANY kills it)

- Adapter: when the interface mismatch is small enough to handle with a single conversion function
- Bridge: when there is only one implementation dimension — adds unnecessary indirection
- Composite: when the tree structure is trivial (depth 1) or never traversed uniformly
- Decorator: when the number of combinations is small and fixed — direct subclassing is clearer
- Facade: when the subsystem is already simple or when the facade would hide information callers need
- Proxy: when simple delegation or a plain function call suffices — proxy adds a maintenance surface
- Flyweight: when object count is small or when extrinsic state computation offsets the memory savings

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-architect/`
