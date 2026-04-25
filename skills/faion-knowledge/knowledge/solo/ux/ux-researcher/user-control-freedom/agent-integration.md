# Agent Integration — User Control and Freedom

## When to use
- Auditing an existing UI flow for missing undo/cancel/back affordances
- Designing destructive-action flows (delete, bulk operations, account termination)
- Reviewing multi-step wizards or onboarding sequences for exit paths
- Writing acceptance criteria that include recoverability requirements
- Evaluating modals and dialogs for compliance with Nielsen Heuristic #3

## When NOT to use
- When designing intentionally irreversible flows (legal e-signature, financial commit) — those need confirmation, not undo
- When content is already fully auto-saved and loss is impossible — undo adds noise
- As a substitute for full heuristic evaluation — run all 10 heuristics together
- When the UI is purely read-only with no state changes

## Where it fails / limitations
- Undo requires server-side state management; agents cannot assess backend feasibility without architecture context
- Soft-delete patterns depend on retention policy and database schema — audit findings may be blocked by infra constraints
- "Emergency exit" placement differs across mobile vs. desktop — a single audit pass may miss platform-specific gaps
- Confirmation dialogs can be a UX smell (overuse) or a safety net (underuse); agents need product context to judge which applies

## Agentic workflow
An agent drives this heuristic by reading UI specs or design tokens, then systematically enumerating every state-changing action and verifying each has an undo or cancel affordance. The agent generates an audit table, flags gaps with H/M/L severity, and proposes inline fixes. For multi-step flows, the agent traces each step node to verify back-navigation and exit points exist throughout.

### Recommended subagents
- `faion-sdd-executor-agent` — executes quality-gate review tasks that include heuristic audits as acceptance criteria
- No dedicated usability agent exists in the current agents/ directory; embed as a Claude subagent call inline

### Prompt pattern
```
Audit this UI flow spec for User Control and Freedom (Nielsen #3).
For each state-changing action, verify:
1. Is undo available? If not, is a confirmation dialog shown?
2. Is cancel/back available at every step?
3. Are modals closeable via X, Escape, outside-click?
Return a markdown table: Action | Undo? | Cancel? | Severity | Fix.
```

```
Given this list of destructive actions: [list]
Classify each as: (a) reversible → add undo, (b) irreversible → add confirmation,
(c) irreversible + catastrophic → add confirmation + delay.
Justify each classification.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| axe-core CLI | Accessibility audit (catches focus-trap and keyboard issues) | `npm i -g axe-cli` / axe-core.com |
| Playwright | Scripted keyboard navigation tests (Escape, Tab, Back) | `npm i -D @playwright/test` / playwright.dev |
| pa11y | Automated a11y checks including ARIA roles on dialogs | `npm i -g pa11y` / pa11y.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma (Plugins API) | SaaS | Partial | Agents can read design JSON via REST; no write-back without plugin |
| UserTesting | SaaS | No | Human moderated; results require human review |
| Maze | SaaS | No | Automated usability tests but analysis requires human interpretation |
| NN/g Articles | Reference | Yes | Agents can fetch and cite heuristic definitions directly |

## Templates & scripts
See `templates.md` for the User Control Audit template (action/exit/destructive tables).

Playwright snippet to verify Escape closes all modals:
```js
// test: escape closes every modal
for (const trigger of modalTriggers) {
  await page.click(trigger);
  await page.keyboard.press('Escape');
  await expect(page.locator('[role="dialog"]')).toBeHidden();
}
```

## Best practices
- Implement soft-delete (trash with 30-day retention) before adding delete confirmation dialogs — undo is always better UX than "are you sure?"
- Use toast + inline Undo button (5-10 second timeout) for frequent reversible actions; never block the user with a modal
- Confirm only truly irreversible, high-impact actions — every unnecessary confirmation trains users to click "OK" blindly
- In multi-step wizards, persist form state across back-navigation; losing input on Back is a control-and-freedom failure
- Escape key must always dismiss any overlay; test this explicitly with Playwright or Cypress keyboard assertions
- For long server-side operations (upload, publish), always expose a Cancel that sends an actual cancellation request — a Cancel button that does nothing is worse than no button

## AI-agent gotchas
- Agent-generated audit tables flag "undo missing" without knowing if the action is server-side-irreversible; always hand off severity judgment to a human reviewer
- LLMs tend to over-recommend confirmation dialogs — push back with "prefer undo" as a default in the prompt
- Agents cannot test actual keyboard behavior; Playwright tests must run in CI to catch Escape/focus-trap regressions
- When generating fix recommendations, agents should not hardcode UI copy ("Item deleted. Undo?") without localization review — flag as [COPY NEEDED]
- Multi-language RTL layouts may reverse button order (Cancel/OK vs OK/Cancel); agent audits based on LTR specs will miss this

## References
- https://www.nngroup.com/articles/user-control-and-freedom/
- https://www.nngroup.com/articles/ten-usability-heuristics/
- Norman, D. — The Design of Everyday Things (2013 revised ed.), Ch. 5 on error prevention
- https://www.smashingmagazine.com/2012/07/undo-design-patterns/
- https://www.uxmatters.com/mt/archives/2010/03/providing-sufficient-user-control.php
