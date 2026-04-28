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
