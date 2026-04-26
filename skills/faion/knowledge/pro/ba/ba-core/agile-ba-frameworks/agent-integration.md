# Agent Integration — Agile BA Frameworks (canonical, ba-core angle)

This file complements the methodology's existing README which leans into Scrum + SAFe ceremony mapping. The ba-core angle focuses on the **canonical published frameworks** — IIBA's Agile Extension to the BABOK Guide v2, the Disciplined Agile (DA) toolkit, and the Agile Analysis Certification (AAC) competency model — and how an LLM agent applies them as first-principles guidance, not ceremony scripts. The sibling file at `../../business-analyst/agile-ba-frameworks/agent-integration.md` already covers sprint-clock pipelines and Jira/Linear integration — do not duplicate that work; route ceremony-driven tasks there.

## When to use

- Picking an agile BA framework for a new initiative when the team has not yet committed to Scrum/SAFe/DA — agent compares frameworks against context (team size, regulatory load, scaling needs).
- Auditing an existing agile delivery against IIBA Agile Extension's seven principles (See the Whole, Think as a Customer, Analyze to Determine What is Valuable, Get Real Using Examples, Understand What is Doable, Stimulate Collaboration and Continuous Improvement, Avoid Waste) — produces a gap report.
- Mapping BABOK v3 knowledge areas onto an agile horizon (Strategy / Initiative / Delivery) — used when an enterprise BA function migrates from waterfall to agile and needs traceability between old artifacts and new cadences.
- Choosing between Disciplined Agile lifecycles (Agile / Lean / Continuous Delivery: Agile / Continuous Delivery: Lean / Exploratory / Program) for a team — agent runs the DA "Way of Working" decision tree.
- Preparing IIBA Agile Analysis Certification (AAC) study material or competency self-assessment — agent grades evidence against published competency areas.
- Writing a constitution / playbook section that says "this is how we do agile BA" — agent generates the framework synthesis and references official sources.

## When NOT to use

- Day-to-day backlog refinement and sprint-keyed artifact generation — that's the business-analyst variant. Use it.
- Pure tooling questions (Jira API, Linear webhooks). Tooling is downstream of framework choice; frameworks here are vendor-neutral.
- Single-team Scrum with no scaling concern and no regulatory traceability need — overhead of consulting canonical frameworks isn't justified.
- Greenfield product discovery — use `continuous-discovery`, `user-story-mapping`, `strategy-analysis`. Agile BA frameworks describe how to *deliver* against discovered opportunities.
- Non-software domains (marketing ops, HR change). The frameworks lean software; mis-applying their vocabulary creates false precision.

## Where it fails / limitations

- **Framework prescriptions are abstract.** IIBA Agile Extension's seven principles are testable as values, not as automation rules — an agent can check evidence but cannot mechanically grade adherence.
- **Disciplined Agile's breadth is its weakness for LLMs.** DA documents 6 lifecycles, ~24 process goals, hundreds of decision points. Without an indexed knowledge base the agent hallucinates DA terms or invents practices.
- **BABOK v3 ↔ Agile mapping is not 1:1.** Knowledge areas were written waterfall-first; the Agile Extension reinterprets them. Agents that quote BABOK v3 directly into agile contexts produce phrasing that confuses certified BAs.
- **Certification material drift.** AAC v1 (2017) vs. v2 vocabulary differs. Pin the version explicitly or grading reports cite stale competencies.
- **No empirical effectiveness data.** Frameworks publish guidance, not outcome benchmarks. An agent recommending "use DA Lean lifecycle" cannot cite measured cycle-time impact — recommendations are evidence-light by nature.
- **Cultural assumptions hidden in text.** All three frameworks assume Western team-based authority distribution; misapplied in highly hierarchical org cultures, the recommendations bounce off political reality.
- **Scope conflict with PMI Disciplined Agile (acquired 2019).** DA materials post-2019 carry PMI brand and overlap with PMI-ACP — version-stamping matters.

## Agentic workflow

Treat this as a **knowledge-retrieval + synthesis pipeline**, not a periodic pipeline. Trigger is one-shot: an analyst asks "which framework, which principles apply, where are we missing them?" Steps: (1) ingest the team's current state (constitution, roadmap, sample backlog, retro notes, regulatory profile); (2) load canonical framework reference packs from `knowledge/pro/ba/ba-core/agile-ba-frameworks/` plus sibling references in `requirements-lifecycle/` and `requirements-prioritization/`; (3) run a comparison matrix (context dimensions × framework prescriptions); (4) emit a `framework-fit.md` report with primary recommendation, secondary alternative, and explicit principle-level gap list; (5) hand off operational follow-up (story refinement, AC generation) to the business-analyst variant agent. Human BA reviews the synthesis — never auto-apply a framework choice.

### Recommended subagents

