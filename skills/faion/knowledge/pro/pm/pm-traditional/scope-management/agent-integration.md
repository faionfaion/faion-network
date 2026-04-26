# Agent Integration — Scope Management (PMBoK)

## When to use
- Fixed-price or fixed-scope contracts where deliverables are contractual and scope creep directly damages margin.
- Regulated programs (medical, finance, government) where scope is part of compliance evidence.
- Multi-vendor programs where contracted scope per vendor must compose into one integrated deliverable.
- Strategic transformations (ERP, CRM, cloud migrations) requiring formal scope statement, WBS, and validated deliverables.
- Programs that already exhibit scope creep symptoms — repeated re-baselining, "while you're in there" requests, confused acceptance criteria.
- Pair with `work-breakdown-structure/`, `wbs-creation/`, `change-control/`, `requirements-documentation/`, `acceptance-criteria/`, `validate-scope/`.

## When NOT to use
- Pre-PMF startups iterating on hypotheses — strict scope control kills learning; use lightweight backlog management.
- Internal R&D / discovery sprints — locking scope before learning is anti-pattern.
- Pure agile teams with stable cross-functional squad and continuous discovery — backlog refinement replaces scope statements.
- One-person side projects — scope statement is overhead.
- When the actual problem is unclear requirements or absent stakeholders, fix `requirements-elicitation`/`stakeholder-engagement` first.

## Where it fails / limitations
- Scope statements written once and never refreshed become museum pieces; teams plan against the actual backlog while the statement contradicts reality.
- "Out of scope" lists protect against named exclusions but miss adjacent unspoken expectations (NFRs, interoperability, accessibility, data migration).
- Acceptance criteria written in business language fail at handoff to engineering; they need testable assertions or they breed disputes.
- LLMs given vague scope statements happily produce confident WBS hallucinations; garbage in, confidently elaborated garbage out.
- Scope baseline locked too early traps the project in obsolete decisions; balance with disciplined change control.
- Gold plating is hard to detect from documentation alone — it shows up as features in the PR that nobody asked for.
- Scope creep blame culture replaces scope control discipline; the fix is process, not finger pointing.
- Requirements traceability matrices (RTMs) require continuous maintenance; abandoned RTMs are worse than no RTM.

## Agentic workflow
Scope is encoded as a typed `scope/baseline.yaml` (objectives, deliverables with acceptance criteria, in_scope, out_of_scope, constraints, assumptions, risks) plus `scope/wbs.yaml` and `scope/rtm.yaml` (requirements traceability). Subagents enforce the baseline: a scope-guard agent reviews PRs / stories against the WBS, flagging work-not-in-WBS or WBS-items-without-implementation. A change-impact agent activates whenever a scope-affecting issue is filed, producing impact analysis for the change-control board. Acceptance criteria are stored as machine-readable Gherkin or rule lists wherever possible.

### Recommended subagents
- `faion-sdd-executor-agent` — drives scope work as SDD tasks (TASK_baseline_scope, TASK_wbs_v1, TASK_rtm_baseline, TASK_validate_deliverable_NN).
- Custom `scope-guard-agent` (sonnet) — given a PR / new ticket, validates against WBS and scope baseline; flags out-of-scope, ambiguous-scope, or unmapped-to-WBS work.
- Custom `acceptance-author-agent` (sonnet) — converts narrative deliverables to testable Gherkin acceptance criteria with explicit boundary conditions.
- Custom `rtm-updater-agent` (sonnet) — for each requirement, traces to design / build / test / acceptance evidence; outputs RTM coverage report (% covered, % verified, % gaps).
- Custom `creep-detector-agent` (sonnet) — scans recent commits, tickets, and Slack threads for emerging scope creep signals (recurring "small" additions, "while you're in there" requests).
- Custom `validation-prep-agent` (haiku) — given an upcoming sign-off, prepares evidence packet matching deliverable acceptance criteria.

### Prompt pattern
```
You are scope-guard. Inputs: PR diff / new ticket, scope-baseline.yaml, wbs.yaml.
Emit STRICT JSON:
{ "verdict": "in_scope|out_of_scope|ambiguous|gold_plating",
  "wbs_match": "<wbs_id>|none",
  "deliverable_match": "<id>|none",
  "rationale": "<= 2 sentences",
  "evidence_quotes": ["from baseline or PR"],
  "next_step": "merge|change_request|reject|clarify_with_<role>" }
Rules: do not infer scope from intent; require explicit baseline match.
gold_plating verdict requires an unrequested-feature line in the diff.
```

