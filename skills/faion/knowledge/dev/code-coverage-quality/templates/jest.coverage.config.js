// purpose: template for code-coverage (jest.coverage.config.js)
// consumes: code-coverage methodology inputs (see AGENTS.md Prerequisites)
// produces: filled-in artefact conforming to content/02-output-contract.xml
// depends-on: 01-core-rules.xml + tool-runtime in same dir
// token-budget-impact: ~200-400 tokens when loaded as context

// jest.config.js — coverage configuration
// Adjust collectCoverageFrom paths for your project structure.
/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageProvider: 'v8', // Native V8 — more accurate for ESM and async
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',      // barrel re-exports — no logic to test
    '!src/**/*.test.{ts,tsx}',
    '!src/**/*.spec.{ts,tsx}',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Raise thresholds for critical paths:
    // './src/auth/': { branches: 90, functions: 90, lines: 90, statements: 90 },
    // './src/billing/': { branches: 90, functions: 90, lines: 90, statements: 90 },
  },
};
