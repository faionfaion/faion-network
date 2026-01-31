# WCAG 2.2 Compliance

## Problem

WCAG 2.2 released October 2023 is becoming the baseline compliance standard by 2025-2026. Organizations still on WCAG 2.0 or 2.1 need to update.

## What's New in WCAG 2.2

### 9 New Success Criteria

| Criterion | Level | Category | Requirement |
|-----------|-------|----------|-------------|
| **2.4.11 Focus Not Obscured (Minimum)** | AA | Operable | Focus indicator at least partially visible (not fully obscured) |
| **2.4.12 Focus Not Obscured (Enhanced)** | AAA | Operable | Focus indicator fully visible (no part obscured) |
| **2.4.13 Focus Appearance** | AAA | Operable | Focus indicator: 2px minimum thickness, sufficient contrast |
| **2.5.7 Dragging Movements** | AA | Operable | All drag actions have non-drag alternative (click, keyboard) |
| **2.5.8 Target Size (Minimum)** | AA | Operable | Touch/click targets 24x24 CSS pixels minimum |
| **3.2.6 Consistent Help** | A | Understandable | Help mechanism in same location across pages |
| **3.3.7 Redundant Entry** | A | Understandable | Don't ask for same info twice in session |
| **3.3.8 Accessible Authentication (Minimum)** | AA | Understandable | No cognitive function tests for login (no puzzles, memorization) |
| **3.3.9 Accessible Authentication (Enhanced)** | AAA | Understandable | No object/image recognition for login (no CAPTCHA) |

### 2.4.11 Focus Not Obscured (Minimum) - Level AA

**Requirement:**
When component receives keyboard focus, indicator is at least partially visible (not completely hidden).

**Fails:**
```
Focus indicator completely hidden by:
→ Sticky header
→ Cookie banner
→ Chat widget
→ Modal overlay
```

**Passes:**
```
Focus indicator visible:
→ Scroll to bring into view
→ Move sticky elements aside
→ Adjust z-index appropriately
→ Ensure focus visible portion
```

### 2.5.7 Dragging Movements - Level AA

**Requirement:**
All drag-and-drop operations must have non-drag alternative.

**Examples:**

| Drag Action | Alternative Required |
|-------------|---------------------|
| Drag to reorder list items | Up/down buttons, cut/paste |
| Drag to resize element | Input field for dimensions |
| Drag to select area | Click corners, keyboard selection |
| Drag slider | Arrow keys, input field |
| Drag to upload file | Click to browse, keyboard |

**Implementation:**
```html
<!-- Drag to reorder -->
<ul>
  <li>
    Item 1
    <button aria-label="Move up">↑</button>
    <button aria-label="Move down">↓</button>
  </li>
</ul>

<!-- Drag to resize -->
<div>
  <label>Width: <input type="number" value="200"> px</label>
  <label>Height: <input type="number" value="100"> px</label>
</div>
```

### 2.5.8 Target Size (Minimum) - Level AA

**Requirement:**
Touch/click targets minimum 24x24 CSS pixels (WCAG 2.2 AA).

**Note:** This is more lenient than previous guidelines recommending 44x44px.

**Exceptions:**
- Inline links in sentences
- User-controlled size
- Essential presentation (flags, maps)
- Target has 24px spacing around it

**Implementation:**
```css
/* Minimum 24x24px */
.button {
  min-width: 24px;
  min-height: 24px;
}

/* Recommended 44x44px for mobile */
@media (pointer: coarse) {
  .button {
    min-width: 44px;
    min-height: 44px;
  }
}

/* Spacing alternative */
.small-button {
  width: 16px;
  height: 16px;
  margin: 4px; /* 16 + 8 = 24px target area */
}
```

### 3.2.6 Consistent Help - Level A

**Requirement:**
If help mechanism available on multiple pages, it must be in same relative order.

**Examples:**
```
Consistent:
→ "Help" link always in header (same position)
→ "Contact us" always in footer
→ Chat widget always bottom-right
→ FAQ link in same sidebar position

Inconsistent (fails):
→ Help link moves around header
→ Sometimes in menu, sometimes in footer
→ Order changes between pages
```

### 3.3.7 Redundant Entry - Level A

**Requirement:**
Don't ask for same information twice unless necessary for security, previous entry no longer valid, or essential.

