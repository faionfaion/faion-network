from anthropic_agents import Agent

investigator = Agent(
    model="claude-sonnet-...",
    system_prompt=(
        "You are an investigation subagent. "
        "After investigation, return STRICT JSON: "
        "{summary: str, refs: list[str], confidence: 'high'|'medium'|'low'}. "
        "Do NOT include source code in your output."
    ),
    max_tokens=600,
)

report = investigator.run("Find every place using auth_v1.")
# report is a JSON object; parent uses report.refs to know where to look
