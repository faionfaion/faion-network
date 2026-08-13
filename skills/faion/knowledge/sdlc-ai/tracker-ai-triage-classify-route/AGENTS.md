# AI Triage, Classify, and Route Inbound Issues

## Summary

**One-sentence:** Pipe every inbound bug or request through a six-step triage agent: classify type, score severity with SLA, dedupe by cosine similarity, apply /area/component/lang labels, route to CODEOWNERS team, assign least-loaded engineer.

**One-paragraph:** Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply `/area/*`, `/component/*`, `/lang/*` labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team. Severity = blocker MUST require an on-call confirmation before the SLA timer arms; everything else is auto-routed. The agent emits a single comment listing every classification it applied so the assignee can dispute any field with one reaction.

**Ефективно для:**

- High-volume tracker, де human triage стає bottleneck.
- Multi-team monorepo з CODEOWNERS as source-of-truth.
- Compliance: SLA timers + audit comment per issue.
- Load-balancing fleet of engineers — fair assignment.

## Applies If (ALL must hold)

- Issue tracker with ≥ 100 open issues and ongoing inbound volume.
- CODEOWNERS file exists and is maintained.
- Team has an on-call rotation for confirming blocker severity.

## Skip If (ANY kills it)

- Tiny project with < 20 issues — triage by hand is faster.
- No CODEOWNERS / team mapping available.
- Cultural resistance to AI-applied labels (review burden outweighs throughput gain).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CODEOWNERS file | text | repo root |
| On-call schedule API | REST endpoint | Opsgenie / PagerDuty |
| Engineer load metric source | API | internal dashboard |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage-pipeline.yaml` | YAML config for the six-step triage pipeline (classify/severity/dedupe/label/route/assign). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-ai-triage-classify-route.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-agent-fixable-triage-gate]]
- [[tracker-github-copilot-workspace]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/triage-pipeline.yaml`

```yaml
# AI triage pipeline — six fixed steps, blocker gate, single transparency comment.
# Drop into the tracker automation runner (Linear webhooks, Jira automation, GH Actions).

input:
  source: tracker.issue.created
  fields: [title, body, reporter, project]

pipeline:
  - id: classify
    model: bert-base-issue-classifier-v3
    out: type
    enum: [bug, story, epic, task, spike]

  - id: severity
    model: severity-scorer-v2
    out: severity
    enum: [blocker, critical, major, minor]
    sla_minutes:
      blocker: 30
      critical: 240
      major: 2880          # 2 days
      minor: 10080         # 7 days

  - id: dedupe
    method: cosine_similarity
    over: title + body
    window: 1000
    threshold: 0.92
    on_match:
      - close_as_duplicate
      - link_both_ways
      - STOP                # short-circuits the rest

  - id: label
    schemes:
      - /area/*
      - /component/*
      - /lang/*

  - id: route
    source: CODEOWNERS
    fallback_team: triage-default

  - id: assign
    policy: least_loaded
    measure: open_issues_in_progress

gates:
  on_severity_blocker:
    require: human_confirm
    via: ["/agent confirm-blocker", "oncall_slash_command"]
    blocks: [severity.arm_sla, assign]
    timeout: 10m
    on_timeout: keep_unconfirmed_no_paging

emit:
  one_comment:
    template: triage-table         # see content/02-transparency-comment.xml
    listen_for_reactions: [":x:"]
    on_reaction:
      revert_disputed_field: true
      requeue_step: true
      edit_in_place: true
```
