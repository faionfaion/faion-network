<!-- purpose: Six-phase migration plan template with gate criteria per phase -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# PM Tool Migration: [Source] → [Target]

## Project Overview

**Objective:** Migrate from [Source] to [Target] by [Date]
**Sponsor:** [Name/Role]
**PM:** [Name]

## Scope

### In Scope
- All active projects ([N])
- Issues from last [N] years
- Attachments under [N] MB
- Key automations ([list])

### Out of Scope
- Archived projects
- Closed issues older than [N] years
- Custom plugins
- Time tracking data

## Timeline

| Phase | Duration | Owner |
|-------|----------|-------|
| Planning | 2-4 weeks | PM |
| Preparation | 2-3 weeks | Admin |
| Pilot | 1-2 weeks | [Team] |
| Full Migration | 1-4 weeks | PM |
| Cutover | 1 week | All |
| Stabilization | 2-4 weeks | Support |

## Risk Register

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data loss | High | Low | Multiple backups + dry-run |
| Team resistance | Medium | Medium | Training + migration champions |
| Integration breaks | High | Medium | Test all integrations in staging |
| Timeline slip | Medium | Medium | 50% buffer on all phases |

## Success Criteria

- [ ] 100% active issues migrated (verified by three-count check)
- [ ] All integrations working in target
- [ ] Team adoption >80% by end of week 2 post-cutover
- [ ] No critical data-loss bugs in first month
- [ ] Source tool decommissioned on scheduled date
