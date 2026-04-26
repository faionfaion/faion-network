# Agent Integration — Structural Design Patterns

## When to use
- Wrapping a third-party / legacy API to fit the codebase's interface (Adapter) — the most common applied case.
- Building HTTP/gRPC middleware chains, log/cache/auth wrappers (Decorator) — when subclassing would explode.
- Hiding a complex subsystem (multi-step workflow, multi-call SDK, multi-service orchestration) behind one entry point (Facade).
- Lazy initialization, access control, smart references (Proxy) — DB connections, image loaders, remote object stubs.
- Tree-shaped domains: file system, UI components, org chart, document AST (Composite).
- Up-front design with multiple variation axes (rendering backend × OS, storage backend × format) (Bridge).
- Memory-bound systems with millions of similar objects (Flyweight) — game entities, terminal grids, map tiles.

## When NOT to use
- One-off adapter for a single call site — write a 5-line function, not a class hierarchy.
- New code where you can change the underlying interface — fix the source instead of layering Adapters.
- Performance-critical hot paths — Decorator/Proxy chains add allocations and indirection (especially in interpreted languages).
- Trivial systems — Facade on top of two functions is over-engineering.
- Domains without recursive structure — Composite is the wrong tool.
- Languages with native decorator/aspect support (Python `@`, TypeScript decorators) — most teams confuse the language feature with the GoF pattern; usually you want the language feature, not the pattern.
- When DI / functional composition solves the problem — first reach for higher-order functions, not class-based wrappers.

## Where it fails / limitations
- **Wrapping pattern collisions:** Adapter / Proxy / Decorator / Bridge all "wrap" — agents (and humans) pick the wrong one and create misnamed code that misleads reviewers.
- **Decorator chains hide ordering bugs:** `auth(cache(log(handler)))` vs `cache(auth(log(handler)))` produce different security postures; pattern names rarely surface this.
- **Composite ⇒ over-uniformity:** treating leaves and composites uniformly often violates Liskov when an operation only makes sense for one kind.
- **Flyweight + mutable state = race conditions:** shared intrinsic state must truly be immutable; concurrency bugs are easy.
- **Bridge requires foresight:** retrofitting Bridge into a tightly coupled abstraction usually means a rewrite.
- **Facade as Garbage Bin:** "FacadeService" that grew into 4k lines of unrelated methods is a top code-smell.
- **Pattern theater:** naming files `*Adapter.py`, `*Decorator.py`, `*Facade.py` doesn't mean the pattern was needed.

## Agentic workflow
Drive structural patterns as a four-pass code-review loop: (1) **smell detector agent** scans diffs for "import incompatibility" / "growing wrapper class" / "long subclass chain" and proposes which structural pattern (if any) fits; (2) **pattern picker** uses the methodology decision tree to pick exactly one pattern, with a 1-line justification (timing/purpose); (3) **implementer agent** generates the refactor as a *separate PR* using `templates.md`; (4) **reviewer agent** checks pitfalls (mutable Flyweight intrinsic, Decorator ordering, Composite over-uniformity). Human approves. Patterns rarely need a green-field application — they earn their keep at refactor time.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts pattern-refactor proposals into SDD `todo/` tasks with explicit acceptance criteria (e.g., "old API removed within 2 sprints").
- A **pattern-picker agent** (purpose-built, worth creating): given a code smell description, returns one of {Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight, none} with a justification and a link to `templates.md`.
- A **decorator-order linter** (purpose-built): for HTTP/gRPC frameworks, validates that auth → rate-limit → tracing → log ordering is correct and stable across services.
- A **wrapper-bloat detector**: flags classes whose only methods delegate verbatim to a wrapped instance (often a sign of unnecessary Adapter or Proxy).

### Prompt pattern
Pattern selection:
```
Code under review: <paste class/function>.
Problem: <one sentence — incompatible interface? complex subsystem?
need access control? add behavior?>.
Using the Pattern Selection Matrix in
solo/dev/software-architect/structural-patterns/README.md, pick exactly
one structural pattern OR answer "no pattern needed". Give 1-line
justification quoting the matrix. Then, if applicable, point to
the matching template in templates.md.
```

Decorator-order check:
```
Given the middleware stack <list of decorators in order>, verify:
1. Auth runs before any side effect (cache, logging, rate-limit).
2. Tracing wraps everything below it.
3. Idempotency / retry sits inside auth, outside business logic.
Output: ordered list with any swap recommendations and a 1-line reason.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` (rule `B019`, `SIM`, `PIE`) | Catch over-wrapping / dead decorators in Python | `pip install ruff` |
| `eslint` + `eslint-plugin-fp` | Discourage class-based wrappers when functions suffice in JS/TS | `npm i -D eslint eslint-plugin-fp` |
| `pyreverse` (pylint) | Generate UML to verify Composite/Bridge structure | included with `pylint` |
| `staticcheck` | Catch unused interface implementations / dead Adapter methods in Go | https://staticcheck.dev |
| `eslint-plugin-import` | Detect circular imports in Decorator chains | `npm i -D eslint-plugin-import` |
| `radon` (Python complexity) | Detect Facade-bloat (cyclomatic complexity per file) | `pip install radon` |
| `dependency-cruiser` | Confirm Bridge separation of abstraction vs implementor | `npm i -g dependency-cruiser` |
| `mypy` / `tsc --noImplicitAny` | Catch Liskov/interface mismatches in Composite/Adapter | https://mypy.readthedocs.io / https://www.typescriptlang.org |
| `claude` (Anthropic CLI) | Run smell-detector + reviewer passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud / SonarQube | SaaS / OSS code quality | API yes | Surfaces "God class" / "Long parameter list" smells that often hint at Facade or Adapter need. |
| CodeClimate / Codacy | SaaS code quality | API yes | Same niche; agents can subscribe to webhooks. |
| GitHub Copilot for PRs | SaaS | yes | Often suggests pattern names — verify with the pattern-picker agent before accepting. |
| Refactoring.guru | docs (free + paid) | n/a | Pattern reference; great few-shot source for agents. |
| jOOQ / Hibernate / Spring AOP | OSS frameworks | yes | Real-world Decorator/Proxy implementations agents can cite. |
| Express.js / Koa / Fastify | OSS | yes | Decorator-style middleware — canonical chain for agents to learn ordering. |
| Envoy / Istio filters | OSS | yes | Network-level Decorator chain; agents propose middleware order via WASM filters. |
| Apollo Server plugins | OSS | yes | GraphQL Decorator chain. |
| Backstage Software Catalog | OSS | yes | Tracks Facade ownership of compound services. |

