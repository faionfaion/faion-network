// purpose: POM skeleton for one route — copy and rename.
// consumes: data-testid attributes from frontend, route path.
// produces: TypeScript class exporting goto + intent-named actions + expect helpers.
// depends-on: @playwright/test (no other deps).
// token-budget-impact: ~40 lines per POM; loaded only by failing specs during triage.
import { Page, Locator, expect } from '@playwright/test';

// Skeleton Page Object — copy and rename for each route.
// Convention: one POM per route; methods named after user intent.
export class ExamplePage {
  readonly page: Page;
  // Declare all locators as properties using data-testid
  readonly primaryElement: Locator;

  constructor(page: Page) {
    this.page = page;
    this.primaryElement = page.getByTestId('primary-element');
  }

  // Navigation: wait for the page to be ready
  async goto() {
    await this.page.goto('/example');
    await expect(this.primaryElement).toBeVisible();
  }

  // Action: named after user intent, not DOM event
  async performAction(input: string) {
    await this.page.getByTestId('input').fill(input);
    await this.page.getByTestId('submit').click();
  }

  // Assertion: use expect() for auto-retry
  async expectSuccess(expected: string) {
    await expect(this.page.getByTestId('result')).toContainText(expected);
  }
}
