# Subagent prompt: <Phase Name>

You <one-paragraph mission statement: what this subagent is for, what side effects it may have, what language it communicates in (English for code/commits, Ukrainian for any user-facing string)>.

## Inputs (orchestrator passes these in spawn message)

- `<param-1>` — <type and meaning>
- `<param-2>` — <type and meaning>
- `<optional-param>` (optional) — <when used>

## Pre-flight

- Working directory: `<absolute path or "from input">`
- Required state assumptions (e.g. `git -C <repo> status --porcelain` is empty before EXECUTE).
- Required env / unlock (e.g. `op-unlock` already run if secrets needed).
- Reference files to read first:
  - `<repo>/AGENTS.md`
  - `<repo>/CHANGELOG.md` (to confirm format)
  - `<feature_folder>/spec.md` and `design.md` (when relevant)

## Workflow

1. <concrete first step>
2. <concrete second step>
3. <concrete third step>
   - <sub-step>
   - <sub-step>
4. <concrete final step that produces the output>

## Output

Either:
- A structured Markdown report with a fixed schema (sections + bullet lists), OR
- A list of files written (paths + meaning), OR
- A last-line marker the orchestrator parses, e.g. `done=<feature-id> commit=<short-sha>` or `verdict=PASS|FAIL-WITH-NITS|FAIL`.

State which one your prompt produces. Pick exactly one.

## Constraints

- NO remote `git push` unless explicitly authorized by the input parameters.
- NO `--no-verify`, `--no-gpg-sign`, `git reset --hard`, force push.
- NO bulk `git add -A` / `git add .`. Stage explicit paths.
- NO `Co-Authored-By` trailer, no emojis in commit messages.
- NO time estimates anywhere in the output. Use complexity levels and token estimates.
- Append a `CHANGELOG.md` entry under `## [Unreleased]` for every commit you make.
- User-facing strings (any `AskUserQuestion` payload, any caption) must be in Ukrainian; everything else in English.

## Done condition

<Observable check that lets the orchestrator decide success vs failure. One paragraph. Examples:>
- The feature folder is now under `.aidocs/<project>/done/<feature-id>/` and `git log -1` shows a commit titled `<type>: <short>`.
- The verifier exit code is 0 and the report contains `verdict=PASS`.
- Both `before.png` and `after.png` exist at the expected paths and were sent successfully.
