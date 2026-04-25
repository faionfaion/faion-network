# Agent Integration — Design Document Advanced Patterns

## When to use
- Feature has a frontend component with non-trivial component hierarchy (more than 2 nesting levels)
- Security attack surface requires explicit mitigation table (auth, XSS, CSRF, injection)
- New external dependencies or third-party services are introduced
- Performance targets are specified in NFRs and must be traced to design decisions
- Feature involves database migrations or backward compatibility concerns
- Full testing strategy (unit + integration + E2E) must be planned at design time

## When NOT to use
- Pure backend feature with no UI — skip component hierarchy (Phase 8)
- Greenfield project with no existing patterns in `features/done/` — establish patterns first
- Spike output — advanced patterns assume known constraints; spikes produce constraints
- When security section would be identical to a recently completed feature — reference the prior design instead

## Where it fails / limitations
- Component hierarchy diagrams require framework knowledge (React, Angular, etc.) — agents will produce generic trees without explicit framework context in the prompt
- Security mitigation table is populated with standard mitigations but may miss domain-specific threats (business logic abuse, multi-tenant isolation) without explicit threat modeling input
- Performance targets in the design must come from NFRs in spec.md; agents will invent numbers if spec is absent
- Migration strategy is frequently boilerplate; agents do not know the actual production data volume or schema version history

## Agentic workflow
An agent reads spec.md (FR-X, NFR-X) and the base design structure (design-doc-structure.md) and extends the design with advanced sections: component hierarchy from the UI requirements, security table from the NFR security items, performance considerations from NFR performance items, and testing strategy aligned to the test pyramid. The agent writes each phase as a section in design.md. The `faion-sdd-executor-agent` then reads the completed design.md to generate implementation tasks that reference the specific AD-X decisions.

### Recommended subagents
- `faion-sdd-executor-agent` — reads design.md advanced sections during task execution; uses security and performance constraints to write code
- Architecture/design subagent (claude-opus-4-7) — required for dependency analysis, security mitigations, migration planning

### Prompt pattern
```
Read {feature}/spec.md for NFR-X security and performance requirements.
Read {feature}/design.md for existing AD-X decisions.
Add the following sections to design.md:
Phase 8: Component hierarchy (tree format, no ASCII art) with TypeScript interface per component.
Phase 10: Security table — Concern | Mitigation | AD Reference. Cover: XSS, CSRF, injection, auth, rate limiting.
Phase 11: Performance table — Concern | Strategy | Target (from NFR) | AD Reference.
Phase 12: Test pyramid — unit coverage % target, integration endpoints list, E2E critical flows.
Phase 13: Migration strategy (only if schema changes exist in design).
Do not invent NFR values — use only values from spec.md NFR-X items.
```

```
Review design.md for traceability gaps.
Output a table: AD-X | Traces to FR-X | Has security implication? | Performance target set?
Flag any AD without FR trace and any NFR without a corresponding design strategy.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | E2E test scaffolding from critical flow list | `npm i -D @playwright/test` / https://playwright.dev |
| `vitest` | Unit test framework matching design test strategy | `npm i -D vitest` / https://vitest.dev |
| `supertest` | Integration test for API endpoints in design | `npm i -D supertest` / https://github.com/ladjs/supertest |
| `owasp-threat-dragon` | Threat modeling to feed security section | https://owasp.org/www-project-threat-dragon/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial — REST API (read) | Component hierarchy can be extracted from Figma frames; agents read via API |
| Storybook | OSS | Yes — file-based | Component specs in stories; agents can read story files for hierarchy |
| Sentry | SaaS | Yes — REST API | Performance baselines from prod data to populate NFR targets in design |
| Datadog | SaaS | Yes — REST API | Same as Sentry for performance data |
| AWS Well-Architected Tool | SaaS | Partial | Security pillar provides standard mitigations; not agent-native |

## Templates & scripts
See `templates.md` for the full design doc template. Advanced sections (Phases 8-13) are documented in this file (README.md).

Inline — generate a test file stub list from design.md component hierarchy:
```bash
#!/usr/bin/env bash
# gen-test-stubs.sh — generate empty test file paths from component list in design.md
DESIGN="${1:-design.md}"
echo "Test stubs to create:"
grep -oP "src/components/\S+\.tsx" "$DESIGN" | while read -r comp; do
  dir=$(dirname "$comp")
  base=$(basename "$comp" .tsx)
  echo "  $dir/__tests__/$base.test.tsx"
done
```

## Best practices
- Component interface TypeScript definitions in Phase 8 become the source of truth — agents copy them into implementation, not the reverse
- Security table must reference a specific AD-X for each mitigation — "use bcrypt" without AD-003 is not traceable
- Performance targets must come from NFR-X in spec.md — never let agents invent latency numbers
- Test pyramid percentages (80% unit, 100% integration endpoints, critical E2E) should be project constants in constitution.md
- Migration strategy is only needed when design.md lists schema changes; if no schema changes, omit Phase 13
- Check `features/done/` for prior designs before writing security or performance sections — reuse mitigations across features
- Design review (human) must happen before impl-plan is written; advanced sections are the main review surface

## AI-agent gotchas
- Agents will add ASCII art component trees by default — explicitly require "tree format, no ASCII art" in the prompt
- Security mitigations without AD references are common agent outputs; require "| AD Reference" column in the prompt
- Component interface definitions in design.md are often incomplete for optional props and event handlers — require full TypeScript interfaces including optional fields
- Agents skip migration strategy when no explicit prompt exists, even when design lists schema changes — add a check step
- E2E critical flows list often covers only the happy path; require error and edge flows explicitly
- Performance strategy column often says "use caching" without specifying cache layer, TTL, or invalidation — require concrete strategy per row

## References
- https://www.industrialempathy.com/posts/design-docs-at-google/ — Design docs at Google
- https://google.github.io/eng-practices/review/ — Google engineering practices
- https://aws.amazon.com/architecture/well-architected/ — AWS Well-Architected Framework
- https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications — Testing trophy
- https://owasp.org/www-project-threat-dragon/ — OWASP Threat Dragon
- https://stripe.com/docs/api — Stripe API as reference for API contract patterns
