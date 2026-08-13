# Context File Cost Budget

## Summary

**One-sentence:** Produces a Context Budget Record over an existing `AGENTS.md` / `CLAUDE.md` — every line classified as instruction, overview or preference, a ceiling enforced, overviews relocated or cut, and a five-run median measurement before any improvement is claimed.

**One-paragraph:** A project context file is the only artefact in the repository that is re-read on every single agent turn, so its cost is standing rather than one-off — and the first controlled measurement of that cost is unflattering. Human-written context files bought about four percentage points of task success for roughly a fifth more inference spend; machine-generated ones measurably *hurt*, going slightly negative on SWE-bench Lite and failing to help in five of the eight settings tested, while still charging the same 20-23% premium. The mechanism is over-compliance: agents treat every line as a hard constraint, including the lines that were only ever background, so a directory listing becomes a rule and a dependency table becomes a boundary the agent will not cross. That is why the rule this methodology enforces is narrow and unpopular — generate a short stub that a human confirms line by line, never an essay, and never let a workflow auto-generate one and accept it unread. The record makes the cut auditable: which lines survived, which were relocated to a path-scoped rule, and what the measured cost delta actually was.

**Ефективно для:**

- Any repo whose `AGENTS.md` or `CLAUDE.md` has grown past a screen and nobody remembers writing half of it.
- Monorepos with nested per-directory context files, where the tax compounds per session.
- Teams about to run a "generate context files for every module" pass — this is the methodology that says don't.
- Anyone who believes their context file helps but has never measured a run without it.

## Applies If (ALL must hold)

- A project-level agent context file exists, or one is about to be created.
- Agent sessions run against this repo often enough that per-turn cost matters.
- You can run the same task set with and without the file and compare.

## Skip If (ANY kills it)

- The file is under about 30 lines of commands and conventions — it is already the shape this produces.
- The context is task-scoped rather than standing (a bundle assembled per task) — see `context-window-curation-for-coding-agents`.
- You are authoring a context file's body from scratch and want prose guidance, not a cost audit — see `claude-md-creation-quality`, then come back here to cut it.
- Nothing runs agents against the repo; the file is documentation for humans and this cost does not apply.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 and R2 are the gate on generation; R3-R6 shape the file; R7 gates any claim about it. |
| `content/02-output-contract.xml` | The Context Budget Record: block classification, ceiling arithmetic, the measurement protocol, and what the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from who wrote the file and what is in it to keep / cut / relocate / delete. |
| `scripts/validate-context-file-cost-budget.py` | Validates a record; enforces the ceiling arithmetic, the overview ban, the human confirmation and the five-run protocol. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/context-budget-record.yaml` | Fill-in record for an audited file; ships valid against the contract. |
| `templates/context-budget-record-delete.yaml` | The delete case — an LLM-generated file nobody confirmed, which the evidence says to remove. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `agents-md-per-module-bootstrap` — nesting and closest-file-wins; this methodology bounds what each of those nested files may contain.
- `context-window-curation-for-coding-agents` — the per-task bundle, which is a different budget: task-scoped and paid once, not standing and paid per turn.
- `claude-md-creation-quality` — how to write the body; no cost evidence attached, so pair it with this.
- `ai-convention-anchoring` — where a convention belongs once it is cut from the context file: a lint rule the agent cannot ignore rather than a line it might over-comply with.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/context-budget-record.yaml`

```yaml
#
# If the file was LLM-generated and nobody confirmed its lines, do NOT edit this
# file - use context-budget-record-delete.yaml, which stops before measurement.
# Validate:  validate-context-file-cost-budget.py context-budget-record.yaml

file: "AGENTS.md"
authored_by: mixed          # human | llm | mixed
current_lines: 318
ceiling: 200                # >200 requires ceiling_justification

# --- Classification (r4, r5, r6). Every line of the file lands in exactly one block. ---
blocks:
  - lines: "1-14"
    kind: instruction
    decision: keep
    confirmed_by_human: true      # build, test and lint commands - the highest-value lines
  - lines: "15-96"
    kind: overview
    decision: cut                 # directory tree + module inventory; the agent lists these on demand
  - lines: "97-140"
    kind: overview
    decision: relocate
    relocate_to: "docs/architecture.md"   # useful to humans, not per-turn agent context
  - lines: "141-188"
    kind: instruction
    decision: keep
    confirmed_by_human: true      # commit format, branch rules, the never-do list
  - lines: "189-244"
    kind: instruction
    decision: relocate
    relocate_to: ".claude/rules/frontend.md"   # applies only under web/; scope it (r5)
  - lines: "245-286"
    kind: preference
    decision: keep
    confirmed_by_human: true
    marked_as_preference: true    # rewritten to "prefer X unless the task says otherwise"
  - lines: "287-318"
    kind: overview
    decision: cut                 # dependency table, regenerated from the lockfile anyway

kept_lines: 104                   # 14 + 48 + 42; must not exceed ceiling

# --- Measurement (r7). Five runs per arm minimum, medians, cost in currency. ---
runs: 5
cost_usd_baseline: 0.94
cost_usd_after: 1.07
cost_accepted_because: >
  13 cents per run buys a measured 5-point success gain on the same task set;
  the pre-cut file cost 1.31 USD for a smaller gain than this.
success_baseline: 0.61
success_after: 0.66
input_tokens_baseline: 41200      # diagnostic only, never the headline figure
input_tokens_after: 47600

verdict: cut
verdict_rationale: >
  318 lines to 104. The two overview blocks and the dependency table were pure
  standing cost; the frontend rules moved to a path-scoped file and now load only
  on turns that touch web/. Success moved 61% to 66% at 13 cents per run more.
```

### `templates/context-budget-record-delete.yaml`

```yaml
#
# The stop condition: authored_by llm with zero human-confirmed blocks resolves to
# delete without measurement. Do not add runs or cost fields below - spending money
# to re-derive a published result is the thing this branch exists to avoid.
# Validate:  validate-context-file-cost-budget.py context-budget-record-delete.yaml

file: "packages/ingest/AGENTS.md"
authored_by: llm
current_lines: 212
ceiling: 200

blocks:
  - lines: "1-212"
    kind: overview
    decision: cut

kept_lines: 0

verdict: delete
verdict_rationale: >
  Written by a repo-wide bootstrap pass on 2026-07-11, never read by anyone, and
  it is a module summary plus a directory tree - the derivable category. This is
  the variant the ETH/LogicStar measurement found slightly negative on task
  success while still charging the full inference premium. Deleted, not audited.
  A stub can be written by hand later if a real instruction turns up for it.
```
