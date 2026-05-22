// purpose:   ESLint v9+ flat config block enforcing React hook discipline
// consumes:  eslint.config.js (composed with other configs)
// produces:  PR-blocking lint errors on hook violations
// depends-on: eslint, eslint-plugin-react-hooks
// token-budget-impact: ~0 tokens at runtime — gate only

import reactHooks from 'eslint-plugin-react-hooks';

export default {
  plugins: {
    'react-hooks': reactHooks,
  },
  rules: {
    // Both MUST be "error", never "warn".
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'error',
  },
};