- `faion-research-agent` — Pulls regulatory and team-context evidence from the project's `.aidocs/` (constitution, retros) before framework selection. Prevents framework-fit-without-evidence errors.
- `faion-brainstorm` — Diverge step when multiple frameworks are plausible (e.g., DA Lean vs. SAFe Essential for a 50-person org). Generates 3-5 framing options before converge.
- `faion-software-architect` skill — Loaded when framework choice has architectural implications (DA Continuous Delivery lifecycle assumes mature DevOps, not all teams qualify).
- `faion-sdd-executor-agent` — Once the framework is chosen, this agent owns SDD constitution updates that codify the choice ("we follow IIBA Agile Extension principles 1-7").
- General `Task` subagent for synthesis — pass the full methodology folder + sibling READMEs (`ba-planning`, `requirements-prioritization`, `solution-assessment`) as context. Cap output at one report, not a series.
- Cross-link to `business-analyst/agile-ba-frameworks/agent-integration.md` for downstream sprint-cadence work — that variant handles the operational layer.

### Prompt pattern

Framework fit assessment:

```
Read .aidocs/constitution.md, .aidocs/roadmap.md, last 3 retros under .aidocs/retros/, and the methodology pack at skills/faion/knowledge/pro/ba/ba-core/agile-ba-frameworks/.
Score the team against (a) IIBA Agile Extension's 7 principles (1=absent, 5=embedded, with one quoted evidence line per score) and (b) Disciplined Agile lifecycle fit (Agile / Lean / CD-Agile / CD-Lean / Exploratory / Program).
Produce framework-fit.md: primary framework, secondary, top 3 principle gaps with concrete remediation actions.
Cite official sources (IIBA, PMI Disciplined Agile) by URL — no paraphrase without source.
```

Principle-gap audit:

```
For each of the 7 IIBA Agile Extension principles, find evidence in <project root>/.aidocs/ and the last 50 PR descriptions.
Output a CSV: principle, score 1-5, evidence quote, gap, suggested next action, owner role (PO/BA/SM/Architect).
Flag any principle with score < 3 as a constitution review item.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert framework reference PDFs (BABOK Agile Extension, DA browser exports) into Markdown the agent can ingest | `apt install pandoc` |
| `jq` | Score-report transformation; framework comparison matrices serialized as JSON | `apt install jq` |
| `pdftotext` (Poppler) | One-shot extraction from BABOK PDFs (note: license forbids redistribution; keep extracts local) | `apt install poppler-utils` |
| `git` + `pre-commit` | Version constitution edits that codify framework choice; reject untracked principle changes | https://pre-commit.com |
| `mermaid-cli` | Render decision-tree diagrams (DA Way-of-Working) into the framework-fit report | `npm i -g @mermaid-js/mermaid-cli` |
| `mkdocs` / `docusaurus` | Publish framework-fit reports as a living team site | https://www.mkdocs.org |
| `csvkit` | Process principle-audit CSV outputs (rank, filter, pivot) | `pip install csvkit` |
| `gh issue` | File principle-gap items into the team backlog with consistent labels | https://cli.github.com |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| IIBA Member Portal | SaaS (paywalled) | No public API | Source of BABOK v3 + Agile Extension; license-bound, no redistribution |
| PMI Disciplined Agile Browser | SaaS (PMI account) | No API | Authoritative DA process goal / decision-point reference |
| Scaled Agile Framework site | SaaS (free read) | Scrape-only | Reference-only; SAFe is implementation, not a BA framework |
| Confluence | SaaS | REST API | Persist `framework-fit.md` and principle-audit CSV next to constitution |
| Notion | SaaS | REST API | Same purpose as Confluence; better for solo / small teams |
| Obsidian + Git | OSS | Filesystem-friendly | Best fit for offline LLM agents; one note per principle |
| Mural / Miro | SaaS | Limited API | Human workshop boards for principle reviews; export to MD |
| Brightspace / Coursera (AAC prep) | SaaS | None | Certification study material; manual ingest only |
| LeanIX | SaaS | REST API | Enterprise architecture context for portfolio-level framework decisions |
| ProcessMaker / Camunda | OSS / SaaS | REST API | Where DA "Lean" lifecycle implies BPMN-driven execution |

## Templates & scripts

The methodology's `templates.md` is sparse; this report uses an inline framework-comparison matrix and a principle scorecard. Both fit ≤50 lines.

Framework comparison matrix (`framework-fit.md` skeleton, fill per project):

```markdown
# Framework Fit Report — <project>

## Context
- Team size: <n>
- Regulatory profile: <none|GDPR|HIPAA|SOC2|FDA|...>
- Scaling: <single team|2-10 teams|10+ teams|portfolio>
- Discovery maturity: <pre|in-flight|post>
- DevOps maturity: <manual|CI|CD|continuous-deployment>

## Comparison

| Dimension | IIBA Agile Extension | Disciplined Agile | SAFe BA |
|-----------|----------------------|-------------------|---------|
| Vendor | IIBA | PMI | Scaled Agile Inc. |
| Scope | Principles + horizons | Toolkit / lifecycles | Scaled framework |
| BA role explicit | Implicit (competencies) | Explicit (DA roles) | Implicit (PO/PM) |
| Scaling guidance | Light | Strong | Strongest |
| Cost to adopt | Low | Medium | High |
| Best fit | Single team / 2-3 teams | Mid-org, mixed cadences | Large enterprise |

