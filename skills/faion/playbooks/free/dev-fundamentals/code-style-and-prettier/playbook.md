---
name: code-style-and-prettier
description: Auto-format JS/TS with Prettier or Python with ruff, wire format-on-save in VS Code, and block unformatted commits with a pre-commit hook.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have an auto-formatter running on every save in VS Code and blocking every commit that contains unformatted code — either Prettier for JS/TS projects or `ruff format` for Python projects.

## Prerequisites

- A JS/TS project with `package.json` (for the Prettier path), OR a Python project with `pyproject.toml` or a plain directory (for the ruff path).
- Node.js 18+ installed (`node --version`).
- Python 3.10+ installed (`python3 --version`).
- VS Code installed with the workspace open.
- Git repository initialised (`git init` or already cloned).

## Steps

### JS/TS: install and configure Prettier

1. Install Prettier as an exact dev dependency so the version is pinned in `package-lock.json`:

   ```bash
   npm install --save-dev --save-exact prettier
   ```

2. Create `.prettierrc` at the project root with a minimal, consistent config:

   ```json
   {
     "semi": true,
     "singleQuote": true,
     "trailingComma": "all",
     "printWidth": 100,
     "tabWidth": 2
   }
   ```

3. Create `.prettierignore` to skip generated files:

   ```
   dist/
   build/
   coverage/
   .next/
   node_modules/
   ```

4. Add a format script to `package.json` under `"scripts"`:

   ```json
   "format": "prettier --write .",
   "format:check": "prettier --check ."
   ```

5. Run `npm run format` once to reformat the existing codebase. Review the diff with `git diff --stat` before committing.

6. Install the Prettier VS Code extension by running in your terminal:

   ```bash
   code --install-extension esbenp.prettier-vscode
   ```

7. Create `.vscode/settings.json` (or add to it) to enable format-on-save:

   ```json
   {
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "editor.formatOnSave": true,
     "[javascript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
     "[typescript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
     "[json]": { "editor.defaultFormatter": "esbenp.prettier-vscode" }
   }
   ```

8. Install husky and lint-staged to block unformatted commits:

   ```bash
   npm install --save-dev husky lint-staged
   npx husky init
   ```

9. Replace the contents of `.husky/pre-commit` with:

   ```sh
   #!/bin/sh
   npx lint-staged
   ```

10. Add lint-staged config to `package.json`:

    ```json
    "lint-staged": {
      "*.{js,jsx,ts,tsx,json,css,md}": ["prettier --write"]
    }
    ```

---

### Python: install and configure ruff format

1. Install ruff (if not already present):

   ```bash
   pip install ruff
   ```

   Or add it to your project:

   ```bash
   pip install --upgrade ruff
   ```

2. Add a `[tool.ruff.format]` section to `pyproject.toml`:

   ```toml
   [tool.ruff]
   line-length = 100

   [tool.ruff.format]
   quote-style = "double"
   indent-style = "space"
   skip-magic-trailing-comma = false
   ```

   If you have no `pyproject.toml`, create one at the project root with that block.

3. Run the formatter once on the whole codebase:

   ```bash
   ruff format .
   ```

4. Install the Ruff VS Code extension:

   ```bash
   code --install-extension charliermarsh.ruff
   ```

5. Create or update `.vscode/settings.json`:

   ```json
   {
     "[python]": {
       "editor.defaultFormatter": "charliermarsh.ruff",
       "editor.formatOnSave": true
     }
   }
   ```

6. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

7. Create `.pre-commit-config.yaml` at the project root:

   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.4.4
       hooks:
         - id: ruff-format
   ```

8. Install the hooks into the local `.git/hooks` directory:

   ```bash
   pre-commit install
   ```

## Verify

**JS/TS:** Open any `.ts` or `.js` file in VS Code, introduce a formatting violation (e.g., remove a semicolon), save. VS Code should reformat it instantly. Then confirm the pre-commit hook works:

```bash
# Introduce a formatting violation and try to commit it
echo "const x = 1" >> src/index.ts
git add src/index.ts
git commit -m "test: verify prettier hook"
```

Prettier should reformat `src/index.ts` and the commit will proceed with the corrected version, or fail if you have `--check` mode. Confirm with:

```bash
npx prettier --check src/index.ts
```

**Python:** Save a `.py` file in VS Code with inconsistent quotes or spacing and confirm it reformats on save. Confirm the hook works:

```bash
echo 'x=1' >> myapp/main.py
git add myapp/main.py
git commit -m "test: verify ruff format hook"
```

The hook should reformat `myapp/main.py` before the commit proceeds. Confirm:

```bash
ruff format --check myapp/main.py
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| VS Code formats with the wrong formatter | Another formatter extension is active (e.g., the built-in JS formatter or Black) | Open `.vscode/settings.json`, add `"editor.defaultFormatter": "esbenp.prettier-vscode"` (JS/TS) or `"charliermarsh.ruff"` (Python) for the affected language block |
| Pre-commit hook does not run on `git commit` | `pre-commit install` was not run in this repo clone | Run `pre-commit install` from the project root; verify `ls .git/hooks/pre-commit` |
| husky hook not firing | `npx husky init` was run but `package.json` has no `"prepare"` script | Add `"prepare": "husky"` to `"scripts"` in `package.json`, then run `npm install` |
| `ruff format` rewrites files but VS Code does not | Extension not installed or workspace reload needed | Run `code --install-extension charliermarsh.ruff`, then reload VS Code with `Ctrl+Shift+P` → "Reload Window" |
| `prettier --check` fails in CI despite passing locally | Different Prettier version installed globally vs. locally | Always run `npx prettier` (project-local) not `prettier` (global); lock the version with `--save-exact` |
| `pre-commit` rewrites files but git shows them unstaged | pre-commit modified the staged files; git sees the diff as unstaged | Stage the reformatted files again (`git add -u`) and re-run `git commit` |

## Next

- [testing-intro-python](../testing-intro-python/playbook.md) — add pytest with coverage so formatted code is also tested before merge.
- [javascript-first-project](../javascript-first-project/playbook.md) — complete JS project bootstrap including ESLint alongside Prettier.
- Upgrade to the `solo` tier to unlock ESLint rule customisation and stricter TypeScript enforcement playbooks.

## References

- [knowledge/free/dev/code-quality/code-review-basics](../../../knowledge/free/dev/code-quality/code-review-basics) — establishes that linters and formatters must run before any code review pass; this playbook automates exactly that gate so reviewers see pre-formatted diffs.
