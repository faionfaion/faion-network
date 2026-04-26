# Agent Integration — Six Core Principles (PMBOK 7)

## When to use
- Validating a PM decision (scope cut, scope add, vendor choice) against principle-based heuristics before committing.
- Auditing an existing project plan to find which guiding principle is being violated.
- Bootstrapping a constitution.md / charter for a new project where you need first-principles framing.
- Coaching a junior PM/agent on "why" a recommendation is good, not just "what."

## When NOT to use
- Pure tactical work (sprint board updates, status reports) — principles add overhead with no decision content.
- Compliance-driven projects where regulatory mandates already prescribe behavior.
- Emergency incident response — switch to OODA / runbooks instead.

## Where it fails / limitations
- The six principles are intentionally abstract; teams reach different conclusions from the same principle.
- "Focus on Value" without measurable success criteria becomes virtue signaling.
- "Sustainability" is the most-skipped principle in tech projects — easy to wave off.
- Provides no priority order between principles when they conflict (e.g., quality vs. value-speed).

## Agentic workflow
Use the principles as a mandatory checklist that an agent runs over any non-trivial PM decision. The agent answers each of the six prompts with evidence; humans review the violations. Anchor the principles in the project's constitution.md so they aren't restated each time.

### Recommended subagents
- `faion-pm-agent` — runs the six-principle audit on a draft plan or decision.
- `faion-sdd-executor-agent` — flags any task that fails the value/quality principles before execution.
- General Claude subagent — produces ADR-style "principle review" appended to design docs.

### Prompt pattern
```
Audit this <plan|decision|ADR> against the PMBOK 7 six core
principles. For each principle output: PASS / WARN / FAIL +
one-sentence evidence. End with the single highest-risk
principle violation and one concrete mitigation.
```

```
Given the project context in <constitution.md>, weight the six
principles for this project (1=low, 5=high) and justify each
weight in one sentence. Output as a yaml block.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Surface PRs/issues touching value or quality concerns | `brew install gh` |
| `pre-commit` | Embeds "Embed Quality" principle as automated gate | `pip install pre-commit` |
| `lighthouse-ci` | Quality + sustainability metrics for web projects | `npm i -g @lhci/cli` |
| `cloud-carbon-footprint` | Sustainability metric for cloud workloads | `npx cloud-carbon-footprint` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | API | Maps features to value/outcomes (Focus on Value) |
| LinearB | SaaS | API | Engineering effectiveness signals (Embed Quality) |
| Climatiq | SaaS | API | Carbon estimates per workload (Sustainability) |
| Confluence | SaaS | API | Holds the principle-based ADRs / decision log |
| Notion | SaaS | API | Same; lighter weight |

## Templates & scripts
See `templates.md` for the principle-by-principle audit table. Inline 6-question audit script:

```bash
#!/usr/bin/env bash
# pmbok7-audit.sh — emit a markdown audit form for a decision.
cat <<'MD'
# PMBOK 7 Audit: <decision>

| Principle | PASS/WARN/FAIL | Evidence |
|-----------|----------------|----------|
| Holistic view | | |
| Focus on value | | |
| Embed quality | | |
| Lead accountably | | |
| Integrate sustainability | | |
| Build empowered teams | | |

## Highest-risk violation
<principle> — <mitigation>
MD
```

## Best practices
- Treat the principles as preconditions, not afterthoughts: run the audit before commitment, not at retrospective.
- For each principle, define one project-specific KPI (e.g., "value" = NPS+activation; "quality" = escaped defects).
- Always name the accountable human for each principle; principles need owners or they drift.
- Re-weight principles per project — a regulated medical product weights "quality" 5/5; an internal hackathon weights "value" 5/5.
- Couple "build empowered teams" with explicit decision-rights (e.g., who can approve scope change, who can ship without review).

## AI-agent gotchas
- LLMs love to mark every principle PASS to be agreeable — force the prompt to identify at least one WARN/FAIL.
- "Sustainability" is poorly represented in training data; supply concrete carbon/energy numbers or skip the principle.
- Don't let agents synthesize the audit and the decision in the same turn — separate "review" from "act."
- Principle audits become noise if run on every issue; gate to decisions worth >X tokens / Y story points.
- Agents conflate "Embed Quality" with "add tests"; force them to cover process quality (review, observability) too.

## References
- PMI PMBOK Guide 7th Edition — Section 3, "Principles of Project Management."
- The Standard for Project Management (PMI, 2021).
- Lean Software Development principles (Poppendieck) — overlaps with "Focus on Value."
