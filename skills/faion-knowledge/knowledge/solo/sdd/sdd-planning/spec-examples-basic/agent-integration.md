# Agent Integration — Specification Examples: Basic

## When to use
- When writing a condensed spec for an MVP feature with clear, well-understood requirements
- Training a spec-writing agent on what "good enough" looks like for fast iteration cycles
- Validating that a generated spec is not over-engineered relative to the feature scope
- As a reference when the full spec-structure template feels excessive for the task at hand

## When NOT to use
- Features with multiple user personas and complex business rules — use the full spec-structure template
- Regulated domains (payments, healthcare, legal) where traceability completeness is non-negotiable
- Features with more than 5 user stories or 10 functional requirements

## Where it fails / limitations
- "One happy path, one error case" AC coverage is insufficient for security-sensitive features — always add an unauthorized-access AC even for basic specs
- Skipping NFRs entirely works for internal tools but not for customer-facing features with latency or availability requirements
- The condensed format lacks an Open Questions section; ambiguities get buried in assumptions

## Agentic workflow
Provide the basic spec example as a reference output in the system prompt when generating a condensed spec. The agent uses it as a structural anchor, producing the five minimum sections (Problem Statement, User Stories, Functional Requirements, Acceptance Criteria, Out of Scope) without padding. A lightweight review pass checks that every FR traces to a US and every AC is testable.

For very simple features (single endpoint, single model), a Haiku-class agent can fill the condensed format accurately; Sonnet is needed when problem statements require interpretation.

### Recommended subagents
- General Claude subagent (Haiku) — filling condensed spec from clear brief; low token cost
- General Claude subagent (Sonnet) — when the problem statement needs interpretation or scope negotiation

### Prompt pattern
```
Write a condensed spec.md for this feature: <description>.
Follow the basic spec example structure: Problem Statement, User Stories (max 3),
Functional Requirements (Must only), Acceptance Criteria (1 happy path + 1 error),
Out of Scope.
Keep each requirement under 20 words. No implementation details.
```

```
Review this condensed spec. Verify:
- Every FR traces to a US (mark FR-X → US-X).
- Every AC uses Given/When/Then language.
- At least one error-case AC exists.
- Out of Scope has at least 2 explicit exclusions.
Output: PASS or list of gaps.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vale` | Check for vague requirement language ("easily", "simple", "fast") | https://vale.sh |
| `wc -l` | Quick size check — condensed spec should be under 80 lines | system |
| `grep -c "FR-"` | Count FRs to verify scope is genuinely small | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub PR description | SaaS | Yes (gh CLI) | Condensed spec fits naturally as PR body; stakeholder review via comments |
| Linear issue body | SaaS | Yes (API) | Map condensed spec to issue; ACs become checklist |
| Notion page | SaaS | Partial | Good for async stakeholder review; API write support |

## Templates & scripts
The full condensed spec is shown inline in `spec-examples-basic/README.md` (authentication example). No additional template needed — the example IS the template for basic features.

Automated scope-size check:
```bash
#!/usr/bin/env bash
# spec-size-check.sh SPEC_FILE
SPEC=${1:?usage: spec-size-check.sh spec.md}
FR_COUNT=$(grep -c "^| FR-" "$SPEC" 2>/dev/null || echo 0)
US_COUNT=$(grep -c "^### US-" "$SPEC" 2>/dev/null || echo 0)
AC_COUNT=$(grep -c "^### AC-" "$SPEC" 2>/dev/null || echo 0)
echo "US: $US_COUNT | FR: $FR_COUNT | AC: $AC_COUNT"
if [ "$FR_COUNT" -gt 10 ]; then
  echo "WARNING: $FR_COUNT FRs — consider using full spec-structure template"
fi
if [ "$AC_COUNT" -lt 2 ]; then
  echo "WARNING: Need at least 1 happy path + 1 error AC"
fi
```

## Best practices
- Start with the condensed format for every feature; upgrade to the full template only when scope grows beyond 5 FRs
- Write the Out of Scope section immediately after User Stories — it prevents scope creep from accumulating before FRs are written
- "Must" priority only in condensed specs — anything "Should" or "Could" goes to a future spec or backlog item
- Token cost of a condensed spec (1100–1650 tokens per the README) means agents can include it in full in their context without budget pressure

## AI-agent gotchas
- Agents generating condensed specs tend to add "Technical Notes" or "Architecture" sections — these belong in design.md; reject them
- The `## Out of Scope` section is the most commonly omitted section when agents condense — make it a required field in your prompt
- Condensed ACs generated without Given/When/Then often read like requirements rather than verifiable scenarios — always enforce the BDD format even for basic specs
- If the agent produces more than 3 US or more than 6 FR, the feature is not "basic" — escalate to full spec-structure process

## References
- https://oauth.net/2/ — OAuth 2.0 (referenced authentication example)
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html — OWASP auth security
- https://cucumber.io/docs/gherkin/reference/ — Gherkin syntax for ACs
- https://www.scaledagileframework.com/features-and-capabilities/ — SAFe feature definition (context for MoSCoW)
