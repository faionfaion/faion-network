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
