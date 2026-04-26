# Agent Integration — Specification Structure

## When to use
- Features with 3+ user personas or 8+ functional requirements where the condensed format is insufficient
- Features requiring formal stakeholder sign-off where completeness is auditable
- Complex integrations where NFRs (performance, security, scalability) must be explicitly contracted before design begins
- When the spec feeds into a multi-agent executor pipeline and full FR/AC traceability is required

## When NOT to use
- MVP features under 5 FRs — use `spec-examples-basic` condensed format instead
- Internal tooling or developer-only features where user persona sections add no value
- Features on a known pattern (nth CRUD endpoint) where all structural decisions are inherited

## Where it fails / limitations
- The "Recommended Skills & Methodologies" section at the bottom is frequently stale — agents generate it once and never update it as design choices are made
- "Open Questions" section is a placeholder that teams skip; ambiguities surface later in design and cause rework
- Full spec v2.0 can reach 500–1200 tokens; in context-constrained executor runs, agents may not load the full spec and miss requirements

## Agentic workflow
The spec-structure process runs in two agent passes. Pass 1: load constitution and any related done/ specs, then generate the backbone — Problem Statement, User Personas, User Stories, and a skeleton FR table with placeholder text. Pass 2: fill each FR with SMART detail, write NFRs, write full AC in Given-When-Then, and complete Out of Scope and Dependencies. This separation prevents agents from conflating requirements discovery with requirement writing.

After both passes, a dedicated review agent checks the quality gate checklist (Completeness, Clarity, Consistency, Context) and returns a structured gap report.

### Recommended subagents
- General Claude subagent (Opus) — Pass 1 (persona/story/FR discovery from fuzzy brief)
- General Claude subagent (Sonnet) — Pass 2 (SMART FR writing, AC formalization, NFR specification)
- General Claude subagent (Haiku) — quality gate checklist validation (structured output task)

### Prompt pattern
```
Pass 1 — Spec backbone:
Read constitution.md and brief: <brief text>.
Output: Problem Statement, 2-3 User Personas, 3-5 User Stories with MoSCoW priority,
FR skeleton table (ID, Requirement placeholder, Traces To, Priority).
Do not write ACs or NFRs yet.
```

```
Pass 2 — Spec body:
Given this spec backbone, fill:
1. Each FR-X with SMART requirement text (one unambiguous SHALL statement).
2. NFR table: performance (<500ms p95), security (relevant controls), scalability targets.
3. AC for each Must-priority FR in Given/When/Then format.
4. Out of Scope: at least 3 explicit exclusions.
5. Dependencies: internal features + external services.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vale` | Lint requirement text for ambiguous words ("easy", "fast", "appropriate") | https://vale.sh |
| `markdownlint` | Enforce section hierarchy and table structure in spec.md | `npm i -g markdownlint-cli` |
| `pandoc` | Export spec.md to PDF/DOCX for stakeholder sign-off | `apt install pandoc` |
| `reqview` | Requirements traceability matrix tool; imports markdown FRs | https://www.reqview.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub PR | SaaS | Yes (gh CLI) | Full spec as PR body; ACs become PR checklist |
| Confluence | SaaS | Partial (REST API) | Enterprise stakeholder review; page hierarchy maps to spec sections |
| Jira (Epic + Story) | SaaS | Partial (REST API) | FR-X → Stories; NFR-X → Constraints; AC → acceptance criteria field |
| Notion (database) | SaaS | Partial | Stakeholder visibility; REST API for programmatic creation |

## Templates & scripts
See `spec-structure/README.md` for the full v2.0 template (inline). See `template-spec/README.md` for the alternative condensed template.

Quality gate script — check completeness before moving to design:
```bash
#!/usr/bin/env bash
# spec-quality-gate.sh SPEC_FILE
SPEC=${1:?usage: spec-quality-gate.sh spec.md}
PASS=true

check() {
  local label=$1; local pattern=$2
  if grep -qP "$pattern" "$SPEC"; then
    echo "PASS  $label"
  else
    echo "FAIL  $label"
    PASS=false
  fi
}

check "Problem Statement"      "^\*\*Who:\*\*"
check "User Stories"           "^### US-\d+"
check "Functional Requirements" "^\| FR-\d+"
check "NFR table"              "^\| NFR-\d+"
check "Acceptance Criteria"    "^\*\*Given:\*\*"
check "Out of Scope"           "^## Out of Scope"
check "Status Approved"        "Status.*Approved"

$PASS && echo "Quality gate: PASS" || echo "Quality gate: FAIL — fix above before design"
```

## Best practices
- The spec v2.0 quality gate has four dimensions (Completeness, Clarity, Consistency, Context) — run all four as a structured review, not a quick skim
- Every NFR must have a numeric target ("< 500ms p95", "10k concurrent users") — qualitative NFRs like "fast response" are rejected at quality gate
- "Open Questions" section should gate the spec from Approved status — unresolved questions are blocker items, not optional notes
- Traceability must be bidirectional: FR → US (forward) and US → AC (forward trace) + AC → FR (back trace validation)
- Recommended Skills section should reference the actual faion skill IDs, not generic names

## AI-agent gotchas
- Agents conflate spec sections with design sections under context pressure — explicit rejection of HOW language in the spec prompt is necessary
- NFR sections generated without numeric targets will cause design-phase debates; enforce numeric targets in the prompt
- The "Related Features" table is often left empty even when feature dependencies exist — always prompt the agent to search done/ specs for related work
- Full spec v2.0 at 800–1200 tokens is safe to include in executor context, but agents may truncate it; provide only the relevant FR and AC sections per task
- Human approval gate (Status: Draft → Approved) must be enforced before design begins; agents that auto-proceed skip stakeholder alignment

## References
- https://www.iso.org/standard/72089.html — ISO/IEC/IEEE 29148 requirements engineering standard
- https://www.scaledagileframework.com/features-and-capabilities/ — SAFe feature requirements
- https://cucumber.io/docs/gherkin/reference/ — Gherkin BDD format
- https://www.reqview.com/doc/traceability-matrix.html — Traceability matrix practices
- https://vale.sh — Prose linting for requirements language
