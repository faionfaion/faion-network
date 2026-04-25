# Agent Integration — Advanced Specification Guidelines

## When to use
- Complex features with multiple user types, non-trivial business logic, or measurable NFRs (performance SLAs, security requirements)
- Mission-critical features where incomplete spec leads to costly rework (payment flows, auth systems, data migrations)
- Features that block other features downstream — incomplete spec cascades into blocked design and tasks
- Features requiring alignment across roles (PM, design, engineering) before development starts
- Any spec that will be consumed by an autonomous agent executor — agents cannot infer unstated requirements

## When NOT to use
- Simple CRUD additions with no business logic — use minimal spec (3-5 sections, ~500 tokens)
- Internal refactors with no user-facing behavior change — use a design doc directly
- Experimental spikes — use a problem statement + timebox, not a full spec
- Features where the spec would be longer than the implementation — signs of over-speccing

## Where it fails / limitations
- Persona sections become boilerplate when the writer has no real user research; generic personas ("busy parent") add noise rather than signal unless grounded in real data
- NFRs with quantified targets (< 200ms p95) are only useful if there is a plan to actually measure them; unmeasured NFRs are broken promises
- 14-section specs have high completion overhead — in solo contexts, most sections serve internal alignment, which already exists in the writer's head; trim ruthlessly
- Traceability chains (FR → US → AC) require maintenance discipline; broken links are worse than no links because they create false confidence
- Acceptance criteria coverage checklists ("security scenarios: unchecked") surface gaps but do not fill them; an agent following the template will produce empty checkbox items without raising them as blockers

## Agentic workflow
An agent can draft a full spec given a problem description, user research notes, and constitution constraints. The highest-value sections for agent drafting are: functional requirements (mechanical from user stories), acceptance criteria (scenario expansion from FR), and out-of-scope table (inversion of in-scope list). Persona writing and NFR quantification require human input — the agent should leave placeholder prompts and request specifics rather than hallucinating numbers. Human review is mandatory before status moves from `Draft` to `Approved`.

### Recommended subagents
- `faion-sdd-executor-agent` — can be invoked in "spec review" mode to validate traceability before a spec is approved; not a dedicated spec-writer agent

### Prompt pattern
```
Write a full SDD specification for: <feature name>.

Context:
- Constitution: <paste relevant sections>
- Problem: <problem statement>
- User types: <list>
- Key constraints: <performance, security, etc.>

Produce all 14 sections. For NFR targets, insert [MEASURE_NEEDED] where you cannot
determine a specific number without measurement data. For personas, use the provided
user types — do not invent personas. Set status: Draft.
```

```
Review this spec for traceability gaps.
For each FR-X, verify: (1) it traces to at least one US-X, (2) at least one AC-X
validates it. For each NFR-X, verify it has a measurement method and priority.
Output: gap table. Do not rewrite the spec.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| vale | Prose linting — enforces "SHALL" over "should", flags passive voice in requirements | `brew install vale` / https://vale.sh |
| markdownlint | Validates spec markdown structure (heading levels, table format) | `npm install -g markdownlint-cli` / https://github.com/DavidAnson/markdownlint |
| grep / ripgrep | Traceability audit — find FR-X references without matching AC-X | System / https://github.com/BurntSushi/ripgrep |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — REST + GraphQL | User stories as issues; FR/AC as sub-items; limited traceability |
| Notion | SaaS | Partial — REST API | Structured spec as database; good for persona/FR tables |
| Confluence | SaaS | Partial — REST API | Enterprise alignment tool; harder to automate traceability |
| Loom / Figma | SaaS | No | Wireframe and video links in the Appendix section — manual |

## Templates & scripts
See `templates.md` for the full 14-section spec template.

Traceability audit script — checks that every FR-X appears in at least one AC-X:
```bash
#!/usr/bin/env bash
# usage: ./check-traceability.sh spec.md
set -euo pipefail
SPEC="$1"
FRS=$(grep -oP 'FR-\d+' "$SPEC" | sort -u)
ACS=$(grep -oP 'AC-\d+.*' "$SPEC")
echo "=== Traceability Audit ==="
for FR in $FRS; do
  if echo "$ACS" | grep -q "$FR"; then
    echo "  OK  $FR — referenced in AC section"
  else
    echo "  MISSING $FR — no AC references this requirement"
  fi
done
```

## Best practices
- Write the problem statement before anything else; if it cannot be written in five sentences, the feature is not understood well enough to spec
- For each NFR, include the measurement method in the same bullet — a target without a measurement plan is aspirational, not contractual
- Keep acceptance criteria at the scenario level (Given/When/Then), not the implementation level — "cart total updates" not "Redux store dispatches updateCart action"
- Define Out of Scope before writing functional requirements — it prevents scope creep from entering the spec mid-draft
- Use the traceability chain (FR → US → AC) as a completeness check, not as bureaucratic overhead — every FR that has no AC is untestable by definition

## AI-agent gotchas
- Agents expand user stories into acceptance criteria mechanically but miss error paths, edge cases, and security scenarios unless explicitly prompted for each category
- NFR hallucination: agents will invent plausible-sounding targets (< 150ms, 99.9% uptime) with no basis in project reality; always mark these for human validation
- Persona inflation: agents generate detailed, coherent personas that feel credible but are fictional — real personas must come from research or explicit human input
- The "14 sections" framing pressures agents to fill every section even when content is thin; thin sections are worse than omitted sections because they add false completeness signals
- Human-in-loop checkpoint: spec status `Draft → Approved` requires human sign-off; agent should not auto-approve even if all checklist items are checked

## References
- https://standards.ieee.org/standard/29148-2018.html (IEEE 29148-2018 Requirements Engineering)
- https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/ (INVEST criteria — Bill Wake)
- https://www.impactmapping.org/ (Impact Mapping — goal-oriented planning)
- https://www.jpattonassociates.com/user-story-mapping/ (User Story Mapping — Jeff Patton)
- "Writing Effective Use Cases" — Alistair Cockburn
