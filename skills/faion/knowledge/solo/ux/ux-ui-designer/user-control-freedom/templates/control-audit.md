# User Control Audit: [Feature]

**Reviewer:** [Name]

## Actions × Control Mechanisms

| Action | Undo Available? | Cancel Available? | Exit Mechanism | Recovery Method | Severity Gap | Recommendation |
|--------|-----------------|-------------------|----------------|-----------------|--------------|----------------|
| [Action] | Y/N | Y/N | [X/Escape/outside] | [How to recover] | H/M/L/None | [Fix] |

Severity: High = irreversible + no confirmation + no undo; Medium = reversible but no user feedback; Low = minor inconvenience.

## Exit Points

| Context | Exit Available? | Methods | Notes |
|---------|-----------------|---------|-------|
| [Modal/dialog] | Y/N | [X + Escape + outside] | |
| [Multi-step flow] | Y/N | [Back + Cancel] | |

## Destructive Actions

| Action | Confirmation? | Undo? | Soft Delete? | Assessment |
|--------|---------------|-------|--------------|------------|
| [Action] | Y/N | Y/N | Y/N | [Appropriate?] |

## Keyboard Accessibility

| Control | Keyboard? | Screen Reader? | Focus Managed? |
|---------|-----------|----------------|----------------|
| Undo (Ctrl+Z) | Y/N | — | — |
| Escape closes modals | Y/N | Y/N | Y/N |
| Cancel button labeled | Y/N | Y/N | — |

## Priority Gaps

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| [Gap] | H/M/L | [Fix] |
