// purpose: ESLint 9 flat config — TS strict, no-explicit-any error, React hooks rules.
// consumes: nothing external; drop at repo root.
// produces: lint pass/fail with @typescript-eslint and react-hooks rules.
// depends-on: eslint>=9, typescript-eslint, eslint-plugin-react-hooks.
// token-budget-impact: ~40 lines.
// eslint.config.js — ESLint 9.x flat config with TypeScript strict + React hooks
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    plugins: { react, 'react-hooks': reactHooks },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': ['error', { allowExpressions: true }],
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
);
