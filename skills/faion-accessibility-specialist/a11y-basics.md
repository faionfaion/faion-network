---
id: a11y-basics
name: "Accessibility Basics"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Accessibility Basics

## Metadata
- **Category:** UX / Accessibility
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #accessibility #wcag #a11y
- **Agent:** faion-usability-agent

---

## Problem

Products exclude users with disabilities. Legal requirements (ADA, Section 508, AODA) are not met. Accessibility is treated as an afterthought. Testing only happens at the end, when fixes are expensive. Teams do not know what to test or how.

Without accessibility evaluation:
- Users with disabilities excluded
- Legal compliance risk
- Expensive late-stage fixes
- Poor experience for many users

---

## Framework

### What is Accessibility?

Accessibility ensures digital products can be used by people with disabilities, including those who are blind, deaf, have motor impairments, or have cognitive disabilities.

### WCAG Principles (POUR)

| Principle | Meaning | Examples |
|-----------|---------|----------|
| **Perceivable** | Can users perceive content? | Alt text, captions, contrast |
| **Operable** | Can users operate controls? | Keyboard access, timing |
| **Understandable** | Can users understand content? | Clear language, predictable |
| **Robust** | Does it work with assistive tech? | Valid code, ARIA |

### WCAG Conformance Levels

| Level | Description | Requirement |
|-------|-------------|-------------|
| **A** | Minimum accessibility | Must have |
| **AA** | Standard for most | Legal requirement in most places |
| **AAA** | Enhanced accessibility | Ideal but not always achievable |

### Evaluation Types

| Type | What it is | When to use |
|------|------------|-------------|
| **Automated testing** | Tools scan for issues | Continuous, catches ~30% |
| **Manual testing** | Human checks with tools | Development, catches ~50% |
| **Assistive tech testing** | Test with screen readers, etc. | Pre-release, real experience |
| **User testing** | People with disabilities test | Validation, catches remaining |

---

## Quick Checks

### Five-Minute Test

```
1. Tab through the page
   - Can you reach everything?
   - Can you see where you are?

2. Zoom to 200%
   - Is everything still usable?
   - Does content reflow?

3. Check one image
   - Does alt text make sense?

4. Check one form
   - Are labels visible and connected?

5. Run axe DevTools
   - Any critical issues?
```

### Pre-Commit Checks

Before code review:
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color contrast passes (4.5:1)
- [ ] Interactive elements keyboard accessible
- [ ] Heading hierarchy is correct

---

## Common Issues

### Example 1: Form Accessibility

**Issue:** Form inputs have no visible labels

**Before:**
```html
<input type="text" placeholder="Email">
```

**Problem:**
- Screen readers may not announce the field purpose
- Placeholder disappears when typing
- Low contrast placeholder text

**After:**
```html
<label for="email">Email address</label>
<input type="text" id="email" name="email"
       aria-describedby="email-hint">
<span id="email-hint">We'll never share your email.</span>
```

### Example 2: Image Accessibility

**Issue:** Decorative image has no alt attribute

**Decorative image (should be hidden):**
```html
<img src="decorative-line.png" alt="" role="presentation">
```

**Informative image (needs description):**
```html
<img src="chart.png" alt="Sales increased 25% in Q3 compared to Q2">
```

**Complex image (needs long description):**
```html
<figure>
  <img src="complex-diagram.png"
       alt="System architecture diagram"
       aria-describedby="diagram-desc">
  <figcaption id="diagram-desc">
    The system consists of three layers: presentation,
    business logic, and data. [Full description...]
  </figcaption>
</figure>
```

---

## Common Mistakes

1. **Relying only on automated tools** - They catch only 30% of issues
2. **Testing only with mouse** - Keyboard users have different experience
3. **Ignoring cognitive accessibility** - Not just visual impairments
4. **Adding ARIA incorrectly** - Bad ARIA worse than no ARIA
5. **Testing at the end** - Should be continuous

---

## Tools

### Automated Testing

| Tool | Type | Use For |
|------|------|---------|
| axe DevTools | Browser extension | Quick page scan |
| WAVE | Browser extension | Visual feedback |
| Lighthouse | Chrome DevTools | Performance + a11y |
| Pa11y | CLI/CI | Automated pipeline |
| SiteImprove | Service | Enterprise scanning |

### Manual Testing

| Tool | Purpose |
|------|---------|
| Colour Contrast Analyser | Check contrast ratios |
| HeadingsMap | Check heading structure |
| Web Developer Toolbar | Inspect page structure |
| ANDI | Section 508 testing |

### Screen Readers

| Tool | Platform | Free |
|------|----------|------|
| NVDA | Windows | Yes |
| VoiceOver | Mac/iOS | Built-in |
| TalkBack | Android | Built-in |
| JAWS | Windows | No ($$$) |

---

## References

- WCAG 2.1 Guidelines: w3.org/WAI/WCAG21/quickref/
- WebAIM: webaim.org
- A11y Project: a11yproject.com
- Deque University: dequeuniversity.com

---

## Sources

- [W3C: WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Introduction to Web Accessibility](https://webaim.org/intro/)
- [A11y Project: Checklist](https://www.a11yproject.com/checklist/)
- [Deque University: Web Accessibility Curriculum](https://dequeuniversity.com/)
- [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

**See also:**
- [a11y-testing.md](a11y-testing.md) - Complete testing process
- [wcag-22-compliance.md](wcag-22-compliance.md) - WCAG 2.2 details
- [accessibility-first-design.md](accessibility-first-design.md) - Design approach
