# Agent Integration — Trade-off Analysis

## When to use
- Comparing 2-N architecture/tech options where the chosen one is hard to reverse (database, cloud provider, primary language, auth provider).
- Generating ATAM-style utility trees and scenarios from a constitution.md or design.md before a major SDD feature.
- Producing decision matrices with weighted criteria for build-vs-buy, monolith-vs-microservices, sync-vs-async, and similar pairwise picks.
- Writing the "Consequences" section of an ADR — the explicit gain/loss list.
- Stakeholder communication: re-rendering the same decision for executives, product, engineering, ops audiences.

## When NOT to use
- Type-2 reversible decisions (which logging library, which CSS framework) — analysis paralysis costs more than the wrong choice.
- When there is no real choice — only one option meets a hard constraint. Skip the matrix; document the constraint.
- When stakeholders haven't been identified yet — agents will invent generic personas and the output looks plausible but binds nobody.
- Pure cost questions answered by a spreadsheet (TCO over 3 years with known unit prices).

## Where it fails / limitations
- LLMs invent crisp criteria weights that look authoritative but reflect generic priors, not your business context. Weights must come from humans.
- Agents converge on "balanced" middle options; without forcing extremes the matrix becomes useless.
- ATAM relies on stakeholder workshops; an agent cannot run one — it can only seed scenarios.
- Hidden trade-offs (org politics, vendor lock-in past 3 years, hiring market) rarely surface unless asked explicitly.
- Sensitivity vs trade-off point distinction is lost on most LLMs; they label everything a trade-off.

## Agentic workflow
Use sonnet for the bulk of comparison work, opus only on irreversible Type-1 decisions where novel framing matters. Run a two-pass: pass 1 (`diverge`) generates a wide option set with raw criteria; pass 2 (`converge`) ranks with weights from the human, then a separate reviewer subagent challenges each row asking "what would make this worse than it looks". Output goes into an ADR plus a stakeholder-rendered summary table.

### Recommended subagents
- `faion-brainstorm` skill — diverge/converge/review cycles map directly onto trade-off analysis (option generation → matrix → red-team).
- `faion-sdd-executor-agent` — owns the resulting ADR file inside the SDD lifecycle (`backlog/ → todo/ → in-progress/`).
- `faion-improver` — surfaces lessons from past trade-off decisions stored in `.aidocs/memory/decisions.md`.

### Prompt pattern
```
Decision: <one-line statement>. Reversibility: Type 1.
Options: [A, B, C]. Criteria: [perf, cost, team-skill, lock-in, reversibility].
For each criterion, give weight (1-5) and per-option score (1-5) with one-sentence rationale.
Then list the top-3 trade-offs we accept by picking <ranked top option>, and the top-3 risks
we still carry. End with one paragraph for executives, no jargon.
```

```
Red-team this decision matrix. For each row, name a scenario in the next 24 months that
would invert the score. Flag any criterion the matrix is silent on.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `adr-tools` | Bash CLI to scaffold ADRs (`adr new "Pick database"`) | https://github.com/npryce/adr-tools |
| `log4brains` | ADR static site generator with diff/history | `npm i -g log4brains` |
| `dasel` / `yq` | Edit YAML/JSON criteria matrices in scripted agent loops | `brew install dasel` |
| `pandoc` | Render ADR+matrix to PDF for stakeholder distribution | `apt install pandoc` |
| `mermaid-cli` | Render utility trees and decision trees to SVG | `npm i -g @mermaid-js/mermaid-cli` |
| `gh` | Open PR with ADR draft, request review from quality attribute owners | https://cli.github.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Structurizr | SaaS/OSS | Yes | DSL-driven; agent can author decision records alongside C4 model. |
| Confluence | SaaS | Partial | API exists but rich-text fidelity poor; prefer Markdown then convert. |
| Notion | SaaS | Yes | Good for stakeholder-facing matrix; API supports tables. |
| Linear | SaaS | Yes | Decision items tracked as issues; ADR linked in description. |
| Backstage TechDocs | OSS | Yes | Markdown ADRs render natively; pairs with adr-tools. |
| Lucidchart | SaaS | Limited | Diagram authoring; not API-first for matrices. |

## Templates & scripts
See `templates.md` for ATAM utility tree, decision matrix, ADR formats. Inline weighted-score helper:

```python
#!/usr/bin/env python3
# score-matrix.py — read a YAML matrix, print ranked options.
import sys, yaml
m = yaml.safe_load(open(sys.argv[1]))  # {options: {A: {crit: score}}, weights: {crit: w}}
ranked = sorted(
    ((opt, sum(scores[c] * m["weights"][c] for c in m["weights"])) for opt, scores in m["options"].items()),
    key=lambda kv: -kv[1],
)
width = max(len(o) for o, _ in ranked)
for opt, total in ranked:
    print(f"{opt:<{width}}  {total:6.2f}")
```

## Best practices
- Force the agent to declare reversibility (Type 1 vs Type 2) up front; analysis depth follows.
- Use 1-5 (not 1-10) scoring scales — humans can't reliably distinguish 7 from 8, and LLMs bias high.
- Demand one concrete failure scenario per "winning" option; absent that, the analysis is theatre.
- Capture the criteria you considered and rejected — future readers learn as much from those.
- Tag every ADR with the quality attributes it touches so the architect skill can cross-reference.
- Run the same matrix for the runner-up option as a sanity check; if they tie within 5%, the criteria are too coarse.

## AI-agent gotchas
- "What do we lose?" is the magic question — without it agents only enumerate gains.
- LLMs treat "cost" as a single criterion; split into capex, opex, opportunity, switching cost.
- Avoid letting one agent both generate options and score them — it scores its own ideas higher (selection bias).
- Cargo-culting: if the agent cites "FAANG uses X", reject and ask for trade-offs in your context (team size, budget, regulatory).
- For ATAM scenarios, agents skip the "response measure" (must be quantitative) — always demand a number with unit.
- When stakeholder-rendering, agents drop nuance for executives; verify the executive summary preserves the key risk.

## References
- Kazman, Klein, Clements (2000). "ATAM: Method for Architecture Evaluation," SEI/CMU. https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
- Hassouna et al. (2025). "ATRAF: Architecture Tradeoff and Risk Analysis Framework."
- Fowler, M. (2009). "TechnicalDebtQuadrant." https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- Joel Parker Henderson — ADR templates. https://github.com/joelparkerhenderson/architecture-decision-record
- Michael Nygard — "Documenting Architecture Decisions." https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ISO/IEC 25010 quality model. https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
