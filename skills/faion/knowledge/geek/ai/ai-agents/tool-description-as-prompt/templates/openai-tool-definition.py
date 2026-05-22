# purpose: OpenAI SDK function definition using 5-part description
# consumes: tool name + function signature + side-effect class
# produces: tool definition (Python dict) conforming to content/02-output-contract.xml schema constraints
# depends-on: 01-core-rules.xml (structured-description-required, under-200-tokens, anti-trigger-required-on-overlap, mutating-marker-required, latency-and-pagination-caps, description-matches-schema)
# token-budget-impact: ~80-180 tokens per tool description
tools = [{
    "type": "function",
    "function": {
        "name": "create_pr",
        "description": (
            "Create a pull request from the current working branch. "
            "Use this when the user has finalized changes and wants them on the remote. "
            "Do NOT use this if the working tree is dirty (run `git_status` first). "
            "Side effect: pushes branch and opens a PR on GitHub. Returns the PR URL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["title"],
        },
    },
}]
