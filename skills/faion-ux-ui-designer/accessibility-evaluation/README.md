---
id: a11y-testing
name: "Accessibility Testing Process"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Accessibility Testing Process

## Metadata
- **Category:** UX / Accessibility
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #testing #accessibility #wcag #a11y
- **Agent:** faion-usability-agent

---

## Process

### Step 1: Automated Scanning

Run automated tools first:

```
Tools:
- axe DevTools (browser extension)
- WAVE (browser extension)
- Lighthouse (Chrome DevTools)
- Pa11y (CI integration)
```

**What automated tools find:**
- Missing alt text
- Color contrast issues
- Missing form labels
- Incorrect heading structure
- Missing language attribute

**What they miss:**
- Alt text quality
- Keyboard usability
- Meaningful reading order
- Context and understanding

### Step 2: Manual Testing

#### Keyboard Testing

Test without mouse:

| Check | How to Test | Pass |
|-------|-------------|------|
| Tab navigation | Tab through page | All interactive elements reachable |
| Focus visible | Watch for focus indicator | Always visible where you are |
| Logical order | Tab and note sequence | Order matches visual flow |
| Skip links | Tab from top | Skip to main content available |
| Traps | Tab everywhere | Can always Tab out |
| Keyboard shortcuts | Test documented shortcuts | Work and don't conflict |

#### Color and Contrast

| Check | Requirement | Tool |
|-------|-------------|------|
| Text contrast | 4.5:1 (normal), 3:1 (large) | Colour Contrast Analyser |
| UI contrast | 3:1 for interactive elements | Same |
| Not color alone | Color not only indicator | Manual check |

#### Content Structure

| Check | What to verify |
|-------|----------------|
| Headings | Logical hierarchy (H1 → H2 → H3) |
| Landmarks | Main, nav, header, footer marked |
| Lists | Proper list markup where appropriate |
| Tables | Headers marked, scope defined |
| Links | Descriptive text (not "click here") |

### Step 3: Screen Reader Testing

Test with actual screen readers:

| Screen Reader | Platform | Users |
|---------------|----------|-------|
| **NVDA** | Windows | Free, common |
| **JAWS** | Windows | Enterprise, expensive |
| **VoiceOver** | Mac/iOS | Built-in |
| **TalkBack** | Android | Built-in |

**Basic screen reader checks:**
- Can you navigate by headings?
- Are images described?
- Do forms announce labels?
- Are state changes announced?
- Can you complete key tasks?

### Step 4: Cognitive Accessibility

Check for cognitive accessibility:

| Check | What to verify |
|-------|----------------|
| Clear language | Plain language, no jargon |
| Consistent navigation | Same location throughout |
| Error prevention | Confirmation before destructive actions |
| Error recovery | Clear error messages with solutions |
| Timeouts | Warnings before timeout, option to extend |
| Animation | Can be paused, no excessive motion |

### Step 5: Document and Fix

Prioritize issues:

| Priority | Description | Fix Timeline |
|----------|-------------|--------------|
| **Critical** | Blocks access completely | Immediately |
| **High** | Major barrier, workaround difficult | This sprint |
| **Medium** | Creates difficulty | Next sprint |
| **Low** | Enhancement, not blocking | Backlog |

---

## Templates

### Accessibility Audit Template

```markdown
# Accessibility Audit Report

**Product:** [Name]
**Version:** [Version]
**Date:** [Date]
**Auditor:** [Name]
**Standard:** WCAG 2.1 Level AA

## Executive Summary

**Overall status:** [Pass/Fail/Partial]
**Critical issues:** [Count]
**Total issues:** [Count]

**Summary:**
[Brief overview of accessibility status]

## Methodology

| Method | Coverage |
|--------|----------|
| Automated scan (axe) | 100% of pages |
| Manual keyboard testing | All interactive elements |
| Screen reader (VoiceOver) | Key user flows |
| Color contrast check | All text and UI |

## Findings by Principle

### Perceivable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| Missing alt text | 1.1.1 | 5 | High |
| Low contrast | 1.4.3 | 12 | High |
| | | | |

### Operable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

### Understandable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

### Robust

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

## Detailed Findings

### Issue 1: [Title]

**WCAG:** [Criterion number and name]
**Priority:** [Critical/High/Medium/Low]
**Location:** [Page/component]

**Problem:**
[Description of the issue]

**Impact:**
[Who is affected and how]

**Recommendation:**
[How to fix]

**Code example:**
```html
<!-- Current -->
<img src="photo.jpg">

<!-- Fixed -->
<img src="photo.jpg" alt="Description of image">
```

### Issue 2: [Title]
[Same structure]

## Testing Checklist

- [x] Automated scan completed
- [x] Keyboard navigation tested
- [x] Screen reader tested
- [x] Color contrast verified
- [ ] User testing with disabled users

## Recommendations

1. **Immediate:** [Critical fixes]
2. **Short-term:** [High priority fixes]
3. **Ongoing:** [Process improvements]
```

### Issue Template

```markdown
## Issue: [Brief title]

**WCAG Criterion:** [e.g., 1.4.3 Contrast (Minimum)]
**Level:** A / AA / AAA
**Priority:** Critical / High / Medium / Low
**Component:** [Where issue occurs]

**Description:**
[What the issue is]

**User Impact:**
[Who is affected, how it affects them]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What currently happens]

**Recommendation:**
[How to fix]

**Resources:**
- [Link to WCAG understanding doc]
- [Link to technique]
```

---

## Checklist

- [ ] Automated scan run
- [ ] All critical issues fixed
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Focus is always visible
- [ ] Screen reader testing done
- [ ] Alt text is meaningful
- [ ] Color contrast passes
- [ ] Form labels present
- [ ] Error messages clear
- [ ] Headings are hierarchical
- [ ] Links are descriptive
- [ ] No keyboard traps
- [ ] Skip links present
- [ ] ARIA used correctly

---

## Sources

- [WebAIM: Accessibility Testing](https://webaim.org/articles/testing/)
- [Deque: Automated Testing Best Practices](https://www.deque.com/blog/automated-testing-best-practices/)
- [A11y Project: How to Test](https://www.a11yproject.com/checklist/#how-to-test)
- [Microsoft: Accessibility Testing](https://learn.microsoft.com/en-us/microsoft-edge/accessibility/test)
- [W3C: Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/)

**See also:**
- [a11y-basics.md](a11y-basics.md) - Fundamentals and quick checks
- [wcag-22-compliance.md](wcag-22-compliance.md) - WCAG 2.2 details
- [testing-with-assistive-technology.md](testing-with-assistive-technology.md) - Deep dive on AT testing
