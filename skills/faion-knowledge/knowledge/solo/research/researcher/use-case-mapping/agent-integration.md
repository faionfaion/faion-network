# Agent Integration — Use Case Mapping

## When to use
- Translating validated user research into specifications eng can build from.
- Drafting acceptance criteria when stories are too thin and edge cases are missed in production.
- Cross-team alignment: business, eng, and QA need a shared model of "what users do".
- Compliance / regulated domains where alternative flows must be explicit.

## When NOT to use
- Pre-discovery: writing use cases before validating problem produces fiction.
- For purely internal scripts / dev tooling — overhead outweighs benefit.
- For exploratory prototyping where requirements are intentionally fuzzy.
- When the team uses Jobs-to-Be-Done + user-story-mapping; pick one model, not three.

## Where it fails / limitations
- Use cases drift from reality if not maintained alongside code; treat them as living docs.
- Over-specification kills agility — keep at user-goal level, not subfunction level, unless safety-critical.
- Alternative flows multiply combinatorially; aim for ~3-5 alts per main flow, not exhaustive.
- "System actor" abstraction confuses agents — they assume the system has agency and write inside-out flows.
- UML use case diagrams add little value over a prioritized table; skip the diagram unless required by stakeholders.

## Agentic workflow
Pipeline: extract actors and goals from interviews → draft main flows → enumerate alternatives → cross-link to tests. Agents are good at templating use cases from validated research and at suggesting missed alternative flows; bad at picking the right level of granularity. Keep humans in the level decision.

### Recommended subagents
- `actor-extractor` (haiku) — pulls actors and primary goals from interviews + persona docs.
- `flow-drafter` (sonnet) — generates main success scenarios in numbered Actor/System format.
- `alt-flow-enumerator` (sonnet) — proposes extension/exception/branch alternatives per main flow step.
- `test-linker` (haiku) — maps each use case step to a test ID for traceability.
- `faion-sdd-executor-agent` to push use cases through SDD spec → design → test-plan lifecycle.

### Prompt pattern
```
Role: flow-drafter.
Input: actor=X, goal=Y, validated_pains.json, current_solutions.json.
Output JSON: {use_case_id, actor, level, preconditions:[...], main_flow:[{step, who:"actor|system", action}], postconditions:[...]}.
Rule: max 10 steps in main flow; if >10, split into sub-use-cases. Write actor steps first, system response second.
```

```
Role: alt-flow-enumerator.
Input: main_flow JSON.
Task: propose alternatives for steps with branching/validation/error potential.
Output JSON: {alts:[{trigger_step, type:"extension|exception|branch", flow:[...]}]}.
Constraint: max 5 alts; sort by likelihood of occurrence in production.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `plantuml` | Render use-case diagrams from text | https://plantuml.com |
| `mermaid-cli` | Render flow diagrams in Markdown | https://github.com/mermaid-js/mermaid-cli |
| `gherkin-lint` | Lint Gherkin scenarios derived from use cases | https://github.com/vsiakka/gherkin-lint |
| `cucumber` | Run Gherkin tests linked to use case IDs | https://cucumber.io |
| `dasel` / `yq` | Manipulate use case JSON/YAML repos | https://github.com/TomWright/dasel |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (API) | Use case = epic with sub-tasks; keep IDs in title. |
| Jira | SaaS | Yes (REST API) | Native Issue Type "Use Case" possible; heavy. |
| Notion | SaaS | Yes (API) | Database-style use case tables with relations. |
| Confluence | SaaS | Yes (API) | Long-form use case spec storage. |
| Lucidchart / Whimsical | SaaS | Partial (limited API) | Use case diagrams for stakeholder reviews. |
| draw.io / diagrams.net | OSS | Yes (CLI export) | Free, version-controllable diagrams. |
| StoriesOnBoard / FeatureMap | SaaS | Yes (API) | Story map ↔ use case mapping. |

## Templates & scripts
See `templates.md` for Use Case Specification and Use Case Summary Table.

Inline use case → Gherkin generator (Python, ≤40 lines):
```python
import json, sys
uc = json.load(open(sys.argv[1]))
print(f"Feature: {uc['use_case_id']} {uc.get('name','')}")
for pre in uc.get("preconditions", []):
    print(f"  Background: Given {pre}")
print(f"\n  Scenario: Main success — {uc.get('name','')}")
for step in uc["main_flow"]:
    actor = "When" if step["who"] == "actor" else "Then"
    print(f"    {actor} {step['action']}")
for post in uc.get("postconditions", []):
    print(f"    Then {post}")
for alt in uc.get("alternative_flows", []):
    print(f"\n  Scenario: Alt — {alt['type']} at step {alt['trigger_step']}")
    for step in alt["flow"]:
        who = "When" if step.get("who") == "actor" else "Then"
        print(f"    {who} {step['action']}")
```

## Best practices
- Use case ID is the connective tissue — link tests, stories, designs, and analytics events back to UC-XXX.
- Write actor actions first, system responses second; agents tend to invert this and the doc reads system-centric.
- Stay at user-goal level by default. Drop to subfunction only for safety-critical or compliance flows.
- Prioritize alts by production likelihood, not by edge-case completeness; perfectionism wastes review cycles.
- Cross-link related use cases (Includes / Extends) but avoid deep hierarchies — three levels max.
- Pair every use case with a "Definition of Ready" review with eng before it enters sprint.

## AI-agent gotchas
- LLMs over-decompose into subfunctions; explicitly cap step count (e.g., max 10).
- Agents invent preconditions that aren't validated ("user has API key") — require precondition citations from interviews or system specs.
- "System validates X" is the most-fabricated step type; require validation rules to come from a business-rules document.
- Postconditions are skipped under token pressure; add a self-check that postconditions length > 0.
- Cross-flow consistency (UC-002 calls UC-005) is not maintained across re-generations; keep a registry file.
- Human-in-loop checkpoints: (1) actor + goal sign-off, (2) level (user vs subfunction) decision, (3) alt-flow trim.

## References
- Alistair Cockburn, "Writing Effective Use Cases" (canonical reference).
- Karl Wiegers & Joy Beatty, "Software Requirements" (3rd ed.) — chapters on use cases and flows.
- IEEE 29148 — requirements engineering standard.
- Gojko Adzic, "Specification by Example" — bridge from use cases to executable specs.
- Cem Kaner, "An Introduction to Scenario Testing" — alt-flow generation techniques.
