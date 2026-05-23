// purpose: Vitest config with V8 branch coverage + diff-gate-friendly thresholds
// consumes: test config bundle decisions from javascript-testing
// produces: vitest.config.ts at repo root
// depends-on: Vitest >= 1.6; @vitest/coverage-v8
// token-budget-impact: ~200 tokens when loaded as context
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./templates/test-setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'lcov', 'html'],
      branches: true,
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.test.{ts,tsx}', 'src/**/__tests__/**', 'src/generated/**'],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 80,
        statements: 80,
      },
    },
  },
})
