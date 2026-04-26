# Agent Integration — Requirements Lifecycle Management

## When to use

- Multi-sprint product where requirements are written once, then evolve over months and need an audit trail (state, version, owner) per requirement.
- Regulated context (medical, fintech, gov) where you must demonstrate that every shipped feature traces back to an approved, versioned requirement.
- Cross-team handover: BA writes, dev implements, QA verifies — each role mutates state on the same artifact and needs a single source of truth.
- Migrating an unmanaged backlog (Notion / Google Docs / email) into a structured `REQ-XXX` repository with explicit states.
- Pairing with `requirements-traceability/` and `requirements-validation/` to close the Identify → Verify loop.

## When NOT to use

- Solo founder pre-PMF: lifecycle ceremony slows discovery; use opportunity-solution-trees and `continuous-discovery` instead.
- Pure agile teams that treat the user story backlog as the spec — story state in Jira/Linear already covers Draft → Done.
- One-off internal scripts or throwaway prototypes — the overhead exceeds the value.
- When stakeholders refuse to sign off in writing; without an Approved gate the model degenerates into a status spreadsheet.

## Where it fails / limitations

- States drift from reality when no automation enforces transitions — the log becomes fiction (mistake #4 in README).
- Two systems of record: tickets in Jira/Linear plus REQ-XXX docs creates double-bookkeeping; pick one canonical store and mirror.
- Version explosion: every wording tweak bumping a version produces noise. Define a "material change" threshold (scope, AC, NFR) before incrementing.
- Lifecycle assumes linear flow; reality has rework loops (Verified → reopened) the README's state diagram does not show.
- LLMs hallucinate state transitions if the current state is not passed in context — they will mark something Approved that is still Proposed.

## Agentic workflow

Treat the requirements repository as a flat directory of Markdown files (`requirements/REQ-XXX.md`) with YAML frontmatter holding state, version, owner, and timestamps. Subagents read the frontmatter, propose a transition, and emit a structured patch (diff or JSON) — never write the file directly without a human or gate agent reviewing. The lifecycle becomes a state machine implemented as a Makefile / script: `make req-propose ID=045`, `make req-approve ID=045`, each invoking a Claude subagent with the relevant prompt template.

### Recommended subagents

- `faion-sdd-executor-agent` — drives the lifecycle as SDD tasks; each transition (Propose → Approve, Approve → Implemented) is a TASK with its own commit and execution report. Maps cleanly to the existing `.aidocs/` flow.
- `password-scrubber-agent` — runs over requirement docs before they are committed to public repos, catching leaked secrets in pasted stakeholder transcripts.
- A custom `ba-lifecycle-agent` (model: sonnet, per `Agent Selection` table in README): owns Identify → Specify, including categorization, conflict detection, ID assignment.
- A custom `ba-validator-agent` (model: opus): owns the Validate gate — runs INVEST / SMART / testability checks and either approves or returns a list of defects to fix.
- A custom `ba-change-impact-agent` (model: opus): produces the impact-analysis section of every CR by walking the traceability graph.

### Prompt pattern

Two-shot pattern: state read → transition proposal.

```
You are the BA lifecycle agent. The requirement below is in state {current_state}.
Allowed next states: {next_states}. Apply the transition rules from
requirements-lifecycle/README.md.

Return strict JSON:
{ "req_id": "REQ-045", "from": "Proposed", "to": "Approved" | "Rejected" | "Deferred",
  "version_bump": "patch|minor|major|none", "rationale": "<=2 sentences",
  "blocking_issues": [] }

REQUIREMENT:
---
{frontmatter + body}
---
```

For change requests, prefix with: `Walk the traceability matrix in
requirements-traceability/ and list every artifact (REQ, design doc, test case)
the proposed change touches. Produce CR-XXX in the template from
requirements-lifecycle/templates.md.`

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log --follow` | Native version history per requirement file (replaces hand-rolled version table) | preinstalled |
| `pre-commit` + custom hook | Block commits where a requirement transitions to a state that violates the rules in README | https://pre-commit.com |
| `yq` | Read/update YAML frontmatter (`yq -i '.status = "Approved"'`) in pipelines | `brew install yq` / `apt install yq` |
| `gh issue` / `gh pr` | Mirror REQ states into GitHub issues so non-BA stakeholders see them in their tool | https://cli.github.com |
| `reqif-tools` (open-source) | Import/export ReqIF for round-tripping with Polarion / DOORS / Jama | https://github.com/strictdoc-project/reqif |
| `strictdoc` | OSS requirements management tool with a CLI; can render HTML and check traceability | https://strictdoc.readthedocs.io |
| `fossil` | Single-file SCM with built-in tickets — viable for very small teams as a self-contained REQ store | https://fossil-scm.org |
| `jq` | Aggregate REQ frontmatter into the Status Summary table from the README template | `apt install jq` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | REST API + webhooks | Heavy enterprise; agents can read items, change state, attach approvals. OAuth. |
| IBM DOORS Next | SaaS/on-prem | OSLC API | Standards-grade traceability; OSLC is verbose, plan for adapters. |
| Polarion ALM | SaaS/on-prem | REST + Webservices | Strong workflow engine; map states to Polarion `status` field. |
| Modern Requirements (for Azure DevOps) | SaaS | ADO REST API | Lifecycle on top of work items; agents drive via `az boards work-item update`. |
| Helix RM (Perforce) | SaaS/on-prem | REST API | Legacy but solid traceability; weaker LLM ecosystem. |
| StrictDoc | OSS | CLI + plain-text store | Best fit for agent workflows: text-first, git-native, deterministic. |
| Doorstop | OSS | Python API | Markdown + YAML, git-native, scriptable from agents. |
| Linear | SaaS | GraphQL API | Treat each REQ as an issue with a custom `lifecycle_state`; agents transition via `issueUpdate`. |
| Jira (Cloud) | SaaS | REST v3 + JQL | Workflow editor maps 1:1 to lifecycle states. Watch rate limits in batch updates. |
| Notion | SaaS | REST API | OK for small teams; weak typing on state fields, easy to corrupt with agents. |
| Confluence + Requirements blueprint | SaaS | REST API | Free-text drift is high; pair with a state plugin. |

## Templates & scripts

The README already provides Status Log, CR, and Version History templates. Inline below is a Python script that scans a `requirements/` dir, validates lifecycle invariants, and prints the Status Summary.

```python
#!/usr/bin/env python3
"""req_status.py — validate REQ lifecycle and emit Status Summary."""
from __future__ import annotations
import sys, pathlib, collections, yaml

ALLOWED = {"Draft","Proposed","Approved","Rejected","Implemented","Verified","Deferred","Deleted"}
NEXT = {
    "Draft": {"Proposed","Deleted"},
    "Proposed": {"Approved","Rejected","Deferred","Deleted"},
    "Approved": {"Implemented","Deferred","Deleted"},
    "Rejected": {"Proposed","Deleted"},
    "Implemented": {"Verified","Deferred"},
    "Verified": {"Deferred","Deleted"},
    "Deferred": {"Proposed","Deleted"},
    "Deleted": set(),
}

def load(path: pathlib.Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing frontmatter")
    fm, _ = text.split("---", 2)[1:]
    return yaml.safe_load(fm)

def main(root: str = "requirements") -> int:
    counts = collections.Counter()
    errors: list[str] = []
    for p in sorted(pathlib.Path(root).glob("REQ-*.md")):
        fm = load(p)
        st = fm.get("status")
        if st not in ALLOWED:
            errors.append(f"{p.name}: bad status {st!r}")
            continue
        prev = fm.get("previous_status")
        if prev and st not in NEXT.get(prev, set()):
            errors.append(f"{p.name}: illegal {prev}->{st}")
        counts[st] += 1
    total = sum(counts.values()) or 1
    print(f"{'Status':<12} {'Count':>5} {'%':>5}")
    for s in ALLOWED:
        c = counts[s]; print(f"{s:<12} {c:>5} {100*c/total:>4.0f}%")
    if errors:
        print("\nERRORS:"); print("\n".join(errors)); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire it into `pre-commit` so any commit touching `requirements/` runs the validator.

## Best practices

- Store requirements as Markdown + YAML frontmatter in git, not in a database — diffs become the version history, `git blame` shows the author, branches model proposed states for free.
- One state field, no parallel statuses. If you need workflow phase + lifecycle state, encode the secondary one as a label, not as a duplicate state machine.
- Make the Approved gate a pull-request approval from a named stakeholder (CODEOWNERS for `requirements/`). Replays the Approval table from the CR template via GitHub's UI.
- Bump versions only on material change: scope shift, new acceptance criterion, NFR change. Wording fixes stay in the same version.
- Tie every commit to a REQ ID using a Conventional Commits scope: `feat(REQ-045): password reset flow`. The traceability link is then queryable with `git log --grep`.
- Keep `Deferred` time-bounded — every Deferred requirement carries a `deferred_until` date; an agent runs weekly and re-proposes anything past due.
- Baseline = a git tag (`req-baseline-2026-Q2`). Compare current vs. baseline with `git diff --stat baseline..HEAD -- requirements/`.

## AI-agent gotchas

- Agents will silently invent transitions. Always pass the current state in the prompt and validate the proposed transition against `NEXT` (above) before persisting.
- LLMs conflate Validation and Verification — explicitly remind them in the system prompt with the table from the README; otherwise they will mark something Verified before any test ran.
- Bulk re-statusing is dangerous. Cap any agent action to N requirements per run (e.g. 10) and require human review on the diff. A runaway agent that flips 200 REQs to Approved is hard to undo.
- Frontmatter parsing fails silently if a stakeholder pastes Smart Quotes into YAML. Add a `pre-commit` hook to reject non-ASCII in keys.
- Change Request impact analysis must be deterministic — drive it from `requirements-traceability` data, not from LLM recall. Use the LLM only to phrase the impact, not to discover it.
- Human-in-the-loop checkpoints (mandatory): Proposed → Approved (sign-off), Approved → Implemented (PR review), Implemented → Verified (QA). The agent prepares the artifact; a human flips the state.
- When the agent revises a requirement, force it to emit the diff, not the full new text — easier to review and avoids whole-document rewrites that lose history.
- Token budget: at >500 REQs do not load the whole repo into context. Index frontmatter only (`yq` aggregate) and load full bodies on demand.

## References

- IIBA BABOK Guide v3, ch. 5 "Requirements Life Cycle Management" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 Requirements Engineering — https://www.iso.org/standard/72089.html
- StrictDoc requirements-as-code toolkit — https://strictdoc.readthedocs.io
- Doorstop (git-native RM) — https://doorstop.readthedocs.io
- ReqIF interchange format — https://www.omg.org/spec/ReqIF/
- Sibling methodologies in this repo: `requirements-traceability/`, `requirements-validation/`, `requirements-prioritization/`, `requirements-documentation/`.
