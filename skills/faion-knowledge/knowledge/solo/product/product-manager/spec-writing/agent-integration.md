# Agent Integration — Product Specification Writing

## When to use
- Feature is large enough (>1 sprint) that engineers and designers need a shared written contract before work starts.
- Cross-team work where multiple stakeholders (legal, support, ops) must approve scope.
- Building against an external SLA or paid customer commitment that requires traceable requirements.
- Onboarding a contractor — the spec is the briefing artefact.

## When NOT to use
- Tiny changes (<1 day, no ambiguity) — a backlog item with acceptance criteria is sufficient.
- Highly exploratory discovery work where requirements will change weekly. Spec the experiment, not the product.
- After implementation as a retroactive doc (it becomes documentation, not a spec — call it that).
- When the team will not maintain the spec post-launch; outdated specs mislead more than they help.

## Where it fails / limitations
- Specs that mix "what" with "how" (UI implementation, DB schema). Engineers ignore the doc; designers feel boxed in.
- 30-page specs nobody reads. Beyond ~5 pages, fidelity drops; structure matters more than completeness.
- Acceptance criteria written as prose paragraphs instead of testable Given/When/Then statements.
- Missing "Non-Goals" — scope creep follows immediately because the boundary is undefined.
- LLM-generated specs are confident in domains the model knows nothing about (regulated industries, edge integrations); they invent requirements.

## Agentic workflow
A research agent gathers inputs (problem statement, persona notes, analytics, prior art) and emits a structured "context" object. A drafter agent fills the spec template with required sections, never inventing acceptance criteria from thin air. A reviewer agent runs the rubric ("does every FR have an AC? are NFRs measurable? are non-goals listed?"). An open-questions agent extracts unknowns and assigns owners. Humans sign off on the goals/non-goals and on any FR labelled "Must".

### Recommended subagents
- `faion-spec-reviewer-agent` — referenced in `README.md`; primary reviewer.
- `faion-task-creator-agent` — splits the approved spec into backlog items with acceptance criteria.
- `faion-mvp-scope-analyzer-agent` — feeds in if the spec must be cut to MVP scope.
- `faion-idea-generator-agent` — solution divergence before the spec freezes one approach.

### Prompt pattern
```
System: You are a PRD drafter. Output ONLY Markdown matching the schema in
  README.md. For each functional requirement, generate a unique ID FR-N and
  pair it with at least one Given/When/Then acceptance row referencing FR-N.
  Forbid implementation hints (DB names, library names, UI components).
Input: {problem, persona, success_metrics, constraints, prior_specs?, research_links}
```

```
System: You are a PRD reviewer. Apply this rubric and return JSON:
  {missing_sections:[], untestable_acs:[], orphan_frs:[], unmeasurable_goals:[],
   leaking_implementation:[], score:0..10}
Reject any spec scoring <7 or with >0 orphan FRs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert spec Markdown → PDF/DOCX/HTML for stakeholders | https://pandoc.org |
| `markdownlint-cli2` | Lint spec structure | `npm i -g markdownlint-cli2` |
| `vale` | Style/clarity checks (Microsoft / Google styles) | https://vale.sh |
| `mermaid-cli` | Render flow/state diagrams embedded in spec | `npm i -g @mermaid-js/mermaid-cli` |
| `gh` | Open PR with spec.md, request reviews from owners | https://cli.github.com/manual |
| `notion-sdk` | Sync spec to Notion for non-technical reviewers | https://github.com/ramnes/notion-sdk-py |
| `pre-commit` | Block commits with malformed FR/AC IDs | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes (REST) | Most flexible, weak structural validation. |
| Confluence | SaaS | Yes (REST) | Required by many enterprises; heavyweight. |
| Linear Docs | SaaS | Yes (GraphQL) | Tight coupling with backlog items. |
| Coda | SaaS | Yes (REST) | Database-backed sections useful for FR/AC tables. |
| GitHub (Markdown in repo) | SaaS | Yes (Git) | Ideal for solo founders / engineering-led teams. |
| Productboard | SaaS | Yes (REST) | "Spec" tab linked to features. |
| Aha! Notebooks | SaaS | Yes (REST) | Strong traceability to OKRs. |
| HackMD / Outline | SaaS/OSS | Yes (REST) | Lightweight collaborative authoring. |

## Templates & scripts
See `README.md` and `templates.md` for the full PRD and Mini-Spec layouts. Inline checker that enforces FR ↔ AC traceability:

```python
import re, sys
text = open(sys.argv[1]).read()
frs = set(re.findall(r"\bFR-\d+\b", text))
ac_refs = set(re.findall(r"\bFR-\d+\b", "\n".join(
    [l for l in text.splitlines() if "Given" in l or "When" in l or "Then" in l])))
