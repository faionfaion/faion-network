# Error Message Design: [Error Type]

## Error Context

- **When it occurs:** [Trigger condition — what user action or system event causes this]
- **Technical cause:** [System-level reason, for dev reference]
- **User impact:** [What the user cannot do as a result]

## Message Content

### What happened (problem statement)
[Plain language description — no technical terms]

### Why it happened (context)
[Brief explanation the user can understand]

### How to fix it (action)
[Specific instruction or action the user can take]

## Visual Design

- **Placement:** [Inline next to field / Banner / Modal / Full page]
- **Style:** [Error icon + red border / Banner color / Modal type]
- **Timing:** [When to show: on blur / on submit / on system failure]
- **Dismissal:** [How it goes away: when user corrects / user dismisses / automatically]

## Recovery Actions

| Button/Link | Action |
|-------------|--------|
| [Primary action] | [What it does] |
| [Secondary action] | [What it does] |

## Assembled Message Example

```
[Short title/summary]

[Detailed explanation in plain language]

[Specific suggested fix]

[Primary Action Button]  [Secondary Action Button]
```

## Accessibility Checklist

- [ ] Error not communicated by color alone (icon or text label present)
- [ ] ARIA role="alert" or live region used
- [ ] Focus moves to error message or first invalid field on form submit
- [ ] Error text has sufficient contrast ratio (4.5:1 minimum)
- [ ] Screen reader readable without visual context
