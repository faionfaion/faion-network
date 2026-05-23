# Agent Integration — C4 Model

## When to use
- New system kickoff: agent generates Level 1 (System Context) + Level 2 (Container) diagrams from a one-page spec to align stakeholders before code lands.
- Documentation-as-code in any repo with `docs/architecture/` — Structurizr DSL or PlantUML files versioned alongside code, regenerated on commit.
- Onboarding: replace "ask the senior dev" with auto-generated Container + Component diagrams.
- Architecture review meetings — feed the existing DSL to an agent and request "what changed in the last 90 days" diff.
- Migration / strangler-fig planning: dual-state (current vs. target) Container diagrams.
- ADRs (`architecture-decision-records/`) — embed Structurizr or Mermaid C4 snippets directly into the decision context.
- Compliance auditors asking for an "architecture overview" — Level 1 + Level 2 + Deployment diagrams cover most requests.

## When NOT to use
- Single-script tools, throwaway PoCs — overhead exceeds value.
- Highly-dynamic systems (event-driven choreographies with hundreds of consumers) — C4's static-structure focus understates runtime complexity. Use Dynamic + Sequence diagrams (or AsyncAPI), not just Containers.
- Enterprise integration / portfolio mapping — Level 0 (System Landscape) is shallow vs. ArchiMate / TOGAF.
- Code-level documentation — Level 4 (Code) is universally agreed to be skipped; auto-generate from IDE if anything.
- Pure infra/network diagrams — use deployment view *plus* a real network diagram tool (e.g., Lucidchart with provider stencils).

## Where it fails / limitations
- **Diagram drift:** without CI generation, the DSL goes stale within weeks. README.md mentions CI but most teams don't wire it.
- **Container vs Component confusion:** teams treat "container" as Docker container; methodology says "separately deployable unit" which can be a function, a JVM, a browser tab. Constant misunderstanding.
- **Mermaid C4 is experimental:** GitHub-native rendering looks great until syntax silently fails; pin Structurizr DSL or PlantUML for anything important.
- **Layer skipping:** agents jump to Component diagrams without Context/Container, producing implementation drawings nobody reads.
- **Notation creep:** colors, shapes, decorators inflate over time and break the "5–10 elements per diagram" guideline.
- **No runtime semantics:** C4 says nothing about consistency model, retries, idempotency — these have to live in ADRs / Dynamic diagrams.
- **Multi-tenant / scale dimension absent:** a single Container on the diagram can mean "1 instance" or "auto-scaled to 200" — important detail not represented.

## Agentic workflow
Drive C4 as docs-as-code: (1) **scaffolder agent** creates `docs/architecture/workspace.dsl` (Structurizr) seeded from the spec — Level 1 + Level 2 first; (2) **diff agent** runs on every PR, regenerates SVG/PNG via Structurizr CLI, posts visual diff as PR comment; (3) **detail agent** generates Level 3 (Component) for any container the PR touches, on demand; (4) **deployment agent** reads Terraform / Helm / Compose to produce the Deployment view; (5) **reviewer agent** flags violations of the "5–10 elements / one level per diagram / always label tech" guidelines. Persist DSL in repo, render to `docs/architecture/diagrams/`. Pair with `architecture-decision-records/` so each ADR can embed a Mermaid C4 snippet inline.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts diagram-driven design tasks (e.g., "introduce a new container `notifications-svc`") into SDD `todo/` items.
- A **Structurizr-DSL agent** (purpose-built, worth creating): single job is to read/write `workspace.dsl`; trained with C4-PlantUML and Structurizr DSL grammars to avoid syntax hallucinations.
- A **deployment-view agent**: reads Terraform plan + K8s manifests + docker-compose and emits the Deployment view automatically — keeps it in sync without human typing.
- A **diagram-linter agent**: enforces methodology rules (≤10 elements, technology labels present, descriptions on relations).

### Prompt pattern
Bootstrap:
```
You are an architect writing Structurizr DSL. From the system summary
in <spec.md>, produce a `workspace.dsl` containing only:
1. Level 1 (System Context): the system, all personas, and external systems.
2. Level 2 (Container): one container per separately-deployable unit.
Add `technology` and `description` to every element and relationship.
Keep ≤10 elements per view. Use `tags` for styling, no inline colors.
Output only valid Structurizr DSL.
```

