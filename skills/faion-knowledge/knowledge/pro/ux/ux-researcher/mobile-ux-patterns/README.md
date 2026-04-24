---
id: mobile-ux-patterns
name: "Mobile UX Patterns & Templates"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Mobile UX Patterns & Templates

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #design #mobile #patterns
- **Agent:** faion-usability-agent
- **Related:** mobile-ux-basics.md

---

## Templates

### Mobile Design Checklist Template

```markdown
# Mobile UX Checklist: [Screen/Feature]

**Date:** [Date]
**Designer:** [Name]
**Device targets:** [iOS/Android/Both]

## Touch Targets

- [ ] Primary buttons: 44pt minimum
- [ ] Clickable text links: adequate spacing
- [ ] Form inputs: easy to tap
- [ ] No targets too close together

## Thumb Reachability

- [ ] Primary actions in easy zone
- [ ] Critical CTAs reachable one-handed
- [ ] Toolbar actions accessible

## Navigation

- [ ] Clear back/close actions
- [ ] Current location obvious
- [ ] Key actions visible (not buried)
- [ ] Gestures have visible alternatives

## Content

- [ ] Key content above fold
- [ ] Text readable without zooming (16px minimum)
- [ ] Images sized for mobile
- [ ] Horizontal scrolling avoided

## Forms

- [ ] Appropriate keyboard types (email, number, etc.)
- [ ] Labels visible when typing
- [ ] Error messages near fields
- [ ] Minimal required fields

## Performance

- [ ] Page loads in <3 seconds on 3G
- [ ] Images optimized
- [ ] Loading states present
- [ ] Offline behavior defined

## Gestures

- [ ] Standard gestures only
- [ ] Alternatives for all gestures
- [ ] Accidental gestures prevented

## Orientation

- [ ] Works in portrait (primary)
- [ ] Works in landscape (if needed)
- [ ] No content lost on rotation
```

### Mobile Pattern Documentation

```markdown
# Mobile Pattern: [Pattern Name]

## Overview
[What this pattern is for]

## When to Use
- [Situation 1]
- [Situation 2]

## When NOT to Use
- [Counter-situation]

## Specifications

### iOS
- Size: [Dimensions]
- Font: [Typography]
- Colors: [Color specs]
- Animation: [Motion specs]

### Android
- Size: [Dimensions]
- Font: [Typography]
- Colors: [Color specs]
- Animation: [Motion specs]

## Behavior

**Default State:**
[Description]

**Active/Pressed State:**
[Description]

**Disabled State:**
[Description]

## Accessibility

- VoiceOver/TalkBack: [How it's announced]
- Focus order: [Tab sequence]
- Touch target: [Size]

## Examples

[Screenshots or links]

## Code Reference

[Link to component]
```

---

## Examples

### Example 1: Mobile Checkout Optimization

**Problem:** 68% mobile cart abandonment

**Before:**
- 5-step checkout
- Desktop-sized forms
- No autofill
- Hidden cost summary

**After:**
- 2-step checkout
- Numeric keyboard for phone/card
- Apple Pay / Google Pay
- Sticky order summary

**Result:** Abandonment reduced to 45%

### Example 2: Mobile Search

**Problem:** Users can't find products on mobile

**Changes:**
- Search bar always visible (not in menu)
- Recent searches shown
- Auto-suggest with images
- Filter overlay (not inline)
- Sort as floating button

**Result:** Search usage up 40%

### Example 3: Mobile Navigation Redesign

**Problem:** Users can't find key features

**Before:**
- Hamburger menu with 20 items
- Important features buried 3 levels deep
- No search
- Small touch targets

**After:**
- Bottom tab bar (5 main sections)
- Most-used actions surfaced
- Global search always visible
- 48dp minimum touch targets

**Result:**
- Task completion up 35%
- Time to key features down 60%
- User satisfaction up

### Example 4: Mobile Form Simplification

**Problem:** Registration abandonment at 75%

**Before:**
- 15 fields on one long page
- No field validation
- Generic keyboard for all inputs
- Required fields not marked

**After:**
- 5 essential fields only
- Step indicator (3 steps)
- Email keyboard, numeric keyboard
- Inline validation
- Social login options

**Result:** Abandonment down to 30%

---

## Navigation Patterns Deep Dive

### Bottom Tab Bar

**Best for:**
- 3-5 main sections
- Frequent switching
- Equal importance

**Specifications:**
- iOS: 49pt height
- Android: 56dp height
- Icons: 24-28px
- Labels: 10-12pt

**Guidelines:**
- Always visible
- One tab active
- Icons + labels (or icons only on Android)
- Badges for notifications

### Hamburger Menu

**Best for:**
- 6+ navigation items
- Less frequent access
- Secondary navigation

**Guidelines:**
- Icon: 24x24dp/pt minimum
- Slide from left
- Overlay or push content
- Close with X or back gesture
- Show current location

**Caution:** Research shows 50% less discovery vs. visible nav

