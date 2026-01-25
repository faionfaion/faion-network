# Accessibility-First Design

## Problem

70-80% of accessibility issues can be avoided at design stage. Retrofitting accessibility is expensive and time-consuming.

## Solution: Design for Accessibility from Day 1

### Color & Contrast

| Element | Minimum Ratio | Standard |
|---------|---------------|----------|
| Body text | 4.5:1 | WCAG AA |
| Large text (18pt+) | 3:1 | WCAG AA |
| UI components | 3:1 | WCAG AA |
| Focus indicators | 3:1 | WCAG AA |
| Enhanced text | 7:1 | WCAG AAA |

**Testing Tools:**
- Colour Contrast Analyser (desktop app)
- WebAIM Contrast Checker
- Chrome DevTools (Lighthouse)
- axe DevTools browser extension

### Design Checklist

**Visual Design:**
- [ ] Color is not only indicator of meaning
- [ ] Text readable on all backgrounds
- [ ] Focus states clearly visible (3:1 contrast minimum)
- [ ] Icons paired with text labels where possible
- [ ] Sufficient white space around elements

**Interactive Elements:**
- [ ] Touch targets 44x44px minimum (WCAG 2.2 recommends 24x24px min)
- [ ] Sufficient spacing between interactive elements (8px+)
- [ ] Hover, focus, and active states designed
- [ ] Keyboard navigation flow considered

**Motion & Time:**
- [ ] No time limits (or adjustable/extendable)
- [ ] Animations can be paused/reduced (prefers-reduced-motion)
- [ ] No auto-playing video with sound
- [ ] Flashing content avoided (<3 flashes/second)

**Content Structure:**
- [ ] Heading hierarchy planned (H1 → H2 → H3)
- [ ] Forms have visible labels
- [ ] Error states designed and helpful
- [ ] Empty states communicate purpose

### Semantic Structure

**Good: Semantic HTML**
```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Main Title</h1>
    <section>
      <h2>Section Title</h2>
      <p>Content here...</p>
    </section>
  </article>
</main>

<aside aria-label="Related content">
  <h2>Related Articles</h2>
</aside>

<footer>
  <p>&copy; 2026 Company Name</p>
</footer>
```

**Bad: Div Soup**
```html
<div class="nav">
  <div class="link">Home</div>
  <div class="link">About</div>
</div>

<div class="content">
  <div class="title">Main Title</div>
  <div class="text">Content...</div>
</div>
```

### Design Handoff to Developers

Include in design specifications:
- Heading levels (H1, H2, H3, etc.)
- Alt text for images
- Link text (avoid "click here")
- Focus order
- ARIA labels for custom components
- Error message copy
- Loading states and announcements

### Common Accessibility Patterns

**Forms:**
```
- Label + Input (connected with for/id)
- Helper text (aria-describedby)
- Error messages (aria-invalid, role="alert")
- Required fields marked (*required, aria-required)
- Field groups (fieldset + legend)
```

**Buttons vs. Links:**
```
Button: Triggers action (submit, toggle, open modal)
Link: Navigates to new page/section

Always use correct semantic element
```

**Modal Dialogs:**
```
- Focus trapped inside modal
- Close with Escape key
- Focus returns to trigger element
- Background marked inert (aria-hidden)
```

**Skip Links:**
```
- "Skip to main content" link
- First focusable element
- Can be visually hidden until focus
```

### Accessibility-First Tools

**Design Tools:**
- Figma: Accessibility plugins (Stark, A11y Annotation Kit)
- Adobe XD: Contrast checker built-in
- Sketch: Stark plugin

**Testing in Design:**
- Color blindness simulators
- Screen reader preview (VoiceOver, NVDA)
- Keyboard navigation prototype testing
- Zoom testing (200%, 400%)

### Inclusive Design Principles

1. **Equitable Use** - Useful to people with diverse abilities
2. **Flexible in Use** - Accommodates preferences and abilities
3. **Simple and Intuitive** - Easy to understand regardless of experience
4. **Perceptible Information** - Communicates effectively to all senses
5. **Tolerance for Error** - Minimizes hazards and adverse consequences
6. **Low Physical Effort** - Can be used efficiently without fatigue
7. **Size and Space** - Appropriate size and space for approach and use

### Mobile Accessibility

**Touch Targets:**
```
Minimum: 24x24px (WCAG 2.2 AA)
Recommended: 44x44px (Apple, Google guidelines)
Optimal: 48x48dp (Material Design)
```

**Mobile Checklist:**
- [ ] Touch targets large enough
- [ ] Spacing between targets adequate
- [ ] Zoom enabled (no user-scalable=no)
- [ ] Text resizes without horizontal scroll
- [ ] Forms work with autofill
- [ ] Screen orientation supported (portrait + landscape)

### Progressive Enhancement

Start with accessible baseline:
```
1. Semantic HTML (works everywhere)
2. CSS for visual presentation
3. JavaScript for enhanced interactions
4. Ensure core functionality works without JS
```

## Sources

- [WebAIM: Introduction to Web Accessibility](https://webaim.org/intro/)
- [W3C: Accessibility Principles](https://www.w3.org/WAI/fundamentals/accessibility-principles/)
- [A11y Project: Checklist](https://www.a11yproject.com/checklist/)
- [Material Design: Accessibility](https://m3.material.io/foundations/accessible-design/overview)
- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
