---
slug: a11y-audit-on-one-screen-1hr
tier: pro
group: role-ux-ui-designer
persona: Designer or a11y specialist auditing a single screen
goal: audit-comply
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Single-screen a11y pass against WCAG 2.2 AA + project standards: automated + manual + AT checks; remediation tickets opened per violation."
content_id: f2d3e81cccf1ac1f
methodology_refs:
  - ai-accessibility-automation-2026
  - ai-assisted-accessibility
  - a11y-basics
  - a11y-testing
  - accessibility-first-design
  - cognitive-inclusion-design
  - testing-with-assistive-technology
  - wcag-22-compliance
---

# A11y audit on one screen (1hr)

## Context

Designer or a11y specialist runs a 1-hour audit on one screen. Automated scan, manual heuristic pass, AT smoke test, ticket per violation, status tracker updated. Done when each violation has a ticket and the screen status is logged.

## Outcome

Open screen with unknown a11y -> WCAG 2.2 AA-compliant + remediation tickets opened. Single-screen a11y pass against WCAG 2.2 AA + project standards: automated + manual + AT checks; remediation tickets opened per violation.

## Steps

1. **Automated scan.** Catch the easy wins. Tasks: Run AI-assisted automated scan on the screen; Triage false positives; Note quick fixes.
2. **Manual heuristic.** Find what automation missed. Tasks: Walk WCAG 2.2 AA against the screen; Check cognitive-inclusion patterns; Capture findings with severity.
3. **AT smoke.** Test with NVDA + VoiceOver at minimum. Tasks: Run flagship task with NVDA; Run flagship task with VoiceOver; Capture AT-only findings.
4. **Ticket.** Tickets, not docs. Tasks: Open a ticket per violation with severity; Pair patterns with design-system tags; Link to evidence per finding.
5. **Update tracker.** Make the screen's state visible. Tasks: Update the screen-status tracker; Note the audit date + auditor; Plan re-audit after fixes.

## Decision points

- **After Automated scan:** Advance only after triage.
- **After Manual heuristic:** Advance only after the heuristic walk is complete.
- **After AT smoke:** Advance only when both screen-readers are tested.
- **After Ticket:** Advance only when every violation has a ticket.
- **After Update tracker:** Done when tracker reflects the audit.

## References

- `faion/knowledge/geek/ux/accessibility-specialist/ai-accessibility-automation-2026`
- `faion/knowledge/geek/ux/accessibility-specialist/ai-assisted-accessibility`
- `faion/knowledge/pro/ux/accessibility-specialist/a11y-basics`
- `faion/knowledge/pro/ux/accessibility-specialist/a11y-testing`
- `faion/knowledge/pro/ux/accessibility-specialist/accessibility-first-design`
- `faion/knowledge/pro/ux/accessibility-specialist/cognitive-inclusion-design`
- `faion/knowledge/pro/ux/accessibility-specialist/testing-with-assistive-technology`
- `faion/knowledge/pro/ux/accessibility-specialist/wcag-22-compliance`
- Related: `accessibility-audit-and-remediation-program-6-weeks`, `heuristic-evaluation-on-a-new-screen-1hr`
