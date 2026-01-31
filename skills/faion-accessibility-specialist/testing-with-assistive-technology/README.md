# Testing with Assistive Technology

## Problem

Automated testing catches only 30-50% of accessibility issues. Manual review improves this to 50-70%, but real assistive technology testing is essential to find the remaining issues.

## Solution: Manual + Assistive Tech Testing

### Testing Layers

```
Automated (30-50%)
  → Manual review (50-70%)
    → Screen reader (70-85%)
      → Keyboard-only (80-90%)
        → User testing (95%+)
```

## Screen Reader Testing

### Screen Readers by Platform

| OS | Screen Reader | Browser | Cost | Market Share |
|----|---------------|---------|------|--------------|
| **Windows** | NVDA (free) | Firefox, Chrome | Free | ~40% |
| **Windows** | JAWS | Chrome, Edge, Firefox | $95-1500 | ~40% |
| **macOS** | VoiceOver | Safari | Built-in | ~15% |
| **iOS** | VoiceOver | Safari | Built-in | Mobile leader |
| **Android** | TalkBack | Chrome | Built-in | Android default |
| **Linux** | Orca | Firefox | Free | <1% |

### Screen Reader Basics

**NVDA (Windows - Recommended for Testing):**
```
Download: nvaccess.org
Activation: NVDA + Space
Stop speech: Ctrl
Navigate headings: H (next), Shift+H (previous)
Navigate links: K (next), Shift+K (previous)
Forms mode: Automatic on form entry
Read all: NVDA + Down Arrow
```

**JAWS (Windows - Enterprise Standard):**
```
Activation: Caps Lock or Insert
Stop speech: Ctrl
Virtual cursor: Arrow keys
Forms mode: Enter/Space on form element
Read all: Insert + Down Arrow
```

**VoiceOver (Mac/iOS - Apple Ecosystem):**
```
macOS activation: Cmd + F5
iOS activation: Triple-click home/side button
VoiceOver modifier: Ctrl + Option (VO)
Navigate: VO + Right/Left Arrow
Interact: VO + Shift + Down Arrow
Rotor: VO + U (web navigation menu)
```

**TalkBack (Android):**
```
Activation: Volume keys up+down simultaneously
Navigate: Swipe right/left
Activate: Double tap
Context menu: Swipe down then right (L shape)
Reading controls: Swipe up/down
```

### Screen Reader Testing Checklist

**Content:**
- [ ] All images have alt text
- [ ] Alt text is meaningful (not generic)
- [ ] Decorative images marked as such (alt="")
- [ ] Complex images have long descriptions
- [ ] Icons have accessible labels

**Structure:**
- [ ] Headings present and hierarchical (H1 → H2 → H3)
- [ ] Landmarks defined (main, nav, header, footer)
- [ ] Lists marked up properly
- [ ] Tables have headers and scope
- [ ] Reading order matches visual order

**Forms:**
- [ ] All inputs have associated labels
- [ ] Error messages announced
- [ ] Required fields marked
- [ ] Helper text associated with inputs
- [ ] Field groups have legends
- [ ] Form validation is accessible

**Navigation:**
- [ ] Skip links work
- [ ] All links have descriptive text
- [ ] Link purpose clear from context
- [ ] No "click here" links
- [ ] Current page indicated

**Dynamic Content:**
- [ ] ARIA live regions for updates
- [ ] Loading states announced
- [ ] Success/error messages announced
- [ ] Modal dialogs trap focus
- [ ] Modals announced on open

**Custom Components:**
- [ ] Correct ARIA roles
- [ ] ARIA states and properties
- [ ] Keyboard interaction works
- [ ] Focus management correct
- [ ] Screen reader announcements clear

## Keyboard Testing

### Why Keyboard Testing Matters

- Screen reader users navigate by keyboard
- Motor disability users may not use mouse
- Power users prefer keyboard
- Touch users need keyboard equivalent
- Legal requirement (WCAG)

### Keyboard Navigation Basics

| Action | Keys |
|--------|------|
| **Navigate forward** | Tab |
| **Navigate backward** | Shift + Tab |
| **Activate button/link** | Enter (or Space for buttons) |
| **Navigate dropdown** | Arrow keys |
| **Select checkbox/radio** | Space |
| **Exit/Cancel** | Escape |
| **Skip to main** | Skip link (Tab from top) |

### Keyboard Testing Checklist

**Basic Navigation:**
- [ ] All interactive elements reachable by Tab
- [ ] Tab order matches visual flow
- [ ] Tab order is logical
- [ ] Skip links present (skip to main content)
- [ ] No keyboard traps (can Tab out)

