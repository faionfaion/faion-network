"""One-shot assistant interaction with run status validation.

Usage:
    result = query_assistant(assistant_id, thread_id, "What is SDD?")
"""
from openai import OpenAI

client = OpenAI()


def query_assistant(assistant_id: str, thread_id: str, question: str) -> str:
    """Add a message to a thread, run the assistant, return the response.

    Args:
        assistant_id: ID of the pre-created assistant.
        thread_id: ID of the existing thread for this conversation.
        question: User's question to add to the thread.

    Returns:
        Assistant's response text.

    Raises:
        RuntimeError: If run ends in any non-completed status.
    """
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=question
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    if run.status != "completed":
        raise RuntimeError(f"Run failed: {run.status} — {run.last_error}")
    msgs = client.beta.threads.messages.list(
        thread_id=thread_id, order="desc", limit=1
    )
    return msgs.data[0].content[0].text.value
