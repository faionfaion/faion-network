# Accessibility Implementation Checklist

Step-by-step checklist for implementing accessible web applications.

## Phase 1: Semantic HTML Foundation

### 1.1 Document Structure

- [ ] Use proper DOCTYPE declaration
- [ ] Set lang attribute on html element
- [ ] Include viewport meta tag
- [ ] Use semantic HTML5 elements (header, nav, main, article, aside, footer)
- [ ] Ensure heading hierarchy (h1 → h2 → h3, no skips)
- [ ] Use section elements with aria-labelledby
- [ ] Avoid div/span soup - use semantic alternatives

### 1.2 Landmarks

- [ ] Add role="banner" or use header for site header
- [ ] Add role="navigation" or use nav for primary navigation
- [ ] Add role="main" or use main for main content (only one per page)
- [ ] Add role="complementary" or use aside for sidebars
- [ ] Add role="contentinfo" or use footer for site footer
- [ ] Add role="search" for search functionality
- [ ] Use aria-label to distinguish multiple landmarks of same type

### 1.3 Lists and Tables

- [ ] Use ul/ol for lists, not div with bullets
- [ ] Use dl/dt/dd for definition lists
- [ ] Use table element for tabular data
- [ ] Include caption or aria-label for tables
- [ ] Use thead, tbody, tfoot for table structure
- [ ] Use th with scope attribute for headers
- [ ] Avoid layout tables or use role="presentation"

## Phase 2: Keyboard Navigation

### 2.1 Tab Order

- [ ] Ensure logical tab order follows visual layout
- [ ] Set tabindex="0" for custom interactive elements
- [ ] Use tabindex="-1" for programmatically focusable elements
- [ ] Avoid positive tabindex values
- [ ] Test full site navigation with Tab key only

### 2.2 Focus Management

- [ ] Ensure visible focus indicators on all interactive elements
- [ ] Use :focus-visible for better UX
- [ ] Trap focus in modals (cycle between first/last element)
- [ ] Return focus to trigger element when closing modals
- [ ] Move focus to main content on page load for SPAs
- [ ] Use skip links for bypass blocks

### 2.3 Keyboard Shortcuts

- [ ] Implement standard keyboard patterns (Enter, Space, Escape, Arrow keys)
- [ ] Support Home/End keys in lists and composites
- [ ] Add keyboard shortcuts documentation
- [ ] Avoid conflicts with browser/screen reader shortcuts
- [ ] Provide keyboard alternative for every mouse action

### 2.4 Interactive Elements

- [ ] Use button for actions (not div with onclick)
- [ ] Use a for navigation (with valid href)
- [ ] Support Enter key on buttons, Space and Enter on custom buttons
- [ ] Support Escape key to close modals/dropdowns
- [ ] Implement roving tabindex for composite widgets

## Phase 3: ARIA Implementation

### 3.1 ARIA Roles

- [ ] Use role="button" for custom buttons
- [ ] Use role="dialog" for modals
- [ ] Use role="alert" for critical announcements
- [ ] Use role="status" for non-critical status updates
- [ ] Use role="tablist/tab/tabpanel" for tabs
- [ ] Use role="menu/menuitem" for application menus (not site navigation)
- [ ] Avoid redundant roles on semantic HTML

### 3.2 ARIA States

- [ ] Set aria-expanded for expandable elements
- [ ] Set aria-pressed for toggle buttons
- [ ] Set aria-checked for custom checkboxes
- [ ] Set aria-selected for selected items
- [ ] Set aria-hidden="true" for decorative elements
- [ ] Set aria-disabled for disabled interactive elements

### 3.3 ARIA Properties

- [ ] Use aria-label for elements without visible text
- [ ] Use aria-labelledby to reference visible labels
- [ ] Use aria-describedby for additional descriptions
- [ ] Use aria-required for required form fields
- [ ] Use aria-invalid for validation errors
- [ ] Use aria-live="polite" for dynamic content
- [ ] Use aria-live="assertive" for urgent updates

### 3.4 ARIA Relationships

