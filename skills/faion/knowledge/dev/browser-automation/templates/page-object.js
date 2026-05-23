/*
 * purpose: Generic Page Object base class with data-test-id helpers
 * consumes: Per-screen DOM
 * produces: Domain-method API
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: ~280 tokens when loaded
 */
// page-object.js — Page Object Model scaffold for Playwright.
// Each page gets its own POM file; selectors never appear inline in tests.

class LoginPage {
  constructor(page) {
    this.page = page;
    // Prefer role/text locators over CSS
    this.usernameInput = page.locator('role=textbox[name="Username"]');
    this.passwordInput = page.locator('role=textbox[name="Password"]');
    this.submitButton = page.locator('role=button[name="Sign in"]');
    this.errorMessage = page.locator('[data-testid="auth-error"]');
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return this.errorMessage.textContent();
  }

  async isLoggedIn() {
    return this.page.locator('[data-testid="dashboard"]').isVisible();
  }
}

module.exports = { LoginPage };
