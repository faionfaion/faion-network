# Agent Integration — Requirements Lifecycle Management (BA Core)

> Sibling file lives at `pro/ba/business-analyst/requirements-lifecycle/agent-integration.md` and covers tooling, services, and operational scripts. This file focuses on the **ba-core angle**: IIBA-style formal definitions of the lifecycle, the underlying state semantics, and how to drive each canonical task with subagents.

## When to use

- The team adopts BABOK Knowledge Area 5 ("Requirements Life Cycle Management") as a working contract and needs a deterministic mapping from BABOK tasks (5.1 Trace, 5.2 Maintain, 5.3 Prioritize, 5.4 Assess Changes, 5.5 Approve) onto agent jobs.
- Onboarding a junior BA / agent that needs the formal definitions of states, attributes, and transitions before touching tools.
- Any project where audit defenders must point to "this requirement followed BABOK 5.x" — the agent must produce evidence per task, not just per ticket.
- Establishing the canonical state model and attribute set that downstream tools (Jira, StrictDoc, Polarion, the sibling `business-analyst` workflow) must conform to.
- Pairing with `requirements-traceability/`, `requirements-prioritization/`, `requirements-validation/`, and `ba-requirements-mgmt/` to compose the full KA5 picture.

## When NOT to use

- The team rejects BABOK and runs pure Scrum on the Jira workflow — apply `agile-ba-frameworks/` instead; lifecycle ceremony will be ignored.
- Pre-PMF discovery where the artifact under change is the problem, not the requirement; use `continuous-discovery/` or `opportunity-solution-trees/`.
- Single-author throwaway work where versioning is `git log`. The IIBA model is heavyweight for a one-person sprint.
- "Lifecycle" as a UI state in a Jira board — that is workflow, not the BABOK lifecycle. Don't conflate the two; agents will then write nonsense state transitions.

## Where it fails / limitations

- BABOK leaves state names to the organisation. The README's 8-state set (Draft / Proposed / Approved / Rejected / Implemented / Verified / Deferred / Deleted) is one valid mapping; teams that adopt a 5-state ISO/IEC/IEEE 29148 set will diverge. Agents must be told *which* state set is canonical.
- Validation vs. Verification confusion: BABOK defines them at distinct tasks (Validate Requirements is in KA6, Verify Requirements is also in KA6), but the README rolls them into the lifecycle. LLMs tend to merge them. Pin the definitions in the system prompt.
- The model assumes a stable baseline. In high-change environments (research, experimental products), the Approved → Implemented arrow is mostly fiction; a high churn rate makes the state log noise.
- Lifecycle does not capture rework. Verified → reopened is a real-world transition the README's diagram suppresses; agents using the diagram literally will refuse legal moves.
- IIBA-style attributes (source, owner, priority, complexity, risk, status, version) double the metadata burden. Agents that maintain only `status` will leak invariants over time.

## Agentic workflow

Treat each BABOK 5.x task as a **discrete agent job** with explicit inputs, outputs, and a state-transition contract. Agents do not "manage requirements" as a vague responsibility; they perform one task per invocation, return a structured artifact, and let a gate agent (or human) decide whether the proposed transition is permitted. The ba-core angle is that the agent is *defining and recording* the lifecycle rules — not just shuffling tickets — so the prompt always includes the definitions from the README plus the canonical state machine.

Map BABOK 5.x → agent job:

| BABOK Task | Agent Job | Input | Output |
|------------|-----------|-------|--------|
| 5.1 Trace Requirements | `ba-trace-agent` | REQ-XXX, related artifacts | Updated traceability matrix row |
| 5.2 Maintain Requirements | `ba-lifecycle-agent` | REQ-XXX (any state) | Re-usable, re-stated requirement with version bump |
| 5.3 Prioritize Requirements | `ba-prioritize-agent` | Set of requirements + criteria | Ordered list with rationale |
| 5.4 Assess Requirements Changes | `ba-change-impact-agent` | CR-XXX | Impact analysis using the README CR template |
| 5.5 Approve Requirements | gate (`faion-sdd-executor-agent` + human) | Validated requirement | State transition to Approved with sign-off record |

### Recommended subagents

