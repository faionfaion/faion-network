try:
    report = subagent.run(...)
except SubagentTimeout:
    report = SubagentReport(
        summary="Subagent timed out before completion.",
        refs=[],
        confidence="low",
        follow_up_questions=["Should we retry with a smaller scope?"]
    )

# Always return a structured failure — never silent errors.