- [ ] Connect labels with aria-labelledby
- [ ] Connect descriptions with aria-describedby
- [ ] Use aria-controls to indicate controlled elements
- [ ] Use aria-owns for logical parent-child relationships
- [ ] Use aria-activedescendant for composite focus management

## Phase 4: Forms and Validation

### 4.1 Form Structure

- [ ] Use label element for all inputs (not placeholder as label)
- [ ] Connect label with for/id attributes
- [ ] Group related fields with fieldset/legend
- [ ] Mark required fields with required attribute and aria-required
- [ ] Use autocomplete attribute for common fields
- [ ] Provide clear field instructions

### 4.2 Input Types

- [ ] Use appropriate input types (email, tel, url, number, date)
- [ ] Use type="search" for search inputs
- [ ] Use type="checkbox" and type="radio" correctly
- [ ] Use select for dropdowns, not custom divs
- [ ] Use textarea for multi-line text

### 4.3 Validation

- [ ] Validate on blur and submit, not on keystroke
- [ ] Set aria-invalid="true" on fields with errors
- [ ] Use aria-describedby to link errors to fields
- [ ] Display errors in live region with role="alert"
- [ ] Provide error summary at top of form
- [ ] Focus first error field on validation failure
- [ ] Clear aria-invalid when error is fixed

### 4.4 Form Submission

- [ ] Use button type="submit" for submit buttons
- [ ] Disable submit button during submission
- [ ] Provide loading state announcement
- [ ] Announce success/failure with live regions
- [ ] Return focus appropriately after submission

## Phase 5: Color and Contrast

### 5.1 Contrast Ratios

- [ ] Normal text: minimum 4.5:1 contrast ratio
- [ ] Large text (18px+): minimum 3:1 contrast ratio
- [ ] UI components: minimum 3:1 contrast ratio
- [ ] Test with contrast checker tools
- [ ] Test in dark mode if supported

### 5.2 Color Independence

- [ ] Never rely on color alone to convey information
- [ ] Add icons or text labels alongside color indicators
- [ ] Use patterns or textures in charts
- [ ] Provide text alternatives for color-coded elements
- [ ] Test in grayscale mode

### 5.3 Focus Indicators

- [ ] Ensure focus indicators have 3:1 contrast
- [ ] Make focus indicators at least 2px wide
- [ ] Use outline-offset for better visibility
- [ ] Test focus visibility on all backgrounds
- [ ] Avoid removing focus styles without replacement

## Phase 6: Images and Media

### 6.1 Images

- [ ] Provide alt text for all meaningful images
- [ ] Use alt="" for decorative images
- [ ] Use aria-hidden="true" for decorative SVGs
- [ ] Describe complex images in surrounding text or aria-describedby
- [ ] Avoid text in images (use CSS or overlay text)
- [ ] Use figure/figcaption for complex images

### 6.2 Icons

- [ ] Hide decorative icons with aria-hidden="true"
- [ ] Provide aria-label for icon-only buttons
- [ ] Use aria-labelledby for icon + text buttons
- [ ] Ensure icon fonts have text fallback
- [ ] Test without icon fonts loaded

### 6.3 Video and Audio

- [ ] Provide captions for all videos
- [ ] Provide transcripts for audio content
- [ ] Provide audio descriptions for video if needed
- [ ] Ensure media controls are keyboard accessible
- [ ] Don't autoplay media
- [ ] Use native video/audio elements or accessible player

## Phase 7: Dynamic Content

### 7.1 Live Regions

- [ ] Use aria-live="polite" for non-urgent updates
- [ ] Use aria-live="assertive" for urgent updates
- [ ] Use role="status" for status updates
- [ ] Use role="alert" for errors/warnings
- [ ] Set aria-atomic="true" for complete announcements
- [ ] Test announcements with screen readers

### 7.2 Single Page Applications

- [ ] Announce route changes to screen readers
- [ ] Update document title on route change
- [ ] Move focus to main content on navigation
- [ ] Use aria-current="page" for current nav item
- [ ] Manage focus on dynamic content insertion
- [ ] Provide loading states during transitions

### 7.3 Modals and Overlays

- [ ] Trap focus within modal
- [ ] Set aria-modal="true" on dialogs
- [ ] Set aria-labelledby pointing to modal title
- [ ] Return focus to trigger element on close
- [ ] Close on Escape key
- [ ] Add backdrop click to close (optional)
- [ ] Prevent body scroll when modal is open

