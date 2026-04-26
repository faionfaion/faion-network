# Agent Integration — Acceptance Criteria

## When to use
- Authoring AC for SDD `spec.md` files (one feature → multiple Given/When/Then scenarios bound to test cases in `test-plan.md`).
- Translating a freeform user story or stakeholder note into testable, machine-parsable AC before a coding subagent picks up the task.
- Generating regression scenarios from a bug report so the fix has a "definition of done" gate before merge.
- Splitting an oversized story: when AC count exceeds ~7 per story, AC themselves become the slicing signal.
- Wiring AC to executable specs (Gherkin → Cucumber/Behave/Playwright `test.step`) so the same artefact drives BA review and CI.

## When NOT to use
- Pure spike / research tasks where the outcome is a learning, not a behaviour. Use a research question + stop condition instead.
- Throwaway prototypes or demos with a lifespan under one sprint — AC overhead exceeds value.
- UX-only changes where the verification is subjective (visual polish, brand tone). Use design review or pixel-diff snapshot tests.
- Operational/ops runbook changes (server tweaks, cron edits) — verify with smoke checks, not AC.
- Negotiation-heavy contracts with external partners where AC ossify before scope is stable; capture as open questions until signed.

## Where it fails / limitations
- **Ambiguous wording survives review.** "Fast", "user-friendly", "intuitive" pass through Gherkin syntax but are still untestable. Linters help but don't catch semantics.
- **Scenario explosion.** Cartesian-product AC (every role × every state × every error) bloats `test-plan.md` and slows CI. Cap with risk-based prioritisation.
- **Implementation leakage.** "Then the row is inserted into `users` table" couples AC to schema. Keep at behaviour level — verify via API, not DB.
- **Drift.** AC written once and never updated diverge from production behaviour. Anchor to living tests; fail CI when AC and test labels mismatch.
- **LLM hallucinated preconditions.** Models invent `Given the user has subscription X` even when no such concept exists in the codebase. Always ground in spec/design/code search.
- **Performance/security NFRs.** Easy to write ("response < 200ms") but expensive to verify continuously. Pair with k6/Artillery in CI or mark as periodic gate.

## Agentic workflow

The flow runs as a 3-stage chain inside the SDD lifecycle: a research subagent grounds AC in existing spec/design docs, an authoring subagent emits Gherkin or rule-based AC into `spec.md`, and a verification subagent maps each criterion to a test case in `test-plan.md` (mandatory at feature level per repo SDD convention). Each AC must carry a stable ID (e.g. `AC-LOGIN-01`) so test-plan, code review, and PR description can cross-reference. Use `faion-feature-executor` to enforce that no task moves out of `in-progress/` until every AC has a passing test reference.

### Recommended subagents
- `faion-sdd-executor-agent` — reads `spec.md` → executes against AC, blocks "done" if any AC unverified (already wired to read AC from spec.md per `agents/faion-sdd-executor-agent.md`).
- `faion-feature-executor` — sequential task runner with quality gates; gate AC coverage before moving task `todo/ → in-progress/ → done/`.
- `faion-brainstorm` — diverge phase: brainstorm edge cases (security, boundary, error, concurrency) before AC authoring; converge phase: dedupe, prioritise.
- `faion-improver` — audits existing AC sets against the "INVEST + testable" rubric; emits patches.

### Prompt pattern

Authoring (XML, structured output):
```xml
<role>BA agent generating Gherkin acceptance criteria.</role>
<inputs>
  <story>{user_story}</story>
  <design>{design_md_excerpt}</design>
  <existing_ac_ids>{ac_id_list}</existing_ac_ids>
</inputs>
<rules>
  - Output JSON: list of {id, title, given[], when[], then[], category}
  - category in: happy, alternative, boundary, error, security, performance
  - Cover happy path + ≥1 error + ≥1 boundary. No implementation terms (DB, ORM, framework names).
  - IDs continue from existing_ac_ids, prefix AC-<FEATURE>-NN.
</rules>
```

