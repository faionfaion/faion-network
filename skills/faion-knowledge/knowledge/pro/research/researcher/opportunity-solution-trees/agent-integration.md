# Agent Integration — Opportunity Solution Trees (OST)

OST connects a desired Outcome to Opportunities (customer needs/pains), Solutions, and Assumption Tests/Experiments. Originally formalised by Teresa Torres in *Continuous Discovery Habits* and now backed by tools like Vistaly, Miro, FigJam, Whimsical, and Productboard.

## When to use
- Translating a single business outcome (KPI, OKR) into a discovery backlog of customer-rooted opportunities.
- Synthesising raw user-research artefacts (interview notes, JTBD, support tickets, NPS verbatims) into a navigable structure.
- Aligning PM/design/engineering on which sub-problems are in scope before any solution is committed.
- Deciding between competing solution ideas under a fixed opportunity ("compare and contrast" via experiments).
- Maintaining a living artefact during continuous discovery cycles (weekly interviews, ongoing experiments).

## When NOT to use
- Pure delivery / sprint planning — use a roadmap, Now/Next/Later, or Jira board instead.
- Compliance, regulatory, or contract-driven work where the "opportunity" is fixed and only execution remains.
- Single-developer side projects where outcome ↔ solution distance is trivial (the tree adds ceremony, not insight).
- Crisis / incident response where speed beats discovery rigour.
- When you have zero customer evidence — building an OST from "what we think users want" produces a confident-looking lie.

## Where it fails / limitations
- Garbage-in/garbage-out: opportunities not grounded in actual interview transcripts become solutions in disguise (most common failure mode).
- Tree explosion: teams brainstorm 50+ opportunities, lose focus, and never run experiments. Width must be pruned.
- Outcome-as-solution: outcome phrased as "ship feature X" short-circuits the entire framework before it starts.
- Single-solution branches: skipping "compare and contrast" yields no real choice; always generate 3+ solutions per opportunity.
- Stale trees: an OST not updated weekly becomes a project-plan-with-extra-shapes.
- LLM hallucination of opportunities: pattern-matched from training data, not from your customers — sounds plausible, traces to nothing.

## Agentic workflow
Best run as a multi-pass pipeline: a researcher subagent ingests raw evidence (transcripts, tickets, surveys) and emits clustered opportunities with citations; a PM/synthesis subagent shapes the tree (outcome → opportunities → solutions); an experiment-designer subagent attaches assumption tests per solution; a critic subagent challenges each node ("is this really an opportunity or a solution?", "what evidence supports this?"). Persist the tree as structured JSON/YAML so each pass is idempotent and diffable, then render to Mermaid/Markdown for humans and push to Vistaly/Miro for the team.

### Recommended subagents
- `faion-research-agent` (existing, see researcher/CLAUDE.md) — runs `pains` and `validate` modes to produce the evidence base.
- `ost-synthesizer` — clusters pains into opportunities, enforces customer-language phrasing, requires evidence citations.
- `ost-solution-generator` — produces ≥3 solution candidates per opportunity, tags each with assumption types (desirability/viability/feasibility/usability/ethicality).
- `ost-experiment-designer` — attaches one falsifiable assumption test per solution (Mom-Test interview, fake-door, prototype, data dive).
- `ost-critic` — adversarial review: flags solutions-disguised-as-opportunities, missing evidence, unfalsifiable experiments, single-solution branches.

### Prompt pattern
```
You are ost-synthesizer. Input: array of interview snippets with stable IDs.
Cluster into opportunities. Rules:
- Phrase each opportunity in the customer's own language (verb + need + context).
- Each opportunity must cite ≥2 snippet IDs as evidence.
- Reject any node that names a solution, technology, or feature.
- Output JSON: {opportunities:[{id, statement, evidence_ids[], parent_id|null}]}.
```
```
You are ost-critic. For each node, answer:
1. Is this an opportunity or a solution wearing a disguise? (cite signal)
2. Evidence count and quality (1-5).
3. Compare-and-contrast: how many sibling solutions exist?
4. Falsifiable experiment attached? Y/N.
Output: {node_id, verdict: keep|rephrase|drop, reason}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` (`mmdc`) | Render OST JSON → SVG/PNG diagrams | `npm i -g @mermaid-js/mermaid-cli` |
| `mdtree` / `markmap-cli` | Markdown indented list → interactive mind-map | `npm i -g markmap-cli` |
| `jq` | Validate / transform OST JSON between passes | apt/brew |
| `yq` | YAML variant for human-edited trees | apt/brew |
| Vistaly REST API | Programmatic CRUD on outcomes/opportunities/solutions/assumption-tests | `docs.vistaly.com` |
| Miro REST API | Push generated tree to a board (sticky-per-node) | `developers.miro.com` |
| Figma/FigJam Plugin API | Custom OST widget (`zhouk/ost-figjam-widget` reference) | `figma.com/developers` |
| Linear / Jira / GitHub APIs | Link Solution nodes → delivery issues | native REST |
| `claude-cli` headless | Run subagents in batch (`-p` mode) for tree passes | `npm i -g @anthropic-ai/claude-code` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Vistaly | OST-native SaaS | Yes (REST + Zapier) | Purpose-built for Torres OST; native Jira/Linear/GitHub sync |
| Miro | Whiteboard SaaS | Yes (REST API, OAuth) | Official OST template; sticky-note OST is brittle for diffs |
| FigJam | Whiteboard SaaS | Partial (Plugin API) | OST widget exists; no full REST CRUD |
| Whimsical | Diagram SaaS | Limited | Embed/share API only, no node-level write |
| Productboard | Product mgmt SaaS | Yes (REST API) | Can host opportunities (Insights → Features); not a true tree UI |
| Mural | Whiteboard SaaS | Yes (REST API) | Generic, OST template available |
| CraftUp OST Builder | Free web tool | No API | Manual; exports MD/CSV/JSON — useful as schema reference |
| Jira Product Discovery | Idea mgmt | Partial | Atlassian community has open OST request; workaround via custom fields |
| Lucidchart | Diagram SaaS | Yes (REST API) | Generic tree shapes, no OST semantics |
| Mermaid Live / GitHub | Diagram-as-code | Native | Best fit for git-tracked, agent-edited OST |

