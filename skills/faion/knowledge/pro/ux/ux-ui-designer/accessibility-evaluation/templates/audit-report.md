# Accessibility Audit Report

**Product:** [Name]
**Version:** [Version]
**Date:** [Date]
**Auditor:** [Name/Team]
**Standard:** WCAG 2.2 Level AA

## Executive Summary

**Overall status:** Pass / Fail / Partial
**Critical issues:** [count]
**Total issues:** [count]

[One paragraph overview of accessibility status and key risk areas.]

## Methodology

| Method | Coverage |
|--------|----------|
| Automated scan (axe-core + Pa11y) | All pages / representative routes |
| Manual keyboard testing | All interactive elements |
| Screen reader (NVDA + Firefox) | Key user flows |
| Screen reader (VoiceOver + Safari) | Key user flows |
| Color contrast check | All text and UI components |

## Findings by Principle

### Perceivable

| Issue | WCAG SC | Count | Priority |
|-------|---------|-------|----------|
| | | | |

### Operable

| Issue | WCAG SC | Count | Priority |
|-------|---------|-------|----------|
| | | | |

### Understandable

| Issue | WCAG SC | Count | Priority |
|-------|---------|-------|----------|
| | | | |

### Robust

| Issue | WCAG SC | Count | Priority |
|-------|---------|-------|----------|
| | | | |

## Detailed Findings

### Issue: [Title]

**WCAG:** [SC number and name, e.g., 1.4.3 Contrast (Minimum)]
**Priority:** Critical / High / Medium / Low
**Location:** [Page URL + selector or component name]

**Problem:** [Description of the issue]
**Impact:** [Who is affected and how]
**Recommendation:** [Cite W3C technique G/H/F number + description]

## Testing Checklist

- [ ] Automated scan completed
- [ ] Keyboard navigation tested (Tab, Shift+Tab, Enter, Escape, arrow keys)
- [ ] Focus visible at all times
- [ ] Tab order matches visual flow
- [ ] No keyboard traps
- [ ] Skip links present and functional
- [ ] Screen reader tested (NVDA+Firefox, VoiceOver+Safari)
- [ ] Meaningful alt text verified
- [ ] Color contrast passes for all text and UI
- [ ] Form labels present and associated
- [ ] Error messages clear and recoverable
- [ ] Heading hierarchy correct (H1 → H2 → H3)
- [ ] Links have descriptive text
- [ ] ARIA used correctly (no duplicate IDs, valid roles)
- [ ] Dynamic content tested (modals, live regions, route changes)
