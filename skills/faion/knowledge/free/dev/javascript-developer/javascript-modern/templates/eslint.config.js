// purpose: template for javascript-modern (eslint.config.js)
// consumes: javascript-modern methodology inputs (see AGENTS.md Prerequisites)
// produces: filled-in artefact conforming to content/02-output-contract.xml
// depends-on: 01-core-rules.xml + tool-runtime in same dir
// token-budget-impact: ~200-400 tokens when loaded as context

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    plugins: {
      react,
      'react-hooks': reactHooks,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': ['error', { allowExpressions: true }],
    },
  },
);