## Templates & scripts

`templates.md` already ships copy-paste templates for each pattern in Python, TypeScript, and Go. The gap is a quick command-line classifier that suggests a pattern from a free-text description. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# pickpattern.py — naive structural-pattern picker via keyword scoring.
# Usage: pickpattern.py "I need to wrap a legacy SOAP client to look like our REST client"
import re, sys
TEXT = " ".join(sys.argv[1:]).lower()
RULES = [
    (r"\b(legacy|third[- ]party|incompatible|wrap an existing|sdk)\b", "Adapter"),
    (r"\b(middleware|chain|add (logging|caching|auth|metrics)|decorator)\b", "Decorator"),
    (r"\b(simplif(y|ied)|hide|complex subsystem|single entry point|orchestrat(e|ion))\b", "Facade"),
    (r"\b(lazy|access control|cache (proxy|fronting)|remote object|smart reference)\b", "Proxy"),
    (r"\b(tree|hierarchy|recursive|file system|nested|ast)\b", "Composite"),
    (r"\b(cross[- ]platform|backend|driver|two dimensions|multiple implementations)\b", "Bridge"),
    (r"\b(millions of objects|memory|tile|sprite|share state)\b", "Flyweight"),
]
scores = {n: 0 for _, n in RULES}
for pat, name in RULES:
    if re.search(pat, TEXT):
        scores[name] += 1
top = sorted(scores.items(), key=lambda kv: -kv[1])
if top[0][1] == 0:
    print("none")
else:
    print(top[0][0])
    if len(top) > 1 and top[1][1] == top[0][1]:
        print(f"# tied with {top[1][0]} — disambiguate via the matrix in README.md")
```
Use it as a sanity check before the pattern-picker agent commits to a name.

## Best practices
- Apply structural patterns at refactor time, not greenfield. The strongest signal is "I keep writing the same wrapper class for the third time."
- Adapter: keep one Adapter per *external* boundary; never adapt your own internal types — fix them instead.
- Decorator: enforce idempotency-friendly ordering (auth → idempotency → rate-limit → tracing → log → handler) and document it in code, not in slack threads.
- Facade: cap method count (~10) and keep it stateless. Beyond that you have a god service.
- Proxy: use it for cross-cutting concerns (caching, auth, lazy load) where adding it does not change call signatures.
- Composite: explicitly write down which operations are leaf-only and which are composite-only — Liskov violations at runtime are nasty.
- Flyweight: enforce immutability of intrinsic state (frozen dataclasses, `Object.freeze`, `Arc<T>`).
- Bridge: only when both axes have ≥3 known variants — otherwise YAGNI.

## AI-agent gotchas
- LLMs over-eager-name patterns ("ServiceFacade", "RepositoryAdapter") for code that's just a class. Require pattern proposals to cite the matrix row that matches.
- Agents conflate Python decorators / TypeScript decorators with the GoF Decorator pattern. Force a clarifying step when the prompt mentions "decorator".
- Agents reorder middleware decorators silently during refactors. Pin decorator order via tests, not just code review.
- Generated Composite implementations often forget Liskov — child operations throw `NotImplementedError`. Add tests that exercise both leaf and composite for every public method.
- Flyweight code generated by an LLM may share mutable dicts; review for accidental shared mutation under concurrency.
- Long sources blow context — feed agents one class at a time plus the README's matrix snippet.
- Human-in-loop checkpoints: (1) any pattern PR that crosses public-API boundaries, (2) middleware-order changes in production frameworks (auth/billing risk), (3) Bridge introductions (irreversible) — review like ADRs.

## References
- Gamma, Helm, Johnson, Vlissides — *Design Patterns* (1994), Structural chapter.
- Refactoring.guru — Structural Patterns — https://refactoring.guru/design-patterns/structural-patterns
- Christopher Okhravi YouTube — Head First Design Patterns walkthroughs — https://www.youtube.com/@ChristopherOkhravi
- Sandi Metz — *Practical Object-Oriented Design in Ruby* (POODR) — for Adapter/Composite intuition.
- Robert C. Martin — *Clean Architecture* — Adapter / Boundary chapters.
- Microsoft Patterns & Practices — Cloud Patterns — https://learn.microsoft.com/azure/architecture/patterns/
- Local methodology: `structural-patterns/README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`
