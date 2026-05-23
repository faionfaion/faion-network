// purpose: commitlint config — Conventional Commits 1.0.0 + project scopes
// consumes: commit message via commit-msg hook
// produces: pass/fail
// depends-on: hook installer (lefthook/husky/pre-commit)
// token-budget-impact: ~150 tokens
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [2, "always", ["feat", "fix", "chore", "refactor", "docs", "test", "perf", "build", "ci", "style", "revert"]],
    "subject-case": [2, "never", ["upper-case", "pascal-case", "start-case"]],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 72],
    "body-leading-blank": [2, "always"],
    "footer-leading-blank": [2, "always"],
    "scope-case": [2, "always", "kebab-case"]
  }
};
