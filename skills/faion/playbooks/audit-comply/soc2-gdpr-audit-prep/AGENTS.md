# SOC2 / GDPR audit prep (annual)

**Playbook slug:** `soc2-gdpr-audit-prep`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Approaching audit window → control evidence current, gaps closed, walkthrough rehearsed, every exception logged with owner + date.

## Scope

Annual SOC2 / GDPR audit deadline approaches. The team brings each required control to current state: every artifact is tagged in the repo, every secret has a verified custodian, the supply chain is provably scanned, and the auditor walkthrough is scripted and rehearsed. Exceptions are logged with remediation owners and dates. Output is an audit binder ready to ship.

### What this playbook covers

Four stages mapped to the auditor's typical question pattern: *(1) what's in scope, (2) is it secure, (3) is it governed, (4) can you walk me through it*. The chain leans on `pro/ba/strategy-analysis-*` to formalise the current-state inventory and on `geek/sdlc-ai/sec-*` and `gov-*` methodologies to convert engineering practice into auditor-readable evidence. Exception ledger format is non-negotiable: every open item carries an owner and a remediation date.

### Non-goals

- Choosing the auditor / commercial procurement — handled by Legal/Finance
- EU AI Act / sector-specific compliance beyond SOC2 + GDPR — covered separately
- Initial certification — assumes recurring-audit cadence; first-time audits add scope

### Prerequisites

- Last year's audit report + remediation list
- List of in-scope systems documented
- Approval-token signed-JWT in place for privileged operations
- Renovate/Trivy + SBOM tooling wired

## Success criteria

The playbook is done when:
- Control-to-artifact map exists and resolves for every control
- Secrets inventory current with named custodian per secret
- Supply-chain scan green within last 30 days
- Walkthrough rehearsal completed end-to-end
- Open exceptions logged with owner + remediation date
- Vendor risk assessment current for all in-scope vendors

## Stages

### Stage 1: Inventory + gap analysis

**Intent:** Map controls to repo artifacts; find gaps.

**Methodologies in chain:**
- `strategy-analysis-current-state` → `ba/strategy-analysis-current-state`
- `strategy-analysis-gap-analysis` → `ba/strategy-analysis-gap-analysis`
- `data-analysis` → `ba/data-analysis`
- `interface-analysis` → `ba/interface-analysis`
- `process-mining-automation` → `ba/process-mining-automation`
- `stakeholder-register-pm-traditional` → `pm/stakeholder-register-pm-traditional`

**Decision gate:**
> Advance when every control has either a green status or a documented gap with owner.

### Stage 2: Close gaps + supply chain

**Intent:** Trivy / CodeQL / container / IaC scans + license compliance run + remediated.

**Methodologies in chain:**
- `sec-trivy-pinned-supply-chain-scan` → `sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `sec-secrets-defense-in-depth` → `sdlc-ai/sec-secrets-defense-in-depth`
- `gov-license-compliance-scan` → `sdlc-ai/gov-license-compliance-scan`
- `secrets-management` → `infra/secrets-management`
- `security-container-scanning` → `infra/security-container-scanning`
- `security-supply-chain` → `infra/security-supply-chain`
- `security-policy-as-code` → `infra/security-policy-as-code`
- `backup-verification-dr` → `infra/backup-verification-dr`

**Decision gate:**
> Advance when scan output is green within 30 days and all P0 supply-chain risks have remediation owners.

### Stage 3: Process + governance evidence

**Intent:** Approval-token JWT + conventional-commits + AI code gate trail = auditable engineering controls.

**Methodologies in chain:**
- `gov-approval-token-signed-jwt` → `sdlc-ai/gov-approval-token-signed-jwt`
- `gov-conventional-commits-enforced` → `sdlc-ai/gov-conventional-commits-enforced`
- `gov-sonarqube-ai-code-gate` → `sdlc-ai/gov-sonarqube-ai-code-gate`
- `eu-ai-act-compliance` → `ai-agents/eu-ai-act-compliance`
- `quality-management-pm-traditional` → `pm/quality-management-pm-traditional`
- `procurement-management-pm-traditional` → `pm/procurement-management-pm-traditional`

**Decision gate:**
> Advance when every privileged action has a JWT trail and there are no untagged commits on protected branches.

### Stage 4: Walkthrough + exception ledger

**Intent:** Rehearse the auditor walkthrough; log exceptions with owners + dates.

**Methodologies in chain:**
- `communications-management-pm-traditional` → `pm/communications-management-pm-traditional`
- `change-control-pm-traditional` → `pm/change-control-pm-traditional`
- `stakeholder-engagement-advanced` → `pm/stakeholder-engagement-advanced`
- `stakeholder-register-pm-traditional` → `pm/stakeholder-register-pm-traditional`
- `risk-register-pm-traditional` → `pm/risk-register-pm-traditional`
- `lessons-learned-pm-traditional` → `pm/lessons-learned-pm-traditional`
- `project-closure-pm-traditional` → `pm/project-closure-pm-traditional`
- `benefits-realization-pm-traditional` → `pm/benefits-realization-pm-traditional`

**Decision gate:**
> Required output: rehearsed walkthrough + signed exception ledger. No 'we'll wing it'.

## Common pitfalls

- Discovering gaps two weeks before the audit — stress + cut corners
- Exception ledger without remediation dates — auditor flags as evergreen
- Walkthrough rehearsed only on slides, not against the live repo
- Vendor risk assessment skipped on "small" SaaS — auditors find them anyway

## Quality checklist (self-review)

- Can I point at the repo artifact for every required control in <30 seconds?
- Do all secrets have named custodians who would answer a midnight page?
- Did we rehearse the walkthrough against the actual repo state?

## Related playbooks

- `incident-postmortem-preventive-backlog`
- `security-review-new-dependency`
- `rfc-to-production-feature-delivery`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **soc2-control-to-repo-artifact-map** (tier `geek`, blocks stage 1) — Inventory stage needs a SOC2-control → repo-artifact mapping template
- **gdpr-dsar-runbook-product-dev-team** (tier `geek`, blocks stage 4) — Walkthrough stage needs a DSAR runbook tuned for product-dev teams
- **vendor-risk-assessment-template** (tier `geek`, blocks stage 1) — Inventory stage references vendor risk assessment but no concrete template exists

## CLI usage

```
faion get-content soc2-gdpr-audit-prep --format md       # human-readable rendering
faion get-content soc2-gdpr-audit-prep --format context  # agent-optimised context bundle
faion get-content soc2-gdpr-audit-prep --format json     # raw structured form
```
