# Agent Integration — Specification Requirements

## When to use
- Starting any non-trivial feature (estimated >3 tasks or touching multiple system layers)
- Stakeholder has described a need in plain language — needs translation into traceable requirements
- Feature has ambiguous scope and "out of scope" must be made explicit before design begins
- Multiple user personas affected — need to distinguish which requirements serve which users
- Acceptance criteria will be used to drive automated tests (BDD/Gherkin)

## When NOT to use
- Bug fix with a clear, already-agreed-upon fix — spec overhead exceeds value
- Purely internal refactor with no user-facing behavior change
- Spike or proof-of-concept — spec assumes known requirements; spikes discover them
- When design is already finalized and requirements are being back-filled without intent to use them

## Where it fails / limitations
- Agents produce SMART-sounding requirements that fail the "Achievable" and "Relevant" criteria when they lack business context — always supply a business value statement in the prompt
- Generated acceptance criteria in Given-When-Then format often miss boundary conditions and security scenarios unless coverage checklist is explicitly required
- INVEST validation for user stories requires knowledge of team velocity; agents cannot know this
- MoSCoW classification output by agents defaults to "Must" for everything without scope constraints — enforce "Must ≤ 60% of scope" in the prompt

## Agentic workflow
A planning subagent reads a product brief or feature request, extracts personas, writes user stories with INVEST validation, produces FR-X requirements with MoSCoW classification, and generates AC-X acceptance criteria in Given-When-Then format. The output spec.md is reviewed by a human and approved before the design phase starts. The `faion-sdd-executor-agent` later uses FR-X → AC-X traceability to validate that each implementation task satisfies its requirement.

### Recommended subagents
- `faion-sdd-executor-agent` — reads spec.md during task execution to verify AC-X criteria are met
- Planning subagent (claude-opus-4-7) — full spec authoring from brief; needs multi-step reasoning for persona+story+AC chain

### Prompt pattern
```
Given the following feature brief: {brief}
1. Define 2 user personas (name, role, goal, pain points).
2. Write user stories in "As a [persona], I want [action], so that [benefit]" format.
   Validate each against INVEST criteria — flag any that fail.
3. Write FR-X functional requirements using "System SHALL..." format.
   MoSCoW: Must ≤ 60% of scope. Each FR traces to a user story.
4. Write NFR-X for performance, security, availability.
5. Write AC-X acceptance criteria in Given-When-Then for each Must FR.
   Cover: happy path, error handling, boundary conditions.
6. Define In Scope and Out of Scope sections explicitly.
Output: spec.md following the template in templates.md.
```

```
Review spec.md. For each FR-X check:
- Does it trace to a user story?
- Is the requirement testable (pass/fail possible)?
- Is there a corresponding AC-X?
Output a traceability matrix: FR-X | US-X | AC-X | Testable | Missing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cucumber` | Execute Given-When-Then acceptance criteria as automated tests | `gem install cucumber` / https://cucumber.io |
| `behave` | Python BDD framework for AC-X execution | `pip install behave` / https://behave.readthedocs.io |
| `reqif-tool` | Import/export requirements in ReqIF standard format | https://github.com/strictdoc-project/strictdoc |
| `strictdoc` | Requirements management + traceability in Markdown/RST | `pip install strictdoc` / https://strictdoc.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — REST + GraphQL | FR-X as Issues with custom fields; AC-X as checklists |
| GitHub Issues | SaaS | Yes — GraphQL API | Lightweight; FR-X as issues with acceptance-criteria label |
| Notion | SaaS | Yes — REST API | Good for rich spec docs with linked databases for traceability |
| Confluence | SaaS | Partial — REST API | Common in enterprise; agents can write via API |
| Coda | SaaS | Yes — REST API | Table-based traceability matrices work well |
| StrictDoc | OSS | Yes — file-based | Markdown-native requirements with auto-generated traceability |

## Templates & scripts
Full spec templates in `templates.md`. See `spec-advanced-guidelines.md` for edge cases.

Inline — validate FR-X traceability in a spec.md:
```bash
#!/usr/bin/env bash
# check-traceability.sh — list FR-X that lack AC-X reference
SPEC="${1:-spec.md}"
echo "FR items without AC reference:"
grep -n "^### FR-" "$SPEC" | while IFS= read -r line; do
  lineno=$(echo "$line" | cut -d: -f1)
  fr=$(echo "$line" | grep -o "FR-[0-9]*")
  # Check next 15 lines for AC reference
  if ! sed -n "$((lineno+1)),$((lineno+15))p" "$SPEC" | grep -q "AC-"; then
    echo "  $fr (line $lineno) — no AC-X reference found"
  fi
done
```

## Best practices
- Write the Business Value Statement before any requirements — agents and reviewers need the "why" anchor
- Use FR-X IDs from the first line; never use section headings as requirement identifiers
- Every FR must have at least one AC; agent output without AC is incomplete spec
- Out of Scope must list specific features with reasons — "not in this release" without a reason is not sufficient
- Keep spec.md under 500 lines; if larger, the feature scope is too broad — split into sub-features
- Run through the coverage checklist (happy path, error handling, boundaries, security, performance) for every Must FR
- Never start design.md until spec.md has human sign-off — design locked to unsigned spec wastes effort

## AI-agent gotchas
- Agents omit "Relevant" and "Time-bound" from SMART criteria unless both are explicitly in the prompt
- Given-When-Then output often reuses the same "Then" clause for multiple scenarios — require unique, specific outcomes
- Agents will write acceptance criteria that are not actually testable ("system should feel fast") — require quantitative values for all NFRs
- Security scenarios (injection, auth bypass) are systematically skipped unless the coverage checklist is in the prompt
- Spec-to-design handoff is a human checkpoint; agents must not begin design.md until spec is approved
- Large specs (>300 lines) fragment agent context — pass only relevant FR-X sections to design subagent

## References
- https://cucumber.io/docs/bdd/ — BDD and Given-When-Then
- https://www.iiba.org/business-analysis-certifications/babok/ — BABOK requirements engineering
- https://www.agilebusiness.org/page/ProjectFramework_10_MoSCoWPrioritisation — MoSCoW method
- https://strictdoc.readthedocs.io — StrictDoc OSS requirements tool
- https://www.projectsmart.co.uk/brief-history-of-smart-goals.php — SMART criteria
