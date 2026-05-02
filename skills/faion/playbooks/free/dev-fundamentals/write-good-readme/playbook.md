---
name: write-good-readme
description: Write an 8-section README for a new open-source package with badges, a 5-line quickstart, and why-vs-alternatives to get your repo noticed.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a polished `README.md` with eight sections covering hero one-liner, demo screenshot or GIF, install, 5-line quickstart, why-vs-alternatives, license, contributing, and acknowledgements — plus two shields.io badges — giving first-time visitors everything they need to decide whether to use your package.

## Prerequisites

- A GitHub repository already created (see `github-account-and-first-repo` if you have not done that yet).
- A working package users can install (even a prototype is enough to write the README).
- Git configured locally and `git push` to `origin main` working.
- No prior README-writing experience required.

## Steps

The examples below use a hypothetical Python package named `fastapi-rate-limiter` published to PyPI by GitHub user `acme-dev`.

1. Open `README.md` in your editor at the root of your repository.

2. Add the H1 title and hero one-liner. The one-liner must answer "what does this do and for whom?" in one sentence:

   ```markdown
   # fastapi-rate-limiter

   _Add per-route rate limiting to any FastAPI app in three lines of code._
   ```

3. Add a badges row immediately after the tagline. Use shields.io dynamic badges so they stay accurate automatically:

   ```markdown
   [![CI](https://img.shields.io/github/actions/workflow/status/acme-dev/fastapi-rate-limiter/ci.yml?label=build)](https://github.com/acme-dev/fastapi-rate-limiter/actions)
   [![PyPI version](https://img.shields.io/pypi/v/fastapi-rate-limiter)](https://pypi.org/project/fastapi-rate-limiter/)
   ```

   Replace `acme-dev/fastapi-rate-limiter` with your own `owner/repo` and update `ci.yml` to match your workflow filename. For an npm package swap the PyPI badge URL to `https://img.shields.io/npm/v/<package-name>`.

4. Add a `## Demo` section with a screenshot or GIF. Place the image file in `docs/demo.gif` and reference it:

   ```markdown
   ## Demo

   ![Rate limiter demo](docs/demo.gif)
   ```

   If you do not have a GIF yet, substitute a terminal screenshot saved as `docs/demo.png`. Never leave this section empty or with a placeholder.

5. Add an `## Install` section with one copy-pasteable command:

   ```markdown
   ## Install

   ```bash
   pip install fastapi-rate-limiter
   ```

   Requires Python 3.10+ and FastAPI 0.100+.
   ```

6. Add a `## Quickstart` section with a 5-line working example — no preamble, no ellipsis:

   ```markdown
   ## Quickstart

   ```python
   from fastapi import FastAPI
   from fastapi_rate_limiter import RateLimiter

   app = FastAPI()

   @app.get("/search", dependencies=[RateLimiter(times=10, seconds=60)])
   async def search(q: str):
       return {"q": q}
   ```

   Start the app with `uvicorn main:app` and hit `/search` more than 10 times in 60 seconds to see a 429 response.
   ```

7. Add a `## Why not X` section comparing at least two alternatives. Be factual and specific — readers use this to make a decision, not to be sold to:

   ```markdown
   ## Why not X

   | | fastapi-rate-limiter | slowapi | fastapi-limiter |
   |---|---|---|---|
   | Storage | in-memory or Redis | Redis only | Redis only |
   | Per-route config | yes | yes | yes |
   | Async-native | yes | no (sync wrapper) | yes |
   | Zero deps (in-memory) | yes | no | no |

   Use `slowapi` if you need battle-tested Starlette middleware with Redis. Use `fastapi-limiter` if your entire team already knows it. Use this library if you want async-native rate limiting that works without Redis for simple projects.
   ```

8. Add `## License`, `## Contributing`, and `## Acknowledgements` sections at the end:

   ```markdown
   ## License

   [MIT](LICENSE)

   ## Contributing

   Open an issue first to discuss the change. Then fork, create a branch (`git checkout -b feat/my-change`), commit, and open a pull request against `main`.
   Run `pytest` and `ruff check .` before pushing.

   ## Acknowledgements

   - [limits](https://limits.readthedocs.io/) — storage backends and rate-limit parsing.
   - [FastAPI](https://fastapi.tiangolo.com/) — the framework this library extends.
   ```

9. Save `README.md`, stage it, and push:

   ```bash
   git add README.md docs/demo.gif
   git commit -m "docs: add full README with badges and quickstart"
   git push origin main
   ```

## Verify

Open your repository on GitHub at `https://github.com/<owner>/<repo>` (replace with your own URL) and confirm:

- The CI badge renders as a green "build passing" pill.
- The PyPI (or npm) version badge shows the current release number, not a grey "invalid" state.
- The Demo image loads inline without a broken-image icon.
- The Quickstart code block displays with Python syntax highlighting.

If a badge shows grey/invalid: the path in the URL does not match the actual workflow filename or package name — double-check the shield URL against `https://img.shields.io/github/actions/workflow/status/<owner>/<repo>/<filename>`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| CI badge shows grey "no status" | Workflow filename in the badge URL does not match the `.github/workflows/` file | Run `ls .github/workflows/` and update the badge URL to the exact filename including `.yml` |
| PyPI version badge shows "invalid" | Package name in the URL is wrong or the package is not yet published | Verify on https://pypi.org/project/<your-package-name>/ that the package exists; fix the badge URL to match |
| Demo GIF does not render on GitHub | Path is wrong or file not committed | Run `git ls-files docs/` to confirm the file is tracked; fix the path in `README.md` to match exactly (case-sensitive on Linux) |
| Why-not table renders as plain text | Table has mismatched column counts or missing header separator row | Validate the Markdown table at https://tableconvert.com/markdown-to-markdown; each row must have the same number of pipes |
| Quickstart code block has no syntax highlighting | Missing language identifier on the fenced code block | Change ` ``` ` to ` ```python ` (or `bash`, `js`, etc.) on the opening fence line |

## Next

- [python-package-manager](../python-package-manager) — publish your package to PyPI so the version badge has real data to display.
- [git-daily-workflow](../../tech-setup/git-daily-workflow) — keep the README up to date with each feature branch using conventional commits.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the `generate-readme` prompt inside this methodology defines the exact eight-section skeleton (Title, Tagline, Badges, Overview, Install, Usage, Development, Contributing, License) that this playbook expands into an 8-section README; the shields.io badge URL patterns used in Steps 3 come directly from that prompt's badge row specification.
