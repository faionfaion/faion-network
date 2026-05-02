---
name: python-first-project
description: Install Python, create a project folder, write hello.py, and run it from the terminal — from zero to working script.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have Python installed on your machine, a dedicated project folder, and a working `hello.py` script that you can run from the terminal and see output.

## Prerequisites

- A terminal (macOS: Terminal or iTerm2; Windows: PowerShell or Windows Terminal; Linux: any shell).
- Admin rights to install software on your machine.
- No prior Python knowledge required.

## Steps

1. Check whether Python is already installed by running `python3 --version` in your terminal.
   - If it prints `Python 3.11.x` or higher, skip to step 5.
   - If you see `command not found` or a version below 3.10, continue with step 2.

2. Install Python:
   - **Windows:** Download the installer from https://www.python.org/downloads/ (choose the latest stable 3.x release). Run it and check "Add Python to PATH" before clicking Install.
   - **macOS (Homebrew):** Run `brew install python3`. If Homebrew is not installed, first run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
   - **macOS / Linux (pyenv):** Install pyenv from https://github.com/pyenv/pyenv#installation, then run `pyenv install 3.12.3 && pyenv global 3.12.3`.
   - **Ubuntu / Debian:** Run `sudo apt update && sudo apt install -y python3 python3-pip`.

3. Confirm the installation succeeded:

   ```bash
   python3 --version
   ```

   Expected output: `Python 3.x.y` (3.10 or higher).

4. Confirm pip is available:

   ```bash
   python3 -m pip --version
   ```

   Expected output: `pip 24.x.x ...`.

5. Create a project folder for your work:

   ```bash
   mkdir ~/projects/my-first-python
   cd ~/projects/my-first-python
   ```

6. Create the script file using a text editor. Open `hello.py` in VS Code, Notepad, or any plain-text editor, then save the following two lines:

   ```python
   name = "World"
   print(f"Hello, {name}! Python is working.")
   ```

7. Run the script from the terminal (make sure you are inside `~/projects/my-first-python`):

   ```bash
   python3 hello.py
   ```

## Verify

Run the script and confirm the output matches exactly:

```bash
python3 hello.py
```

Expected terminal output:

```
Hello, World! Python is working.
```

If you see that line, Python is installed and your script runs correctly.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: python3` after installation on Windows | Python was not added to PATH during install | Re-run the Python installer, check "Add Python to PATH", or add `C:\Users\<you>\AppData\Local\Programs\Python\Python3x\` to PATH manually via System → Environment Variables |
| `command not found: python3` on macOS | macOS ships `python3` only after Xcode Command Line Tools | Run `xcode-select --install` and wait for it to finish, then retry |
| `SyntaxError: invalid syntax` on the `print` line | File was accidentally saved with a `.txt` extension | Rename the file to `hello.py` (remove `.txt`) and rerun |
| Output is missing quotes or curly braces | File is not UTF-8 or copy-paste introduced smart quotes | Re-type the f-string manually instead of copy-pasting |
| `python3` works but `python` does not | Only `python3` binary is in PATH (common on Linux) | Use `python3 hello.py` throughout; optionally add `alias python=python3` to `~/.bashrc` |

## Next

- [python-package-manager](../python-package-manager) — install third-party libraries with pip or uv for your next script.
- [vscode-first-project-setup](../../tech-setup/vscode-first-project-setup) — configure VS Code with Python extension, linting, and auto-format.
- [testing-intro-python](../testing-intro-python) — write your first automated test with pytest.

## References

- [knowledge/free/dev/python-developer/python-basics](../../../knowledge/free/dev/python-developer/python-basics) — the tooling guidance (uv, ruff, mypy) in `python-basics` informed Steps 3–4 on verifying the Python executable and pip; this playbook uses `python3 --version` and `python3 -m pip --version` as the exact observable checks that match the methodology's "project bootstrap" entry conditions.