- `faion-sdd-executor-agent` (this repo) — owns approval gates as SDD tasks; each Approve / Reject / Defer is a single-task commit with rationale, mapping cleanly onto BABOK 5.5.
- `password-scrubber-agent` (this repo) — must run before any requirement document containing pasted stakeholder transcripts is committed; otherwise the lifecycle log leaks secrets.
- A custom `ba-lifecycle-agent` (model: sonnet, per the README's own Agent Selection table) — owns BABOK 5.2 Maintain: re-uses, re-states, and re-versions requirements; refuses to invent state transitions outside `NEXT[current]`.
- A custom `ba-validator-agent` (model: opus) — runs INVEST / SMART / testability checks at the Proposed → Approved gate; emits a list of blocking defects rather than silently approving.
- A custom `ba-change-impact-agent` (model: opus) — owns BABOK 5.4 Assess Changes; consumes the traceability graph and produces the Impact Analysis section of the CR template.

### Prompt pattern

State-aware single-task pattern. Always pass the canonical state set, the current state, and the allowed next states.

```
You are the BA lifecycle agent for BABOK KA5 task {task_id} ("{task_name}").

Canonical state set (from requirements-lifecycle/README.md):
  Draft, Proposed, Approved, Rejected, Implemented, Verified, Deferred, Deleted.

Current state: {current_state}
Allowed next states: {next_states}
Material-change rule: bump version only when scope, AC, or NFR changes;
  wording-only edits keep the version.

Return strict JSON:
{
  "req_id": "{req_id}",
  "task": "{task_id}",
  "from_state": "{current_state}",
  "to_state": "<one of {next_states} or null if no transition>",
  "version_action": "patch|minor|major|none",
  "attributes_changed": ["status", "version", ...],
  "rationale": "<=2 sentences referencing BABOK 5.x>",
  "blocking_issues": []
}

REQUIREMENT (frontmatter + body):
---
{requirement}
---
```

For 5.4 Assess Changes prepend: `Walk the traceability matrix in
requirements-traceability/ and list every artifact (REQ, design, test) the
proposed change touches. Use the CR template from
requirements-lifecycle/templates.md verbatim.`

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log --follow` | Native version history per requirement file (replaces hand-rolled version table from the README) | preinstalled |
| `pre-commit` | Block commits whose state transitions violate `NEXT[current]` | https://pre-commit.com |
| `yq` | Read/update YAML frontmatter (`yq -i '.status = "Approved"'`) | `apt install yq` / `brew install yq` |
| `jq` | Aggregate frontmatter into the README's Status Summary table | preinstalled or `apt install jq` |
| `jsonschema` (Python) | Validate frontmatter against a BABOK-attribute schema (id, source, owner, priority, status, version, …) | `pip install jsonschema` |
| `gh issue` | Mirror REQ states into GitHub issues for non-BA stakeholders | https://cli.github.com |

## Services & apps

The sibling `business-analyst/requirements-lifecycle/agent-integration.md` covers Jama, DOORS, Polarion, Modern Requirements, Linear, Jira, Notion, Confluence, StrictDoc, Doorstop. The ba-core file does not duplicate that table; load it on demand. From the BA-fundamentals angle, the relevant signal is: **the tool must let agents read and write `status` and `version` deterministically and emit a webhook on transition.** Tools that only allow free-text status fields (e.g. plain Notion) make BABOK 5.2 / 5.5 unenforceable for agents.

## Templates & scripts

The README already provides Status Log, Change Request, and Version History templates. Inline below is a tiny attribute-schema validator that enforces the BABOK-style attribute set on every requirement file before a state transition runs.

```python
#!/usr/bin/env python3
"""req_attrs.py — enforce BABOK-style attribute set on REQ-XXX.md files."""
from __future__ import annotations
import sys, pathlib, yaml

REQUIRED = {"id", "name", "description", "status", "priority",
            "source", "owner", "version", "created", "modified", "author"}
STATES = {"Draft","Proposed","Approved","Rejected",
          "Implemented","Verified","Deferred","Deleted"}

def load(path: pathlib.Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing frontmatter")
    fm = text.split("---", 2)[1]
    return yaml.safe_load(fm) or {}

def check(path: pathlib.Path) -> list[str]:
    fm = load(path); errs: list[str] = []
    missing = REQUIRED - fm.keys()
    if missing:
        errs.append(f"{path.name}: missing attrs {sorted(missing)}")
    if fm.get("status") not in STATES:
        errs.append(f"{path.name}: bad status {fm.get('status')!r}")
    if not str(fm.get("id", "")).startswith("REQ-"):
        errs.append(f"{path.name}: id must match REQ-XXX")
    return errs

def main(root: str = "requirements") -> int:
    errs: list[str] = []
    for p in sorted(pathlib.Path(root).glob("REQ-*.md")):
        errs += check(p)
    for e in errs:
        sys.stderr.write(e + "\n")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire into `pre-commit` so any commit touching `requirements/` runs the validator before the lifecycle state-machine check from the sibling file.

## Best practices

- Pin the canonical state set in a single file (`requirements/_states.yaml`) and reference it from every prompt; do not rely on the LLM remembering the README.
- Treat the BABOK attribute set (id, name, description, status, priority, source, owner, version, created, modified, author) as a hard schema; missing attributes block the commit, not just warn.
- Bump versions per the material-change rule (scope / AC / NFR). Encode the rule as a checklist the agent must answer before incrementing.
- Keep `Validate` and `Verify` distinct in prose, headers, and prompts. The README itself contrasts them in a table — paste that table into the system prompt.
- Make the Proposed → Approved transition irreducible: one named stakeholder, one timestamp, one signature line in the requirement file. No anonymous "Approved by team".
- Time-bound `Deferred` with a `deferred_until` date; an agent re-proposes anything past due. Otherwise the backlog turns into a graveyard.
- Tie every commit that touches code to the REQ ID via Conventional Commits scope (`feat(REQ-045): …`). Traceability becomes `git log --grep REQ-045`.
- Baseline = a git tag. Comparing baselines is `git diff --stat baseline..HEAD -- requirements/`, not a ceremony.

## AI-agent gotchas

- Agents will silently invent transitions if the current state is not in the prompt. Always pass `current_state` and `allowed_next_states`; reject any output where `to_state` is outside the allowed set.
- LLMs conflate Validation (right thing) and Verification (built right). Force them to quote the README's Validation-vs-Verification table before they answer.
- Bulk transitions are dangerous. Cap any agent action at 10 requirements per run and require human sign-off on the diff before merging. A runaway "approve all" is hard to undo.
- Frontmatter parsing fails silently when stakeholders paste smart quotes, em-dashes, or non-breaking spaces into YAML. Reject non-ASCII in keys; tolerate it in values only.
- Change-impact analysis must be deterministic — drive it from `requirements-traceability` data; use the LLM only to phrase the impact, never to discover affected artifacts.
- Mandatory human-in-the-loop checkpoints (BABOK 5.5 Approve cannot be automated): Proposed → Approved (stakeholder sign-off), Approved → Implemented (PR review), Implemented → Verified (QA sign-off). The agent prepares the artifact; a human flips the state.
- When an agent revises a requirement, force it to emit a unified diff, not a full rewrite. Whole-document rewrites destroy `git blame` history and break traceability.
- At >500 requirements, do not load the full repo into context. Index frontmatter only (`yq` aggregate) and pull bodies on demand; otherwise the agent quietly truncates and loses requirements.
- Do not let agents mark anything Verified without a linked test result. Require `verified_by: TC-XXX` in the frontmatter; reject otherwise.

## References

- IIBA BABOK Guide v3, Knowledge Area 5 "Requirements Life Cycle Management" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering — https://www.iso.org/standard/72089.html
- IEEE 830-1998 (superseded but still referenced) — Recommended Practice for Software Requirements Specifications.
- BABOK KA6 Requirements Analysis & Design Definition — covers Validate (6.6) and Verify (6.5); read alongside KA5.
- Sibling methodologies in this repo: `requirements-traceability/`, `requirements-validation/`, `requirements-prioritization/`, `requirements-documentation/`, `ba-requirements-mgmt/`.
- Sibling angle for this methodology: `pro/ba/business-analyst/requirements-lifecycle/agent-integration.md` (tooling, services, operational scripts).