**Focus Indicators:**
- [ ] Focus indicator always visible
- [ ] Focus indicator sufficient contrast (3:1 minimum)
- [ ] Focus indicator not hidden by other elements
- [ ] Custom focus states implemented
- [ ] Focus doesn't jump unexpectedly

**Interactive Elements:**
- [ ] Buttons activate with Enter and Space
- [ ] Links activate with Enter
- [ ] Dropdowns open with Enter/Space
- [ ] Dropdowns navigate with arrows
- [ ] Checkboxes toggle with Space
- [ ] Radio buttons select with arrows
- [ ] Text inputs receive text immediately

**Custom Components:**
- [ ] Accordions work (Enter to expand/collapse)
- [ ] Tabs work (Arrow keys to switch)
- [ ] Modals trap focus
- [ ] Modals close with Escape
- [ ] Carousels navigate with keys
- [ ] Tooltips appear on focus

**Complex Interactions:**
- [ ] Drag-and-drop has keyboard alternative
- [ ] Sliders work with arrow keys
- [ ] Multi-select works with Shift/Ctrl + arrows
- [ ] Context menus accessible
- [ ] All gestures have keyboard equivalent

## Common Issues Found

### Top Screen Reader Issues

1. **Missing form labels**
   - Input announces as "Edit, blank"
   - Fix: `<label for="email">Email</label>`

2. **No skip navigation**
   - Must tab through entire nav every page
   - Fix: Add skip link to main content

3. **Inaccessible custom components**
   - Custom select announces as "Group"
   - Fix: Use proper ARIA roles and states

4. **Missing alt text**
   - Image announces as filename
   - Fix: Add meaningful alt attribute

5. **Poor focus management**
   - Focus lost after modal closes
   - Fix: Return focus to trigger element

6. **Keyboard traps**
   - Cannot Tab out of modal or widget
   - Fix: Implement Escape key and proper focus management

### Typical Keyboard Issues

1. **No visible focus**
   - `outline: none` without replacement
   - Fix: Provide clear custom focus style

2. **Illogical tab order**
   - Tab order doesn't match visual layout
   - Fix: Adjust source order or use tabindex carefully

3. **Mouse-only interactions**
   - Hover menus, custom controls
   - Fix: Add keyboard equivalents

4. **Missing skip links**
   - Must tab through entire header
   - Fix: Add skip to main content link

5. **Enter/Space not working**
   - Custom buttons don't activate
   - Fix: Add keydown event handlers

## Testing Workflow

### Quick Test (15 minutes)

```
1. Keyboard test (5 min)
   → Tab through entire page
   → Can you reach everything?
   → Is focus always visible?

2. Screen reader spot check (5 min)
   → Navigate headings (H key)
   → Navigate landmarks (D key in NVDA)
   → Try one form

3. Automated scan (5 min)
   → Run axe DevTools
   → Check critical issues
```

### Comprehensive Test (2-4 hours)

```
1. Automated scan (30 min)
   → axe DevTools full scan
   → WAVE scan
   → Lighthouse audit
   → Document all issues

2. Keyboard navigation (1 hour)
   → Full page Tab through
   → Test all interactions
   → Custom components
   → Document keyboard issues

3. Screen reader testing (1-2 hours)
   → NVDA + Firefox (or JAWS + Chrome)
   → Navigate by headings
   → Navigate by landmarks
   → Test all forms
   → Test dynamic content
   → Document issues

4. Mobile screen reader (30 min)
   → VoiceOver on iOS Safari
   → TalkBack on Android Chrome
   → Test gestures
   → Test forms
```

## Learning Screen Readers

### NVDA Quick Start

1. **Install:** Download from nvaccess.org
2. **Start:** Run NVDA, it speaks immediately
3. **Stop speech:** Press Ctrl
4. **Basic navigation:**
   - Tab: Move through page
   - H: Next heading
   - K: Next link
   - F: Next form field
   - NVDA + Down Arrow: Read all
5. **Practice:** Try on bbc.com or gov.uk

### VoiceOver Quick Start (Mac)

1. **Start:** Cmd + F5
2. **Basics:**
   - VO = Ctrl + Option
   - Navigate: VO + Right/Left Arrow
   - Interact: VO + Shift + Down Arrow
   - Exit: VO + Shift + Up Arrow
3. **Rotor:** VO + U (navigation menu)
4. **Practice:** Try on apple.com

## Sources

- [WebAIM: Screen Reader Testing](https://webaim.org/articles/screenreader_testing/)
- [NVDA User Guide](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [Apple: VoiceOver Getting Started](https://support.apple.com/guide/voiceover/welcome/mac)
- [Deque: Keyboard Testing](https://www.deque.com/blog/keyboard-testing/)
- [Google: TalkBack Guide](https://support.google.com/accessibility/android/answer/6283677)
