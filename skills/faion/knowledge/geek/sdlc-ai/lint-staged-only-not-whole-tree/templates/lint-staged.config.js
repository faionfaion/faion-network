// lint-staged.config.js — wire husky's pre-commit through lint-staged.
// Install: npm i -D lint-staged husky
// .husky/pre-commit body: `npx lint-staged`
//
// Each glob receives ONLY the staged files matching it.
// Tools that need the project graph (tsc, mypy) live in a separate
// pre-commit hook with pass_filenames: false — never here.

export default {
  "*.{js,jsx,ts,tsx,json,css,graphql}": [
    "biome check --write --no-errors-on-unmatched",
  ],

  "*.py": [
    "ruff check --fix",
    "ruff format",
  ],

  "*.{md,mdx}": [
    "prettier --write",
  ],

  "*.{yml,yaml}": [
    "yamllint -c .yamllint.yml",
  ],

  "*.sh": [
    "shellcheck --severity=style",
  ],
};
