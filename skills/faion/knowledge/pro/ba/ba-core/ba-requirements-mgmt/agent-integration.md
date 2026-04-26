# Agent Integration — BA Requirements Management

Scope: ongoing maintenance of an approved requirement set, change impact
analysis (CIA) on incoming change requests, and requirements architecture
(viewpoints, hierarchy, dependencies). Distinct from `requirements-lifecycle/`
(state machine) and `requirements-traceability/` (links to design/tests).

## When to use

- Stable product past MVP where the requirement count exceeds ~50 and human
  memory of "what we agreed" no longer scales — periodic review cadence pays off.
- Change-heavy environments (enterprise integrations, regulated domains) where
  every CR must be costed and risk-assessed before approval.
- Multi-team systems where one team's requirements depend on another's; you
  need an explicit dependency graph and viewpoint partitioning to prevent
  silent conflicts.
- Audit / certification preparation (ISO 9001, SOC2, MDR) where reviewers ask
  "show me your requirements baseline and how it has changed since last audit".
- Migrating a legacy backlog into a structured architecture (BR → SR → FR
  decomposition) so AI agents can reason about scope changes.

## When NOT to use

- Pre-PMF / discovery: requirements churn faster than maintenance ceremony can
  follow; use `continuous-discovery` and disposable RFCs instead.
- Tiny teams (<5 people, single product) where Slack + a Linear backlog covers
  change discussion — formal CIA forms add bureaucracy without payoff.
- Pure agile shops with no contractual requirement baseline; the user-story
  backlog already encodes scope, and CIA = a 5-minute estimation chat.
- One-shot internal tools or research prototypes — the change cost analysis
  exceeds the change cost.

## Where it fails / limitations

- CIA is only as good as the traceability data: if `requirements-traceability/`
  is stale, the impact assessment under-counts affected artifacts.
- Effort columns ("hours") are guesses dressed as numbers — teams treat them as
  commitments. Mark them as 80% confidence intervals or T-shirt sizes.
- Viewpoint partitioning (business / user / technical / operational) overlaps
  in practice; the same requirement lives in multiple views. Pick a primary.
- Hierarchy decomposition encourages premature breakdown — BR → SR → FR trees
  with one child per parent are noise. Collapse single-child branches.
- Periodic review degenerates into rubber-stamping if no automation flags
  drifted requirements (no recent commits, no test coverage, no owner).
- "Archival strategy" is rarely implemented; teams keep everything forever
  and search degrades. Define a hard retention policy.

## Agentic workflow

Drive the three sub-disciplines as separate agent loops sharing a single
`requirements/` Markdown+YAML store. Maintenance: a scheduled agent walks
the repo weekly, flags requirements with stale `last_review`, missing owner,
or no traceability link, and opens a PR with `needs_review: true`. Change
impact: every CR opens an issue → an agent computes the impact table by
querying the traceability graph → a human approves before the CR moves to
the lifecycle's `Approved` state. Architecture: an agent renders the current
hierarchy and dependency graph (Mermaid / Graphviz) on every commit and
detects orphans (no parent), cycles, and conflicts.

### Recommended subagents

- `faion-sdd-executor-agent` — implements each Change Request as an SDD task
  with spec → design → test-plan → impl, mirroring the CIA template's
  "Effort by area" rows.
- `password-scrubber-agent` — sweeps requirement bodies before commit; CIA
  attachments often paste raw stakeholder emails.
