# Agent Integration — Product Specification Writing

## When to use
- Converting an MVP-scoping output or roadmap initiative into a buildable spec.md before SDD execution.
- A subagent is about to implement a feature and needs WHAT/WHY locked before HOW.
- Stakeholder review is required prior to engineering — the spec is the artifact.
- Producing acceptance criteria that drive both implementation and tests (this repo's faion-feature-executor + faion-sdd-execution rely on them).

## When NOT to use
- Tiny bug fixes or refactors — a one-line issue is enough.
- Rapid prototypes / spikes where the goal is to learn — write a research brief, not a spec.
- Internal-only platform work with no user surface — design doc / RFC fits better.

## Where it fails / limitations
- LLMs mix WHAT and HOW; specs leak into engineering territory unless schema-constrained.
- Acceptance criteria written by an LLM without test data are vague ("works correctly").
- Specs drift after implementation; agents rarely update them post-merge.
- Over-long specs (>3 pages) get skimmed; the longer the spec, the lower the comprehension.
- Open Questions section gets dropped silently; agents pretend to know the answer.

## Agentic workflow
A spec-author subagent receives `{problem, hypothesis, scope_must, scope_wont, persona, success_metric}` from MVP-scoping. It emits a structured spec JSON: `{overview, problem, goals, non_goals, user_stories[], functional_requirements[], non_functional_requirements[], acceptance_criteria[], out_of_scope[], open_questions[]}`. A reviewer subagent validates: every FR has a unique ID and Must/Should/Could priority; every feature has Given-When-Then acceptance criteria; non-goals is non-empty; open-questions is honest (not "none"). A formatter subagent renders to `.aidocs/<feature>/spec.md` matching the SDD convention. The faion-feature-executor skill consumes the resulting spec.md.

### Recommended subagents
- `faion-spec-reviewer-agent` — spec-quality reviewer named in this methodology's metadata.
- `faion-mvp-scope-analyzer-agent` — feeds MVP scope into the spec author.
- `faion-mlp-spec-analyzer-agent` — converts story-map tasks into user stories.
- `faion-sdd-executor-agent` (this repo) — consumes spec.md to drive implementation per SDD.
- `faion-feature-executor` (skill) — runs the spec → tests → impl pipeline.

### Prompt pattern
```
Write a product spec as JSON. Schema:
{
  "overview": "<one paragraph>",
  "problem": {"current": "...", "pains": [...], "impact": "..."},
  "goals": [{"name", "metric", "current", "target"}],
  "non_goals": ["..."],          // MUST be non-empty
  "user_stories": [{"id":"US-1","persona","action","benefit"}],
  "functional_requirements": [{"id":"FR-1","text","priority":"M|S|C"}],
  "non_functional_requirements": [{"id":"NFR-1","kind":"perf|sec|scale|a11y","criterion"}],
  "acceptance_criteria": [{"feature_id":"FR-1","scenarios":[{"given","when","then"}]}],
  "out_of_scope": [{"item","reason"}],
  "open_questions": [{"q","owner","status"}]   // MUST be honest, not empty if you have unknowns
}
Reject if any FR lacks priority, any feature lacks Given-When-Then, or non_goals is empty.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI | Create/track spec PRs alongside code | https://cli.github.com |
| Linear API | Spec docs attached to projects | https://developers.linear.app |
| Notion API | Spec database with status field | https://developers.notion.com |
| `markdownlint-cli2` | Lint spec markdown for structure | https://github.com/DavidAnson/markdownlint-cli2 |
| `vale` | Style-check specs (clarity, voice) | https://vale.sh |
| `pandoc` | Convert spec.md to PDF/HTML for review | https://pandoc.org |
| `mermaid-cli` | Render flow/sequence diagrams in spec | https://github.com/mermaid-js/mermaid-cli |
| `gherkin-lint` | Validate Given-When-Then syntax | https://github.com/vsiakka/gherkin-lint |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes (REST) | Most popular spec home; agent-writable databases |
| Confluence | SaaS | Yes (REST) | Enterprise default; heavyweight |
| Coda | SaaS | Yes (REST) | Spec + automation hybrid |
| Linear Docs | SaaS | Yes (GraphQL) | Specs tied to issues |
| GitHub / GitLab Wiki + repo `.aidocs/` | OSS | Yes | This repo's pattern: spec.md in version control |
| ProductBoard | SaaS | Yes (REST) | Insights → spec linkage |
| Aha! Notebook | SaaS | Yes (REST) | Strategy + spec linkage |

## Templates & scripts
See `templates.md` for the full PRD template and the mini-spec for quick features. Spec linter (≤ 35 lines):

```python
# spec_lint.py — fail spec.json if structurally weak
import json, sys, re
spec = json.load(sys.stdin)

def has(d, key): return bool(d.get(key))

errs = []
if not has(spec, "non_goals"): errs.append("non_goals required, non-empty")
if not has(spec, "goals"): errs.append("goals required")
for g in spec.get("goals", []):
    if not g.get("metric") or not g.get("target"):
        errs.append(f"goal '{g.get('name')}' missing metric/target")

frs = spec.get("functional_requirements", [])
fr_ids = {fr["id"] for fr in frs}
for fr in frs:
    if not re.match(r"^FR-\d+$", fr.get("id","")): errs.append(f"bad FR id: {fr.get('id')}")
    if fr.get("priority") not in ("M","S","C"): errs.append(f"{fr.get('id')} missing priority")

acs = spec.get("acceptance_criteria", [])
acs_for = {ac["feature_id"] for ac in acs}
for fr_id in fr_ids:
    if fr_id not in acs_for:
        errs.append(f"{fr_id} has no acceptance_criteria")

print(json.dumps({"ok": not errs, "errors": errs}, indent=2))
sys.exit(1 if errs else 0)
```

## Best practices
- Keep WHAT and HOW separate. Spec answers what + why; design doc answers how.
- Every functional requirement needs a unique ID and a priority (M/S/C).
- Every feature needs Given-When-Then acceptance criteria — these become test cases.
- Non-Goals is mandatory and non-empty. List ≥ 3 items.
- Cap most specs at 1–3 pages; if longer, split into sub-features.
- Include success metrics with current and target values, not just direction.
- Treat Open Questions as honest unknowns; never list "none" — there are always unknowns.
- Version the spec; on every change, update the status (Draft / Review / Approved / Superseded).

## AI-agent gotchas
- LLMs sneak HOW into FRs ("the system shall use Postgres"). Prompt-level rule: requirements describe behaviour, not implementation.
- "The system shall be fast" is not measurable — force NFRs to include numeric criteria (latency p95 < X ms).
- Agents will fabricate metrics if not given inputs. Pass actual current values; require source citation.
- Open-Questions is the most-skipped section; force minimum 1 question or an explicit `[]` with note "verified all knowns".
- Spec drift: after implementation, re-run a diff agent to detect FRs that changed and update the spec.
- Human-in-loop checkpoints: (a) Goals & Non-Goals approval, (b) FR/AC lock-in before implementation, (c) Open Questions resolution before "Approved" status.

## References
- Joel Spolsky, "Painless Functional Specifications" parts 1–4 https://www.joelonsoftware.com/2000/10/02/painless-functional-specifications-part-1-why-bother/
- Marty Cagan, "Inspired" — opportunity assessment + product spec patterns.
- Atlassian PRD template https://www.atlassian.com/agile/product-management/requirements
- Lenny Rachitsky — "How the best PMs write specs" https://www.lennysnewsletter.com/
- This repo's SDD doc convention — `.aidocs/` and `.product/` patterns.