Diff:
```
Old DSL: <paste old workspace.dsl>
New DSL: <paste new workspace.dsl>
Summarize architectural changes in 5 bullets max: containers added,
removed, retechnified; relationships added/removed; cross-cutting
impacts. Then state the ADRs that should be written or updated.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `structurizr-cli` | Render workspace.dsl → PNG/SVG/Mermaid/PlantUML, headless | https://github.com/structurizr/cli |
| `plantuml.jar` + C4-PlantUML | Render PlantUML C4 diagrams in CI | https://github.com/plantuml-stdlib/C4-PlantUML |
| `mermaid-cli` (`mmdc`) | Render Mermaid C4 to SVG/PNG | `npm i -g @mermaid-js/mermaid-cli` |
| `likec4` | Modern alternative DSL with TS-based authoring + Vite preview | https://likec4.dev |
| `goadesign/model` | C4 model in Go DSL — for Go shops | https://github.com/goadesign/model |
| `arch-as-code` | OSS suite around Structurizr | https://github.com/trilogy-group/arch-as-code |
| `gh-actions/structurizr-render` | Pre-built GitHub Action to render on PR | search GitHub Marketplace |
| `pandoc` | Combine README + diagrams into single PDF for stakeholders | `apt install pandoc` |
| `claude` (Anthropic CLI) | Run scaffolder + diff passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Structurizr Cloud | SaaS | API yes | Authoritative SaaS by Simon Brown; supports DSL upload via API. |
| Structurizr On-Premises (Lite) | self-host | yes | Free; agents push DSL via REST API. |
| IcePanel | SaaS collaborative C4 | API yes | Best UX for non-technical stakeholders; export-only API for read-back. |
| LikeC4 | OSS / SaaS preview | yes | TypeScript-first DSL + interactive site; agents diff-friendly. |
| draw.io / diagrams.net | SaaS / OSS | partial | Visual editor with C4 stencils; not text-versionable — avoid for docs-as-code. |
| Backstage TechDocs | OSS dev portal | yes | Surfaces C4 diagrams alongside service catalog; agent-callable via Backstage API. |
| GitHub / GitLab Pages | hosting | yes | Render and host generated SVG/HTML diagrams from CI. |
| Lucidchart | SaaS | partial | OK for one-off; not docs-as-code; expensive for solo. |
| ArchiMate via Archi | OSS modeling | partial | Heavier enterprise modeling; rarely needed alongside C4. |
| OpenAPI + AsyncAPI catalogs | OSS | yes | Complement C4 with explicit interface contracts; agents can cross-link. |

## Templates & scripts

`templates.md` ships Structurizr DSL, PlantUML, and Mermaid C4 templates. The gap is a CI hook that renders + diffs on every PR. Inline drop-in (≤50 lines):

```yaml
# .github/workflows/c4-render.yml — render Structurizr DSL on PR + post diff.
name: c4-render
on:
  pull_request:
    paths: ['docs/architecture/**']
permissions:
  contents: read
  pull-requests: write
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Render Structurizr DSL
        uses: docker://structurizr/cli:latest
        with:
          args: export -workspace docs/architecture/workspace.dsl -format mermaid -output docs/architecture/out
      - name: Render also as PlantUML+SVG
        run: |
          docker run --rm -v "$PWD":/usr/local/structurizr structurizr/cli \
            export -workspace docs/architecture/workspace.dsl -format plantuml -output docs/architecture/out
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: c4-diagrams
          path: docs/architecture/out/
      - name: Comment with diagram links
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          message: |
            **C4 diagrams updated.** Mermaid + PlantUML rendered for this PR.
            Download from the workflow artifacts.
```
The diff agent reads the artifact pair (old/new SVG hashes) and writes a human-readable change summary.

## Best practices
- Pick **one** notation per repo — Structurizr DSL is the safest default for non-trivial systems; Mermaid C4 only for inline ADR snippets.
- Always start with Level 1; never let an agent jump to Level 3 without Level 2 already merged.
- Label every relationship with technology + intent ("HTTPS / JSON, places order"). Unlabeled arrows are noise.
- Cap diagrams at 5–10 elements; if you exceed, split — methodology is correct, agents need the explicit constraint.
- Render diagrams in CI (Structurizr CLI in Docker) — never let humans hand-export PNG.
- Treat the DSL as code: linted, code-reviewed, semantic-versioned alongside the system.
- Pair every ADR with the C4 view it touches; embed a Mermaid C4 snippet in the ADR header for context.
- Pin Mermaid C4 syntax version — it is still experimental and evolves.

## AI-agent gotchas
- LLMs hallucinate Structurizr DSL keywords (e.g., invent `protocol "GraphQL"` syntax). Validate every generated DSL with `structurizr-cli validate` before merging.
- Agents over-decompose into microservices on Container view because of training-data bias. Force the prompt to include team size + monolith default.
- Agents skip technology labels constantly. Add a lint rule: every element/relationship without a non-empty `technology` is rejected.
- Mixing levels in one diagram is a frequent agent error — explicitly say "Only Level 2 elements; do not draw classes/components."
- Long DSLs blow context. Split workspaces by bounded context and let the agent edit one file at a time.
- Diagram diffs as text are noisy; pair with rendered SVG hashes so reviewers see real visual changes.
- Human-in-loop checkpoints: (1) initial Level 1 sign-off, (2) any new container, (3) deployment-view changes that move data across regions/clouds — these decisions usually require ADRs too.

## References
- C4 Model official site (Simon Brown) — https://c4model.com/
- Structurizr DSL docs — https://docs.structurizr.com/dsl
- Structurizr CLI — https://github.com/structurizr/cli
- C4-PlantUML — https://github.com/plantuml-stdlib/C4-PlantUML
- Mermaid C4 syntax — https://mermaid.js.org/syntax/c4.html
- IcePanel C4 e-book — https://icepanel.io/blog/2025-11-26-ebook-communicating-architecture-with-the-c4-model
- LikeC4 — https://likec4.dev
- The C4 Model book (O'Reilly, 2026) — https://www.oreilly.com/library/view/the-c4-model/9798341660113/
- Local methodology: `c4-model/README.md`, `templates.md`, `examples.md`, `checklist.md`
