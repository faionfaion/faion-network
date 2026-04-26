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
