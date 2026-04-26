// tests/at/nvda-form-error.spec.js (Windows runner)
// Requires: @guidepup/playwright, @guidepup/guidepup
// Purpose: Assert NVDA announces inline form validation error within 1.5s.
const { nvdaTest } = require('@guidepup/playwright');

nvdaTest('NVDA announces required-email error', async ({ page, nvda }) => {
  await page.goto('https://example.test/signup');

  // Navigate to first heading
  await nvda.perform(nvda.keyboardCommands.moveToNextHeading); // H key

  // Navigate to first form field
  await nvda.perform(nvda.keyboardCommands.moveToNextFormField); // F key

  // Type invalid email
  await nvda.type('not-an-email');

  // Submit form
  await page.keyboard.press('Enter');

  // Wait for aria-live region to fire
  await page.waitForTimeout(1500);

  const phrases = await nvda.spokenPhraseLog();
  const heard = phrases.join(' | ').toLowerCase();

  // Assert intent, not exact phrasing
  if (!heard.includes('email') || !(heard.includes('invalid') || heard.includes('required'))) {
    throw new Error(`Expected NVDA to announce email error. Got: ${heard}`);
  }
});
