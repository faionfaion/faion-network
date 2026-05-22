// purpose: Jest/Vitest branch-coverage config for JS/TS suites.
// consumes: project repo; see the methodology AGENTS.md for input contract.
// produces: the working artifact described above; placement: Place at repo root.
// depends-on: the tooling pinned in the methodology's AGENTS.md.
// token-budget-impact: zero — local-only template; build/CI time is the only cost.
// jest.config.js — coverage thresholds with global + per-directory gates.
// Adjust collectCoverageFrom globs to match your project structure.
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.test.{ts,tsx}',
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
    // Raise threshold for business-critical directories
    './src/services/': {
      branches: 90,
      functions: 90,
      lines: 90,
    },
  },
};
