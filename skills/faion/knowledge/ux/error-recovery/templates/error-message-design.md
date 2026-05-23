# Error Message Design: [Error Type]

## Error Details

- **When it occurs:** [Trigger condition, e.g., "form submitted with invalid email"]
- **Technical cause:** [System reason, e.g., "regex validation failure"]
- **User impact:** [What user cannot do, e.g., "cannot proceed to next step"]

## Message Content

### What happened
[Human-readable description — no technical terms, no error codes]

### Why it happened
[Brief cause explanation that helps user understand, not debug]

### How to fix it
[Specific action the user can take right now]

## Visual Design

- **Placement:** [Where to show — inline next to field / top banner / modal]
- **Style:** [Error indicator — red border + icon + text / banner color]
- **Timing:** [When to show — on blur / on submit / immediately on type]
- **Dismiss:** [Auto / manual — errors require manual dismissal]

## Actions Available

- [Primary action — button label, e.g., "Retry" or "Try a different card"]
- [Secondary action if applicable — e.g., "Work Offline" or "Contact Support"]

## Example Message

```
[Title/Summary — what happened, one line]

[Detailed explanation — why + how to fix]

[Action button 1]   [Action button 2]
```

## Accessibility

- [ ] Error announced via ARIA live region
- [ ] Focus moves to error or error summary on submit
- [ ] Error indicated by icon + text, not color alone
- [ ] Error text meets 4.5:1 contrast ratio
