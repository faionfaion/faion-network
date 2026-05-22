# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

from claude_code import Task

result = Task.run(
    subagent_type="general-purpose",
    prompt=(
        "Find every place in /home/nero/repo/src that uses the legacy `auth_v1` "
        "function. Return only: summary (1-2 sentences) + list of file:line refs. "
        "Do NOT paste source code — the parent will re-read the files it cares about."
    ),
    description="Find legacy auth_v1 usages"
)
# result.text typically < 500 tokens; result.refs available
