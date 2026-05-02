---
name: python-package-manager
description: Set up uv as your Python package manager, create a project, add dependencies, and run scripts without activating a virtual environment.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have `uv` installed, a new Python project with a committed lockfile, at least one third-party dependency installed, and a script you can run with `uv run` — without ever manually activating a virtual environment.

## Prerequisites

- A terminal (macOS: Terminal or iTerm2; Windows: PowerShell or Windows Terminal; Linux: any shell).
- Python 3.10+ already available (see [python-first-project](../python-first-project) if not).
- Git installed and initialised in your project folder (optional but recommended for lockfile tracking).
- No prior experience with `pip`, `venv`, or `poetry` required.

## Steps

1. Install `uv` via the official installer:

   **macOS / Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **Windows (PowerShell):**
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Restart your terminal after installation so the `uv` binary is in `PATH`.

2. Confirm `uv` is available:

   ```bash
   uv --version
   ```

   Expected output: `uv 0.x.y (...)`.

3. Create a new project called `myproject`:

   ```bash
   uv init myproject
   cd myproject
   ```

   This creates `pyproject.toml`, `hello.py`, and a `.python-version` file pinning the Python version.

4. Add a third-party dependency — for example, `requests`:

   ```bash
   uv add requests
   ```

   `uv` resolves, downloads, and installs `requests` into a local `.venv/`, then writes the exact resolved versions to `uv.lock`.

5. Write a simple script. Open `myscript.py` in any text editor and save:

   ```python
   import requests

   response = requests.get("https://httpbin.org/get")
   print(response.status_code)
   print(response.json()["url"])
   ```

6. Run the script without activating the virtual environment:

   ```bash
   uv run python myscript.py
   ```

   `uv run` automatically uses the project's `.venv`.

7. Commit the lockfile and add `.venv/` to `.gitignore`:

   ```bash
   echo ".venv/" >> .gitignore
   git init          # skip if git is already initialised
   git add pyproject.toml uv.lock .gitignore myscript.py
   git commit -m "chore: init project with uv"
   ```

   The lockfile `uv.lock` must be committed — it guarantees every contributor installs the exact same dependency versions.

## Verify

Run the script and check the output:

```bash
uv run python myscript.py
```

Expected output (two lines):

```
200
https://httpbin.org/get
```

HTTP status `200` confirms `requests` resolved correctly and the network call succeeded.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `uv: command not found` after install | Shell profile was not reloaded | Close and reopen your terminal, or run `source ~/.bashrc` (Linux) / `source ~/.zshrc` (macOS) |
| `ModuleNotFoundError: No module named 'requests'` | Script was run with `python myscript.py` instead of `uv run` | Always use `uv run python myscript.py`; never invoke the system Python directly in a uv project |
| `uv.lock` keeps changing on every `uv sync` | Different `uv` versions on different machines | Pin `uv` version in CI (`uv 0.x.y`) and upgrade all machines together |
| `.venv/` accidentally committed | `.gitignore` was not updated before `git add .` | Run `git rm -r --cached .venv/`, add `.venv/` to `.gitignore`, then commit |
| `uv add` installs but script still fails import | A second Python interpreter (system `python3`) is used outside `uv run` | Use `uv run` for every command; do not mix `uv` with `pip install` in the same project |

## Next

- [testing-intro-python](../testing-intro-python) — add pytest with `uv add --dev pytest` and write your first test.
- [dotenv-secrets-management](../dotenv-secrets-management) — load API keys safely with `python-dotenv` (add it via `uv add python-dotenv`).
- [python-first-project](../python-first-project) — revisit the basics if you skipped it and now want to understand what `hello.py` does.

## References

- [knowledge/free/dev/python-developer/python-modern-2026](../../../knowledge/free/dev/python-developer/python-modern-2026) — the tooling-stack section documents `uv init`, `uv add`, `uv run`, and the `uv.lock` commit rule relied on in Steps 3–7; the lockfile-commit rationale in Step 7 maps directly to the methodology's "Commit uv.lock to version control" rule.
