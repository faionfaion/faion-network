<!-- purpose: Release plan skeleton with cadence + matrix + deprecations. -->
<!-- consumes: input from methodology -->
<!-- produces: artefact for downstream agent -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-500 tokens when loaded as context -->

# Release Plan: v[X.Y.Z]

## Metadata
- **Release Date:** [Date]
- **Release Manager:** [Name]
- **Type:** [Major/Minor/Patch]

## Release Goal
[What this release achieves for users — one sentence outcome]

## Success Metrics
| Metric | Current | Target | Tracking |
|--------|---------|--------|----------|
| [Metric] | [X] | [Y] | [How] |

## Contents

### Features
| Feature | Ticket | Owner | Status |
|---------|--------|-------|--------|
| [Feature 1] | [#123] | [Name] | Ready |

### Bug Fixes
| Fix | Ticket | Priority |
|-----|--------|----------|
| [Bug 1] | [#789] | High |

### Other Changes
- [Config change]
- [Dependency update]

## Excluded (Next Release)
| Item | Reason |
|------|--------|
| [Feature] | Not ready |

## Cross-Team Dependencies
| Dependency | Owner | Status | Evidence |
|------------|-------|--------|----------|
| [Dep 1] | [Name] | [Status] | [URL] |

## Risks
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Plan] |

## Rollback Plan
[How to rollback if issues occur — must be drillable in staging]

## Readiness Matrix (customer_visible items only)
| Function | Artifact | Owner | Status | Evidence |
|----------|----------|-------|--------|----------|
| eng | CI green + DoD | [Name] | green | [URL] |
| docs | Updated docs | [Name] | green | [URL] |
| support | Support macros | [Name] | green | [URL] |
| marketing | Release notes draft | [Name] | green | [URL] |
| legal | Cleared | [Name] | n/a | — |

## Communication Plan
| Audience | What | When | Who |
|----------|------|------|-----|
| Internal team | Release notes | Day before | PM |
| Customers | Email + changelog | Day of | Marketing |

## Timeline
| Time | Action | Owner |
|------|--------|-------|
| T-2d | Feature freeze | PM |
| T-1d | Final testing in staging | QA |
| T-0 9am | Deploy to production | Eng |
| T-0 11am | Send communications | Mkt |
| T+1d | Monitor and retro trigger | Team |
