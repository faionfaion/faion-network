# Agent Integration — BA Governance & Planning

## When to use
- Setting up decision rights, change control, and approval workflow for a new product/squad before requirements work starts.
- Standing up a communication plan when a project crosses 3+ stakeholder groups (sponsor, dev, ops, legal/compliance).
- Preparing elicitation logistics (interviews, workshops, document analysis) and choosing techniques per information type.
- Auditing an existing requirements process where rework, scope drift, or sign-off ambiguity has been observed.
- Drafting RACI / decision-authority matrices for a regulated build (SOX, HIPAA, GDPR) where audit trail is mandatory.

## When NOT to use
- A solo founder / single-team early MVP — formal governance burns time you do not have; use lightweight `requirements-prioritization` + `stakeholder-analysis` instead.
- Pure engineering refactors with no external stakeholders — governance overhead is waste; rely on PR review.
- Research spikes / discovery sprints where the goal is learning, not committing scope.
- Crisis incidents — switch to incident command, not governance.

## Where it fails / limitations
- Heavy templates die in fast-moving Agile teams; the matrix becomes shelfware within a sprint.
- Decision-authority tables freeze at project kickoff and silently rot when org charts change — without periodic re-validation, escalation paths point to people who left.
- "Steering committee" approval thresholds invite parking-lot politics: requirements get bundled to dodge tier limits.
- The framework is silent on async / distributed teams; assumes synchronous workshops as the default elicitation mode.
- It does not specify who owns the artifacts or where they live (Confluence vs Jira vs Git) — agents need that decided externally.

## Agentic workflow
Drive governance setup as a three-phase subagent flow: (1) a discovery subagent inventories stakeholders, decisions, and existing artifacts; (2) a drafting subagent generates the decision-authority matrix, change-control flow, and communication plan from templates; (3) a review subagent walks the draft against `stakeholder-analysis` outputs and the `requirements-lifecycle` checklist, flagging gaps. All three should write to a single `governance.md` artifact under the project's `.aidocs/` SDD tree so downstream BA work (`elicitation-techniques`, `requirements-documentation`) can link in.

### Recommended subagents
- `faion-sdd-executor-agent` — runs governance artifact creation as an SDD task with quality gates; ensures `governance.md` lands in `.aidocs/in-progress/<feature>/` with required sections.
- `password-scrubber-agent` — sweep generated communication plans before commit; stakeholder rosters often leak emails / phone numbers that should be in 1Password references, not markdown.
- A custom `ba-governance-drafter` subagent (not yet defined) is the natural future addition — narrow system prompt, reads the README + this file, outputs only the matrix + change-control + comms plan.

### Prompt pattern
```
System: You draft BA governance artifacts. Use templates from
README.md sections 1–3. Output only the three tables: decision-authority,
change-control steps, communication audience matrix. No prose.
User: Stakeholders: <list>. Decisions in scope: <list>.
Existing tools: <Jira/Confluence/Git>. Compliance: <SOX|HIPAA|none>.
```

```
System: You review a draft governance.md against BABOK KA-1 Planning.
Flag: missing escalation paths, ambiguous approval thresholds,
unstated artifact owners, channels without feedback loops.
User: <paste governance.md>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Issue/PR-based change control; gates approvals via CODEOWNERS | github.com/cli/cli |
| `jira-cli` (ankitpokhrel) | Create/move change requests, query approval queues | github.com/ankitpokhrel/jira-cli |
| `atlassian-python-api` | Programmatic Confluence page creation for governance.md publishing | pypi.org/project/atlassian-python-api |
| `acli` (Atlassian CLI) | Native Jira/Confluence ops without a Python dep | developer.atlassian.com/cloud/acli |
| `glab` | Same as `gh` for GitLab change-control gating | gitlab.com/gitlab-org/cli |
| `pandoc` | Convert governance.md → DOCX/PDF for sponsor sign-off | pandoc.org |
| `mkdocs` + `mkdocs-material` | Static-site publish of governance docs with audit-trail history | mkdocs.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira | SaaS | Yes — REST + `jira-cli` | Decision log via custom issue type "Decision"; change requests via "CR" type |
| Confluence | SaaS | Yes — REST | Live home for governance.md; supports page restrictions for sign-off scopes |
| GitHub Issues + CODEOWNERS | SaaS | Yes — `gh` | Strongest agent-driven approval gate; CODEOWNERS = decision-authority matrix |
| Notion | SaaS | Partial — REST OK, hierarchy quirky | Good for comms plans; weak audit trail for regulated work |
| Linear | SaaS | Yes — GraphQL | Lightweight; "Triage" maps to change-control intake |
| ProcessMaker / Camunda | OSS | Yes — REST | Use only when change-control flow needs branching > 4 steps |
| dbt + Metabase | OSS/SaaS | Yes | Governance KPIs: cycle time per CR, % requirements traced |
| 1Password CLI (`op`) | SaaS | Yes | Stakeholder contact data lives here, NOT in governance.md |

## Templates & scripts
See `templates.md` for governance / comms / elicitation templates (currently empty in this methodology — fill before relying on it). The README sections 1–3 carry the canonical tables. Below is a small helper that scaffolds a governance artifact from the README templates so a subagent can generate consistent output.

```bash
#!/usr/bin/env bash
# scaffold-governance.sh — emit governance.md skeleton
set -euo pipefail
PROJECT="${1:?project slug}"
OUT="${2:-.aidocs/in-progress/$PROJECT/governance.md}"
mkdir -p "$(dirname "$OUT")"
cat >"$OUT" <<EOF
# Governance — $PROJECT
_Last reviewed: $(date -I) — re-validate every 30 days._