**Fails:**
```
Multi-step form:
Step 1: Enter email
Step 2: Enter email again (for no reason)

Checkout:
Billing address: [form]
Shipping address: [same form, no "same as billing" option]
```

**Passes:**
```
Multi-step form:
Step 1: Enter email (saved)
Step 2: Email pre-filled or not asked

Checkout:
Billing address: [form]
☑ Shipping same as billing (auto-fills)
```

**Exceptions:**
- Re-entering password for confirmation (security)
- Information changed (need to reverify)
- Essential (legal requirement)

### 3.3.8 Accessible Authentication (Minimum) - Level AA

**Requirement:**
Login doesn't require cognitive function test (no memorization, puzzles, calculations).

**Fails:**
```
❌ Remember complex password exactly
❌ Math problems (2 + 2 = ?)
❌ "Type the 3rd and 7th character of your password"
❌ Pattern drawing from memory
```

**Passes:**
```
✅ Password managers allowed
✅ Copy/paste enabled
✅ Biometrics (fingerprint, face ID)
✅ Email magic links
✅ SMS codes (object recognition, not memorization)
✅ Passkeys / WebAuthn
```

**Implementation:**
```html
<!-- Allow paste -->
<input type="password" autocomplete="current-password">

<!-- Support password managers -->
<input type="email" autocomplete="username">
<input type="password" autocomplete="current-password">
```

### 3.3.9 Accessible Authentication (Enhanced) - Level AAA

**Requirement:**
Login doesn't require object or user recognition (no CAPTCHA with images).

**Fails:**
```
❌ Image CAPTCHA ("Select all traffic lights")
❌ Distorted text CAPTCHA
❌ Audio CAPTCHA (sound recognition)
```

**Passes:**
```
✅ Invisible reCAPTCHA (behavior analysis)
✅ hCaptcha (accessibility mode)
✅ Rate limiting / device fingerprinting
✅ Honeypot fields
✅ Email verification
```

## Migration from WCAG 2.1 to 2.2

### Changes to Existing Criteria

**2.4.7 Focus Visible (Level AA) - Modified**
- Now requires focus indicator for all components
- More specific requirements
- Links to new 2.4.11, 2.4.12, 2.4.13

### Obsolete Criteria

**4.1.1 Parsing (Level A) - REMOVED**
- Browsers now handle HTML parsing errors
- No longer necessary to test
- Validation still good practice

## Implementation Checklist

**Quick Wins (Low Effort, High Impact):**
- [ ] Enable password paste
- [ ] Add autocomplete to forms
- [ ] "Same as billing" checkbox
- [ ] Ensure focus not obscured by sticky elements
- [ ] Check target sizes (24x24px minimum)

**Moderate Effort:**
- [ ] Add keyboard alternatives to drag-and-drop
- [ ] Ensure help links consistent location
- [ ] Pre-fill forms where possible
- [ ] Remove cognitive function tests from auth

**Higher Effort:**
- [ ] Implement passkey authentication
- [ ] Replace image CAPTCHAs (AAA)
- [ ] Audit all focus visibility (AA/AAA)
- [ ] Comprehensive form redundancy review

## Testing for WCAG 2.2

**Automated Tools (partial coverage):**
- axe DevTools (supports some 2.2 criteria)
- WAVE (being updated)
- Lighthouse (being updated)

**Manual Testing Required:**
- Focus not obscured (scroll, sticky elements)
- Drag alternatives (try all interactions)
- Target sizes (measure in DevTools)
- Consistent help (navigate multiple pages)
- Redundant entry (complete full form flow)
- Authentication (try with password manager)

## Timeline

**Adoption:**
- WCAG 2.2: October 2023 (published)
- EU: Expected requirement 2025-2026
- US ADA: WCAG 2.1 AA required April 2026 (2.2 future)
- EN 301 549: Will incorporate 2.2 in next update

**Recommendation:**
- Aim for WCAG 2.2 AA compliance now
- Future-proof your accessibility
- Easier to implement incrementally

## Sources

- [W3C: WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)
- [W3C: What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [Deque: WCAG 2.2 Quick Reference](https://www.deque.com/blog/wcag-2-2-is-here/)
- [WebAIM: WCAG 2.2 Overview](https://webaim.org/articles/wcag22/)
- [TPGi: WCAG 2.2 Map](https://www.tpgi.com/wcag-2-2-all-new-success-criteria/)
