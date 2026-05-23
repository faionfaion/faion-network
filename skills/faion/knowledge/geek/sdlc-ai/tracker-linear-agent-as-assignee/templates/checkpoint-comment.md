<!-- purpose: Checkpoint comment template (elapsed time + current step). -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

<!--
  Agent checkpoint comment for a Linear issue.
  Post one comment per state transition: started, in-progress, blocked,
  ready-for-review. The header line is parsed by the runtime — keep it
  on the FIRST line, in the EXACT format below.
-->

[{{agent.name}} · {{state}} · {{elapsed_minutes}}m]
{{ task list, one bullet per concrete step, with ✅ done | ⏳ in-progress | ⛔ blocked }}
{{ optional: file paths or function names touched, for reviewer context }}

<!--
  Final checkpoint (state=ready-for-review) MUST contain the PR URL
  on its own line so Linear auto-links it to the issue:

      PR opened: https://github.com/<org>/<repo>/pull/<n>

  Do NOT post the PR link in any earlier checkpoint; reviewers anchor
  on the PR and skip the spec correction the checkpoints exist for.
-->
