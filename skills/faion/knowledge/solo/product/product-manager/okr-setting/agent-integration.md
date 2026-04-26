# Agent Integration — OKR Setting

## When to use
- Quarterly goal-setting with 2-50 person teams that need shared focus.
- Mid-sized org with 3-5 strategic priorities that must cascade across teams.
- Solo creator / founder using OKRs to focus a self-directed quarter.
- Aligning a cross-functional initiative (eng + design + marketing) on shared outcome metrics.
- Existing goal system is broken (everyone "achieved 100%" or no one tracks).

## When NOT to use
- Pre-PMF startup where every week pivots — OKRs become stale before the quarter ends; use weekly bets instead.
- Agencies / consultancies where every project is a deliverable — billable utilization tracking beats OKRs.
- Pure delivery teams (compliance, internal IT) — OKRs need outcome variability that does not exist in service work.
- Org with no metric infrastructure — KRs that require new instrumentation will fail because the data never arrives.
- Psychologically unsafe culture — OKRs are amplifiers; in fear-driven orgs they devolve into sandbagging or punishment.

## Where it fails / limitations
- KR-as-task is the universal failure mode: "ship feature X" gets dressed up as a key result.
- "Stretch" sandbagging — teams pick KRs they know they will hit at 100% to look good.
- OKR theatre — beautiful documents, weekly check-ins as performance, no real behavior change.
- Cascading dilution — by the time a top-level OKR reaches an IC, it is unrecognizable or trivially achievable.
- Coupling to compensation destroys the system — any KR tied to bonus instantly becomes sandbagged.
- 70% target is a heuristic, not a law; perfectly calibrated KRs cluster around 60-80% and that is fine.

## Agentic workflow
A drafting agent ingests the company strategy + previous quarter's learnings + current baselines and proposes 3 candidate Objectives, each with 3 candidate KRs (specific, baselined, time-bound). A challenger agent attacks every KR for being a task, missing baseline, or trivial — proposes revisions. A cascade agent generates draft team OKRs that ladder up to company OKRs without simply restating them. A weekly-tracker agent reads metric dashboards, scores progress, and drafts the check-in summary. Human PM owns final wording and prioritization; humans must own the "why this matters" line per Objective.

### Recommended subagents
- A drafter agent (Opus) — strategic decomposition; needs the strongest reasoning model.
- A KR-challenger agent (Sonnet) — single job: identify task-disguised-as-KR and missing baselines.
- A cascade agent — generates team-level OKRs from company OKRs and flags duplicates.
- A weekly-tracker agent — connects to metrics layer, scores 0.0-1.0, drafts narrative.
- `faion-mlp-impl-planner-agent` — once OKRs are set, plans the experiments under each KR.

### Prompt pattern
```
Strategy: <company strategy and current state>.
Previous OKRs and their final scores: <list>.
Baselines: <current numbers for candidate KRs>.
Propose 3 candidate Objectives. For each:
- Objective: inspiring, qualitative, max 10 words
- 3 KRs: each numeric, baselined, time-bound, outcome (not task)
- "Why this matters": 1-2 sentences linking to strategy
Reject any KR that starts with "ship/launch/build/release".
```

```
You are the KR-challenger. For each KR below, decide:
- Is this a task or an outcome? (if task, rewrite or delete)
- Is the baseline stated? (if not, demand baseline)
- Is the target ambitious? (>30% movement from baseline preferred)
- Is the metric instrumentable? (if requires new tracking, flag)
Output: diff with rationale per change.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh project` | Manage OKRs as GitHub Project with custom fields (KR, baseline, target, current) | https://cli.github.com/manual/gh_project |
| `linear-cli` | Linear "Initiatives" map well to Objectives | https://developers.linear.app |
| `dbt` | Define KR metrics with versioned lineage | https://docs.getdbt.com |
| `metabase` API / `superset` API | Auto-build OKR dashboard from metric definitions | https://www.metabase.com/docs/latest/api-documentation |
| `pandoc` | Generate the printable OKR doc from one source-of-truth markdown | https://pandoc.org |
| `slack` API | Push weekly check-in to channel automatically | https://api.slack.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Lattice | SaaS | Yes (REST API) | OKR + performance review combined. |
| 15Five | SaaS | Yes (REST API) | OKRs + weekly check-ins; integrates with Slack. |
| Quantive (Gtmhub) | SaaS | Yes (REST API) | OKR-native, KR auto-update from data sources. |
| Mooncamp | SaaS | Yes (REST API) | OKR + weekly progress posts; cheap. |
| Notion / Coda | SaaS | Yes (REST API) | DIY OKR tracker; flexible, agent-writable. |
| Linear | SaaS | Yes (GraphQL) | Initiatives + projects map to Objectives + KR efforts. |
| Asana | SaaS | Yes (REST API) | Goals module is OKR-shaped. |
| OpenProject | OSS | Yes (REST API) | Self-hostable; supports OKR-style goal hierarchies. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline KR-quality linter:

