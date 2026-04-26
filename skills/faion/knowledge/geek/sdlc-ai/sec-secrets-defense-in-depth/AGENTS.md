# Two-Layer Secret Scanning: Gitleaks + Verified TruffleHog

## Summary

Run two complementary secret scanners in two different lifecycle stages. Layer one is `gitleaks` as a pre-commit hook on the developer or agent machine: sub-second, regex-based, blocks the commit before any secret enters local git history. Layer two is `trufflehog --results=verified` in CI on every PR: it actively calls the issuing provider (AWS STS, GitHub, Stripe, Slack, OpenAI, Anthropic) to confirm the candidate token is live, and treats verified findings as P0 incidents that trigger immediate rotation before revert.

## Why

No single secret scanner wins. Gitleaks is fast and local but cannot tell a real key from a plausible one, so on its own it produces noise that humans and agents learn to bypass. TruffleHog inverts the trade-off — over 800 detector types, 2026's adaptive AI detection, and live verification cuts false positives close to zero, but it is too slow and network-heavy for a pre-commit hook. Layering them turns each tool's weakness into the other's job: gitleaks stops the obvious leaks at write time, TruffleHog confirms the survivors at PR time. GitGuardian's 2026 sprawl report measured 29 million new secrets leaked publicly in 2025 with an 81% surge specifically in AI-service tokens — the failure mode is now agents pasting `sk-...` keys into commits, which is exactly what the two-layer pattern catches.

## When To Use

- Every repository, no exception — even single-developer prototypes, because a leaked AWS or OpenAI key costs more than the project earns.
- Repos where AI agents commit on behalf of humans — verified scanning is the only check that distinguishes a real `sk-ant-` token from a docstring example.
- Monorepos with mixed languages and config formats where naive pattern matchers miss provider-specific encodings (JWT, .pem, dotenv, terraform tfvars).
- Migrations of historical secrets — pair with `detect-secrets` baseline so that historical findings can be ratcheted out without blocking every PR.

## When NOT To Use

- There is no NOT case for the two layers themselves; only the *depth* (1 layer vs 2) varies. A throwaway gist might run only gitleaks pre-commit and skip the CI verifier.
- Air-gapped repos with no network egress in CI — TruffleHog verification calls providers, which is impossible without egress; substitute provider-specific offline format checks.
- Generated code drops where every blob is regenerated from a private template store — scan the template store instead of the generated tree.

## Content

| File | What's inside |
|------|---------------|
| `content/01-precommit-block.xml` | Local gitleaks hook configuration and the no-bypass rule for agents and humans. |
| `content/02-verified-ci-gate.xml` | The TruffleHog `--results=verified` PR gate and the rotate-before-revert response contract. |
| `content/03-rotation-runbook.xml` | Concrete provider-rotation steps when a verified secret lands and the audit trail it leaves. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gitleaks.toml` | Allowlist + extend-default rules tuned to ignore docs/test fixtures. |
| `templates/trufflehog-action.yml` | GitHub Actions step running TruffleHog on PR diff with verified-only output. |
| `templates/precommit-secrets.yaml` | `pre-commit` framework block wiring gitleaks into the standard hook chain. |
