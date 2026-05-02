# Feature 048: Tier Playbooks — Test Plan

## Drift sentinels (run on every commit during authoring)

| ID | Sentinel | Tool | Pass criterion |
|----|----------|------|----------------|
| DS1 | All citation paths resolve | `validate-tier-playbook.py` | Every `## References` path exists under `skills/faion/knowledge/` |
| DS2 | Tier ≤ rule | same script | Every citation tier ≤ playbook tier (via `tier-manifest.json` ordering) |
| DS3 | 8-section structure | same script | All 7 H2 sections present + ordered (`Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`) |
| DS4 | Front-matter complete | same script | 8 required keys present + valid values |
| DS5 | Slug shape | same script | Regex `^[a-z][a-z0-9-]{2,40}$` matches |
| DS6 | No duplicate slugs cross-tier | dedicated check | `find playbooks -name playbook.md` extracts slugs from front-matter; assert globally unique |
| DS7 | AGENTS.md ≤80 lines | shell `wc -l` | Per group folder + tier folder + root |
| DS8 | last_verified ≤180 days | script flag | Warn-only on commit; block on PR-merge if older |
| DS9 | Citation rationale specific | heuristic | Length ≥10 chars; not in generic-phrase blocklist (`"explains"`, `"covers"`, `"introduces"` without specificity) |
| DS10 | No `foo`/`bar` placeholders in steps | grep | `grep -E "\bfoo\b\|\bbar\b\|\bexample\.com\b"` returns 0 in Steps section |

## Per-playbook acceptance test

For each authored playbook, all DS1-DS10 must pass plus:

1. **Manual spot-check** (random 3 per wave):
   - Steps are action-leading + specific
   - Verify section has concrete check (curl response, file existence, log line, browser state)
   - Troubleshooting has ≥1 named pitfall
   - References ≥1 citation with playbook-specific rationale

2. **Smoke run** (where applicable):
   - If playbook describes a CLI command, run it in a sandbox; assert it works as documented
   - If playbook describes a SaaS signup flow, screenshot validation by reviewer

## Wave acceptance test

Per wave (free, solo, pro, geek):

1. 30 playbooks delivered in `skills/faion/playbooks/<tier>/`
2. `python3 scripts/validate-tier-playbook.py skills/faion/playbooks/<tier>/**/playbook.md` exits 0 for all
3. Tier `AGENTS.md` updated with index of new groups
4. Group `AGENTS.md` updated with one-line entry per playbook
5. CHANGELOG.md wave-summary entry under `## [Unreleased]`
6. `tier-manifest.json` `playbook_paths` includes all populated groups for the tier

## Feature-level acceptance test

1. AC1-AC8 from `spec.md` verified (each maps to a check)
2. End-to-end smoke:
   ```bash
   find skills/faion/playbooks -name playbook.md | wc -l   # = 120
   ```
3. End-to-end validator:
   ```bash
   find skills/faion/playbooks -name playbook.md -print0 \
     | xargs -0 -I {} python3 scripts/validate-tier-playbook.py {}
   ```
   Exits 0 for all 120 files.
4. Spec compliance: random 5 playbooks per tier (= 20 total) reviewed against `playbook-spec.md`
5. Discovery surface check: `faion/SKILL.md`, `faion/CLAUDE.md`, `skills/CLAUDE.md` all reference playbooks; tier-manifest.json populated

## Validator self-test (phase 3)

Before wave 1 dispatches:

| Test | Setup | Expected |
|------|-------|----------|
| valid playbook passes | minimal spec-compliant playbook | exit 0 |
| missing front-matter key | drop `tier` key | exit 1, error: "missing key: tier" |
| missing section | omit `## Verify` | exit 1, error: "missing section: Verify" |
| section out of order | swap `Steps` and `Prerequisites` | exit 1, error: "section out of order" |
| broken citation path | cite non-existent methodology | exit 1, error: "path does not exist" |
| tier exceeds | free playbook cites geek methodology | exit 1, error: "tier solo > free" |
| invalid slug | uppercase or special chars | exit 1, error: "slug regex" |
| generic rationale | "this methodology explains X" | exit 1, error: "generic rationale" |

## Regression tests (post-wave)

After each wave, re-run validator on all *prior* waves to detect:
- Cross-wave slug collisions
- Newly-broken methodology paths (if a methodology was renamed/moved)
- Tier-manifest divergence

## Rollback criteria

| Trigger | Action |
|---------|--------|
| Wave validator failure rate >10% | Pause dispatch, triage |
| Wave validator failure rate >25% on retry | Escalate to user, paused-loop |
| Duplicate slug detected post-merge | Roll back the duplicate; rename via versioned slug or move to TIER-2 |
| Citation path breaks after merge of unrelated work | Update citation; do not block — methodology corpus has its own lifecycle |

## Reviewer subagent (random spot-check)

Per wave: dispatch `faion-sdd-execution`-style reviewer agent on 3 random playbooks.

Reviewer prompt:
```
Review playbook at <path>. Apply the playbook-spec checklist:
- Action-leading verbs? Real commands? Verify section concrete? Troubleshooting named pitfalls?
- Citation rationale playbook-specific (not generic)?
- Tier inheritance respected?
Report: PASS / FAIL-WITH-NITS / FAIL with specific issues.
```

Track verdicts in `.aidocs/in-progress/feature-048-tier-playbooks/review-log.md`.

## Definition of Done

Feature is done when:

- [ ] AC1-AC8 satisfied
- [ ] All 120 playbooks pass validator
- [ ] All wave-summary CHANGELOG entries merged into a single feature CHANGELOG entry
- [ ] Discovery surface (SKILL.md, CLAUDE.md, tier-manifest) updated
- [ ] Convention spec validated (8-item self-checklist)
- [ ] Random 20-playbook spec-compliance review passes (≤2 FAIL-WITH-NITS, 0 FAIL)
- [ ] Feature folder moves to `.aidocs/done/feature-048-tier-playbooks/`
