# Accessibility & WCAG 2.2 Best Practices 2026

## M-UX-033: WCAG 2.2 Compliance

### What's New in WCAG 2.2

Released October 2023, baseline compliance standard by 2025-2026.

**9 New Success Criteria:**

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| Focus Not Obscured (Min) | AA | Focus indicator must be at least partially visible |
| Focus Not Obscured (Enhanced) | AAA | Focus indicator fully visible |
| Focus Appearance | AAA | 2px minimum focus indicator |
| Dragging Movements | AA | All drag actions have non-drag alternative |
| Target Size (Minimum) | AA | 24x24 CSS pixels minimum |
| Consistent Help | A | Help mechanism in same location across pages |
| Redundant Entry | A | Don't ask for same info twice |
| Accessible Authentication (Min) | AA | No cognitive function tests for login |
| Accessible Authentication (Enhanced) | AAA | No object/image recognition for login |

**Target Size Examples:**
```css
/* Minimum 24x24px */
.button {
  min-width: 24px;
  min-height: 24px;
  /* Or 44x44px for touch targets (recommended) */
}
```

**Dragging Alternatives:**
| Drag Action | Alternative Required |
|-------------|---------------------|
| Drag to reorder | Up/down buttons |
| Drag to resize | Input field for value |
| Drag to select area | Click corners |

---

## M-UX-034: Accessibility-First Design

### Problem

70-80% of accessibility issues can be avoided at design stage.

### Solution: Design for Accessibility from Day 1

**Color & Contrast:**
| Element | Minimum Ratio |
|---------|---------------|
| Body text | 4.5:1 |
| Large text (18pt+) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

**Design Checklist:**
- [ ] Color is not only indicator of meaning
- [ ] Text readable on all backgrounds
- [ ] Focus states clearly visible
- [ ] Touch targets 44x44px minimum
- [ ] Sufficient spacing between interactive elements
- [ ] No time limits (or adjustable)
- [ ] Animations can be paused/reduced

**Semantic Structure:**
```html
<!-- Good: Semantic structure -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
<main>
  <article>
    <h1>Main Title</h1>
    <section>
      <h2>Section Title</h2>
    </section>
  </article>
</main>

<!-- Bad: Div soup -->
<div class="nav">
  <div class="link">Home</div>
</div>
```

---

## M-UX-035: Regulatory Compliance 2026

### Key Regulations

| Regulation | Region | Deadline | Standard |
|------------|--------|----------|----------|
| ADA (DOJ Rule) | US | April 2026 | WCAG 2.1 AA |
| European Accessibility Act | EU | June 2025 (new) / June 2030 (all) | EN 301 549 |
| AODA | Canada (Ontario) | Now | WCAG 2.0 AA |
| Section 508 | US Federal | Now | WCAG 2.0 AA |

**EAA Scope:**
- E-commerce websites
- Banking services
- Electronic communications
- Transport services
- E-books

**Compliance Checklist:**
- [ ] Accessibility statement published
- [ ] WCAG conformance documented
- [ ] User testing with assistive tech
- [ ] Regular audits scheduled
- [ ] Remediation plan for issues

---

## M-UX-036: Testing with Assistive Technology

### Problem

Automated testing catches only 30-50% of issues.

### Solution: Manual + Assistive Tech Testing

**Testing Layers:**
```
Automated (30-50%) → Manual review → Screen reader → Keyboard-only → User testing
```

**Screen Reader Testing:**

| OS | Screen Reader | Browser |
|----|---------------|---------|
| Windows | NVDA (free) | Firefox, Chrome |
| Windows | JAWS | Chrome, Edge |
| macOS | VoiceOver | Safari |
| iOS | VoiceOver | Safari |
| Android | TalkBack | Chrome |

**Keyboard Testing:**
| Action | Keys |
|--------|------|
| Navigate | Tab, Shift+Tab |
| Activate | Enter, Space |
| Navigate options | Arrow keys |
| Exit/Cancel | Escape |
| Skip to main | Skip link |

**Common Issues Found:**
1. Missing form labels
2. No skip navigation
3. Inaccessible custom components
4. Missing alt text
5. Poor focus management
6. Keyboard traps

---

## M-UX-037: AI-Assisted Accessibility

### Problem

Accessibility testing is time-consuming.

### Solution: AI Tools for Accessibility

**AI-Powered Tools:**

| Tool | Function |
|------|----------|
| axe DevTools | Automated testing, AI suggestions |
| Accessibility Insights | Microsoft's testing suite |
| WAVE | Browser extension |
| Lighthouse | Chrome DevTools built-in |
| accessiBe | AI-powered overlay (controversial) |

**Caution on Overlays:**
> AI overlays don't fix underlying code issues. They're band-aids, not solutions. Focus on building accessible from the start.

**Best Practice:**
```
1. Automated scan (catch low-hanging fruit)
2. AI suggestions for fixes
3. Manual verification
4. User testing with people with disabilities
5. Continuous monitoring
```

**Key Insight:** "The future of accessible design isn't about tricking assistive technology - it's about building products that work for everyone from the start."

---

## Quick Reference: ARIA

**When to Use ARIA:**
```
No ARIA is better than bad ARIA.
First rule of ARIA: Don't use ARIA if you can use native HTML.
```

**Common ARIA Patterns:**

| Pattern | Use Case | Example |
|---------|----------|---------|
| aria-label | Describe element | `<button aria-label="Close">X</button>` |
| aria-labelledby | Reference visible text | `<div aria-labelledby="title">` |
| aria-describedby | Additional description | `<input aria-describedby="hint">` |
| aria-live | Dynamic updates | `<div aria-live="polite">` |
| aria-expanded | Expandable sections | `<button aria-expanded="false">` |
| aria-hidden | Hide decorative | `<span aria-hidden="true">★</span>` |

---

*Accessibility Best Practices 2026*
*Sources: WCAG.com, Nielsen Norman Group, WebAIM*
