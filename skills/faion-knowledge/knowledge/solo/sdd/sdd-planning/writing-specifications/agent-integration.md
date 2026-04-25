# Agent Integration — Writing Specifications

## When to use
- Feature is new and requirements have not been written down anywhere
- Existing feature needs scope expansion and current spec is absent or too vague to drive design
- Constitution is new and needs to capture tech decisions before development begins
- Stakeholder and developer have different mental models of what the feature does
- Requirements exist informally (Slack messages, verbal agreements) and need to be formalized

## When NOT to use
- Bug report with a clear reproduction path — write a task directly, not a spec
- Infrastructure change (server config, deployment pipeline) with no user-visible behavior
- Feature already has an approved spec — open and amend it rather than re-writing from scratch
- Experiment/spike where the output will determine whether to proceed at all

## Where it fails / limitations
- Phase 1 (load context) requires `.aidocs/constitution.md` to exist; new projects stall if constitution is written in the same session
- Socratic dialogue cannot be automated — user must be present for requirements elicitation phases
- SMART criteria assessment requires domain knowledge that Haiku and fast-path agents lack
- Large specs (>300 lines) lose coherence; agents begin contradicting earlier sections
- "Out of Scope" is the hardest section to populate correctly — agents tend to leave it empty or list obvious exclusions

## Agentic workflow
A spec-writing agent begins by loading constitution and related completed specs to establish vocabulary and patterns. Requirements elicitation runs as a synchronous dialogue with the user (not delegatable to a subagent). Once requirements are captured, a Sonnet agent drafts each section sequentially, showing it to the user before moving to the next. SMART validation and traceability checking are delegated to `faion-sdd-reviewer-agent (mode: spec)` as a final gate. The approved spec is saved and the feature directory is created under `.aidocs/features/backlog/`.

### Recommended subagents
- `faion-sdd-reviewer-agent (mode: spec)` — SMART/INVEST compliance, FR→US traceability, completeness check
- Any Opus agent for constitution writing — requires complex trade-off reasoning across tech choices

### Prompt pattern
```
You are writing spec.md for feature: {feature_name}
Constitution: {constitution_summary}
Related completed features: {done_feature_slugs}

Phase 1: Ask the user "Tell me about the problem. Who suffers and how?"
After each answer, apply Five Whys (one why per turn, stop when root cause found).
Do not proceed to drafting until problem is clear.
```

```
Draft spec.md section by section for feature: {feature_name}
Collected requirements: {requirements_text}

Order: problem statement → personas (min 2) → user stories → FR-X (SMART) →
NFR-X → acceptance criteria (Given-When-Then) → out of scope → dependencies

Show each section to user before continuing. Do not batch sections.
Every FR must reference a US. Every AC must reference a FR.
Save to: .aidocs/features/backlog/{NN}-{feature}/spec.md
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ls .aidocs/features/backlog/` | Find next available feature number (NN prefix) | built-in |
| `grep -c "^### FR-"` | Count functional requirements in spec | built-in |
| `grep "so that"` | Verify user stories have benefit clauses | built-in |
| `grep -c "Given:"` | Count Given-When-Then acceptance criteria | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes | Sync FR-X items as issues; `GET /issues` for backlog import |
| Jira | SaaS | Yes | Epic → Story → AC hierarchy maps to spec structure |
| Productboard | SaaS | Partial | User evidence API for grounding requirements in research |
| Canny | SaaS | Partial | Feature vote data useful for MoSCoW prioritization input |
| GitHub Issues | SaaS | Yes | `gh issue list --label spec` for existing requirement tracking |

## Templates & scripts
See `spec-structure.md` for the full spec template v2.0 and `spec-requirements.md` for SMART criteria details.

Feature directory bootstrap:
```bash
#!/usr/bin/env bash
# Create feature directory structure for new spec
DOCS_DIR=".aidocs/features/backlog"
# Find next available two-digit prefix
last=$(ls "$DOCS_DIR" 2>/dev/null | grep -Eo "^[0-9]+" | sort -n | tail -1)
next=$(printf "%02d" $(( ${last:-0} + 1 )))
read -rp "Feature slug (e.g. user-auth): " slug
feature_dir="$DOCS_DIR/${next}-${slug}"
mkdir -p "$feature_dir"
echo "# Spec: ${slug}" > "$feature_dir/spec.md"
echo "**Status:** Draft" >> "$feature_dir/spec.md"
echo "Created feature directory: $feature_dir"
```

## Best practices
- Write problem statement in terms of user pain, not feature description — "Users cannot export data" not "We need an export button"
- Each persona needs a role, goal, pain point, and context (when/where they use the feature); two fields is not enough
- MoSCoW priority must be assigned to every FR; unclassified requirements default to "must" during implementation, which causes scope creep
- NFRs without numbers are not enforceable — "response time < 500ms p95" vs "fast response"
- Link spec to related features in `features/done/` — agents will reuse established patterns rather than reinventing
- Validate the spec checklist before marking approved: SMART, INVEST, traceability, AC testability
- Out of scope items should name specific features that were explicitly discussed and rejected, not generic exclusions

## AI-agent gotchas
- Agents write "as a user, I want X" without the "so that Y" — the benefit clause is where value hides; enforce it
- Five Whys loops: agents stop at 3 whys because they run out of context or confidence — prompt explicitly "one more why"
- Agents treat NFRs as optional sections and write vague ones — enforce "must have a number and a unit" rule
- Constitution writing anti-pattern: agents inventory the tech stack but skip the "why" for each choice — rationale is what constitution is for
- AC items are frequently not testable: "system should handle errors gracefully" has no Given-When-Then — reject these
- When spec is long, agents begin contradicting earlier sections by turn 15+ — break large features into sub-specs

## References
- [User Stories Applied — Mike Cohn](https://www.mountaingoatsoftware.com/books/user-stories-applied)
- [Specification by Example — Gojko Adzic](https://gojko.net/books/specification-by-example/)
- [IREB Requirements Engineering Fundamentals](https://www.ireb.org/en/cpre/fundamentals/)
- [Jobs-to-be-Done Framework](https://jtbd.info/)
- [Product Requirements Document Guide — ProductPlan](https://www.productplan.com/learn/product-requirements-document/)