## Templates & scripts
See `templates.md` for the methodology data model. Inline reference: a minimal JSON schema agents can produce and validate between passes.

```yaml
# ost.yaml — agent-friendly canonical form
outcome:
  id: O-1
  metric: "Activation rate W1"
  target: "30% → 45% by Q3"
opportunities:
  - id: OP-1
    parent: O-1
    statement: "New users can't tell what to do first after signup"
    evidence: [INT-04, INT-09, TKT-211]   # interview/ticket IDs
    sizing: { reach: high, impact: high, confidence: med }
solutions:
  - id: S-1
    parent: OP-1
    statement: "Interactive 3-step product tour"
    assumption_types: [desirability, usability]
  - id: S-2
    parent: OP-1
    statement: "Templated starter project on first login"
    assumption_types: [desirability, feasibility]
experiments:
  - id: E-1
    parent: S-1
    type: prototype-test
    riskiest_assumption: "users will complete a 3-step tour"
    success_metric: "≥60% complete tour"
    falsifier: "<40% complete"
```

```bash
# render OST yaml → mermaid → svg
yq -o=json ost.yaml | jq -r '
  "graph TD",
  (.outcome | "O[\(.id): \(.metric)]"),
  (.opportunities[] | "O --> \(.id)[\(.statement)]"),
  (.solutions[] | "\(.parent) --> \(.id)((\(.statement)))"),
  (.experiments[] | "\(.parent) --> \(.id)>\(.type)]")
' > ost.mmd
mmdc -i ost.mmd -o ost.svg
```

## Best practices
- Anchor every opportunity to ≥2 evidence IDs (transcript line, ticket, survey row). No evidence → no node.
- Enforce customer language at the opportunity layer; reject feature/tech vocabulary via a regex/critic pass.
- Generate ≥3 solutions per opportunity before any selection — "compare and contrast" is the whole point.
- Pick one target opportunity per discovery cycle; the rest stay parked. Width without depth is theatre.
- Store the OST as code (YAML/JSON in git); Miro/Vistaly is a render target, not the source of truth.
- Re-run the critic agent after every human edit; trees decay fast.
- Tag each solution with assumption type (desirability/viability/feasibility/usability/ethicality) so experiment design is targeted.
- Keep the tree shallow but iteratable: 1 outcome × 5–7 opportunities × 3 solutions × 1 experiment beats a 200-node monster.
- Use stable IDs (`O-1`, `OP-3`, `S-7`) — agents diff and reference by ID, not statement text.

## AI-agent gotchas
- LLMs love to invent opportunities that pattern-match the domain ("users want better UX") with no transcript trace — always require evidence_ids and verify they exist.
- One-shot generation conflates layers: outcomes phrased as features, opportunities phrased as solutions. Run a dedicated layer-validator pass.
- "Generate 3 solutions" prompts return three rephrasings of the same idea unless you force structural diversity (e.g., one tech, one process, one content solution).
- Token-budgeted single-call OST → shallow, lossy. Use multi-pass: ingest → cluster → critique → expand → diff.
- Subagents drift on terminology between calls; pin a glossary (Outcome / Opportunity / Solution / Assumption Test) in every system prompt.
- Don't let the agent "finish" the tree. OST is never done; the agent should output `next_interview_questions` and `next_riskiest_assumption`, not a closing summary.
- Visual tools (Miro, FigJam) are write-mostly for agents — round-tripping a hand-edited Miro board back into structured form is brittle. Prefer git-tracked YAML as the canonical form, sync one-way to the visual tool.
- Be wary of "AI OST builders" that produce a tree from a one-line prompt; they hallucinate confidence. Useful only as a starter scaffold to be torn down by evidence.
- Experiments often degrade into "we'll measure usage after launch" — that is not falsifiable. Force a pre-registered failure threshold (e.g., `<40% completion = drop`).

## References
- Teresa Torres — *Continuous Discovery Habits* (book) and producttalk.org OST canonical guide: https://www.producttalk.org/opportunity-solution-trees/
- Tools of the Trade roundup: https://www.producttalk.org/2023/09/tools-of-the-trade-opportunity-solution-tree/
- Vistaly OST product + API: https://www.vistaly.com/product/opportunity-solution-tree
- Vistaly Jira integration: https://docs.vistaly.com/documentation/integrations/jira
- Miro OST template: https://miro.com/templates/opportunity-solution-tree/
- FigJam OST template: https://www.figma.com/templates/opportunity-solution-tree/
- FigJam OST widget (open source): https://github.com/zhouk/ost-figjam-widget
- Vistaly OST patterns deep-dive: https://blog.vistaly.com/posts/ost_patterns
- Teresa Torres on AI-assisted OST synthesis: https://www.producttalk.org/ai-opportunity-solution-trees/
- Sibling methodology in this repo: `../continuous-discovery/README.md`
