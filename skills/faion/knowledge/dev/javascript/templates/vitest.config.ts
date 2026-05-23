// purpose: Vitest config with jsdom + coverage (v8) + setup file for tests.
// consumes: nothing external; drop at repo root.
// produces: vitest test run with coverage report under ./coverage.
// depends-on: vitest, @vitejs/plugin-react, jsdom.
// token-budget-impact: ~30 lines.
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/', '**/*.d.ts'],
      thresholds: { lines: 80, branches: 80, functions: 80, statements: 80 },
    },
  },
});
