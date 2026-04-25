# Agent Integration — Writing Specifications

## When to use
- Before any LLM-assisted implementation: the spec is the anti-hallucination anchor
- When requirements come as vague user requests or Slack messages — transform them into structured FR-X + AC-X artifacts
- Writing CLAUDE.md or project rules files: use the three-tier boundary system (Always / Ask First / Never)
- Producing a spec that will be the primary context for an execution agent — it must be LLM-executable, not just human-readable
- Any feature affecting multiple files, teams, or external APIs — explicit contracts prevent drift

## When NOT to use
- Bug fix with a known root cause and clear fix — write the fix, not a spec
- Configuration-only change — no functional requirements to specify
- One-off script or throwaway prototype — overhead exceeds value
- When requirements are so volatile they'll change before implementation starts — spec after stabilization

## Where it fails / limitations
- LLMs write fluent specs but miss non-obvious constraints: performance SLOs, security edge cases, data-at-rest requirements — human review is mandatory
- The "curse of instructions": spec > 200 FRs causes agent adherence to drop; prioritize ruthlessly and split into phases
- Given-When-Then scenarios produced by agents are often too happy-path; error handling, boundary conditions, and security scenarios require explicit prompting
- Agents conflate "WHAT to build" with "HOW to build" when writing specs — enforce the separation with a post-spec review prompt
- Specs written without an existing codebase context produce incorrect assumptions about what already exists

## Agentic workflow
A spec-writing agent receives a problem statement and user stories, then generates a structured spec using the Minimal Viable Spec or Full Spec template. A second agent (fresh context, reviewer role) validates the spec against SMART criteria and the AC coverage checklist, flagging vague requirements and missing error/security scenarios. The spec is not considered complete until the reviewer outputs "SPEC APPROVED." The approved spec then becomes the primary system context for all downstream execution agents.

### Recommended subagents
- Haiku — fill out spec template sections (mechanical form completion)
- Sonnet — review spec for clarity, SMART compliance, AC completeness
- Opus — architect complex multi-system specs where holistic thinking matters
- `faion-task-executor-agent` — consumes the approved spec as its first context document

### Prompt pattern
```
You are a spec writer. Problem statement: [description]
Write a spec following the Minimal Viable Spec structure:
1. Problem (who cannot do what, why it matters)
2. Solution (high level, no implementation details)
3. Requirements: FR-001 through FR-NNN, each SHALL statement, SMART criteria
4. Acceptance Criteria: AC-001 through AC-NNN, Given-When-Then format
5. Out of Scope (explicit exclusions)
Use concrete values everywhere. Replace all vague terms: "fast" → "< 500ms p95",
"many" → "10,000 concurrent", "secure" → specific mechanism.
```

```
Review this spec for LLM executability. Check:
1. Every FR has at least one AC
2. ACs use concrete values (no "valid", "fast", "many")
3. Error scenarios are covered (what happens when X fails)
4. Security scenario present (auth bypass, injection attempt)
5. "Out of Scope" section exists
Output: APPROVED or list of issues to fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Generate spec from problem statement; inject as CLAUDE.md context | https://docs.anthropic.com/en/docs/claude-code |
| `gh` (GitHub CLI) | Create spec as GitHub issue or PR for review | https://cli.github.com |
| ChatPRD | SaaS spec assistant | https://www.chatprd.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ChatPRD | SaaS | Partial | Generates PRD from description; API not public |
| Linear | SaaS | Yes | Store specs as issues with FR- prefix; GraphQL API |
| Notion | SaaS | Partial | Spec hosting; REST API for read/write |
| GitHub Issues | SaaS | Yes | Spec as issue; agent can read/write via `gh` CLI |

## Templates & scripts
See `templates.md` for Minimal Viable Spec and Full Spec templates.

Spec quality gate script (inline):
```bash
#!/usr/bin/env bash
# check-spec.sh <spec_file>
# Validates basic LLM-executability of a spec
set -euo pipefail
SPEC=${1:-spec.md}
ERRORS=0
check() {
  if ! grep -q "$1" "$SPEC"; then
    echo "FAIL: Missing '$1'"
    ERRORS=$((ERRORS + 1))
  else
    echo "OK: Found '$1'"
  fi
}
check "FR-0"
check "AC-0"
check "Given"
check "When"
check "Then"
check "Out of Scope"
# Check for vague terms
for VAGUE in "fast" "many" "large" "good" "proper" "appropriate"; do
  COUNT=$(grep -ci "\b$VAGUE\b" "$SPEC" 2>/dev/null || echo 0)
  if [ "$COUNT" -gt 0 ]; then
    echo "WARN: Vague term '$VAGUE' found $COUNT times — replace with measurable value"
  fi
done
[ "$ERRORS" -eq 0 ] && echo "SPEC OK" || echo "SPEC FAILED: $ERRORS blocking issues"
exit "$ERRORS"
```

## Best practices
- Write specs in the same repository as the code (`.aidocs/`), not in a separate wiki — agents can read them as file context
- Use the three-tier boundary system in the spec's Boundaries section: Always / Ask First / Never — this maps directly to agent autonomy settings
- Include real code examples in the spec for patterns that must be followed — "show don't tell" works for agents as well as humans
- Divide large specs into phases with explicit phase boundaries before handing to an execution agent — prevents context overflow and drift
- Trace every FR to at least one user story (US-X) and at least one AC — traceability makes the spec machine-verifiable

## AI-agent gotchas
- Agents produce specs in active voice about the system ("The system should...") but then switch to passive voice mid-spec; instruct to use SHALL consistently for requirements
- Without the "Out of Scope" section, agents include out-of-scope features in their implementation — this section is the most important boundary setter
- Specs that use relative comparisons ("faster than current", "more secure") give the agent no anchor; always provide absolute baselines
- An agent reading its own generated spec is unreliable for completeness review — always use a second, fresh-context agent for review
- The AC coverage checklist (happy path, error handling, boundary conditions, security, performance, accessibility) is rarely complete without explicit instruction; prompt for each category separately

## References
- https://addyosmani.com/blog/good-spec/ — Addy Osmani, writing good specs for AI agents
- https://www.humanlayer.dev/blog/writing-a-good-claude-md — HumanLayer, CLAUDE.md writing guide
- https://www.anthropic.com/engineering/claude-code-best-practices — Anthropic, Claude Code best practices
- https://www.productcompass.pm/p/ai-prd-template — AI PRD template by OpenAI product lead
