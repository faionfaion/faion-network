# Accessibility Audit Report

**Product:** [Name]
**Version:** [Version]
**Date:** [YYYY-MM-DD]
**Auditor:** [Name / Team]
**Standard:** WCAG 2.1 Level AA (+ WCAG 2.2 delta where noted)

## Executive Summary

**Overall status:** Pass / Partial / Fail
**Critical issues:** [Count]
**Total issues:** [Count]

[Brief overview: what was tested, major gaps, recommended next steps.]

## Methodology

| Method | Scope | Tools |
|--------|-------|-------|
| Automated scan | All pages | axe-core, Pa11y, Lighthouse |
| Manual keyboard | All interactive elements | Browser, no mouse |
| Screen reader | Key user flows | NVDA+Firefox, VoiceOver+Safari |
| Color contrast | All text and UI elements | Colour Contrast Analyser |
| Cognitive review | Copy, forms, error messages | Manual |

## Findings by Principle

### Perceivable

| Issue | WCAG SC | Count | Priority |
|-------|---------|-------|----------|
| Missing alt text | 1.1.1 | [N] | High |
| Low contrast text | 1.4.3 | [N] | High |

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

### Issue [N]: [Brief title]

**WCAG:** [e.g., 1.4.3 Contrast (Minimum)]
**Priority:** Critical / High / Medium / Low
**Location:** [Page or component URL/name]

**Problem:** [What the issue is.]

**User Impact:** [Who is affected and how — screen reader users, keyboard users, low-vision users, etc.]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]

**Recommendation:**
[How to fix — include code snippet if applicable.]

---

## Untested Criteria

The following criteria were not testable in this audit (require AT user or specific device):

| WCAG SC | Reason |
|---------|--------|
| 2.1.2 No Keyboard Trap | Requires screen reader user validation |

## Recommendations

1. **Immediate (Critical):** [Fix list]
2. **Short-term (High):** [Fix list]
3. **Process:** [Ongoing improvements — CI gate, training, procurement policy]
