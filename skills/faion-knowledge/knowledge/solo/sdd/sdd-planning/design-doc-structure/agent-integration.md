# Agent Integration — Design Document Structure

## When to use
- After `spec.md` is approved (status: Approved) and before writing the implementation plan
- When a feature has non-trivial technical decisions: schema design, API contracts, caching strategy, auth model
- When code will be written by an agent executor — the design.md is the authoritative instruction set for what files to create/modify and why
- When the feature spans multiple files or services: design.md prevents agents from making local decisions that break the overall architecture
- For any feature where a security or performance concern exists — these sections create explicit review targets

## When NOT to use
- Single-file, single-concern changes with no architectural decisions (a design doc for "add a log statement" is waste)
- When spec.md is still in Draft — design decisions cannot be made until requirements are stable
- Internal refactors with no API/schema changes: write an ADR instead if a pattern decision is being made
- Spike/research tasks: output is an ADR or updated spec, not a design doc

## Where it fails / limitations
- The FR → AD-X traceability matrix requires that the spec's FR-X IDs are stable; specs revised after design is started invalidate the coverage matrix and require full re-sync
- File structure tables become wrong as implementation evolves — agents executing tasks may discover additional files needed; design.md must be updated or it becomes misleading
- API contracts in design.md are prose/JSON, not machine-validated — they can drift from actual implementation without Dredd/Pact enforcement in CI
- "Alternatives Considered" sections require genuine exploration; agents will generate plausible-sounding alternatives that were never actually evaluated
- Security and performance sections are easily written as vague checklists; without specific targets and owners, they provide no actionable guidance

## Agentic workflow
An agent generates design.md in one pass after loading spec.md and constitution.md. It derives architectural decisions (AD-X) by mapping each FR-X to one or more decisions, then fills the file structure table from those decisions. API contracts are generated from FR-X endpoint requirements. The human reviews the AD-X alternatives and consequences sections — these require domain judgment. The agent then self-validates using the design quality gate checklist before marking the document as `Review`. Human sets `Approved`.

### Recommended subagents
- `faion-sdd-executor-agent` — writes design.md as part of the design phase; uses the quality gate checklist to self-validate before marking for review

### Prompt pattern
```
Write a design document for feature: <feature-name>.

Inputs:
- spec.md: <paste spec content>
- constitution.md relevant sections: <paste>

Instructions:
1. For each FR-X in the spec, create one or more AD-X that implement it.
2. Build the file structure table: every CREATE or MODIFY entry must trace to an FR and AD.
3. For API endpoints, use OpenAPI-style request/response documentation.
4. For each AD-X, list at least 2 rejected alternatives with concrete rejection reasons.
5. Fill security and performance sections with specific mitigations tied to FR-X.
6. Run the design quality gate checklist internally; list any failed items as Open Questions.
Status: Draft.
```

```
Review this design document for completeness.
Check: (1) every FR-X from spec has at least one AD-X, (2) every file in file-structure
table traces to an FR and AD, (3) all API endpoints have error response schemas,
(4) security section addresses auth and input validation.
Output: gap table only. Do not rewrite the document.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| markdownlint | Validates heading structure, table format, link syntax in design.md | `npm install -g markdownlint-cli` / https://github.com/DavidAnson/markdownlint |
| swagger-cli | Validates inline OpenAPI YAML blocks if extracted from design.md | `npm install -g @apidevtools/swagger-cli` / https://github.com/APIDevTools/swagger-cli |
| vale | Prose style linting — enforces "SHALL" language in requirement statements | `brew install vale` / https://vale.sh |
| ripgrep | Traceability audit: `rg 'FR-\d+' design.md` vs `rg 'FR-\d+' spec.md` | System / https://github.com/BurntSushi/ripgrep |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub / GitLab PR | SaaS | Yes | Design doc review via PR; inline comments on specific AD-X sections |
| Backstage TechDocs | OSS | Partial | Renders design.md as browsable technical documentation |
| Miro / FigJam | SaaS | No | Used for component diagram sketches referenced in design.md appendix |
| dbdiagram.io | SaaS | No — manual | Data model diagrams; embed SVG export in design.md appendix |

## Templates & scripts
See `README.md` for the complete Design Document Structure v2.0 template (full inline template included).

Design quality gate check (validates traceability between spec and design):
```bash
#!/usr/bin/env bash
# usage: ./design-quality-gate.sh spec.md design.md
set -euo pipefail
SPEC="$1"
DESIGN="$2"
echo "=== Design Quality Gate ==="
# Check all spec FRs appear in design
SPEC_FRS=$(grep -oP 'FR-\d+' "$SPEC" | sort -u)
DESIGN_FRS=$(grep -oP 'FR-\d+' "$DESIGN" | sort -u)
for FR in $SPEC_FRS; do
  if echo "$DESIGN_FRS" | grep -q "$FR"; then
    echo "  OK  $FR — covered in design"
  else
    echo "  FAIL $FR — not referenced in design"
  fi
done
# Check all design files have FR and AD traces
echo ""
echo "=== File Table Trace Check ==="
grep -P '\| (CREATE|MODIFY)' "$DESIGN" | while IFS= read -r line; do
  file=$(echo "$line" | grep -oP '`[^`]+`' | head -1)
  has_fr=$(echo "$line" | grep -qP 'FR-\d+' && echo "yes" || echo "NO")
  has_ad=$(echo "$line" | grep -qP 'AD-\d+' && echo "yes" || echo "NO")
  echo "  $file: FR=$has_fr AD=$has_ad"
done
```

## Best practices
- Write AD-X entries before filling the file structure table — decisions should drive file layout, not the other way around
- Every rejected alternative in AD-X must state a concrete rejection reason tied to the project's constitution, NFRs, or constraints — "too complex" is not a concrete reason
- The file structure table is the implementation plan's predecessor: every file listed here becomes a task in the implementation plan; keep it precise
- Separate data models (TypeScript interface) from database schemas (SQL DDL) — they often diverge and agents conflate them
- Mark security mitigations with the specific threat they address (SQL injection, CSRF, privilege escalation) — generic "use HTTPS" entries provide no value

## AI-agent gotchas
- Agents copy FR-X IDs from spec to design without verifying the spec's FR-X numbering is complete — gaps in FR numbering (FR-001, FR-003 with no FR-002) propagate silently
- API contracts in design.md are often aspirational and not validated against the spec's AC scenarios — an AC that requires a 422 response code may have no corresponding error schema in the design
- The "Alternatives Considered" table is the highest-hallucination-risk section: agents produce three alternatives that sound reasonable but were never evaluated; prompt explicitly to only list alternatives that were genuinely considered
- File structure tables include files the agent assumes will be needed based on training patterns (e.g., `index.ts` barrel exports) that are not required by any FR — these produce unnecessary tasks in the implementation plan
- Human-in-loop checkpoint: design.md status changes from `Draft` to `Review` by agent, `Review` to `Approved` by human — never let an agent mark its own design as Approved

## References
- https://www.industrialempathy.com/posts/design-docs-at-google/ (Google's approach to design docs)
- https://www.ietf.org/rfc/rfc2119.txt (RFC 2119: SHALL/SHOULD/MAY terminology)
- https://c4model.com/ (C4 model for software architecture diagrams)
- https://adr.github.io/ (ADR organization — related to AD-X pattern in design docs)
- https://swagger.io/specification/ (OpenAPI Specification — for API contracts section)
