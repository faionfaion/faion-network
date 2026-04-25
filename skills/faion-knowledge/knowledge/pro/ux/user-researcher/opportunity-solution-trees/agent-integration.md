# Agent Integration — Opportunity Solution Trees (OST)

## When to use
- Continuous discovery cadence (Teresa Torres' "weekly touchpoint with customers" model) where the team needs a living artefact to connect outcomes → opportunities → solutions → experiments.
- Quarterly planning to translate one north-star outcome into a backlog of research-grounded opportunities.
- Cross-functional alignment when product, design, and engineering disagree on whether to ship Solution A or Solution B.
- Onboarding a new PM or designer to the team's discovery context.
- Refactoring a feature roadmap that has drifted into solution-first thinking.

## When NOT to use
- Pre-discovery: when the team has no customer interviews, an OST is fiction.
- Strict waterfall delivery where the backlog is fixed for the next 6+ months.
- Single-experiment hypotheses (e.g., a one-off A/B test) — overkill, use a hypothesis canvas.
- For OKR setting itself; OST starts with an outcome, it does not generate one.
- Compliance / regulatory work where the "outcome" is binary (pass/fail) — opportunities don't branch meaningfully.

## Where it fails / limitations
- Trees grow into wallpaper; without pruning they become unreadable and stale.
- Opportunity ≠ solution discipline collapses under pressure — teams paste features as opportunities ("add export button" is not an opportunity).
- Treating the tree as a Gantt chart kills its discovery purpose; it is a thinking tool, not a delivery plan.
- Without a structured interview cadence, the opportunities tier turns into a brainstorm dump.
- Cross-team trees fragment: each squad runs its own without rolling up to a portfolio outcome.

## Agentic workflow
Use agents to maintain the tree's hygiene: classify nodes (outcome / opportunity / solution / experiment), surface stale branches, cluster duplicate opportunities, and generate experiment briefs from a chosen solution. Discovery decisions stay human; the agent's role is to keep the artefact accurate, deduplicated, and linked to interview evidence. Maintain the tree as structured data (YAML or JSON) backing a Miro/FigJam render — agents can edit data, humans review the visual.

### Recommended subagents
- A purpose-built `ost-curator` subagent: ingests interview-evidence snippets, attaches them to opportunity nodes, flags opportunities with no supporting evidence after 30 days.
- `faion-brainstorm` — diverges on candidate solutions for a chosen opportunity, then converges on top 3 for human review.
- `faion-sdd-executor-agent` — converts a chosen experiment into a test plan (success metric, sample size, instrumentation).
- A `node-classifier` subagent that lints proposed nodes for category errors (solution masquerading as opportunity).

### Prompt pattern
"Given the OST YAML below and 12 new interview snippets, propose new opportunity nodes (≤ 1 sentence each, customer language, no solutions). For each, list the snippet IDs supporting it. Reject any duplicates of existing opportunities (cosine similarity ≥ 0.85)."

"Given opportunity `O.users-cant-find-export`, generate three candidate solutions ranging from low to high investment. For each, propose one experiment (assumption, method, success criterion, sample size, duration)."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Miro REST API | Render OST on shared board | https://developers.miro.com |
| FigJam REST API | Alternative render surface | https://www.figma.com/developers/api |
| Whimsical API (limited) | Lightweight tree boards | https://whimsical.com |
| Mermaid CLI | Static OST renders in repos / docs | `npm i -g @mermaid-js/mermaid-cli` |
| Graphviz `dot` | High-density tree rendering for export | `apt install graphviz` |
| `gh` CLI | Link experiments to GitHub issues | https://cli.github.com |
| Linear / Jira CLI | Sync experiments to delivery | `npm i -g @linear/sdk` / Jira REST |
| Dovetail API | Pull interview tags as evidence | https://developers.dovetail.com |
| Notion API | Source-of-truth tree if not in Miro | https://developers.notion.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Miro | SaaS | Yes (REST + webhooks) | OST template most teams use |
| FigJam | SaaS | Partial (REST API) | Strong for design teams |
| Whimsical | SaaS | Limited | Fast trees, weaker API |
| Mural | SaaS | Yes (REST API) | Enterprise board control |
| Productboard | SaaS | Yes (REST API) | Good for opportunity management at scale |
| Dovetail | SaaS | Yes (REST API) | Evidence repository to wire under nodes |
| Notion | SaaS | Yes (REST API) | Tree-as-database pattern |
| Roam Research / Logseq | SaaS / OSS | Limited | Personal OST workflow |
| Tability / Quantive | SaaS | Yes | OKR roll-up at the outcome layer |
| Linear | SaaS | Yes (GraphQL) | Experiments tracked as issues |

## Templates & scripts
See `templates.md` and `examples.md` for OST diagrams, prompt sets, and per-node templates.

Inline OST schema (YAML, agent-editable):

```yaml
# ost.yaml — single outcome, n opportunities, m solutions, k experiments
outcome:
  id: O0
  statement: "Increase weekly active editors by 20% in Q3"
  metric: "WAU_editors"
opportunities:
  - id: O1
    statement: "Editors lose work after browser crashes"
    evidence: [INT-031, INT-044, SUPP-118]
    last_validated: 2026-04-01
    solutions:
      - id: S1
        statement: "Local-first autosave with conflict resolution"
        experiments:
          - id: E1
            hypothesis: "Autosave reduces lost-work tickets by 50%"
            method: "Cohort A/B, 4 weeks"
            success: "≥ 30% reduction, p<0.05"
            owner: "@alice"
            status: "running"
```

## Best practices
- One outcome per tree; multiple outcomes → multiple trees, never a hydra.
- Opportunities phrased in customer language ("I lose my work when…"), not in feature language.
- Every opportunity has at least two evidence references; otherwise mark as `unvalidated` and prune.
- Solutions are mutually exclusive within an opportunity — pick one to test, not all.
- Experiments have a written kill criterion; without one, the experiment never ends.
- Re-run a tree review every 2 weeks; archive validated/dead branches with a date.
- Connect each experiment to a delivery ticket and an instrumentation plan; otherwise the experiment can't be measured.
- Keep tree depth ≤ 4 levels (outcome → opportunity → solution → experiment); deeper trees indicate scope confusion.

## AI-agent gotchas
- Agents readily invent opportunities ("users want speed") with no evidence; lint requires evidence IDs from a known source store.
- LLMs collapse opportunity and solution ("opportunity: add bulk export") — node-classifier subagent must reject or rewrite.
- Stale branches accumulate when no agent has authority to archive; assign archival to a human owner field on each node.
- Agents synthesise experiment outcomes from prior knowledge; require explicit "results: TBD" until evidence is logged.
- Tree-rendering agents flatten the structure when rendering, losing parent-child semantics; always serialise from the YAML/JSON, not from the diagram.
- When syncing to Miro, agents over-write hand-edits unless the API call uses optimistic concurrency (etag/version field).
- Bulk-import of interview snippets without dedup floods the tree; force similarity check before adding evidence.

## References
- Teresa Torres — *Continuous Discovery Habits* (2021), Product Talk blog — https://www.producttalk.org/opportunity-solution-tree/
- Marty Cagan — *Inspired* and *Empowered*
- David J. Bland & Alex Osterwalder — *Testing Business Ideas*
- Itamar Gilad — *Evidence-Guided* (2024)
- Productboard "Opportunity prioritisation" guide — https://www.productboard.com
- Miro OST template gallery — https://miro.com/templates/opportunity-solution-tree/