- Custom `ba-cia-agent` (model: opus, per the README's Agent Selection table):
  generates the impact assessment table by walking trace links; does not
  decide accept/reject — produces evidence for a human gate.
- Custom `ba-arch-auditor-agent` (model: sonnet): runs nightly, validates
  the BR/SR/FR hierarchy, flags orphans/cycles, regenerates the dependency
  diagram.
- Custom `ba-maintenance-agent` (model: haiku for triage, escalate to sonnet):
  scans frontmatter for staleness signals (`last_review > 90d`, missing
  `owner`, status drift) and files PRs.

### Prompt pattern

CIA generation (deterministic walk + LLM phrasing):

```
You are the BA change-impact agent. Input: CR body + traceability JSON for
every REQ touched. Do NOT invent links; use only what is in the JSON.

Return strict JSON:
{
  "cr_id": "CR-018",
  "areas": [
    {"area": "Requirements", "items": ["REQ-045","REQ-101"], "effort_h": 6},
    {"area": "Design", "items": ["DES-12"], "effort_h": 4},
    {"area": "Code", "items": ["mod/auth"], "effort_h": 12},
    {"area": "Tests", "items": ["TC-203","TC-204"], "effort_h": 5}
  ],
  "risks": [{"risk":"...", "p":"M", "i":"H", "mitigation":"..."}],
  "stakeholder_impact": ["..."],
  "recommendation": "Accept|Reject|Defer",
  "rationale": "<=2 sentences"
}
```

Architecture audit:

```
Validate the hierarchy in requirements/ against the rules in
ba-requirements-mgmt/README.md §3. Emit a JSON report with:
orphans (no parent), cycles (dependency loop), single-child chains
(collapse candidates), conflicts (two REQs with opposing AC).
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git diff baseline..HEAD -- requirements/` | Diff current set against an approved baseline tag — the auditable record of "what changed" | preinstalled |
| `yq` | Aggregate frontmatter for periodic-review reports (`yq '.last_review' requirements/REQ-*.md`) | https://github.com/mikefarah/yq |
| `pre-commit` + custom hook | Block commits that bump a requirement without updating the change log or impact table | https://pre-commit.com |
| `mermaid-cli` (`mmdc`) | Render the requirement hierarchy + dependency graph as PNG/SVG on every CI run | https://github.com/mermaid-js/mermaid-cli |
| `graphviz` (`dot`) | Alternative renderer for large graphs; better for >100 nodes | https://graphviz.org |
| `strictdoc` | Run requirements lint + traceability checks; emits HTML report with cross-views | https://strictdoc.readthedocs.io |
| `gh issue / gh pr` | CR lifecycle: each CR is an issue, the impact table is the PR description | https://cli.github.com |
| `jq` | Stitch multiple per-REQ JSON files into a Status / Architecture summary table | preinstalled |
| `dotenv-linter` / `vale` | Style and prose linting on requirement bodies — keeps wording consistent across maintenance edits | https://vale.sh |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | REST API, webhooks | Native CIA report ("Suspect Links"); agents can read suspect set and draft impact tables. |
| IBM DOORS Next | SaaS/on-prem | OSLC API | "Change Set" workflow maps to CR; OSLC is verbose, write thin adapters. |
| Polarion ALM | SaaS/on-prem | REST + Webservices | Built-in Wiki-style requirement architecture views; agents update via REST. |
| Jira + Structure plugin | SaaS | REST v3 + Structure API | Cheapest way to express BR/SR/FR hierarchy; CIA is bespoke. |
| Linear | SaaS | GraphQL API | Use issue relations for dependencies; weak for formal architecture views. |
| StrictDoc | OSS | CLI + plain-text store | Deterministic, git-native; ideal target for agent automation. |
| Doorstop | OSS | Python API | Markdown + YAML; agents script CIA in Python directly against the API. |
| ReqView | Desktop / SaaS | JSON / ReqIF export | Useful for stakeholders who refuse markdown; agents drive via export round-trip. |
| Modern Requirements (Azure DevOps) | SaaS | ADO REST | "Smart Trace" gives CIA inputs; pair with `az boards`. |
| Helix RM | SaaS/on-prem | REST API | Strong baselining; agent ecosystem thin. |

## Templates & scripts

The README ships CIA and Architecture templates. Inline below: a script that
combines maintenance + architecture audit (orphans, cycles, staleness) on a
flat `requirements/` Markdown store.

```python
#!/usr/bin/env python3
"""req_audit.py - architecture + maintenance audit for REQ-XXX.md store."""
from __future__ import annotations
import sys, pathlib, datetime as dt, yaml, collections

STALE_DAYS = 90

def load(p: pathlib.Path) -> dict:
    text = p.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{p}: missing frontmatter")
    fm, _ = text.split("---", 2)[1:]
    d = yaml.safe_load(fm) or {}
    d["_path"] = p
    return d

def audit(root: str = "requirements") -> int:
    reqs = {r["id"]: r for r in (load(p) for p in pathlib.Path(root).glob("REQ-*.md"))}
    today = dt.date.today()
    orphans, stale, no_owner, cycles = [], [], [], []
    # orphans: parent missing
    for rid, r in reqs.items():
        parent = r.get("parent")
        if parent and parent not in reqs:
            orphans.append(f"{rid} -> missing parent {parent}")
        if not r.get("owner"):
            no_owner.append(rid)
        lr = r.get("last_review")
        if isinstance(lr, dt.date) and (today - lr).days > STALE_DAYS:
            stale.append(f"{rid} (last_review {lr})")
    # cycle detection on `depends_on`
    visiting, visited = set(), set()
    def dfs(node: str, path: list[str]) -> None:
        if node in visiting:
            cycles.append(" -> ".join(path + [node])); return
        if node in visited or node not in reqs: return
        visiting.add(node)
        for dep in reqs[node].get("depends_on") or []:
            dfs(dep, path + [node])
        visiting.discard(node); visited.add(node)
    for rid in reqs: dfs(rid, [])
    rc = 0
    for label, items in [("ORPHANS", orphans), ("STALE", stale),
                         ("NO_OWNER", no_owner), ("CYCLES", cycles)]:
        if items:
            rc = 1; print(f"\n{label}:"); print("\n".join(f"  {i}" for i in items))
    if rc == 0: print("OK: no findings")
    return rc

if __name__ == "__main__":
    sys.exit(audit(*sys.argv[1:]))
```

Wire it into CI; on `main`, post the report as a GitHub comment on a rolling
"BA Health" issue.

## Best practices

- Anchor every periodic review to a baseline tag (`req-baseline-2026-Q2`). The
  question "what changed since last review" must be answerable with one
  `git diff`, not a meeting.
- Make CIA mandatory for any CR touching ≥2 requirements; under that, allow a
  one-line note. The threshold prevents form fatigue.
- Capture effort in T-shirt sizes (S/M/L/XL) by area, not in hours. Convert to
  hours only at planning time. Stops false precision.
- Treat the dependency graph as code: store it in a `.mmd` file generated
  from frontmatter, never hand-drawn. Diff is then meaningful.
- Single primary viewpoint per requirement (`view: business | user | tech | ops`)
  plus optional secondary views as labels. Avoids duplication across views.
- Set a hard cap on hierarchy depth (e.g., 3 levels: BR → SR → FR). Anything
  deeper is task decomposition and belongs in the implementation plan.
- Archive on tag, not delete: a quarterly tag `req-archive-2026-Q2` snapshots
  retired REQs; remove from `requirements/` so daily search stays fast.
- Owner field is mandatory and personal (not a team). Empty owner = the
  requirement is dead.

## AI-agent gotchas

- LLMs hallucinate impacted artifacts when the trace data is incomplete; the
  CIA agent must REFUSE to produce numbers if `traceability.json` is empty
  for a given REQ — return `"effort": null, "reason": "no trace data"`.
- "Effort_h" hallucination: agents pick suspiciously round numbers (4, 8, 16).
  Force a calibration prompt: pass historical CR effort data and require the
  agent to anchor its estimate to a similar past CR by ID.
- Architecture agents will invent parents to "fix" orphans. Forbid creation of
  hierarchy nodes; only flag and let a human decide.
- Periodic review agents will mass-mark `last_review = today` to clear the
  staleness flag without actual review. Require a human signature (commit
  author = stakeholder, not the bot) for the field to count.
- Dependency cycle detection must run server-side; LLMs miss long cycles. Use
  the script above, then ask the LLM only to phrase the remediation.
- Bulk archival is destructive — cap any archive run to N requirements per PR
  with mandatory human review on the diff.
- Token budget: never load the full requirement bodies for an architecture
  audit. Aggregate frontmatter only (`yq -o=json`) and load a body on demand.
- Human-in-the-loop checkpoints (mandatory): CR Accept/Reject/Defer decision,
  Archival, Hierarchy restructure, Conflict resolution between requirements.

## References

- IIBA BABOK Guide v3, ch. 5.5 "Maintain Requirements" and 5.4 "Assess
  Requirements Changes" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 §6.5 "Requirements management process" —
  https://www.iso.org/standard/72089.html
- INCOSE Systems Engineering Handbook v5, ch. 4.4 "Requirements Definition
  and Management" — https://www.incose.org/products-and-publications/se-handbook
- StrictDoc requirements-as-code — https://strictdoc.readthedocs.io
- Doorstop git-native RM — https://doorstop.readthedocs.io
- Sibling methodologies in this repo: `requirements-lifecycle/`,
  `requirements-traceability/`, `requirements-prioritization/`,
  `requirements-validation/`, `requirements-documentation/`.