```python
#!/usr/bin/env python3
"""kr-lint.py — fail OKR docs that contain task-shaped KRs."""
import sys, re, yaml

TASK_VERBS = {"ship", "launch", "build", "release", "create", "design", "implement", "deploy"}

def lint(path):
    with open(path) as f:
        doc = yaml.safe_load(f)
    errs = []
    for obj in doc["objectives"]:
        for kr in obj["key_results"]:
            text = kr["text"].lower()
            first = text.split()[0] if text else ""
            if first in TASK_VERBS:
                errs.append(f"[{obj['name']}] task-shaped KR: '{kr['text']}'")
            if "baseline" not in kr:
                errs.append(f"[{obj['name']}] KR missing baseline: '{kr['text']}'")
            if "target" not in kr:
                errs.append(f"[{obj['name']}] KR missing target: '{kr['text']}'")
            if "deadline" not in kr:
                errs.append(f"[{obj['name']}] KR missing deadline: '{kr['text']}'")
    return errs

errs = lint(sys.argv[1])
for e in errs: print(e)
sys.exit(1 if errs else 0)
```

## Best practices
- 3 Objectives, 3 KRs each, max. More is wishful, not focus.
- Every KR has a baseline number on the day OKRs are committed. No baseline = no commitment.
- Decouple OKRs from compensation. The moment money is on the line, sandbagging dominates.
- Score weekly with confidence (high/med/low), not progress-percent — confidence is forward-looking, percent is backward.
- The "why this matters" sentence is more important than the wording of the Objective. Lose the why and OKRs are vanity prose.
- Commit a kill condition per Objective: "we drop this if X by week 6." Keeps you honest.
- Solo creators: limit to 1 Objective with 3 KRs per quarter. More than that is fantasy.

## AI-agent gotchas
- LLMs produce gorgeous Objective prose ("delight users with magical experiences") that has zero strategic content. Force "why this matters" tied to a specific business reality.
- Models default to KRs-as-tasks because shipping is concrete. Apply a hard banned-verb list: ship/launch/build/release/create/design/implement/deploy.
- Baselines get hallucinated. Require explicit baseline citation (dashboard URL, query, or "TO BE INSTRUMENTED" with owner).
- Cascade agents flatten everything — team OKRs become a restatement of company OKRs. Force decomposition: each level adds resolution, not a copy.
- Weekly tracker agents over-write the narrative every week, hiding trend. Append, do not replace.
- Human-in-loop checkpoint: final OKR set requires explicit human sign-off; agents are too eager to ship the draft.
- Human-in-loop checkpoint: end-of-quarter scoring is sensitive — agents will over-credit progress to look successful. Require human review of final 0.0-1.0 scoring.
- Coupling OKRs to AI-driven performance reviews is a category error. Do not let agents auto-translate KR scores into individual performance ratings.

## References
- John Doerr, "Measure What Matters" — the canonical OKR text (Google/Intel lineage).
- Christina Wodtke, "Radical Focus" — practical OKR + weekly cadence, much better for small teams.
- Felipe Castro — "What Matters" OKR resources: https://felipecastro.com/en/okr/what-is-okr/
- Lenny Rachitsky — OKR field-notes: https://www.lennysnewsletter.com/p/are-okrs-still-a-thing
- "Re:Work" by Google — OKR templates and case studies: https://rework.withgoogle.com/guides/set-goals-with-okrs/