Verification (gate prompt):
```xml
<task>For each AC in spec.md, locate test reference in test-plan.md.
Return JSON: {ac_id, has_test, test_ref|null, gap_reason|null}.
If any has_test=false, halt task and return FAIL.</task>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gherkin-lint` | Lint `.feature` files: enforce style, no duplicate scenarios, required tags. | `npm i -g gherkin-lint` · github.com/vsiakka/gherkin-lint |
| `cucumber` (JS/Ruby/JVM) | Execute Gherkin AC as tests; reports map scenario → AC ID via tags. | `npm i -D @cucumber/cucumber` |
| `behave` | Python BDD runner for Gherkin. Pairs well with Django/FastAPI services. | `pip install behave` |
| `pytest-bdd` | Gherkin AC executed via pytest fixtures; reuses existing pytest infra. | `pip install pytest-bdd` |
| `Playwright` `test.step()` | Map AC steps directly to UI assertions; AC ID in step name. | `npm i -D @playwright/test` |
| `SpecFlow` / `Reqnroll` | .NET BDD runner; Reqnroll is the maintained fork (post-SpecFlow EOL 2024). | reqnroll.net |
| `Karate` | API-focused Gherkin; one tool for AC-driven contract tests. | github.com/karatelabs/karate |
| `gauge` | ThoughtWorks Markdown-based AC executor (alternative to Gherkin syntax). | gauge.org |
| `cucumber-tag-expressions` | Filter AC by tag (`@happy`, `@security`) in CI matrix. | cucumber.io/docs/cucumber/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Xray / Zephyr | SaaS | Yes (REST API) | Store AC on the story; Xray links AC ↔ test case ↔ execution. Agents POST AC via `/rest/api/3/issue`. |
| Linear | SaaS | Yes (GraphQL) | AC live in issue description; bots read/update via API key. Lightweight, no native AC fields — convention-driven. |
| Azure DevOps | SaaS | Yes (REST API) | Native "Acceptance Criteria" field on Work Items; Reqnroll integrates AC ↔ test runs. |
| GitHub Issues + sub-issues | SaaS | Yes (REST/GraphQL) | AC as task list checkboxes; PRs auto-close on merge. Best for OSS/solo flows. |
| Cucumber Studio (ex-HipTest) | SaaS | Partial (REST) | Collaborative Gherkin editor; sync to git. Agent integration via webhooks. |
| Testomat.io | SaaS | Yes (CLI + API) | AC-as-tests management with auto-import from feature files. |
| Allure TestOps | SaaS/OSS | Yes (REST) | Run results back-link to AC IDs in reports. |
| Notion / Confluence | SaaS | Partial | AC tables work but no test linkage; use only for early-stage drafting before moving to Jira/Linear. |

## Templates & scripts

See `templates.md` for BDD and rule-based templates; `examples.md` for login and shopping-cart cases. The repo SDD convention ties AC into `spec.md` and `test-plan.md` — the script below validates that link.

```bash
#!/usr/bin/env bash
# ac-coverage.sh — verify every AC ID in spec.md has a matching test in test-plan.md
# Usage: ac-coverage.sh <feature-dir>
set -euo pipefail
DIR="${1:?feature dir required}"
SPEC="$DIR/spec.md"
PLAN="$DIR/test-plan.md"
[[ -f "$SPEC" && -f "$PLAN" ]] || { echo "missing spec.md or test-plan.md" >&2; exit 2; }

# Extract AC IDs (format: AC-<SLUG>-NN)
mapfile -t AC_IDS < <(grep -oE 'AC-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
mapfile -t TEST_REFS < <(grep -oE 'AC-[A-Z0-9]+-[0-9]+' "$PLAN" | sort -u)

missing=()
for id in "${AC_IDS[@]}"; do
  if ! printf '%s\n' "${TEST_REFS[@]}" | grep -qx "$id"; then
    missing+=("$id")
  fi
done

if (( ${#missing[@]} )); then
  echo "FAIL: ${#missing[@]} AC without test coverage:" >&2
  printf '  %s\n' "${missing[@]}" >&2
  exit 1
fi
echo "OK: ${#AC_IDS[@]} AC, all covered."
```

