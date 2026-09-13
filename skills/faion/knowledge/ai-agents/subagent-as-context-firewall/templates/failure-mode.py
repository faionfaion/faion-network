# purpose: Reference anti-example: a leaky subagent that pastes evidence into the parent
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

try:
    report = subagent.run(...)
except SubagentTimeout:
    report = SubagentReport(
        summary="Subagent timed out before completion.",
        refs=[],
        confidence="low",
        next_actions=["Retry with a smaller scope."]
    )

# Always return a structured failure — never silent errors.
