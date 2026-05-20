# New-project machine setup (laptop + desktop)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Multi-machine senior gets a new engagement → both machines productive on client stack within a half-day, no credential leakage between engagements.

Half-day setup ceremony when a new outsource engagement starts. Output: laptop + desktop (+ optionally a client-issued VDI) productive on the client stack, with isolated credentials per engagement and dotfiles synced. Avoids credential mixing between concurrent engagements.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Stack provision

**Intent:** Install the language + package manager the client demands.

**Tasks**
- Read client language/framework guide
- Install per the language-framework-guide methodology
- Set up Python via Poetry if applicable
- Verify on both laptop and desktop

**Outputs**
- Stack installed both machines
- Hello-world build green

**Decision gate**

Advance only when both machines build the client hello-world.

### Stage 2 — Credential isolation

**Intent:** Stop one client's keys leaking into another's repo.

**Tasks**
- Adopt per-client credential isolation pattern
- Use trunk-based branching with branch-by-abstraction where applicable
- Document onboarding rituals for new credential rotation
- Decide VDI vs BYOD per VDI-vs-BYOD matrix

**Outputs**
- Per-client vault entries
- VDI decision logged

**Decision gate**

Advance only when credentials cannot cross between engagements.

### Stage 3 — Sync + bootstrap

**Intent:** Make the second machine identical to the first.

**Tasks**
- Adopt dotfiles-management workflow
- Bootstrap second machine from dotfiles
- Adopt living-documentation for engagement-specific tooling
- Document the bootstrap script for next engagement

**Outputs**
- Dotfiles bootstrap script
- Both machines synced
- Engagement-specific tooling doc

**Decision gate**

Done when both machines pass the same build + lint.

## Common pitfalls

- Using global credentials by accident — breaks isolation
- Skipping dotfiles sync — second machine drifts in week 2
- Treating VDI/BYOD as a personal preference — it's a security policy decision

## Quality checklist

- Could I onboard a third machine in half the time using my doc?
- Did I isolate every credential per engagement?
- Did I match the client stack exactly, not approximately?

## Related playbooks

- `foreign-client-engagement-bootstrap`
- `foreign-client-project-kickoff`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `multi-machine-outsource-dev-env-bootstrap` (blocks stage 3)
- `per-client-credential-isolation-pattern` (blocks stage 2)
- `vdi-vs-byod-decision-matrix` (blocks stage 2)
