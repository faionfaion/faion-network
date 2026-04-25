# Agent Integration — Visibility of System Status (Nielsen Heuristic #1)

## When to use
- Auditing any interactive UI where user actions trigger asynchronous operations (form submissions, file uploads, API calls, background jobs)
- Code review: checking that every button, link, and form has loading, success, and error states implemented
- Before a launch: sweep all user flows to verify no "dead click" moments where the UI appears unresponsive
- When support tickets or session recordings show users double-clicking or resubmitting forms
- Designing real-time features (chat, live data feeds, collaborative editing) where continuous state communication is critical

## When NOT to use
- Static informational pages with no interactive elements — no states to communicate
- Background operations the user does not need to know about (e.g., background cache refresh that completes in <100ms)
- Micro-interactions that are already covered by platform defaults (OS-level progress bars for file transfers)
- When audit findings for this heuristic are already documented and tracked — don't re-audit, fix the known issues

## Where it fails / limitations
- Agents can detect missing loading states in component code but cannot verify that the state is visually perceivable (contrast, animation speed, placement on screen)
- Toast notifications and banners are easy to miss — position, timing, and contrast must be validated visually, not just by code inspection
- Real-time status (WebSocket, SSE) requires testing under actual network conditions — static analysis cannot simulate latency or disconnection
- ARIA live region correctness requires screen reader testing; agents can add the attribute but cannot verify the announcement behavior
- Progress bar accuracy depends on backend progress events — if the backend sends no progress updates, the bar becomes indeterminate regardless of design intent

## Agentic workflow
An agent can systematically review component files for interactive elements (buttons, forms, links) and verify that each has at minimum: a loading state (disabled + spinner or text change), a success state (confirmation), and an error state (error message). It produces a gap report sorted by severity. The agent should also check ARIA attributes (`aria-busy`, `aria-live`, `role="status"`) for accessibility compliance. Human visual verification of timing and placement is the required checkpoint before marking issues as resolved.

### Recommended subagents
- `faion-usability-agent` — full heuristic review with heuristic #1 as primary focus
- general code agent — scans component library for all interactive elements and maps them to their implemented states

### Prompt pattern
```
Review the following React/HTML component. For each interactive element (button, form, link, input):
1. Does it have a loading state? (disabled + visual indicator)
2. Does it have a success state? (confirmation message or visual change)
3. Does it have an error state? (error message with recovery action)
4. Is there an ARIA attribute for dynamic state (aria-busy, aria-live, role="status")?
Report missing states as: MISSING | PARTIAL | PRESENT
Include file:line for each finding.
```

```
Given the following response time data for API endpoints (endpoint, p50_ms, p95_ms, p99_ms),
recommend the appropriate loading indicator type for each endpoint:
- <100ms: no indicator needed
- 100ms-1s: spinner or button state change
- 1s-10s: progress bar or skeleton screen
- >10s: progress bar with percentage + cancel option
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` CLI | Detects ARIA live region and status role violations | `npm i -g @axe-core/cli` / github.com/dequelabs/axe-core |
| `playwright` CLI | Automates interaction flows and can assert UI state changes after async operations | `npm i -D @playwright/test` / playwright.dev |
| `lighthouse` CLI | Detects missing button disabled states and interaction-blocking patterns | `npm i -g lighthouse` / github.com/GoogleChrome/lighthouse |
| `eslint-plugin-jsx-a11y` | Static lint for ARIA attributes; catches missing `aria-live` on dynamic regions | `npm i -D eslint-plugin-jsx-a11y` / github.com/jsx-eslint/eslint-plugin-jsx-a11y |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LogRocket | SaaS | Yes — REST API | Session recordings; agent can query sessions with rage-clicks to find unresponsive elements |
| FullStory | SaaS | Yes — REST API | Rage-click and dead-click detection; surfaces elements that lack visible feedback |
| Hotjar | SaaS | Partial | Rage-click heatmaps; visual review required |
| Sentry | SaaS | Yes — REST API | Pairs error events with user interactions; shows which actions produce silent errors |
| Datadog RUM | SaaS | Yes — API | Real user monitoring with interaction timing; agent can query p95 interaction response times |
| Checkly | SaaS | Yes — CLI | Synthetic monitoring; can assert that loading states appear and resolve within SLA |

## Templates & scripts
See `templates.md` for the Status Feedback Audit template.

Inline Playwright test — verify loading state appears on form submit:
```typescript
// tests/loading-state.spec.ts
import { test, expect } from '@playwright/test';

test('submit button shows loading state during async operation', async ({ page }) => {
  await page.goto('/checkout');
  await page.fill('[name="email"]', 'test@example.com');

  const submitButton = page.locator('button[type="submit"]');

  // Click and immediately check for loading state
  const [, loadingState] = await Promise.all([
    submitButton.click(),
    // Loading state should appear within 100ms
    expect(submitButton).toHaveAttribute('aria-busy', 'true', { timeout: 100 }),
  ]);

  // Button should be disabled during load
  await expect(submitButton).toBeDisabled();

  // Wait for completion and verify success or error state
  await expect(page.locator('[role="status"]')).toBeVisible({ timeout: 10000 });
});

test('file upload shows progress indicator', async ({ page }) => {
  await page.goto('/upload');
  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser'),
    page.click('[data-testid="upload-trigger"]'),
  ]);
  await fileChooser.setFiles('tests/fixtures/sample.pdf');
  await expect(page.locator('[role="progressbar"]')).toBeVisible({ timeout: 500 });
});
```

## Best practices
- Every clickable element must give visible feedback within 100ms of the click — if the operation takes longer, show a loading state immediately, then update when complete
- Disable the trigger element (button, link) during async operations to prevent double-submission — re-enable on success or error
- Distinguish between skeleton screens (known layout, loading content) and spinners (unknown layout or very short wait) — use the right pattern for the context
- Document auto-dismiss timing for toast notifications: 3-5 seconds for success, indefinite for errors (user must dismiss manually)
- "All changes saved" document status is more reassuring than a save button — continuous auto-save with status text outperforms explicit save actions for documents
- Connection status indicators (online/offline/reconnecting) are required for any real-time feature — users need to know if their actions are being persisted
- Provide a cancel option for operations that take >10 seconds — users should not be trapped waiting

## AI-agent gotchas
- Agents can add loading state code but cannot verify that the spinner animation actually runs (CSS animation may be disabled by OS "Reduce Motion" setting — must be handled separately)
- Static analysis of components misses loading states that are implemented at the page/container level rather than the component level — audit must trace data flow, not just component props
- ARIA `aria-live="polite"` and `aria-live="assertive"` have different screen reader behaviors; agents often use "assertive" where "polite" is correct, causing disruptive announcements
- Rage-click detection from analytics tools requires a minimum traffic volume to surface patterns — on low-traffic products, manual testing with session replay is more effective
- Progress bar completeness percentage is only meaningful if the backend provides real progress events; agents must check if the backend actually supports progress reporting before designing a percentage bar

## References
- https://www.nngroup.com/articles/visibility-system-status/
- https://m3.material.io/components/progress-indicators/overview
- https://developer.apple.com/design/human-interface-guidelines/progress-indicators
- https://webaim.org/articles/usable/
- https://www.nngroup.com/articles/response-times-3-important-limits/ (Miller/Card/Newell response time thresholds)
