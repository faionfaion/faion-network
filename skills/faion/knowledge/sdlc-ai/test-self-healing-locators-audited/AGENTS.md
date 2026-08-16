# Self-Healing Locators with Mandatory Audit Diff

## Summary

**One-sentence:** Restrict E2E selector self-healing to candidates matching the original locator's accessibility role AND accessible name; require every heal to land as a reviewable diff before CI consumes it.

**One-paragraph:** In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.diff` or equivalent) before the next CI run consumes it. Auto-healing without an audit trail is silent test rot; allowing arbitrary CSS-substitution heals is how an E2E suite ends up clicking the wrong button on a payment screen.

**Ефективно для:**

- Playwright/Cypress/Selenium suites з частими selector breaks.
- WCAG-aware UIs, де role+accessible-name надійні.
- Payment / checkout flows: silent click-wrong-button — недопустиме.
- Audit-driven QA orgs: heal-diff як changelog для tests.

## Applies If (ALL must hold)

- E2E suite (Playwright / Cypress / Selenium) where locators break often.
- AI healer is enabled or proposed.
- Reviewer capacity exists to triage `healed-selectors.diff` weekly.

## Skip If (ANY kills it)

- Suite small enough that broken locators are fixed by hand in minutes.
- Application has no accessible-name affordances (legacy / canvas-only UI).
- Team unwilling to gate healing on review — healer will be effectively disabled.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing E2E suite | code | tests/e2e/ |
| Accessibility-tree snapshot of app | JSON | tests/fixtures/ |
| Healer plugin / CLI | binary | deps |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/healer-ci.yml` | CI workflow that emits heals to a diff file and gates next run on human merge. |
| `templates/healer-policy.json` | Healer policy with match dimensions, blocklist, scope, rollback window. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-self-healing-locators-audited.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[test-mutation-feedback-loop]]
- [[test-tdd-red-green-split-agents]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/healer-ci.yml`

```yaml
# Drop-in GitHub Actions snippet for self-healing locator audit gate.
name: e2e-with-healer

on: pull_request

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: pnpm install --frozen-lockfile
      - run: pnpm playwright install --with-deps
      - name: Run E2E with healer
        run: pnpm playwright test --reporter=list
        # healer writes healed-selectors.diff and exits 1 on heal
      - name: Check for unapproved heals
        if: failure()
        run: |
          if [ -s healed-selectors.diff ]; then
            echo "::error::Healer produced selector changes; review healed-selectors.diff"
            cat healed-selectors.diff
            exit 1
          fi

  healer-apply:
    needs: e2e
    if: contains(github.event.head_commit.message, 'healer:approved')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: git apply healed-selectors.diff
      - run: rm healed-selectors.diff
      - name: Open follow-up PR
        run: 'gh pr create --title "chore(e2e): apply approved healer diff" --body "Automated."'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### `templates/healer-policy.json`

```json
{
  "$comment": "Self-healing locator policy. Read by the healer before every heal attempt.",
  "match": {
    "require_role_equality": true,
    "require_accessible_name_match": true,
    "name_match_kind": "regex",
    "name_match_flags": "i",
    "case_insensitive_role": true,
    "allow_class_only_heal": false,
    "allow_xpath_index_heal": false,
    "allow_text_only_heal": false
  },
  "exclude_paths": [
    "tests/e2e/payments/**",
    "tests/e2e/auth/**",
    "tests/e2e/account-deletion/**",
    "tests/e2e/admin/role-elevation/**"
  ],
  "diff": {
    "path": "healed-selectors.diff",
    "exit_after_write": 1,
    "approval_marker": "healer:approved",
    "approval_marker_in": "commit-message"
  },
  "limits": {
    "max_heals_per_run": 25,
    "max_files_touched_per_run": 10
  }
}
```