## Phase 8: Mobile and Responsive

### 8.1 Touch Targets

- [ ] Minimum touch target size: 44x44 pixels
- [ ] Add spacing between adjacent touch targets
- [ ] Ensure buttons are easy to tap on mobile
- [ ] Avoid hover-only interactions
- [ ] Test on actual mobile devices

### 8.2 Responsive Design

- [ ] Test at 200% zoom level
- [ ] Ensure text reflows without horizontal scroll
- [ ] Avoid fixed positioning that blocks content
- [ ] Test portrait and landscape orientations
- [ ] Support text resizing without breakage

### 8.3 Motion and Animation

- [ ] Respect prefers-reduced-motion
- [ ] Disable animations for users who prefer reduced motion
- [ ] Avoid auto-playing carousels
- [ ] Provide pause/play controls for animations
- [ ] Avoid flashing content (3 flashes per second max)

## Phase 9: Testing

### 9.1 Automated Testing

- [ ] Run axe or Lighthouse accessibility audit
- [ ] Integrate axe-core into unit tests
- [ ] Test with Pa11y CI in build pipeline
- [ ] Check WAVE browser extension
- [ ] Fix all automated issues before manual testing

### 9.2 Manual Testing

- [ ] Navigate entire site with keyboard only
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Test at 200% zoom
- [ ] Test in high contrast mode
- [ ] Test with browser extensions disabled (ad blockers, etc.)

### 9.3 Screen Reader Testing

- [ ] Test landmark navigation
- [ ] Test heading navigation
- [ ] Test form interaction
- [ ] Test dynamic content announcements
- [ ] Test table navigation
- [ ] Test modal and dialog interaction

### 9.4 Browser Testing

- [ ] Test in Chrome + NVDA
- [ ] Test in Firefox + NVDA
- [ ] Test in Safari + VoiceOver
- [ ] Test in Edge + Narrator (optional)
- [ ] Test mobile Safari + VoiceOver
- [ ] Test mobile Chrome + TalkBack

## Phase 10: Documentation and Maintenance

### 10.1 Documentation

- [ ] Document accessibility features
- [ ] Create accessibility statement page
- [ ] Document keyboard shortcuts
- [ ] Provide contact for accessibility issues
- [ ] Include WCAG conformance level (A, AA, AAA)

### 10.2 Team Training

- [ ] Train developers on WCAG guidelines
- [ ] Train designers on accessible design
- [ ] Train QA on accessibility testing
- [ ] Train content creators on alt text and captions
- [ ] Establish accessibility review process

### 10.3 Ongoing Maintenance

- [ ] Include accessibility in code review checklist
- [ ] Run automated tests on every PR
- [ ] Schedule quarterly manual audits
- [ ] Monitor for regressions
- [ ] Update as WCAG guidelines evolve

## Quick Reference: Common Patterns

### Skip Link

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<main id="main-content">...</main>
```

### Modal Focus Trap

```javascript
// First and last focusable elements
const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
const lastFocusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
const last = lastFocusable[lastFocusable.length - 1];

// Trap focus
modal.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstFocusable) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      firstFocusable.focus();
    }
  }
});
```

### Live Region

```html
<!-- Polite announcements -->
<div role="status" aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

<!-- Urgent announcements -->
<div role="alert" aria-live="assertive" aria-atomic="true">
  {errorMessage}
</div>
```

### Form Error

```html
<label for="email">Email (required)</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Please enter a valid email</span>
```

## Checklist Summary

| Phase | Items | Critical |
|-------|-------|----------|
| Semantic HTML | 20 | 15 |
| Keyboard Navigation | 20 | 18 |
| ARIA Implementation | 25 | 20 |
| Forms and Validation | 18 | 15 |
| Color and Contrast | 12 | 10 |
| Images and Media | 15 | 12 |
| Dynamic Content | 15 | 12 |
| Mobile and Responsive | 12 | 10 |
| Testing | 18 | 15 |
| Documentation | 11 | 5 |
| **Total** | **166** | **132** |
