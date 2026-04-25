# Agent Integration — Design Patterns Overview

## When to use
- Agent needs to pick a category before drilling into specific pattern files (Creational / Structural / Behavioral / Distributed / Architectural).
- Reviewing code or design for pattern misuse — agent uses this overview as the index, then jumps into the specific pattern doc.
- Onboarding new code generation: agent reads this first to understand the project's pattern vocabulary, then applies the right specific pattern.
- Mapping classic patterns to modern language features (e.g., Iterator → generator, Strategy → first-class function) so agent doesn't over-engineer.
- Cross-referencing patterns when the right answer combines several (Decorator + Strategy, Repository + Unit of Work, Outbox + Saga).

## When NOT to use
- Specific pattern implementation — go directly to `creational-patterns/`, `behavioral-patterns/`, `structural-patterns/`, or `distributed-patterns/`.
- One-off scripts where pattern overhead exceeds value.
- Pure architecture (style) decisions (monolith vs microservices vs serverless) — those live in their own methodologies.
- Cloud-native / distributed-only design — `distributed-patterns/` is the better entry.

## Where it fails / limitations
- This is a navigation document. It's a poor source for implementation; agents that anchor on it without descending produce shallow code.
- "Modern alternatives" table can mislead: not every Strategy should become a lambda; sometimes the class form documents intent better.
- Pattern bingo: agents see this catalog and want to apply 5 patterns to a 50-line problem. Counter with "what's the simplest thing that works?".
- Tech-giant examples (Netflix uses Proxy, Amazon uses Strategy) are illustrative, not prescriptive — agents over-extrapolate.
- Cloud-native patterns (Service Mesh, Sidecar, Ambassador) are infra patterns; conflating them with code patterns confuses the design conversation.

## Agentic workflow
Use this overview as a router: agent reads README, identifies the category, then opens the specific pattern's `agent-integration.md` and `templates.md`. Default model is sonnet for category selection; haiku for descending into a specific pattern's implementation; opus only when combining patterns across categories (e.g., CQRS + Event Sourcing + Outbox). Always pair with `architectural-patterns` when the question is "where does this pattern live in our layered architecture?".

### Recommended subagents
- `faion-sdd-executor-agent` — primary executor; reads this overview, then applies a specific pattern via its sibling methodology.
- `faion-brainstorm` — for "which pattern fits?" diverge/converge over 3+ candidates.
- `faion-improver` — captures pattern-misuse mistakes back into `.aidocs/memory/mistakes.md`.

### Prompt pattern
```
Pick a design pattern category for this problem: <description>.
Constraints: <language, framework, perf, testability>.
Use the patterns-overview README as the map. Output:
1) Category (Creational/Structural/Behavioral/Distributed/Architectural),
2) Top 2 candidate patterns with one-sentence rationale each,
3) Modern language alternative if it would be simpler,
4) Pointer to the specific methodology folder to drill into next.
```

```
Audit this module for pattern misuse using patterns-overview as the lens.
Report: applied patterns (with confidence), missing patterns that would help, and
"pattern bingo" (over-engineered) cases. Each finding ≤ 2 lines.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` / `eslint` / `golangci-lint` | Surface pattern-implementation smells (unused params, overlong constructors) | per language |
| `radon` / `lizard` | Cyclomatic complexity (high CC often signals missing pattern) | `pip install radon lizard` |
| `dependency-cruiser` | TS/JS module-relation rules (catches Decorator/Adapter overuse) | `npm i -D dependency-cruiser` |
| `import-linter` | Python import boundaries (Repository pattern enforcement) | `pip install import-linter` |
| `archunit` | Java pattern compliance tests | https://www.archunit.org/ |
| `mermaid-cli` | Render pattern collaboration diagrams for ADRs | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Refactoring.Guru | Web | Yes | Canonical reference; agent can cite directly. |
| Patterns.dev | Web | Yes | Modern JS/React patterns; useful for FE refactor prompts. |
| SourceMaking | Web | Yes | Pattern catalog with examples. |
| Microsoft Cloud Design Patterns | Web | Yes | Cloud-native pattern reference. |
| Enterprise Integration Patterns (Hohpe) | Web | Yes | Messaging patterns canonical reference. |

## Templates & scripts
This is an overview/navigation doc. See sibling methodology folders for templates:
- `creational-patterns/templates.md`
- `structural-patterns/templates.md`
- `behavioral-patterns/templates.md`
- `distributed-patterns/templates.md`
- `architectural-patterns/templates.md`

Inline pattern-fit decision tree (paste into ADR or design doc):

```text
Problem: object creation varies?       → creational-patterns/
Problem: composition / interface fit?  → structural-patterns/
Problem: behavior / responsibility?    → behavioral-patterns/
Problem: distributed coordination?     → distributed-patterns/
Problem: app-wide structure?           → architectural-patterns/
None of the above: pattern is overkill — write the simplest code that passes tests.
```

## Best practices
- Pick a category first, pattern second. Most arguments about "Strategy vs Command" go away when the category is clear.
- Always state the alternative — "we picked Decorator over inheritance because…". Without the alternative the choice is ceremony.
- Modern language features replace many GoF patterns; don't use a pattern when a function, generator, or DI container already provides it.
- A pattern is justified by ≥2 reasons: testability, extension, multi-implementation, removal of duplication. One reason is usually not enough.
- Document patterns at the top of the file/module (one-line comment), not in a separate Wiki — keeps future agents from reinventing.
- Prefer composition of small patterns over deep hierarchies; agent code with 4 inheritance levels is a smell.

## AI-agent gotchas
- "Pattern bingo": agent suggests Factory + Builder + Singleton + Adapter for a 30-line class. Demand a single pattern unless multi-pattern is justified.
- Mislabeling: agents call any class with a `create_*` method a "Factory"; verify it actually decouples creation from use.
- Naming: agent renames classes to `*Factory`, `*Manager`, `*Service` without changing structure — surface the actual relationship in the diagram, not the suffix.
- "Modern alternative" trap: agent eliminates a pattern by inlining a lambda, losing the documented intent. Push back when the pattern was load-bearing.
- Cloud-native patterns conflated with code patterns: agent suggests "use Sidecar for this database call" — that's not what Sidecar is.
- Anti-patterns missed: God Object, Anemic Domain Model, Service Locator (often called "DI" wrongly). Always ask agent for anti-patterns before patterns.

## References
- Gamma, Helm, Johnson, Vlissides (1994). "Design Patterns: Elements of Reusable Object-Oriented Software."
- Fowler, M. "Patterns of Enterprise Application Architecture" (2002).
- Hohpe & Woolf. "Enterprise Integration Patterns" (2003).
- Newman, S. "Building Microservices" (2nd ed., 2021).
- Refactoring.Guru — https://refactoring.guru/design-patterns
- Patterns.dev — https://www.patterns.dev/
- Microsoft Azure Architecture Center patterns — https://learn.microsoft.com/en-us/azure/architecture/patterns/
- Enterprise Integration Patterns site — https://www.enterpriseintegrationpatterns.com/
