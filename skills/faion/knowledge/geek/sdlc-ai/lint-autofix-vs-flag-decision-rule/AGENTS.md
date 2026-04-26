# Autofix-vs-Flag Decision Rule for Coding Agents

## Summary

A coding agent applies a linter or scanner autofix automatically if and only if all four of the following hold: (1) the fix is purely syntactic (formatter, import sort, type annotation, dead-code removal); (2) the tool ships an explicit `--fix` / `--write` / `--autofix` mechanism with a `fix:` block (ruff, biome, eslint --fix, semgrep --autofix where the rule has `fix:`, prettier); (3) the test suite still passes after the fix; (4) the diff is smaller than 50 lines or every change matches a single rule ID. Findings that fail any of those four — CodeQL alerts without a fix block, secrets, CVEs without a patch version, license conflicts, SonarQube cognitive-complexity hotspots — are FLAGGED, not auto-applied: the agent posts a PR suggestion or draft PR for human review and never lands the change in the same loop.

## Why

This is the policy spine of every "agent green-locks the lint" workflow. Pure-syntax fixes are near-100% safe per BitsAI-Fix academic findings and the same conclusion is reached by Factory.ai's "lint green as merge gate" framing and DeepMind's CodeMender, which validates fixes by running tests before submitting. Anything semantic (security, license, design) needs verification and retry; making the agent treat both classes the same is the dominant cause of agents merging confident-looking but wrong patches. The four-condition gate gives the agent a deterministic predicate to evaluate per finding, removing creative judgment from the inner loop.

## When To Use

- Always — this is the meta-rule that wraps every other lint/SAST/SCA methodology in this knowledge base.
- Encoded in the agent's system prompt as a checklist: "for finding X, do conditions 1–4 hold? if yes autofix, else flag."
- Encoded in the CI agent's logic: a fix that fails any condition becomes a draft-PR comment, not a commit.

## When NOT To Use

- Read-only audit runs (the agent is reporting, not fixing) — the gate is moot.
- One-shot bulk migrations (e.g., codemod sweeps) where the rule is "all-or-nothing" by design — encode the all-or-nothing exception explicitly, do not let the four-condition rule fight the migration.
- Stateful side effects outside the repository (rotating a secret, opening a JIRA ticket) — these are governed by approval-token and incident methodologies, not by autofix policy.

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-conditions.xml` | The four-condition predicate the agent evaluates per finding and the autofix-vs-flag branch. |
| `content/02-flag-classes.xml` | The five classes that always flag: SAST without fix block, secrets, unpatched CVEs, license conflicts, complexity hotspots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-policy.txt` | Drop-in system-prompt block encoding the four conditions and the five flag classes. |
| `templates/decision-table.md` | Quick-reference decision table mapping (tool, finding kind) to (autofix, flag, escalate). |
