---
name: vscode-first-project-setup
description: Install VS Code, add 5 essential extensions, open a project folder, configure auto-format on save, and use the integrated terminal.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have VS Code installed with five production-grade extensions (Prettier, ESLint, GitLens, EditorConfig, Live Server), a project folder open in the editor, auto-format on save enabled via `settings.json`, and the integrated terminal ready so you never need to leave VS Code during a coding session.

## Prerequisites

- A computer running macOS, Linux, or Windows.
- An internet connection for downloading VS Code and extensions.
- A project folder on disk (even an empty one works — create it with `mkdir my-project`).
- No prior coding tool experience required.

## Steps

1. Download VS Code from https://code.visualstudio.com/download. Choose the installer for your OS (`.dmg` for macOS, `.deb`/`.rpm` for Linux, `.exe` for Windows). Run the installer and accept the default options; on Windows tick "Add to PATH" so you can launch VS Code from the terminal.

2. Verify the installation by opening a terminal (macOS: `Terminal.app`; Windows: PowerShell) and running:
   ```bash
   code --version
   ```
   You should see a version line such as `1.89.1`. If the command is not found on macOS, open VS Code, press `Cmd+Shift+P`, type `Shell Command: Install 'code' command in PATH`, and press Enter.

3. Install the five essential extensions. Run these five commands from any terminal (or paste them one by one into the VS Code integrated terminal after Step 7):
   ```bash
   code --install-extension esbenp.prettier-vscode
   code --install-extension dbaeumer.vscode-eslint
   code --install-extension eamodio.gitlens
   code --install-extension EditorConfig.EditorConfig
   code --install-extension ritwickdey.LiveServer
   ```
   Each command prints `Extension 'X' is already installed` or `Installing extensions...` followed by `Extension 'X' was successfully installed.`

4. Open your project folder in VS Code:
   ```bash
   code /path/to/my-project
   ```
   Or use the GUI: File → Open Folder, navigate to `my-project`, and click "Open". The Explorer sidebar on the left shows the folder tree.

5. Configure auto-format on save. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux), type `Open User Settings (JSON)`, and press Enter. VS Code opens `settings.json`. Add the following keys inside the top-level `{}` object (create the file from scratch if it is empty):
   ```json
   {
     "editor.formatOnSave": true,
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "[javascript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[typescript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[python]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     }
   }
   ```
   Save the file with `Cmd+S` / `Ctrl+S`. For Python projects replace the Python entry with `"ms-python.black-formatter"` if you install the Black Formatter extension instead of Prettier.

6. Add an `.editorconfig` file at the root of `my-project` so EditorConfig enforces consistent line endings and indentation regardless of OS:
   ```ini
   root = true

   [*]
   indent_style = space
   indent_size = 2
   end_of_line = lf
   charset = utf-8
   trim_trailing_whitespace = true
   insert_final_newline = true

   [*.py]
   indent_size = 4
   ```
   Create the file via File → New File, name it `.editorconfig`, paste the content above, and save.

7. Open the integrated terminal: press `` Ctrl+` `` (backtick) or go to View → Terminal. The terminal opens at the bottom of the window with your project folder as the working directory. Confirm with:
   ```bash
   pwd
   ```
   The output should be the full path to `my-project`.

8. Launch Live Server to preview an HTML file in the browser. Create `my-project/index.html` with any content (e.g., `<h1>Hello</h1>`), right-click the file in the Explorer sidebar, and choose "Open with Live Server". Your default browser opens at `http://127.0.0.1:5500/index.html`. Saving `index.html` while Live Server is running auto-reloads the page.

## Verify

Open any `.js` or `.ts` file in your project (create `my-project/hello.js` with the content `const x=1` if you have none), add a deliberate formatting issue (no spaces around `=`), and save with `Cmd+S` / `Ctrl+S`. VS Code must auto-format the file to `const x = 1` before your eyes.

Also confirm all five extensions appear in the installed list:
```bash
code --list-extensions | grep -E "esbenp|dbaeumer|eamodio|EditorConfig|ritwickdey"
```
The command must print all five extension IDs.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `code --version` returns "command not found" on macOS | `code` not added to shell PATH | Open VS Code → `Cmd+Shift+P` → `Shell Command: Install 'code' command in PATH`. Restart the terminal. |
| `code --install-extension` prints "ENFILE: too many open files" on Linux | ulimit too low | Run `ulimit -n 4096` in the same terminal session, then retry the install commands. |
| Auto-format on save does nothing | Another formatter is the default, or `formatOnSave` is overridden per-language | Open `settings.json` and confirm `editor.defaultFormatter` is `"esbenp.prettier-vscode"` and there is no conflicting `"editor.formatOnSave": false` in a workspace `.vscode/settings.json` file. |
| ESLint shows "ESLint is not installed" in the status bar | `eslint` package missing from the project | Run `npm install --save-dev eslint` inside `my-project` and add a minimal `eslint.config.js` (see https://eslint.org/docs/latest/use/configure/). |
| Live Server opens but page stays blank | `index.html` not at the project root VS Code opened | Confirm the open folder in VS Code is the parent of `index.html`, not a parent directory above it. |
| GitLens shows "No repository found" | Folder is not a Git repository | Run `git init` inside `my-project` in the integrated terminal. GitLens activates on the next file open. |

## Next

- [github-account-and-first-repo](../github-account-and-first-repo/playbook.md) — create a GitHub account and push `my-project` to a remote repository.
- [ssh-key-setup-github](../ssh-key-setup-github/playbook.md) — configure SSH authentication so `git push` never asks for a password.
- Add a `prettier.config.js` at the project root to customise Prettier rules (print width, single vs double quotes) beyond the defaults.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the `.editorconfig` and `.vscode/settings.json` patterns in this playbook follow the same "encode one team standard, remove drift" principle that bootstrap uses for branch protection; both prevent config inconsistencies from compounding across contributors.