Acceptance criteria authoring prompt: `Convert deliverable description to Gherkin scenarios with Given/When/Then and explicit Examples table where parameterizable. Reject any criterion that is not testable.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git tag baseline-vN` | Version-control scope baseline; tag locks | preinstalled |
| `yq` / `jq` | Patch baseline.yaml, wbs.yaml, rtm.yaml | `apt install yq jq` |
| `mermaid-cli` (`mmdc`) | Render WBS tree, RTM matrix | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Render scope statement to PDF/DOCX for sign-off | https://pandoc.org |
| `behave` / `cucumber` / `pytest-bdd` | Run executable acceptance criteria | language-specific |
| `pre-commit` | Block scope edits without change-request reference / sponsor approval | https://pre-commit.com |
| `gh` / `glab` | Mirror change requests as PRs against scope/baseline.yaml | https://cli.github.com |
| `csvkit` | Slice large RTM exports | `pip install csvkit` |
| `markdownlint` | Enforce structure on scope/baseline.md | `npm i -g markdownlint-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira / Linear / Azure DevOps | SaaS | REST + JQL/GraphQL | Backlog of in-scope work; epic ↔ WBS mapping. |
| Polarion / Jama / DOORS | SaaS / on-prem | REST/OSLC | Enterprise requirements + RTM (regulated domains). |
| Notion / Confluence / SharePoint | SaaS | REST | Scope statement host; weak typing — validate on commit. |
| ProductBoard / Aha! | SaaS | REST | Product roadmap + scope intent; agents read, do not write. |
| ReqSuite / Modern Requirements | SaaS | REST | Lighter alternative to Polarion. |
| Smartsheet | SaaS | REST | Scope + WBS in single sheet for SMB. |
| GitHub Projects / GitLab Epics | SaaS | REST/GraphQL | Lightweight scope tracking for engineering-led programs. |
| Cucumber Studio / Xray BDD | SaaS | REST | Hosted Gherkin acceptance criteria + execution linkage. |
| TestRail / Zephyr | SaaS | REST | Validation evidence. |

## Templates & scripts
README provides Requirements Documentation, Scope Statement, RTM templates. Inline below: a script that audits RTM coverage from `scope/rtm.yaml`.

```python
#!/usr/bin/env python3
"""rtm_coverage.py — audit requirements traceability matrix coverage."""
import sys, yaml, pathlib

def main(path: str = "scope/rtm.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    items = data["requirements"]
    total = len(items)
    if not total:
        sys.stdout.write("No requirements.\n")
        return 0
    has_design = sum(1 for r in items if r.get("design"))
    has_build = sum(1 for r in items if r.get("build"))
    has_test = sum(1 for r in items if r.get("test"))
    has_accept = sum(1 for r in items if r.get("status") == "accepted")
    pct = lambda n: 100 * n / total
    print(f"design   {has_design}/{total} ({pct(has_design):.0f}%)")
    print(f"build    {has_build}/{total} ({pct(has_build):.0f}%)")
    print(f"test     {has_test}/{total} ({pct(has_test):.0f}%)")
    print(f"accepted {has_accept}/{total} ({pct(has_accept):.0f}%)")
    return 0 if has_design == total and has_test == total else 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

## Best practices
- Scope baseline lives in git, not a wiki; tag baseline locks (`baseline-v1`); CODEOWNERS = sponsor on `scope/`.
- Always include explicit out-of-scope list — "if it's not listed, it might be in" loses every dispute.
- Acceptance criteria are testable assertions, not narrative; convert to Gherkin or executable rules wherever possible.
- RTM coverage is a release gate: 100% of requirements must trace to design + test + acceptance evidence before sign-off.
- Constraints and assumptions are first-class — surfacing them prevents the disputes that scope statements were supposed to resolve.
- Distinguish product scope (features) from project scope (work) — confusion between the two creates phantom deliverables.
- Pair every scope change with cost + schedule re-estimate in the same change request; reject standalone scope deltas.
- Use MoSCoW prioritization on requirements (Must/Should/Could/Won't); rejecting nothing means committing to everything.
- Run a scope creep retro monthly — review accepted "small" changes and quantify cumulative drift.
- "Saying no" is a process, not an attitude; offer alternatives (next phase, separate project) and document the decision.

## AI-agent gotchas
- LLMs hallucinate scope based on plausibility; require baseline matches and reject "scope inferred from intent".
- Agents writing acceptance criteria default to vague pass/fail; force Gherkin Given/When/Then with explicit Examples tables.
- RTM updaters silently re-link evidence to wrong requirement when IDs are similar; always require unique stable IDs and exact-match linking.
- Gold plating detection is fragile via diff alone; pair with feature-flag review and product-owner sign-off.
- Auto-merging in-scope verdicts removes critical human judgment; agent emits verdict, human merges.
- Scope baselines edited mid-CR break audits; protect with branch protection and require approved CR ID in commit message.
- Stakeholder-specific scope ("just for the CFO dashboard") creates hidden scope; force enumeration in baseline.
- Agents reading legacy requirements docs accept ambiguity rather than flagging it; force the agent to emit an `ambiguity_log`.
- Long context: large RTMs (>500 reqs) blow the prompt; partition by feature area and operate on slices.
- Human-in-the-loop checkpoints (mandatory): baseline lock, baseline change, gold-plating verdicts, deliverable validation/sign-off, RTM gap closure decisions.

## References
- PMI PMBOK 7e — Planning Performance Domain (Scope).
- PMI PMBOK 6e — Project Scope Management Knowledge Area.
- IIBA BABOK v3 — Requirements Lifecycle Management knowledge area.
- ISO 21500 / 21502 — scope management guidance.
- DSDM / MoSCoW prioritization.
- Cohn, M. — "User Stories Applied" (acceptance criteria patterns).
- Adzic, G. — "Specification by Example" (executable acceptance).
- Sibling methodologies: `work-breakdown-structure/`, `wbs-creation/`, `change-control/`, `requirements-documentation/`, BA `requirements-prioritization/`, BA `acceptance-criteria/`.
