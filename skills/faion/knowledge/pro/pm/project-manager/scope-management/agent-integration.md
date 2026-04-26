# Agent Integration — Scope Management

## When to use
- Project initiation: drafting scope statement, requirement collection, baselining
- Mid-project change requests where impact assessment must precede approval
- Multi-stakeholder programs with conflicting priorities (need MoSCoW + traceability)
- Contracted/fixed-price work where every out-of-scope item is a margin event
- Requirements traceability for regulated domains (medtech, fintech, gov)

## When NOT to use
- Continuous-discovery agile product (kill scope baselines; use rolling outcomes instead)
- Pure research/spike work where scope is the question
- Internal tools at < 10 users where formal sign-off is theater
- Crisis incidents (incident scope is "stop the bleeding", not a PMP doc)

## Where it fails / limitations
- Scope baselines age fast in adaptive contexts — by month 3 the doc lies
- Stakeholders sign off on scope they did not read; later disputes anyway
- Requirements traceability matrices (RTM) become orphaned after sprint 2
- Exclusions are rarely written explicitly; ambiguity wins disputes
- Gold-plating from agents: LLMs add "while we're here" features that breach scope
- "Functional vs non-functional" boundary is fuzzy (auth: which?), causes gaps
- Change control bottlenecks if every scope tweak needs a CCB meeting

## Agentic workflow
A requirements-extractor subagent reads stakeholder input (interviews, emails, slack threads, RFPs), normalizes into business/stakeholder/solution/transition/non-functional buckets with MoSCoW priorities, and emits a requirements doc. A scope-validator agent checks completeness (every "must" has acceptance criteria, every deliverable has an owner). A change-impact agent evaluates incoming change requests across schedule, cost, risk, and downstream dependencies. PM signs off; agent writes ADR. Pair with `business-analyst` and `sdd-planning` skills.

### Recommended subagents
- `requirements-extractor` — distills stakeholder text into structured requirements
- `scope-validator` — checks for completeness, ambiguity, missing exclusions
- `change-impact-analyzer` — quantifies CR effect on schedule/cost/quality
- `traceability-keeper` — links requirements to design, code, tests; updates RTM

### Prompt pattern
```
You are a requirements-extractor. From {transcripts}, extract requirements
in JSON {id, type: business|stakeholder|solution|transition|nfr, statement,
priority: must|should|could|wont, source, acceptance_criteria}. Reject any
statement that lacks a verifiable AC; emit a clarifying question instead.
```

```
You are a change-impact-analyzer. CR: {cr_text}. Project state: {wbs.json}.
Return impact JSON {affected_wp_ids, schedule_delta_days, cost_delta_usd,
risk_delta, dependencies_broken, recommendation: approve|reject|defer,
rationale}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert RTM/scope docs across formats (Word, PDF, MD) | https://pandoc.org |
| `marp` / `mkdocs` | Publish scope docs as a versioned site | https://marp.app, https://mkdocs.org |
| `gh` | Track scope items as GitHub Issues with `requirement` label | https://cli.github.com |
| `jira` (CLI) | Sync requirements as Jira issues, link to deliverables | https://github.com/ankitpokhrel/jira-cli |
| `dot` (Graphviz) | Render dependency / traceability graphs | https://graphviz.org |
| `csvkit` | Manipulate RTM CSVs | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | Yes | Requirements + traceability, REST API |
| IBM DOORS Next | SaaS / on-prem | Partial | Heavy enterprise, OSLC API |
| Helix RM (Perforce) | SaaS | Yes | RM + ALM integration |
| Confluence | SaaS | Yes | Lightweight requirements pages, REST API |
| Notion | SaaS | Partial | DB-backed requirements, API quirks |
| ReqView | Desktop / SaaS | Yes | OSLC, ReqIF import/export |
| Aha! | SaaS | Yes | Roadmaps + scope, REST API |
| Modern Requirements | SaaS (Azure DevOps add-on) | Partial | ADO-bound |

## Templates & scripts
See templates.md for scope statement and RTM. Inline traceability checker:

```python
# trace_check.py — flag requirements without design/test coverage
import csv, sys
rows = list(csv.DictReader(open("rtm.csv")))
missing = []
for r in rows:
    if r.get("priority") == "must" and (not r.get("design_ref") or not r.get("test_ref")):
        missing.append(r["id"])
if missing:
    print(f"GAP: {len(missing)} must-haves missing design/test refs:")
    for i in missing: print(" -", i)
    sys.exit(1)
print("OK")
```

```python
# moscow_lint.py — enforce MoSCoW invariants
import yaml, sys
spec = yaml.safe_load(open("requirements.yaml"))
errs = []
musts = [r for r in spec if r["priority"] == "must"]
if not musts: errs.append("no MUST requirements — scope undefined")
for r in spec:
    if not r.get("acceptance_criteria"):
        errs.append(f'{r["id"]}: missing acceptance criteria')
    if r["priority"] == "must" and r.get("status") == "wont":
        errs.append(f'{r["id"]}: MUST cannot be Wont')
print("\n".join(errs) or "OK")
sys.exit(1 if errs else 0)
```

## Best practices
- Write exclusions before inclusions — saying "no" up front prevents 80% of scope disputes
- Every scope item has: source stakeholder, AC, owner, traceability ID — no exceptions
- Baseline scope at end of planning; subsequent changes go through change control with cost/schedule/risk delta
- Use MoSCoW with quotas (e.g., max 60% must) to force prioritization
- For agile contexts, use "outcome scope" (KPI movement) over "feature scope" (list)
- RTM lives in source control as YAML/CSV, not a Word doc — agents and humans both edit
- Capture every "while you're at it" gold-plating attempt as a CR; do not absorb silently

## AI-agent gotchas
- LLMs paraphrase requirements into different wording each pass; freeze canonical text and require diff-based edits
- Agent-extracted requirements drop priority info silently; force `priority` as a required JSON field
- Requirement IDs renumber on regeneration if not pinned; use UUIDs or content-hash IDs
- Change-impact agents underestimate ripple cost (schedule networks); validate against CPM
- Gold-plating: agents add unrequested NFRs ("must support 1M req/s"); cap NFR generation to those with explicit source
- Acceptance criteria written by agents tend to be tautological ("system shall display the page when page is displayed") — review for testability
- For regulated work, agent must not redact source quotes from RTM; auditor needs original wording

## References
- PMBoK 7th: Planning Performance Domain
- BABOK v3 (IIBA) — requirements analysis
- Karl Wiegers, *Software Requirements* (3rd ed.) — INVEST and ambiguity guides
- IEEE 29148-2018 — requirements engineering standard
- Atlassian, "Scope creep without ceremony": https://www.atlassian.com/agile/project-management/scope-creep
