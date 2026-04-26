# SonarQube AI Code Quality Gate

## Summary

Repos where a meaningful share of code is AI-generated MUST run SonarQube/SonarCloud with the "Sonar way for AI Code" quality gate (or a custom gate marked `Qualified for AI Code Assurance`) and connect Sonar's MCP server to the coding agent. The gate enforces stricter thresholds for cognitive complexity, duplication, security-hotspot density, and the AI-code trust score; the agent reads findings via MCP and rewrites until the gate is green. PRs that do not pass the AI-tuned gate cannot be merged, regardless of who or what authored the diff.

## Why

AI-generated code has a measurably different defect profile than human code: more lookalike bugs (almost-correct copies of training examples), more dead code, shallower tests, and more cognitive-complexity hotspots. Sonar's published April 2026 telemetry puts AI-authored code at 42% of all committed code across observed repos, and the default "Sonar way" gate was never tuned for those failure modes. The "Sonar way for AI Code" gate raises bug-density and duplication thresholds and adds the AI trust score; the MCP server lets the agent itself loop until clean, turning the gate from a blocker into a productive constraint.

## When To Use

- Any team where AI-authored commits exceed ~25% of weekly diff volume (Copilot, Claude Code, Cursor, Codex, Devin).
- Regulated industries (finance, healthcare, government) where audit evidence of an AI-aware quality gate is a procurement/SOC2 requirement.
- Enterprise-scale monorepos that already report quality dashboards to leadership.
- Any repo emitting libraries to other teams where shallow-test and lookalike-bug regressions are expensive to chase down.

## When NOT To Use

- Tiny solo projects — overhead exceeds value; ruff + biome + semgrep cover most of the same surface for free.
- Pure greenfield prototypes under daily API churn — the gate's duplication metric will fight the architecture before it stabilizes.
- Read-only or vendored mirrors — there is no PR surface to gate.
- Internal demos / spike branches that will be deleted — bootstrap cost is not recoverable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-quality-gate.xml` | The AI-tuned quality gate, MCP loop, and the agent-rewrite-until-green contract. |
| `content/02-suppression-discipline.xml` | When suppression is allowed vs blocked, and the "no override of the gate" rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sonar-project.properties` | Project-level config pointing at the AI-tuned gate. |
| `templates/sonar-quality-gate.json` | Custom quality-gate definition (thresholds for AI code). |
