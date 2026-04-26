# Architecture Decision Records

## Summary

An Architecture Decision Record (ADR) is a short document capturing one architecturally significant decision: Context (why the decision was needed), Decision (what was decided), Consequences (trade-offs accepted), and Alternatives (options rejected with reasons). ADRs are immutable once accepted — never delete or edit accepted content; create a new superseding ADR instead. Store in `docs/adr/` under version control alongside the code they affect.

## Why

Architecture decisions outlive the engineers who made them. Without written rationale, teams re-litigate the same decisions, onboard new members slowly, and make changes that violate original constraints. ADRs are also the cheapest way to satisfy "show decision rationale" controls in SOC2/ISO 27001 audits. The key discipline is writing during the decision, not after: retroactive ADRs lose their forecasting value.

## When To Use

- Any technology choice: language, framework, database, cloud provider
- Architecture style decisions: monolith vs microservices, REST vs gRPC, sync vs async
- Design pattern decisions at system scope: CQRS, Saga, Event Sourcing, API Gateway
- Third-party service selection: auth provider, payment gateway, monitoring tool
- Breaking changes: API versioning strategy, data migration approach
- Security decisions: auth mechanism, encryption standard, compliance approach
- Infrastructure decisions: container orchestration, CI/CD pipeline, deployment strategy
- Bootstrapping a new repo: ADR-0001 documents the starting architecture

## When NOT To Use

- Trivial decisions (file naming, single-developer style choices) — overhead not justified
- Reversible cheap changes (variable names, internal helpers)
- Throwaway PoCs where decisions don't outlive the demo
- Ultra-confidential decisions (M&A, vendor pricing) that cannot live in a public Git repo

## Content

| File | What's inside |
|------|---------------|
| `content/01-formats-and-lifecycle.xml` | Nygard, MADR 4.0, Y-Statement formats compared; ADR lifecycle (Draft → Proposed → Accepted/Rejected → Deprecated/Superseded); immutability principle |
| `content/02-process-and-tooling.xml` | Git workflow for ADRs; CI/CD validation; team governance (who proposes, who accepts); tools (adr-tools, log4brains, pyadr) |
| `content/03-agent-workflow.xml` | Four-pass agentic pipeline: trigger detection, alternatives generation, critic/red-team, link-back; AI-agent gotchas for fabricated data and trendy recommendations |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-nygard.md` | Minimal Nygard format: Title, Status, Context, Decision, Consequences |
| `templates/adr-madr.md` | Full MADR 4.0 format with Decision Drivers, Considered Options, Pros/Cons table |
| `templates/adr-lint.sh` | Bash script validating ADR files for required sections and legal status values |
