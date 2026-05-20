# PR review for IaC / Helm / GHA change

**Slug:** `pr-review-for-iac-helm-gha-change` · **Tier:** pro · **Complexity:** medium

## Context

A pull request touching Terraform, Helm, or GitHub Actions has a verdict (approve / request-changes) with concrete review notes covering blast radius, state safety, secret exposure, and rollback path.

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Prepare

Achieve the 'prepare' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Inventory

Achieve the 'inventory' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Decide approach

Achieve the 'decide approach' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Execute

Achieve the 'execute' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Verify

Achieve the 'verify' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 6: Document & decide

Achieve the 'document & decide' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/geek/sdlc-ai/gov-conventional-commits-enforced`
- `knowledge/geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `knowledge/pro/infra/cicd-engineer/gha-workflow-structure`
- `knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery`
- `knowledge/pro/infra/devops-engineer/finops-devops-cost-tagging`
- `knowledge/pro/infra/devops-engineer/helm-charts`
- `knowledge/pro/infra/devops-engineer/secrets-management`
- `knowledge/pro/infra/devops-engineer/security-as-code`
