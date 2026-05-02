---
name: dotenv-secrets-management
description: Keep API keys and database credentials out of your code using .env files, .gitignore, and python-dotenv or dotenv for Node.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `.env` file holding real credentials (like `OPENAI_API_KEY` and `DATABASE_URL`) that is ignored by Git, a committed `.env.example` template for teammates, and working code that loads those variables at runtime using `python-dotenv` (Python) or `dotenv` (Node).

## Prerequisites

- Git installed and a project folder already tracked by a repo (`git init` or cloned).
- Python 3.10+ **or** Node.js 18+ depending on your stack.
- A terminal (macOS: Terminal or iTerm2; Windows: PowerShell or Windows Terminal; Linux: any shell).
- At least one real credential to protect — for example, an OpenAI API key from https://platform.openai.com/api-keys or a Postgres connection string.

## Steps

### Create the .env file

1. In your project root, create a file named `.env` (no extension):

   ```bash
   touch .env
   ```

2. Open `.env` in your editor and add your real credentials, one per line:

   ```
   OPENAI_API_KEY=sk-proj-abc123yourrealkey
   DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/myappdb
   ```

   Use `KEY=VALUE` format — no spaces around `=`, no quotes (unless the value contains spaces).

### Add .env to .gitignore before the first commit

3. Open (or create) `.gitignore` in your project root and add these lines:

   ```
   .env
   .env.local
   .env.*.local
   ```

4. Verify the file is now ignored:

   ```bash
   git status
   ```

   `.env` must **not** appear under "Changes to be committed" or "Untracked files". If it does, you have not saved `.gitignore` or the path is wrong — fix before continuing.

### Commit a .env.example template instead

5. Create `.env.example` with placeholder values (safe to commit):

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

6. Add and commit the example file:

   ```bash
   git add .env.example
   git commit -m "chore: add .env.example template"
   ```

### Load variables at runtime

**Python — using python-dotenv:**

7. Install the library:

   ```bash
   pip install python-dotenv
   ```

   Or with Poetry: `poetry add python-dotenv`.

8. At the top of your entry-point file (e.g. `main.py` or `app.py`), add:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()  # reads .env from the current working directory

   openai_api_key = os.getenv("OPENAI_API_KEY")
   database_url = os.getenv("DATABASE_URL")
   ```

   `load_dotenv()` is a no-op when the variables are already set by the shell (e.g. in production), so this pattern works identically in dev and prod.

**Node.js — using dotenv:**

7. Install the package:

   ```bash
   npm install dotenv
   ```

8. At the top of your entry-point file (e.g. `index.js` or `server.js`), add:

   ```js
   import 'dotenv/config';   // ESM (Node 18+ with "type": "module")
   // or
   require('dotenv').config(); // CommonJS

   const openaiApiKey = process.env.OPENAI_API_KEY;
   const databaseUrl = process.env.DATABASE_URL;
   ```

## Verify

Run the following one-liner from your project root to confirm `.env` is ignored and the variable loads:

```bash
git status --short | grep "\.env$"
```

The command must return **no output**. If it prints `?? .env` or `A  .env`, the file is not ignored — re-check `.gitignore`.

For a live runtime check (Python):

```bash
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY', 'NOT LOADED'))"
```

Expected output: your actual key value (e.g. `sk-proj-abc123yourrealkey`). If it prints `NOT LOADED`, check that `.env` is in the same directory you ran the command from.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `git status` still shows `.env` as untracked after editing `.gitignore` | `.gitignore` was saved in the wrong directory, or `.env` was already staged | Run `git ls-files --error-unmatch .env` to confirm it is not tracked. Ensure `.gitignore` is in the repo root (same level as `.git/`). |
| `os.getenv("OPENAI_API_KEY")` returns `None` | `load_dotenv()` not called, or `.env` is in a different directory | Confirm `load_dotenv()` appears before the `getenv` call. Pass an explicit path: `load_dotenv("/absolute/path/to/.env")`. |
| `process.env.OPENAI_API_KEY` is `undefined` in Node | `dotenv/config` import placed after other imports that read `process.env` | Move the `import 'dotenv/config'` line to the very first line of the entry-point file. |
| Leaked key committed to GitHub | `.env` was tracked before `.gitignore` was set up | Rotate the key immediately at the provider. GitHub secret scanning at https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning will alert you, but it cannot invalidate the key — you must revoke and regenerate it manually. |
| `.env.example` exposes real values | Real credentials were pasted into the example file | Replace all values with descriptive placeholders like `your_openai_api_key_here` before committing. |

## Next

- `git-daily-workflow` — learn `git add`, `git commit`, and branching so you never accidentally stage `.env` during day-to-day work.
- `python-first-project` — set up a complete Python project structure with `python-dotenv` integrated from the start.
- Consider upgrading to a secrets manager (AWS Secrets Manager, Doppler, or 1Password CLI) when you have multiple environments — covered in the solo tier.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — defines the rule to add `.env` and `*.pem` to `.gitignore` before the first commit and to rotate any accidentally committed secret immediately; this playbook operationalises that rule as concrete `.gitignore` steps and a pre-commit verify check.
