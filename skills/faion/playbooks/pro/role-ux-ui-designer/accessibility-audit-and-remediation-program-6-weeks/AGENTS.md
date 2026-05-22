---
slug: accessibility-audit-and-remediation-program-6-weeks
tier: pro
group: role-ux-ui-designer
persona: Accessibility lead or product designer running an a11y program
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Full product audited to WCAG 2.2 AA, prioritized remediation backlog shipped, regression tests with assistive tech, compliance evidence packaged.
content_id: 86b15f4103f4efd4
methodology_refs:
  - ai-accessibility-automation-2026
  - ai-assisted-accessibility
  - a11y-basics
  - a11y-testing
  - accessibility-first-design
  - ada-title-ii-compliance-2026
  - cognitive-inclusion-design
  - regulatory-compliance-2026
  - testing-with-assistive-technology
  - wcag-22-compliance
  - accessibility-evaluation
---

# Accessibility audit and remediation program (6 weeks)

## Context

Accessibility lead runs a 6-week program across the product. Includes automated + manual + AT audit, prioritized remediation, regression tests, an a11y user panel, CI gates, and a compliance evidence pack. Done when all critical + major findings are remediated, AT regression tests pass, and compliance pack is filed with legal.

## Outcome

Audit gap -> WCAG 2.2 AA across product + shipped remediation + compliance evidence ready for legal/ADA. Full product audited to WCAG 2.2 AA, prioritized remediation backlog shipped, regression tests with assistive tech, compliance evidence packaged.

## Steps

1. **Scope + plan.** Define what gets audited and what good looks like. Tasks: Inventory products + flows in scope; Pick WCAG 2.2 AA + applicable regional rules (ADA Title II 2026); Define severity rubric + ship-blocking thresholds.
2. **Automated + AI sweep.** Catch the easy wins fast. Tasks: Run AI-assisted automated scan across product; Triage findings; reject false positives; Quick-fix low-effort high-impact items.
3. **Manual audit.** Find what automation cannot. Tasks: Heuristic + manual review per WCAG 2.2 AA; Cognitive inclusion checks on flagship flows; Document each finding with severity + repro steps.
4. **AT testing.** Test with the tools real users use. Tasks: Run NVDA + VoiceOver + JAWS test scripts on flagship flows; Recruit a small a11y user panel for live sessions; Capture critical issues missed by other layers.
5. **Remediation.** Ship the fixes, not just file them. Tasks: Prioritize critical + major findings into sprint backlog; Pair with engineering on patterns; update design system; Track burndown until criticals = 0.
6. **Regression in CI.** Prevent backsliding. Tasks: Wire a11y tests into CI pipeline; Add AT-based regression checks for flagship flows; Block merges on regression.
7. **Compliance pack.** Hand legal what they need to file. Tasks: Compile VPAT/ACR evidence; Map findings + fixes to WCAG criteria; Hand off to legal with sign-off.

## Decision points

- **After Scope + plan:** Advance only when scope is signed by product + legal.
- **After Automated + AI sweep:** Advance only after triage is human-reviewed.
- **After Manual audit:** Advance when severities are confirmed by a second reviewer.
- **After AT testing:** Advance only after each flagship flow passes AT smoke test.
- **After Remediation:** Advance when criticals = 0 and majors are below threshold.
- **After Regression in CI:** Advance only when CI has run a11y checks on >=2 release cycles.
- **After Compliance pack:** Done when legal accepts the pack.

## References

- `faion/knowledge/geek/ux/accessibility-specialist/ai-accessibility-automation-2026`
- `faion/knowledge/geek/ux/accessibility-specialist/ai-assisted-accessibility`
- `faion/knowledge/pro/ux/accessibility-specialist/a11y-basics`
- `faion/knowledge/pro/ux/accessibility-specialist/a11y-testing`
- `faion/knowledge/pro/ux/accessibility-specialist/accessibility-first-design`
- `faion/knowledge/pro/ux/accessibility-specialist/ada-title-ii-compliance-2026`
- `faion/knowledge/pro/ux/accessibility-specialist/cognitive-inclusion-design`
- `faion/knowledge/pro/ux/accessibility-specialist/regulatory-compliance-2026`
- `faion/knowledge/pro/ux/accessibility-specialist/testing-with-assistive-technology`
- `faion/knowledge/pro/ux/accessibility-specialist/wcag-22-compliance`
- `faion/knowledge/pro/ux/ux-ui-designer/accessibility-evaluation`
- Related: `a11y-audit-on-one-screen-1hr`, `design-system-v1-to-v2-migration-12-weeks`
