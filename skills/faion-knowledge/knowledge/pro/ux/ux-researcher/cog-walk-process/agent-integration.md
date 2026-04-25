# Agent Integration — Cognitive Walkthrough: Process

## When to use
- Running a structured, multi-evaluator cognitive walkthrough where outputs (planning sheet, per-step forms, summary report) must be produced consistently.
- CI-integrated walkthroughs: every preview deploy of a critical flow (signup, checkout, onboarding) gets an automated walk and the report attached to the PR.
- Cross-evaluator aggregation: two human evaluators + one agent each fill the form; a reconciler agent merges results.
- Re-evaluation after fixes — agent re-runs the full process artifact-by-artifact and produces a delta report.

## When NOT to use
- Ad-hoc one-screen reviews — use cog-walk-basics, not the full process. Process overhead isn't worth it.
- When task sequence is not yet stable (changing daily). Lock the action sequence first, then walk.
- Studies where stakeholders need real user voice — process produces inspection findings, not user evidence.
- Multi-app journeys spanning systems the agent can't render (native installer + email + browser) without orchestration.

## Where it fails / limitations
- Step boundaries are fuzzy: "Click X then enter Y" is one step or two depending on the form. Inconsistent boundaries make per-step counts meaningless.
- Severity ranking is the weakest link — agents and humans disagree most here. Without a calibration pass, the report's prioritization is noise.
- The "correct action sequence" assumes one happy path; real users branch. Walkthrough doesn't surface alternative-path issues.
- Evaluator fatigue is real for humans, invisible for agents — but agents introduce different fatigue (context window drift, theme contamination across steps).
- Reports become verbose; stakeholders skim. Force a one-page exec summary rule into the synthesizer.

## Agentic workflow
Treat the process as a small SDD pipeline. Step 1: a `planner` agent fills the Walkthrough Planning Template from a PRD or feature spec. Step 2: a screen-capture script (Playwright) produces one screenshot per step with metadata. Step 3: a stateless `evaluator` agent fills the Evaluation Form per step. Step 4: a `reporter` agent merges all forms into the Summary Report Template and prioritizes. Step 5: file each High/Medium issue as a tracked ticket. Human-in-loop checkpoints: after Step 1 (persona/sequence sanity check) and after Step 4 (severity calibration).

### Recommended subagents
- `walk-planner` — converts spec → Walkthrough Planning Template (persona, task, action sequence, scope).
- `walk-evaluator` — per-step Q1-Q4 evaluator with vision; same as cog-walk-basics evaluator but bound to the locked step sequence.
- `walk-reporter` — aggregates evaluation JSON into the Summary Report Template; produces issue table with severity.
- `walk-reconciler` — merges N independent evaluators (humans + agents); marks consensus vs disputed findings.
- `faion-sdd-executor-agent` — wraps the whole pipeline as an SDD task with the report as the deliverable.

### Prompt pattern
Planner:
```
Input: feature spec at <path>, target persona <persona.md>.
Produce: filled Walkthrough Planning Template (markdown).
Action sequence MUST be the minimum-clicks happy path. Number each step.
Out of scope: any branch, error path, or expert shortcut.
```

Reporter:
```
Inputs: <step_*.eval.json> files, planning template.
Produce: filled Summary Report Template.
Rules: at most 3 High issues. Every issue cites step number + Q1/Q2/Q3/Q4 + one-line fix.
Positive findings section: list at least 3 things that worked (anti-fixation).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Capture per-step screenshots + post-action screen for Q4 | `npm i -D @playwright/test` |
| `figma-export` / Figma REST | Pull prototype frames as images per step | https://www.figma.com/developers/api |
| `jq` | Query / merge per-step eval JSON | system pkg |
| `pandoc` | Render report to PDF/HTML for stakeholders | system pkg |
| `gh issue create --label "cog-walk"` | File issues from High/Med findings | gh CLI |
| `mermaid-cli` | Render task-flow diagram from action sequence | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Figma | SaaS | Yes — REST + Variables API | Best source of step-by-step frames for prototype walks. |
| Storybook | OSS | Yes — static HTML | Component-level walks; one component = one step set. |
| Maze | SaaS | Partial | Run human follow-up tests on flows agent flagged. |
| Linear / Jira / GitHub Issues | SaaS | Yes — APIs/CLI | Sink for prioritized findings. |
| Notion / Confluence | SaaS | Yes — APIs | Long-term home for report; agent posts via API. |
| Loom | SaaS | No — recordings | Use for sharing report walkthrough with stakeholders, not agent input. |

## Templates & scripts
See `templates.md` for Planning, Evaluation, and Summary Report templates. Minimal pipeline driver:

```bash
#!/usr/bin/env bash
# run-cog-walk.sh — orchestrate planner → captures → evaluators → report
set -euo pipefail
SPEC="${1:?spec.md required}"
PERSONA="${2:?persona.md required}"
OUT=cog-walk-$(date +%Y%m%d-%H%M)
mkdir -p "$OUT"

claude -p "Run walk-planner on $SPEC with persona $PERSONA" > "$OUT/plan.md"
node capture.js "$OUT/plan.md" "$OUT/shots/"           # Playwright per step

for s in "$OUT"/shots/step_*.json; do
  claude -p "Run walk-evaluator on $s" > "${s%.json}.eval.json"
done

claude -p "Run walk-reporter on $OUT/shots/*.eval.json + $OUT/plan.md" > "$OUT/report.md"
echo "Report: $OUT/report.md"
```

## Best practices
- Lock the action sequence before any evaluation runs. Mid-walk changes invalidate per-step JSON.
- Use 2-4 evaluators (mix of agent + human). Single-evaluator walks miss ~40% of issues per Nielsen heuristics literature; the same applies here.
- Make agent evaluators independent: do not feed earlier step evaluations into later ones, or theme contamination explodes.
- Every "No" must include a concrete fix in the same JSON output. Reports without fixes don't drive change.
- Keep the report's executive summary to ≤5 bullets; force the agent into a token budget.
- Track re-evaluation deltas (resolved / new / regressed) per release; this is the only metric that proves the walk is paying off.
- Tag each finding with the affected screen + component name so devs can map issues to code.

## AI-agent gotchas
- Action-sequence drift: agents like to "improve" the sequence mid-walk. Pin it as immutable input.
- Severity calibration is biased: agents over-mark Medium. Constrain to a fixed distribution (e.g., max 20% High, 50% Medium, 30% Low).
- Q4 (progress) requires the post-action screen. Capture both before+after; static-only walks systematically miss missing-feedback issues.
- Prototypes with broken interactions cause Q4 false positives. Mark "interaction limitation, ignored" explicitly in eval JSON.
- When reconciling humans + agent, agent confidence sounds higher than humans'; weight human-only findings by 1.5x in tie-break.
- Exec summary contamination: if the planner agent saw a hypothesis ("we think users get stuck on step 3"), the reporter will confirm it. Strip hypotheses from planner prompt.
- Tickets filed by agent should be labeled `auto-cog-walk` and reviewed in batch — do not auto-assign engineers.

## References
- Nielsen Norman Group — Cognitive Walkthrough Workshop
- usability.gov — How to Run a Cognitive Walkthrough
- Wharton, Rieman, Lewis, Polson — The Cognitive Walkthrough Method: A Practitioner's Guide
- Interaction Design Foundation — How to Conduct a Cognitive Walkthrough
- Spencer — The Streamlined Cognitive Walkthrough Method