## Recommendation
- Primary: <framework>
- Rationale (3 bullets)
- Secondary fallback: <framework>

## Principle gaps (IIBA AE)
| # | Principle | Score 1-5 | Evidence | Action |
|---|-----------|-----------|----------|--------|
| 1 | See the Whole |  |  |  |
| 2 | Think as a Customer |  |  |  |
| 3 | Analyze to Determine What is Valuable |  |  |  |
| 4 | Get Real Using Examples |  |  |  |
| 5 | Understand What is Doable |  |  |  |
| 6 | Stimulate Collaboration and Continuous Improvement |  |  |  |
| 7 | Avoid Waste |  |  |  |
```

## Best practices

- **Pin framework versions in the constitution.** "IIBA Agile Extension v2 (2017), Disciplined Agile via PMI Browser as of <quarter>." Without pin, agent output drifts as upstream content updates.
- **Treat the seven IIBA principles as audit checklist, not aspiration.** Score quarterly with quoted evidence; principle scores < 3 become explicit backlog items, not "we'll do better."
- **Choose one canonical framework, supplement with techniques from others.** Mixing DA + SAFe + IIBA AE without an anchor produces vocabulary chaos. Pick the anchor, label the borrowed techniques.
- **Cite primary sources, never blog summaries.** Agents trained on aggregator content reproduce errors. Prompt explicitly: "cite IIBA, PMI, Scaled Agile only."
- **Decouple framework selection from tooling selection.** Choosing DA does not pick Jira; choosing Linear does not pick Scrum. Agents that conflate them produce false constraints.
- **Run principle audit before framework switch, not after.** Switching frameworks to fix a principle gap usually fails — the gap is cultural. Address principles first; framework follows.
- **Document explicit non-adoptions.** "We do not adopt SAFe Portfolio level — we have one product." Saves future agents from re-litigating.
- **Refresh the framework-fit report after major team or scope changes.** Triggers: team size doubles, new regulatory load, M&A, new product line.

## AI-agent gotchas

- **Hallucinated DA process goals.** Disciplined Agile has ~24 process goals; agents under context pressure invent plausible-sounding extras. Force the agent to enumerate from a vetted list — fail closed if it can't.
- **BABOK v3 quoted into agile contexts verbatim.** Knowledge-area definitions are waterfall-tinted; quoting them as agile guidance misleads. Always cross-reference with the Agile Extension first.
- **Principle scoring without evidence quotes.** Models hand back "Principle 4: 4/5" with no quote. Reject any score row missing a quoted source line.
- **SAFe-as-framework confusion.** Agents pattern-match on "agile + scaling" → SAFe regardless of fit. Add a guard: "if team < 50 people, do not propose SAFe."
- **DA lifecycle proliferation.** When given 6 lifecycle options the agent picks "all of them apply" — useless. Force a single primary + at most one alternative.
- **AAC competency drift.** Agents reproduce 2017 competency wording in 2025 contexts. Pin the AAC version in system prompt or grading is dated.
- **Vendor bias.** Anthropic-trained models lean toward Atlassian / SAFe content (over-represented online). When asked about DA or IIBA, output is thinner — boost via explicit reference packs.
- **Auto-edits to constitution.md.** Constitution is the single source of truth; agent must propose diffs, never write directly. Always review-then-merge.
- **Citation of paywalled IIBA / PMI content.** Some agents quote BABOK passages verbatim. License risk. Restrict to summary + URL; never inline long quotes.
- **Confusing Disciplined Agile (PMI) with Disciplined Agile Delivery (Scott Ambler, pre-2019).** Different scope, different vocabulary. Pin the post-2019 PMI version unless explicitly using the legacy material.
- **Treating ceremony coverage as principle adherence.** Running stand-ups does not equal "Stimulate Collaboration." Force evidence beyond ceremony attendance.

## References

- Methodology files: `./README.md`, `./checklist.md`, `./templates.md`, `./examples.md`, `./llm-prompts.md`
- Sibling (operational variant): `../../business-analyst/agile-ba-frameworks/agent-integration.md`
- IIBA Agile Extension to the BABOK Guide v2: https://www.iiba.org/standards-and-resources/agile-extension/
- IIBA BABOK v3: https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/
- IIBA Agile Analysis Certification (AAC): https://www.iiba.org/business-analysis-certifications/agile-analysis-certification/
- PMI Disciplined Agile Browser: https://www.pmi.org/disciplined-agile/da-browser
- Scott Ambler — Disciplined Agile background: http://www.disciplinedagiledelivery.com
- Scaled Agile Framework 6.0 (reference, not BA framework): https://framework.scaledagile.com
- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- IIBA seven agile principles overview: https://www.iiba.org/business-analysis/agile-extension/
