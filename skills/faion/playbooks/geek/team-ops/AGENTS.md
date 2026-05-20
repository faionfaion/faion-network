# Geek / Team Ops

Playbooks for product-dev teams (2-10 engineers) running AI-augmented SDLC. Citation scope: all four tiers (`knowledge/free/ + solo/ + pro/ + geek/`).

| Slug | Goal |
|------|------|
| `quarter-planning-okr-reset` | Close one quarter and open the next with retro, OKRs, top-3 bets, RACI, and a populated backlog |
| `rfc-to-production-feature-delivery` | Move an approved RFC through PM/BA/Architect/Dev/QA/DevOps to production behind a flag with telemetry |
| `hire-onboard-product-dev-2-weeks` | Take a signed offer to first merged PR + first on-call shadow in 14 days |
| `big-migration-postgres-monolith` | Cross-quarter major migration with proven rollback, dual-stack window, and clean post-audit |
| `incident-postmortem-preventive-backlog` | Convert a paging alert into a published postmortem and merged preventive PRs |
| `soc2-gdpr-audit-prep` | Reach the annual audit window with current evidence, closed gaps, and a rehearsed walkthrough |
| `daily-standup-ai-prebrief` | Run a 15-min exception-driven standup on top of an AI-generated pre-brief |
| `pr-review-with-junior-mentoring` | Run a paired PR review that grows the junior with a written next-PR checklist |
| `sentry-datadog-alert-triage` | Close every in-hours alert with a verdict and an audit log |
| `backlog-grooming-pm-tech-lead` | Make the top of backlog spec-ready every week in 1 hour |
| `sprint-planning-sdd-task-expansion` | Turn spec-ready stories into SDD feature folders with task expansion |
| `security-review-new-dependency` | Approve, defer, or reject a new dependency with SBOM diff + ADR before merge |
| `hiring-screen-take-home-review` | Score a take-home apples-to-apples against the team's own quality floors |
| `weekly-architectural-review` | Catch architectural drift weekly in 45 min and promote good patterns |
| `biweekly-retro-mistake-memory` | Run a 45-min retro that produces 2-3 owned experiments, fed by mistake-memory |
| `adopt-faion-org-wide-overrides` | Adopt faion across a team with company-specific overlays that shadow defaults |
| `cross-role-handoff-pm-architect-dev-qa-devops` | Single living artifact moves a feature through 5 roles with DoR/DoD gates |
| `hire-to-productive-60-days-in-house` | First owned feature shipped by day 45 for a new in-house product hire |
| `quarterly-okr-cascade-weekly-review` | Cascade OKRs company→team→personal with weekly check-ins and a quarterly blameless retro |

Spec: `../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-playbook-v2.py <path>/playbook.yaml`.
