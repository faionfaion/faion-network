# License Compliance as a Build-Blocking Gate

## Summary

Every release pipeline runs an automated license scan against an explicit allowlist. Free OSS-shipped projects use GitHub's `licensee` for source detection; commercial SaaS or shipped binaries use FOSSA (or Black Duck / ScanCode) to produce an SPDX/CycloneDX SBOM and a deny/flag/approve decision per dependency. Copyleft licenses (GPL, AGPL, SSPL) introduced into proprietary builds block the pipeline; the agent regenerates the `NOTICE` / `THIRD_PARTY.md` attribution file on every dependency change. License scanning runs on PR, not just on release.

## Why

License violations are legal liability, not just hygiene. AGPL pulled into a SaaS triggers a source-disclosure obligation across the entire stack; HashiCorp's BSL switch demonstrated how a single dep license change can invalidate a downstream product. Manual review does not scale once an AI agent is autonomously adding dependencies. Continuous license scanning produces a "living SBOM" required by the EU Cyber Resilience Act (mandatory September 2026 reporting, full December 2027) and US Executive Order 14028; FOSSA reports 99.8% accuracy across 17+ languages and 20+ build systems, which closes the gap human review left open.

## When To Use

- Any product distributed externally — SaaS, downloadable, OSS published — where license obligations attach.
- Enterprise procurement contexts where customers ask for an SBOM and a license attestation.
- Repos where AI agents add dependencies autonomously; the agent is the new "developer who didn't read the license".
- Products subject to EU CRA (anything sold in the EU after Sep 2026) or US federal procurement (EO 14028 SBOM mandate).

## When NOT To Use

- Internal-only tools that never leave the org boundary — no redistribution, no obligation.
- Hobby projects with zero compliance bar (still good hygiene if free; skip if it slows you down).
- Vendored read-only mirrors — license obligations follow the upstream redistribution, not the mirror.
- Pure data repos with no compiled artifact — apply data-license review instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-allowlist-and-block.xml` | License allowlist, copyleft block, NOTICE regeneration, agent decision flow. |
| `content/02-sbom-as-release-artifact.xml` | SPDX/CycloneDX SBOM as a signed release artifact, EU CRA alignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/license-policy.yml` | Allow / flag / deny policy consumed by FOSSA / scancode-toolkit / `pip-licenses`. |
| `templates/license-check.yml` | GitHub Actions workflow running licensee + a CycloneDX SBOM emitter on every PR. |
