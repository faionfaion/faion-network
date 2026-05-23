# purpose: Architect PR review report template, six sections + verdict.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a architect-pr-review-checklist artefact validating against scripts/validate-architect-pr-review-checklist.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: architect-pr-review-checklist-<repo>-<pr-num>
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
pr_url: <URL>
verdict: <ship|block|escalate>
---

## 1. Contract
- public API shape changes documented? <yes|no>
- backward compatibility preserved? <yes|no>

## 2. Dependency direction
- module boundary respected (inner -> outer only)? <yes|no>
- forbidden cross-imports introduced? <yes|no>

## 3. Error model
- error types named and documented? <yes|no>
- swallowed exceptions / silent recovery present? <yes|no>

## 4. Observability
- structured logs at module boundaries? <yes|no>
- metrics + traces aligned with module ownership? <yes|no>

## 5. Security
- secret / PII echo risk? <yes|no>
- authn/authz delta documented? <yes|no>

## 6. ADR conformance
- relevant ADRs respected? <yes|no>
- new architectural decision documented? <yes|no>

## Verdict
<one paragraph>

## Time spent
<minutes>; if > 15, see escalation rule.