### Tab Bar (Content Tabs)

**Best for:**
- 2-5 content categories
- Within one section
- Horizontal content types

**Specifications:**
- Height: 48dp/pt
- Touch target: Full tab width
- Indicator: 2-3dp underline

**Types:**
- Fixed tabs (few items)
- Scrollable tabs (many items)

---

## Form Patterns

### Progressive Disclosure

Show fields as needed:

```
Step 1: Email only
  → Verify email
Step 2: Name + Password
  → Create account
Step 3: Optional profile info
  → Skip or complete
```

### Inline Validation

```
[Input field]
✓ Valid (green check)
✗ Invalid (red, with message)
```

**Rules:**
- Validate on blur (not on keypress)
- Show success for complex fields
- Clear, specific error messages
- Don't validate until user leaves field

### Smart Defaults

| Field | Smart Default |
|-------|---------------|
| **Country** | Detect from IP |
| **Phone** | Format based on country |
| **Date** | Show date picker |
| **Credit card** | Auto-detect card type |

---

## Interaction Patterns

### Pull to Refresh

**Behavior:**
```
1. Pull down from top
2. Show spinner/indicator
3. Fetch new content
4. Animate content update
```

**Guidelines:**
- Works in scrollable lists
- Minimum pull distance: 100-150px
- Haptic feedback
- Cancel if user scrolls back

### Swipe Actions

**Common uses:**
- Swipe left: Delete
- Swipe right: Archive/Complete
- Full swipe: Immediate action
- Partial swipe: Show action buttons

**Guidelines:**
- Reveal actions progressively
- Use familiar icons
- Destructive actions need confirmation
- Provide undo when possible

### Long Press

**Uses:**
- Context menu
- Reorder mode
- Multi-select

**Guidelines:**
- Haptic feedback on activation
- Visual indication (scale, highlight)
- Clear exit method
- Don't hide primary actions behind long press

---

## Loading Patterns

### Skeleton Screens

```
Instead of spinner, show:
[Gray placeholder matching content layout]
  ┌─────────┐
  │ ▓▓▓▓▓   │ ← Image placeholder
  ├─────────┤
  │ ▓▓▓▓▓▓  │ ← Title placeholder
  │ ▓▓▓     │ ← Description
  └─────────┘
```

**Benefits:**
- Feels faster
- Shows layout
- Reduces perceived wait

### Progressive Loading

```
1. Show critical content first
2. Load images lazily
3. Defer below-fold content
4. Pre-fetch likely next steps
```

### Optimistic UI

```
User action
  → Show success immediately
  → Send to server in background
  → If fails, undo and show error
```

**Use for:**
- Like/favorite
- Simple updates
- Non-critical actions

---

## Empty States

### Types

| Type | Message | Action |
|------|---------|--------|
| **First use** | "No items yet" | "Add your first" |
| **User cleared** | "All done!" | "Add more" |
| **No results** | "No matches" | "Try different search" |
| **Error** | "Can't load" | "Try again" |

### Guidelines

- Explain why it's empty
- Provide clear next action
- Use friendly tone
- Consider illustration
- Don't blame user

---

## Error Patterns

### Error Messages

**Structure:**
```
[Icon] What went wrong
       Why it happened (optional)
       [Action Button]
```

**Examples:**

❌ Bad: "Error 404"
✅ Good: "Page not found. It may have been moved."

❌ Bad: "Invalid input"
✅ Good: "Email must include @"

### Retry Patterns

| Scenario | Pattern |
|----------|---------|
| **Network error** | "Retry" button |
| **Server error** | "Retry" + "Contact support" |
| **Temporary** | Auto-retry with countdown |
| **Permanent** | Clear message, alternative path |

---

## Onboarding Patterns

### Types

| Pattern | When to use |
|---------|-------------|
| **Welcome tour** | Complex app, many features |
| **Progressive disclosure** | Learning by doing |
| **Empty state** | Explain as user encounters |
| **Contextual tips** | Just-in-time help |

### Guidelines

```
Keep it short:
- 3-5 screens maximum
- Skip option always visible
- Show value, not features
- Let users try immediately
```

---

## References

- Mobile Design Pattern Gallery by Theresa Neil
- iOS Human Interface Guidelines
- Material Design Guidelines
- Touch Design for Mobile Interfaces by Steven Hoober
- Mobile First by Luke Wroblewski

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Mobile UX Patterns & Templates | haiku | Task execution: applying established methodologies |

## Sources

- [Mobile UX Patterns](https://www.mobile-patterns.com/) - Pattern library
- [Pttrns Mobile Design Patterns](https://www.pttrns.com/) - Screenshot library
- [Mobile Design Patterns](https://www.nngroup.com/articles/mobile-usability/) - Nielsen Norman Group
- [UI Patterns for Mobile Apps](https://www.smashingmagazine.com/2018/02/comprehensive-guide-ui-design/) - Smashing Magazine
- [Mobbin Design Patterns](https://mobbin.design/) - Latest app designs
