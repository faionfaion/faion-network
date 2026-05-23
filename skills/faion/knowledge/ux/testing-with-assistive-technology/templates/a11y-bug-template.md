<!-- purpose: a11y bug report template enforcing WCAG SC + repro + APG + scope -->
<!-- consumes: a11y finding -->
<!-- produces: triage-ready ticket -->
<!-- depends-on: content/01-core-rules.xml bug-report-format rule -->
<!-- token-budget-impact: ~150 tokens when loaded as context -->

# A11y bug: <one-line title>

- **WCAG SC:** 1.4.3 (Contrast minimum)
- **Surface:** web-app / settings page
- **AT used:** VoiceOver 14.x on macOS Sonoma
- **Repro:**
  1. Navigate to /settings
  2. Tab to "Save" button
  3. Observe contrast ratio 3.2:1 against background
- **Suggested APG pattern:** Button (https://www.w3.org/WAI/ARIA/apg/patterns/button/)
- **Scope:** 1 file (theme tokens)
- **Severity:** high
