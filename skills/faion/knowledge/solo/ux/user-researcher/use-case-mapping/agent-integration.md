# Agent Integration — Use Case Mapping

## When to use
- Requirements elicitation: translating stakeholder conversations into structured system behavior
- Before writing tickets: ensuring features cover all actors and alternative flows, not just the happy path
- API design: mapping use cases to endpoints before writing any code
- QA test planning: use cases map 1:1 to test scenarios and edge case coverage
- Onboarding new engineers: use case specifications are faster to parse than code for understanding what a system does

## When NOT to use
- During early ideation when scope is still fluid — formalized use cases lock in assumptions too early
- For pure UI/visual design tasks where user flow diagrams (journey maps) communicate better
- For internal batch jobs or background processes with no human actor
- When the team is using BDD with Gherkin — use cases and Gherkin scenarios overlap; pick one to avoid double documentation

## Where it fails / limitations
- Use case mapping is actor-centric; it does not capture data models, state machines, or system internals
- Alternative flows are commonly under-specified — teams document the happy path and ship without mapping errors
- Use cases go stale quickly if not linked to implementation; they become archaeology rather than living documentation
- The diagram component (use case diagram) adds effort but little value in solo/small-team contexts — the specification table is enough
- Agent-generated use cases miss implicit preconditions that are obvious to domain experts but not to an LLM

## Agentic workflow
Claude subagents can draft use case specifications from product descriptions or user story input, generate the Use Case Summary Table from a list of features, and identify missing alternative flows by pattern-matching against common error categories (auth failure, network error, validation error, empty state). The agent output is a first draft that requires review by a domain expert for completeness of preconditions and alternative flows.

### Recommended subagents
- `faion-persona-builder-agent` — maps use cases from persona + goal input; generates use case specifications
- `faion-sdd-executor-agent` — uses finalized use cases to generate QA test scenarios

### Prompt pattern
```
Generate use case specifications for the following product feature.
For each use case:
1. Identify the primary actor and their goal
2. List 2-3 preconditions
3. Write the main success scenario as actor/system step pairs
4. Add at least 2 alternative flows: one for validation failure, one for the most likely error

Feature: {feature description}
Actors: {list of user roles}
```

```
Review these use cases for missing alternative flows.
For each use case, check: auth failure, network/timeout, empty state, permission denied.
Add missing alternatives in the same format as existing ones.

Use Cases: {specifications}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `plantuml` | Render use case diagrams from text | plantuml.com; `brew install plantuml` |
| `mermaid-cli` | Render use case / sequence diagrams in CI | `npm i -g @mermaid-js/mermaid-cli` |
| `structurizr-cli` | C4 model + use case documentation as code | github.com/structurizr/cli |
| `notion` API | Store and link use case specifications to tickets | developers.notion.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes | API for creating linked issues from use cases |
| Notion | SaaS | Yes | Database for use case specification store |
| Confluence | SaaS | Yes | REST API for publishing specs to team wiki |
| PlantUML Server | OSS | Yes | Self-host; accepts text, returns diagram PNG |
| Lucidchart | SaaS | Partial | API for diagram creation; limited shape support |

## Templates & scripts
See `templates.md` for Use Case Specification and Use Case Summary Table.

Inline helper — generate PlantUML use case diagram from spec table:
```python
def specs_to_plantuml(actors: list[str], use_cases: list[dict]) -> str:
    """
    use_cases: [{"id": "UC-001", "name": "...", "actor": "..."}]
    """
    lines = ["@startuml", "left to right direction"]
    for actor in actors:
        lines.append(f'actor "{actor}"')
    lines.append("rectangle System {")
    for uc in use_cases:
        lines.append(f'  usecase "{uc["name"]}" as {uc["id"]}')
    lines.append("}")
    for uc in use_cases:
        lines.append(f'  "{uc["actor"]}" --> {uc["id"]}')
    lines.append("@enduml")
    return "\n".join(lines)

diagram = specs_to_plantuml(
    actors=["Freelancer", "Admin"],
    use_cases=[
        {"id": "UC001", "name": "Create Invoice", "actor": "Freelancer"},
        {"id": "UC002", "name": "Manage Users", "actor": "Admin"},
    ]
)
print(diagram)
```

## Best practices
- Write use case names as verb-noun pairs ("Create Invoice", "Reset Password") — noun-only names ("Invoice") are ambiguous
- Limit each use case to one session-level goal; if a use case requires two separate login sessions to complete, split it
- Number use cases with stable IDs (UC-001) from the start — references break if you renumber
- Map every use case to at least one test scenario before marking it reviewed; use cases without test coverage are unverifiable
- Preconditions that are always true system-wide (e.g., "server is running") are not meaningful preconditions — only document preconditions that can plausibly fail
- Keep the specification at user goal level, not implementation level; "Actor clicks the blue button" is a UI detail, not a use case step

## AI-agent gotchas
- Agents will generate use cases at inconsistent levels of abstraction — mix of summary-level and subfunction-level in the same output; require explicit level specification
- Alternative flows generated by agents are often obvious but incomplete: agents default to "validation fails → show error" and miss business rule violations (e.g., "invoice amount exceeds credit limit")
- Agents frequently omit postconditions; require them explicitly in the prompt
- Use case diagrams generated as PlantUML by agents often have syntax errors in relationship notation; always render and validate before publishing
- Human checkpoint required before use cases are handed to engineering — agents produce plausible-looking specs that may encode wrong business rules

## References
- Alistair Cockburn: *Writing Effective Use Cases* (Addison-Wesley)
- Nielsen Norman Group: Use Cases vs. User Stories — https://www.nngroup.com/articles/user-stories-vs-use-cases/
- PlantUML Use Case Diagrams: https://plantuml.com/use-case-diagram
- Mermaid Diagrams: https://mermaid.js.org
- IEEE 830: Software Requirements Specification standard
