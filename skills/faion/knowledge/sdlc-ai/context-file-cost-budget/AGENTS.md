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

## Related

- `agents-md-per-module-bootstrap` — nesting and closest-file-wins; this methodology bounds what each of those nested files may contain.
- `context-window-curation-for-coding-agents` — the per-task bundle, which is a different budget: task-scoped and paid once, not standing and paid per turn.
- `claude-md-creation-quality` — how to write the body; no cost evidence attached, so pair it with this.
- `ai-convention-anchoring` — where a convention belongs once it is cut from the context file: a lint rule the agent cannot ignore rather than a line it might over-comply with.