Wire this into the pre-commit hook for SDD task dirs, or call from `faion-feature-executor` quality gate before flipping a task to `done/`.

## Best practices
- **Stable IDs first.** Assign `AC-<FEATURE>-NN` before content. IDs become the spine joining spec.md, test-plan.md, PR description, CI report, and changelog.
- **One observable behaviour per scenario.** Multiple `Then` lines OK only if same observation (state + side-effect). Split when assertions diverge.
- **Negative cases ≥ 30%.** Ratio of error/boundary/security AC to happy-path AC under 1:2 is a smell — agents tend to overfit happy path.
- **Avoid `And` chains > 3 in `Given`.** Long preconditions hint that the scenario should be a higher-level test or that the state setup belongs in a `Background`.
- **Behaviour level only.** No `database`, `Redis`, `kafka`, `class`, `function`, route paths in AC. Verify those via design.md / code review, not AC.
- **Tag taxonomy.** `@happy`, `@error`, `@boundary`, `@security`, `@perf`, `@a11y`, `@i18n`. Drives CI matrix and risk-based selection.
- **Living docs.** Generate AC docs from `.feature` files (`cucumber --format html`) and publish to the SDD `done/` snapshot; AC must match production behaviour or CI fails.
- **AC are the contract, not the implementation plan.** If a stakeholder edit changes AC, that's a scope change — not a coding fix.

## AI-agent gotchas
- **Hallucinated entities.** LLMs invent fields ("`subscription_tier`", "`MFA enabled`") not in the model. Mitigation: pre-load `data-analysis.md` ERD or design.md schema into the prompt as ground truth.
- **Implementation creep.** Agents leak DB/ORM/route names into Gherkin. Mitigation: post-process with a regex denylist (`SELECT|INSERT|UPDATE|/api/|class |def `) and reject violators before write.
- **Symmetric coverage bias.** Models pad with happy-path duplicates rather than thinking adversarially. Mitigation: explicit prompt slot "list 3 ways this can fail before writing AC".
- **Test-plan drift.** Coding agent updates code → AC stays stale. Always require the same PR to update spec.md AC + test-plan.md test ref + code; pre-commit gate via `ac-coverage.sh`.
- **Token-cost trap on huge specs.** Loading full spec.md every iteration wastes context. Pass only the AC IDs being edited + their direct neighbours.
- **Locale & i18n erasure.** Agents default to English/USD examples; AC silently exclude UA/EU contexts. Add explicit locale matrix per project.
- **Human-in-the-loop checkpoint.** Stakeholder sign-off on AC happens BEFORE coding starts. Do not let `faion-sdd-executor-agent` autonomously generate + execute AC in one chain — split: agent drafts → human reviews → agent executes.
- **Performance NFR theatre.** "<200ms" written but never measured. Either wire to a real benchmark gate (k6, locust, Lighthouse CI) or remove the AC.

## References
- BABOK v3, ch. 10 "Techniques" — Acceptance and Evaluation Criteria.
- Lawrence, "Acceptance Criteria — Patterns and Anti-patterns" (Agile Alliance, 2017).
- Wynne, Hellesoy, Tooke — *The Cucumber Book*, 2nd ed. (Pragmatic, 2017).
- Adzic — *Specification by Example* (Manning, 2011).
- Reqnroll docs — reqnroll.net (post-SpecFlow .NET BDD).
- Cucumber tag expressions — cucumber.io/docs/cucumber/api/#tag-expressions.
- ISO/IEC/IEEE 29148:2018 — Requirements engineering, AC guidance.
- Internal: `agents/faion-sdd-executor-agent.md`; SDD `spec.md`/`test-plan.md` convention in repo `AGENTS.md`.