errs = []
required = ["## Overview","## Problem","## Goals","## Non-Goals","## User Stories",
            "## Requirements","## Acceptance Criteria","## Out of Scope","## Open Questions"]
for sect in required:
    if sect not in text: errs.append(f"missing section: {sect}")
orphans = frs - ac_refs
if orphans: errs.append(f"FRs without AC: {sorted(orphans)}")
if not re.search(r"^\| Metric \| Current \| Target \|", text, re.M):
    errs.append("missing measurable success metrics table")
if "implementation:" in text.lower() or "schema:" in text.lower():
    errs.append("possible implementation leak — review")
for e in errs: print("FAIL:", e)
sys.exit(1 if errs else 0)
```

## Best practices
- Use IDs (FR-1, NFR-1, US-1) and reference them throughout. Without IDs, traceability collapses on first edit.
- Always include Non-Goals; they prevent scope creep more reliably than priority labels.
- Cap functional requirements at ~15 per spec. Larger features should be split.
- Make every goal measurable with a current/target table. "Improve UX" is not a goal.
- Keep "how" out: no library names, no schemas, no UI mocks (mocks live in design doc, linked).
- Open Questions section is mandatory; an empty section signals fake confidence.
- Specs are versioned: track decisions made post-approval as an addendum, never silently rewrite.
- Pair with `mvp-scoping` if the FR list exceeds capacity — cut to Must/Should/Could before publishing.

## AI-agent gotchas
- LLMs default to elaborate prose; force structured templates with explicit section headings or reject output.
- Acceptance criteria written as restatements of FRs ("FR-2: search works → AC: search works"). Require unique G/W/T phrasing per AC.
- Models invent NFRs ("99.99% uptime", "GDPR compliant") without basis — strip generic NFR boilerplate unless backed by source.
- Open Questions section gets dropped because the model "answers" everything. Tell it explicitly: list things you do NOT know.
- Personas conflated with user types (e.g. "the user"). Inject persona ids and require them in every story.
- Long context with prior specs: agents copy-paste old FRs without updating IDs, creating duplicates. Reset numbering or reuse existing IDs deliberately.
- Specs containing PII / customer names: scrub via pre-publish hook; LLMs do not redact reliably.
- Token cost: a typical spec ≈ 4–8k tokens output; embed only the diffed sections in iteration to save context.
- Always require human approval on goals + non-goals before any FR work; those decisions encode strategy and cannot be delegated.

## References
- Marty Cagan — *Inspired* (PRD vs vision document).
- Joel Spolsky — "Painless Functional Specifications": https://www.joelonsoftware.com/2000/10/02/painless-functional-specifications-part-1-why-bother/
- ProductPlan — PRD guide: https://www.productplan.com/glossary/product-requirements-document/
- Aha! — PRD template library: https://www.aha.io/roadmapping/guide
- Atlassian — PRD template: https://www.atlassian.com/agile/product-management/requirements
- Lenny Rachitsky — "How to write a great PRD": https://www.lennysnewsletter.com/p/how-to-write-a-prd
