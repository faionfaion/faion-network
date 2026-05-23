# PM Tool Migration: [Source] → [Target]

**Objective:** [Goal] | **Sponsor:** [Name] | **PM:** [Name]

## Scope

### In Scope
- Active projects: [N]
- Issues from last [N] years
- Attachments under [N] MB
- Key automations

### Out of Scope
- Archived projects
- Issues closed over [N] years ago
- Custom plugins without target equivalents
- Time-tracking data

## Phase Timeline

| Phase | Duration | Owner |
|-------|----------|-------|
| Planning | 2-4 weeks | PM |
| Preparation | 2-3 weeks | Admin |
| Pilot | 1-2 weeks | Pilot team |
| Full Migration | 1-4 weeks | PM |
| Cutover | 1 week | All |
| Stabilization | 2-4 weeks | Support |

## Risk Register

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data loss | High | Low | Multiple backups + two-pass load |
| Team resistance | Medium | Medium | Training + champions |
| Integration breaks | High | Medium | Test all integrations pre-cutover |
| Identity remapping failures | High | Medium | HR-verified email map |

## Rollback Triggers (pre-defined)

| Trigger | Threshold | Response |
|---------|-----------|----------|
| Data loss detected | Any | Immediate rollback |
| Critical integration failure | Any | Immediate rollback |
| Team productivity drop | over 50% | 48-hour review |
| User adoption | under 30% at 1wk | Planned rollback |

## Success Criteria

- [ ] 100% active issues migrated (validated by count diff)
- [ ] All integrations working (tested day 0)
- [ ] Team adoption over 80% by week 2
- [ ] No critical bugs in first month
- [ ] id-map committed to project repo as permanent artifact
