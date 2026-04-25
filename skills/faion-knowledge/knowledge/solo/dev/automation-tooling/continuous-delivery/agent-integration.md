# Agent Integration — Continuous Delivery (Index)

## When to use
- Routing — a user asks about CD without specifying basics vs pipelines vs strategies. This file's "When to Read What" table is the dispatch.
- Producing an executive summary of CD for a stakeholder doc; the Quick Reference here is the right grain.
- Cross-linking from other knowledge bases (trunk-based-dev, feature-flags, tdd-workflow) into a single CD landing page.

## When NOT to use
- For implementation. All actionable detail lives in `cd-basics/` (principles, prerequisites, roadmap) and `cd-pipelines/` (YAML, deployment strategies, monitoring).
- For Continuous Deployment (auto-prod-deploy) deep dives — the matrix here flags the difference but does not cover the safety net (canary analysis, SLO gating) needed for full auto-deploy.
- For team-process change-management — Accelerate / DevOps Handbook are referenced; this file does not unpack them.

## Where it fails / limitations
- Pure index file (~90 lines). Agents that read only this file will produce vague advice; they must fan out to the children.
- "DORA elite performance" targets are stated as bullets without measurement guidance — see `cd-basics/` for that, and `pro/infra/cicd-engineer/dora-metrics/` for instrumentation.
- "Related" links assume sibling files exist; in this knowledge base `tdd-workflow.md` lives elsewhere — agents may need to resolve cross-tier paths.
- The CD vs CD matrix conflates "auto-deploy prod" (Continuous Deployment) with operational rigor; teams reach Continuous Deployment via stronger telemetry, not just by flipping a switch.

## Agentic workflow
Treat this file as a router. The agent reads the user's question, consults the "When to Read What" table, then opens exactly one child file and produces output from that. For broad audits (CD readiness across N services), the agent should batch: open `cd-basics/` once, score each service, then drop into `cd-pipelines/` only for services that need pipeline work.

### Recommended subagents
- `general-purpose` — routing decisions and producing summaries.
- `faion-sdd-executor-agent` — when CD adoption is a multi-feature initiative.
- A narrow `cd-router` task agent — input: user question; output: one of {cd-basics, cd-pipelines, feature-flags, trunk-based-dev-*}; nothing else.

### Prompt pattern
```
The user asked: "<question>". Use the table in
solo/dev/automation-tooling/continuous-delivery/README.md to pick ONE
sibling file. Read only that file, then answer. Do not synthesize from this
index alone.
```
```
Produce a one-page CD primer for a non-engineering stakeholder using only
the Quick Reference + CD vs CI vs Continuous Deployment matrix from this
file. No code. End with three concrete asks (budget/time/access) needed to
adopt CD.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` / `glab` | Inspect deploy events, environments, approvals | github / gitlab CLI |
| `dora-team/fourkeys` | Compute DORA metrics across services | github.com/dora-team/fourkeys |
| `cd-cli` (homegrown) | Wrap children's tooling under one entrypoint | n/a |

(Index-level tooling is intentionally minimal. See `cd-basics/agent-integration.md` and `cd-pipelines/agent-integration.md` for the real tool catalogue.)

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sleuth.io / LinearB | SaaS | Yes | DORA dashboards across services — useful at the index level for executive views. |
| GitHub Environments / GitLab Environments | SaaS | Yes | Approval gates as the CD-vs-CDeployment fulcrum. |

(Full service catalogues live in the children.)

## Templates & scripts
See `cd-basics/agent-integration.md` (CD-readiness scorecard) and `cd-pipelines/agent-integration.md` (pipeline + rollback wrapper). This index intentionally has no scripts of its own.

## Best practices
- Always answer from the most specific file: `cd-pipelines` for YAML, `cd-basics` for principles, `feature-flags` for release control, `trunk-based-dev-*` for branching. The index is for routing only.
- Use the CD vs CI vs CDeployment matrix verbatim when explaining the distinction; teams confuse them constantly.
- Pair "DORA elite" claims with measurement instructions, not aspirational targets — agents that quote the elite numbers without instrumentation create false expectations.
- When linking to "Continuous Deployment," note the additional safety bar: automated canary analysis, SLO-based rollout gates, real-time monitoring tied to deploy events.

## AI-agent gotchas
- Agents try to answer implementation questions from this index alone and produce hand-wavy bullets. Force a child-file read.
- Quoting the matrix while skipping prerequisites in `cd-basics` leads teams to "adopt CD" without CI or test coverage in place.
- "Continuous Deployment" prompts trigger agents to enable auto-deploy on services that lack canary analysis or rollback. Block auto-deploy until the prerequisites in `cd-basics` are checked off.
- Cross-link rot: agents follow `tdd-workflow.md` to a non-existent neighbor. Validate paths before writing the response.

## References
- Jez Humble & David Farley, Continuous Delivery (Pearson, 2010).
- Nicole Forsgren et al., Accelerate (IT Revolution, 2018).
- Gene Kim et al., The DevOps Handbook (IT Revolution).
- DORA: https://www.devops-research.com/research.html
- Martin Fowler, Continuous Delivery: https://martinfowler.com/bliki/ContinuousDelivery.html
- Children: `solo/dev/automation-tooling/cd-basics/`, `cd-pipelines/`.
- Related: `solo/dev/automation-tooling/feature-flags/`, `trunk-based-dev-principles/`, `trunk-based-dev-patterns/`.
