# Agent Integration — User Control and Freedom

## When to use
- Heuristic audit of a feature spec or UI description for missing undo/cancel/exit mechanisms
- Generating a User Control Audit report (action table with undo/cancel/recovery columns) from a screen list
- Code review assistance: checking that destructive actions in backend code have corresponding soft-delete or undo hooks
- Accessibility review: verifying keyboard escape paths and focus management in modal/dialog flows
- Design review of multi-step wizards or onboarding flows for trapped-user patterns

## When NOT to use
- As a substitute for actual usability testing — agent can identify structural absence of controls, but cannot assess whether users actually feel trapped without behavioral data
- For complex undo architecture in database-backed systems — agent can identify the need and pattern, but undo implementation requires engineering judgment about consistency and rollback scope
- When the system genuinely cannot support undo (e.g., sent emails, executed financial transactions) — agent should note this, but the design solution (clear warnings, confirmation dialogs) requires human decision

## Where it fails / limitations
- Agent works from described or listed UI elements; it cannot detect missing controls in rendered interfaces it cannot see
- Undo feasibility depends on backend architecture (event sourcing, soft deletes, transaction logs) — agent cannot assess technical feasibility without codebase context
- Confirmation dialog recommendations may be excessive for the actual risk level; human designer judgment is needed to calibrate warning frequency
- Agent has no access to usage data showing where users actually abandon or feel stuck

## Agentic workflow
A Claude subagent receives a list of user-facing actions (e.g., from a feature spec or screen inventory) and outputs a User Control Audit table: each action rated for Undo availability, Cancel availability, Exit mechanism, and Recovery method. It flags gaps as High/Medium/Low severity based on action destructiveness. For each gap, it outputs a specific remediation recommendation drawn from the heuristic patterns (undo toast, soft delete, multi-step exit, confirmation dialog).

### Recommended subagents
- `faion-sdd-executor-agent` — execute the audit as a structured SDD task with documented findings
- General Claude subagent with UX heuristics role — review feature specs for missing control patterns

### Prompt pattern
```
You are a UX auditor applying Nielsen's Heuristic #3 (User Control and Freedom).
Given the list of user actions below, produce a User Control Audit table with columns:
Action | Undo Available | Cancel Available | Exit Mechanism | Recovery Method | Severity Gap | Recommendation

Severity: High = irreversible + no confirmation; Medium = reversible but no feedback; Low = minor inconvenience.
For each High severity gap, provide a specific implementation recommendation.

Actions to audit:
[list of user-visible actions, e.g.: "delete account", "submit order", "publish post", ...]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| axe-core CLI | Flags missing keyboard escape paths, focus traps in dialogs | `npm install -g @axe-core/cli` / https://github.com/dequelabs/axe-core |
| Playwright | Scripted keyboard navigation testing — verify Escape key closes modals, Back button works | `npm install -D playwright` / https://playwright.dev |
| jest-axe | Unit-test accessibility (including focus management) in React component tests | `npm install -D jest-axe` / https://github.com/nickcolley/jest-axe |
| pa11y | CLI accessibility runner; catches missing dialog close mechanisms | `npm install -g pa11y` / https://pa11y.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial (REST read) | Export flow/prototype structure; agent checks for back/cancel linkages in prototype connections |
| Deque Axe Monitor | SaaS | Yes (API) | Automated a11y scanning including focus trap detection; REST API for results |
| Hotjar / FullStory | SaaS | No direct agent API | Rage-click and exit heatmaps reveal where users feel trapped; export data for agent context |
| PostHog | OSS/SaaS | Yes (REST API) | Session recordings + event data; use to identify rage-click patterns on non-cancellable flows |
| Sentry | OSS/SaaS | Yes (API) | If trapped users trigger error states (back button = 404, etc.), Sentry captures these |

## Templates & scripts
See `templates.md` for the User Control Audit template. Below is a Playwright snippet to verify modal Escape-key behavior:

```javascript
// verify-escape-exits.spec.js — check that all modals close on Escape
const { test, expect } = require('@playwright/test');

const MODAL_TRIGGERS = [
  { trigger: '[data-testid="delete-btn"]', modal: '[role="dialog"]' },
  { trigger: '[data-testid="settings-btn"]', modal: '[aria-label="Settings"]' },
  // Add more trigger/modal pairs as needed
];

for (const { trigger, modal } of MODAL_TRIGGERS) {
  test(`Escape closes modal triggered by ${trigger}`, async ({ page }) => {
    await page.goto(process.env.BASE_URL || 'http://localhost:3000');
    await page.click(trigger);
    await expect(page.locator(modal)).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator(modal)).not.toBeVisible();
  });
}
```

## Best practices
- Prefer undo over confirmation for reversible actions — undo feels less disruptive and reduces friction for expert users
- Use soft delete (move to trash/archive) by default for any content deletion; permanent delete requires explicit secondary confirmation
- Every modal must have at least three exit paths: X button, Escape key, and clicking outside — implement all three, not just one
- In multi-step wizards, always show step count and provide Back on every step except the first; an Exit option should persist throughout
- Avoid "Are you sure?" confirmations for non-destructive actions — confirmation fatigue causes users to click through without reading
- Auto-save + discard-on-exit is safer than Save/Cancel for form editing — removes the decision burden while preserving control

## AI-agent gotchas
- Agent audit based on action names alone may miss context-dependent severity; "delete" in a shopping cart (trivially reversible) is different from "delete account" (high stakes)
- Agent cannot detect focus traps in rendered interfaces without accessibility tooling; always pair agent audit with axe-core or pa11y run
- Human-in-loop checkpoint: undo/cancel implementation decisions require engineering sign-off; agent audit identifies the need, not the implementation approach
- Agent may recommend confirmation dialogs for actions where the better solution is undo (more modern, less disruptive); review recommendations against the undo-vs-confirmation heuristic in the README
- Keyboard shortcut verification (Escape, Ctrl+Z) requires live browser testing; agent cannot substitute for Playwright or manual keyboard navigation checks

## References
- https://www.nngroup.com/articles/user-control-and-freedom/
- https://www.smashingmagazine.com/2012/07/undo-design-patterns/
- https://www.uxmatters.com/mt/archives/2010/03/providing-sufficient-user-control.php
- https://alistapart.com/article/giveuserscontrol/
- Don Norman, *The Design of Everyday Things* (revised ed.)
