# Agent Integration — Behavioral Design Patterns

## When to use
- Code review where conditional/switch chains, duplicated event-listener wiring, or growing if/else state machines indicate a missing pattern.
- New feature design where multiple algorithms need to be selected at runtime (Strategy), domain events fan-out (Observer/pub-sub), or workflows have explicit states (State).
- Refactoring a monolithic class into smaller, testable pieces by externalizing the variable behavior (Strategy, Template Method, Visitor).
- Building extensible middleware/handler chains (Chain of Responsibility) — request validation, auth pipelines, log enrichers.
- LLM-driven code generation that needs a vocabulary of named patterns to constrain output and keep code idiomatic.

## When NOT to use
- Two-line if/else with one likely future variant — pattern overhead outweighs benefit; revisit when third variant arrives.
- Pure data-transformation pipelines that map cleanly to functions or streams — patterns add ceremony.
- Languages with first-class FP idioms (Rust, Haskell, modern TS) — many GoF behavioral patterns reduce to higher-order functions.

## Where it fails / limitations
- Pattern-zealotry produces over-abstracted code; LLMs are especially prone to inserting Strategy interfaces with one implementation.
- Visitor patterns add friction when adding new entity types; only worth it when adding new operations is the dominant axis.
- Observer-heavy code becomes hard to debug ("who fired this?"); pair with a canonical event log.
- State pattern objects can leak business invariants across files; consider a state-machine library (XState, statecharts) for non-trivial flows.
- Mediator collapses into a god-object if every component routes through it.

## Agentic workflow
Run a recognizer agent that scans diffs/files for code-smell signatures (long switch on type, repeated subscribe boilerplate, growing if-state chains), proposes the matching pattern, and outputs a concrete refactor diff. A separate critic agent challenges the proposal: is the abstraction load-bearing, or are we adding a one-impl interface? Use `templates.md` to constrain the agent's idioms per language. Always keep a behavioral-patterns ADR for non-obvious choices (e.g., why Observer was chosen over a message bus).

### Recommended subagents
- `faion-brainstorm` — diverge over candidate patterns when more than one fits.
- `faion-sdd-execution` — small refactor task with tests proving behavior preservation.
- `faion-improver` — periodic sweep for over-abstraction (one-impl interfaces, dead Strategy slots).

### Prompt pattern
```
INPUT: <file>.ts and a brief on the change driver (new payment provider, new event consumer).
TASK: Identify the smallest pattern that fits (Strategy, Observer, State, CoR, Template).
Justify against the change driver. Reject patterns that introduce more than one
new file unless they remove an existing if/else by at least 30% LOC.
OUTPUT: refactor diff + tests + 3-line ADR rationale.
```

```
ROLE: pattern-critic
TASK: Argue against the proposed pattern. Suggest a simpler alternative
(plain function, lookup table, library state machine). Score 1-5 for
extensibility, debuggability, learning curve, lines added, lines removed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ruff / pylint | Detect long branches, complexity (Python) | `pip install ruff` |
| eslint + plugin-sonarjs | Cyclomatic complexity, switch length (TS/JS) | npm |
| golangci-lint | gocyclo, cyclop (Go) | https://golangci-lint.run/ |
| jscpd | Duplicate-code detection — pre-pattern signal | `npm i -g jscpd` |
| Lizard | Cross-language complexity scanner | `pip install lizard` |
| Semgrep | Custom rules for "switch on type" / pattern smells | https://semgrep.dev/ |
| ast-grep | Structural search across languages for refactor sites | https://ast-grep.github.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sourcegraph / Cody | SaaS | Yes | Find all callers of a Strategy, batch-refactor consumers |
| GitHub Copilot Workspace / Claude Code | SaaS | Yes | Diff-driven refactors that follow pattern templates |
| XState (Stately) | OSS+SaaS | Yes | Use instead of hand-rolled State pattern for non-trivial FSMs |
| RxJS / RxPy | OSS | Yes | Modern alternative to hand-rolled Observer |
| Apache Camel / Spring Integration | OSS | Partial | Heavy CoR/mediator runtimes for JVM apps |
| EventEmitter (Node) / Pyee (Python) | OSS | Yes | Built-in Observer; agent-friendly idioms |

## Templates & scripts
See `templates.md` for Strategy, Observer, Command, State, CoR, Template, Mediator, Iterator, Visitor implementations in Python, TypeScript, Go. Inline complexity scanner that flags pattern-candidate files:

```bash
#!/usr/bin/env bash
# pattern-candidates.sh — list files most likely to need a behavioral pattern.
set -euo pipefail
DIR="${1:-src}"
# Python/TS/Go: cyclomatic complexity > 15 + at least one switch/match on type
lizard -C 15 -L 200 "$DIR" -X --csv 2>/dev/null \
  | awk -F, 'NR>1 && $2>15 {print $5}' \
  | sort -u \
  | while read -r f; do
      if grep -E 'switch \(|match.*:|isinstance\(' "$f" >/dev/null 2>&1; then
        echo "$f"
      fi
    done
```

## Best practices
- Trigger pattern application off measured smells (complexity, duplication, change frequency), not aesthetics.
- Start with the simplest representation: function pointer, dict-of-functions, lookup table. Promote to a class-based pattern only when type signatures or shared state demand it.
- Pair Observer with a structured event taxonomy (event names, payloads, version) — undisciplined Observer becomes an undebuggable spaghetti.
- Use library state machines (XState, statecharts4j) for >3 states or guards/actions; hand-rolled State is only justified for tiny, stable flows.
- For Strategy, keep the interface narrow — one method most of the time; multi-method strategies usually want to be a Service.
- Always add tests that exercise pattern boundaries (new strategy, new state transition, new handler in chain) — regressions hide there.

## AI-agent gotchas
- Agents reflexively apply Strategy with one implementation "for future flexibility"; force a 2nd-impl-or-no-pattern rule.
- Observer patterns generated by LLMs often forget to unsubscribe — memory leaks in long-lived processes. Require an explicit `dispose`/`close` in the template.
- Visitor implementations frequently mismatch the entity hierarchy after edits; demand exhaustiveness checks (TS `never`, Python `assert_never`).
- Command pattern code from LLMs lacks idempotency keys when used for retried operations; require a key in the prompt for any networked command.
- Human-in-loop gates: code review for any new abstraction; require a "would a function suffice?" comment before merging.

## References
- "Design Patterns: Elements of Reusable Object-Oriented Software" — GoF
- https://refactoring.guru/design-patterns/behavioral-patterns
- https://martinfowler.com/eaaCatalog/
- https://stately.ai/docs/state-machines-and-statecharts
- https://www.rxjs.dev/
- https://github.com/kamranahmedse/design-patterns-for-humans
