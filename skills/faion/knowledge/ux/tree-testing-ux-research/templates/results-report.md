<!-- purpose: Per-task tree-test findability results with problem areas and IA-revision recommendations -->
<!-- consumes: raw tree-test tool export (per-task success/directness/path data) -->
<!-- produces: filled tree-testing results report markdown -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~390 tokens filled -->

# Tree Testing Results

**Test dates:** <start> to <end>
**Participants:** <participants>
**Tasks:** <tasks>
**IA Version:** <version>
**Tool:** <tool>

## Executive Summary

**Overall success rate:** <x> — <overall_success_rate>
**Overall directness:** <x>
**Worst 3 tasks:** [Task IDs with success rates]

**Key findings:**
1. <finding_1>
2. <finding_2>
3. <finding_3>

---

## Per-Task Results

### Task 1: "<scenario_text>"

**Success rate:** <x> | **Directness:** <x> | **Median time:** <x_sec>

**Path analysis:**
| Path taken | Count | % |
|------------|-------|---|
| <correct_path> | N | X% |
| <wrong_path_1> | N | X% |
| <abandoned> | N | X% |

**First clicks:**
| Category | % of users |
|----------|------------|
| <correct_section> | X% |
| <wrong_section> | X% |

**Root cause:** <root_cause>
**Recommendation:** [Specific label rename or restructuring with evidence]

---

## Problem Areas Summary

| Issue | Affected Tasks | Severity | Recommended Fix |
|-------|----------------|----------|-----------------|
| [Label confusion on "X"] | 2, 5, 8 | High | Rename to "Y" |
| [Missing category for Z] | 3 | Medium | Add "Z" under Section A |

## Recommendations

**High priority (blocking for launch):**
1. <change_1>
2. <change_2>

**Consider (improvement):**
1. <change_3>

**Monitor (track post-launch):**
1. [Area — low severity, may self-resolve]

---
_Next action: Iterate IA, increment version to <n_1>, re-test problem tasks before build._
