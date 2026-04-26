# direnv + mise Setup Checklist

## mise Installation

- [ ] Install mise: `curl https://mise.run | sh`
- [ ] Add shell integration to ~/.bashrc: `eval "$(mise activate bash)"`
- [ ] Reload shell: `source ~/.bashrc`
- [ ] Verify: `mise --version`
- [ ] Install default Python: `mise install python@3.12`
- [ ] Set global Python: `mise use --global python@3.12`
- [ ] Verify: `mise current` shows python 3.12.x
- [ ] Install Node.js if needed: `mise install node@22`

## direnv Installation

- [ ] Install direnv: `sudo apt install direnv`
- [ ] Add shell hook to ~/.bashrc: `eval "$(direnv hook bash)"`
- [ ] Hook MUST be AFTER mise activation in .bashrc
- [ ] Hook MUST be LAST line (or near last) in .bashrc
- [ ] Reload shell: `source ~/.bashrc`
- [ ] Verify: `direnv --version`

## Shell Integration Order

Verify ~/.bashrc has this order:
- [ ] 1. Standard bash config (prompt, aliases, etc.)
- [ ] 2. `eval "$(mise activate bash)"` (mise first)
- [ ] 3. `eval "$(direnv hook bash)"` (direnv last)

## Per-Project Setup

For each project:
- [ ] Create `.tool-versions` or `mise.toml` with required runtimes
- [ ] Install runtimes: `mise install`
- [ ] Create `.envrc` with project environment setup
- [ ] Allow direnv: `direnv allow`
- [ ] Verify runtimes active: `python --version`, `node --version`
- [ ] Verify venv active (if Python): `which python` points to .venv

## .envrc Content Checklist

- [ ] `use mise` to activate mise runtimes
- [ ] `layout python-venv .venv` for Python projects
- [ ] `dotenv_if_exists .env` to load secrets
- [ ] `PATH_add` for project-specific scripts
- [ ] `watch_file` for dependency files (requirements.txt, pyproject.toml)
- [ ] Non-secret env vars exported (LOG_LEVEL, DEBUG, etc.)
- [ ] No secrets hardcoded in .envrc (use .env instead)

## .gitignore Updates

- [ ] `.direnv/` added to .gitignore
- [ ] `.venv/` added to .gitignore
- [ ] `.env` added to .gitignore
- [ ] `.mise.local.toml` added to .gitignore
- [ ] `.envrc.local` added to .gitignore (if using local overrides)
- [ ] `.envrc` is committed (it's safe, contains no secrets)
- [ ] `.tool-versions` is committed

## Multi-Version Setup

- [ ] All needed Python versions installed via mise
- [ ] All needed Node.js versions installed via mise
- [ ] Each project has correct version in .tool-versions
- [ ] Switching directories automatically switches versions
- [ ] Test: `cd project-a && python --version` shows correct version
- [ ] Test: `cd project-b && python --version` shows different version

## Security Verification

- [ ] New .envrc files require `direnv allow` before executing
- [ ] .env files are not committed to git
- [ ] No secrets in .envrc files
- [ ] direnv blocks untrusted .envrc in cloned repos
- [ ] Sensitive files excluded from version control

## Troubleshooting Checklist

- [ ] If direnv not loading: check `eval "$(direnv hook bash)"` in .bashrc
- [ ] If wrong Python version: check `mise current` and .tool-versions
- [ ] If venv not activating: check .envrc has `layout python-venv .venv`
- [ ] If changes not applying: run `direnv reload`
- [ ] If mise not finding version: run `mise install`
- [ ] If permission denied on .envrc: run `direnv allow`
