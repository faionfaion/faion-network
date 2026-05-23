<!-- purpose: per-tool decision-table reference of fix vs flag outcomes by rule class. -->
<!-- consumes: tool name + finding kind + autofix capability flag. -->
<!-- produces: decision-record (per-row decision routing). -->
<!-- depends-on: content/01-core-rules.xml; templates/agent-policy.txt. -->
<!-- token-budget-impact: low — ~250 tokens. -->

# Autofix vs Flag — Decision Table

| Tool | Finding kind | Has `fix:` block? | Action |
|------|--------------|-------------------|--------|
| ruff | format / import-sort / E / W / I | yes | autofix (`--fix && format`) |
| ruff | F401 unused-import | yes | autofix |
| ruff | T20 print() in prod | no auto | flag (decide remove vs convert to logger) |
| biome | format / quote / semi | yes | autofix (`--write`) |
| biome | noExplicitAny | no | flag (type the value) |
| eslint | recommended autofixable | yes | autofix (`--fix`) |
| prettier | any | yes | autofix |
| semgrep | rule with `fix:` | yes | autofix (`--autofix`) |
| semgrep | rule without `fix:` | no | flag (PR suggestion) |
| codeql | any alert | no | flag (block PR, propose Copilot Autofix as suggestion) |
| snyk code | any | partial | flag (propose Snyk Agent Fix patch as suggestion) |
| snyk oss | CVE with patched version | yes | autofix bump in dedicated PR |
| snyk oss | CVE without patched version | no | flag, escalate to human |
| gitleaks | secret found | n/a | ROTATE first, then clean up; never silent strip |
| trufflehog | verified secret | n/a | P0 incident; rotate, then revert |
| fossa / licensee | license conflict | n/a | ALWAYS human escalation |
| sonarqube | cognitive complexity hotspot | n/a | flag, propose refactor as draft PR |
| sonarqube | duplicated block | n/a | flag, propose extraction as draft PR |
| trivy | container CVE | n/a | flag if no patched base image; bump base image in dedicated PR |
| commitlint | non-conformant message | yes | autofix on hook (rewrite); fail on CI if push slipped through |

Every "autofix" row also requires: tests pass after fix, diff < 50 lines or single rule ID.