## Decision Authority
| Decision Type | Authority | Escalation | Artifact |
|---------------|-----------|------------|----------|
| New requirement | BA Lead | PM | Jira REQ |
| Scope change | Steering | Sponsor | Jira CR |
| Priority change | PO | PM | Backlog |

## Change Control
1. Submit CR (Jira "CR" type)
2. Impact assessment (T-shirt: S/M/L/XL)
3. Review by authority above
4. Approve / Reject / Defer
5. Update baseline; link CR → REQ

## Communication
| Audience | Info | Format | Frequency | Channel |
|----------|------|--------|-----------|---------|
| Sponsor | Status, risks | Summary | Weekly | Email |
| Dev | Reqs detail | Full doc | Per sprint | Jira |
| Ops | Release plan | Checklist | Pre-release | Slack |

## Owners
- Artifact owner: <name>
- Decision-log owner: <name>
- Re-validation cadence: 30 days
EOF
echo "Wrote $OUT"
```

## Best practices
- Treat the decision-authority matrix as code: keep it in Git next to `governance.md`, review changes via PR, never edit Confluence in place.
- Re-validate the matrix on a fixed cadence (30 days). Stale escalation paths are the #1 cause of stuck CRs.
- Map every comms channel to a feedback mechanism — "email weekly digest" without a reply expectation is a write-only channel and decays in 3 weeks.
- Bind change-control thresholds to objective signals (story points, $ impact, regulatory flag), not vibes; otherwise the threshold drifts.
- Co-locate governance.md with `stakeholder-analysis.md` and `requirements-lifecycle.md` in `.aidocs/`, then cross-link — the three documents only work together.
- For elicitation prep, pre-commit the technique-selection table (README §3) per session. Agents otherwise default to "interview" for everything.
- Capture every decision (including rejections and defers) — the audit trail is the deliverable, not the matrix.

## AI-agent gotchas
- LLMs over-template: they happily emit a 6-tier steering committee for a 4-person project. Cap output by passing team size + compliance flag in the system prompt.
- Stakeholder rosters in generated markdown frequently include real PII pulled from chat history; always run `password-scrubber-agent` (or equivalent) before commit.
- Agents conflate "approval" with "review" — be explicit: an approver has veto, a reviewer comments. The matrix must enforce that wording.
- When the agent does not know who an authority is, it invents a plausible role name ("VP of Platform"). Force `<TBD>` placeholders and a human confirmation step before publishing.
- Change-control flows generated by LLMs frequently lack a "reject + reason" terminal state, leaving CRs in limbo. Validate every flow has reject + defer + approve as terminal.
- Communication plans tend to suggest Slack for everything; agents must be told the org's primary async channel or they hallucinate one.
- Human-in-the-loop checkpoints required: (1) sign-off on the authority matrix before any requirements are baselined; (2) sponsor confirmation of comms cadence; (3) post-kickoff dry-run of the CR flow with one synthetic CR.
- Do not let agents auto-close CRs even on green CI — governance integrity depends on human approval traces.

## Integration with sibling methodologies
- `stakeholder-analysis` feeds the audience matrix in §2 — never draft comms without it.
- `requirements-prioritization` consumes the priority-change authority row from §1 — keep them in sync.
- `requirements-traceability` depends on the change-control flow defining stable IDs (REQ-NNN, CR-NNN) before any baseline.
- `elicitation-techniques` is the runtime counterpart of §3 (preparation) — governance plans the session, elicitation runs it.
- `requirements-validation` reuses the approval thresholds from §1 to decide which artifacts need sponsor sign-off vs reviewer-only.

## Failure modes seen in practice
- **Matrix-vs-reality drift:** the published matrix says "Steering Committee approves scope changes," but in reality the PM emails the sponsor and ships. Symptom: audit findings during regulatory review. Fix: monthly sample of CRs vs matrix.
- **Approval-tier inflation:** every CR escalates to "XL / Steering" because impact assessment is skipped. Symptom: steering meetings with 30+ items. Fix: enforce T-shirt size with a checklist + mandatory link to impact analysis.
- **Channel sprawl:** comms plan starts with email + Jira; six weeks later there are five Slack channels, two Confluence spaces, and a shared Drive folder, none referenced in the plan. Fix: agent runs a quarterly `comms-audit` task that diffs declared channels vs actual.
- **Unowned artifacts:** governance.md exists, no one updates it. Fix: a single `Owner:` line + cron-triggered subagent that opens a "stale doc" issue at day 30.

## References
- BABOK Guide v3, Knowledge Area 1: Business Analysis Planning & Monitoring — IIBA, 2015.
- "Decision Rights: Who Decides What and Who Decides How" — Rogers & Blenko, HBR, 2006.
- BABOK Agile Extension v2 — IIBA + Agile Alliance, 2017 (lightweight governance patterns).
- GitHub CODEOWNERS docs — docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Atlassian "Decision documentation template" — atlassian.com/software/confluence/templates/decision
- Camunda BPMN governance patterns — camunda.com/bpmn/reference/
- IIBA "BA Planning Quick Tip Guide" — iiba.org (member-only).
- Spotify "Decision Records" engineering blog — engineering.atspotify.com (ADR pattern adapted for BA).
