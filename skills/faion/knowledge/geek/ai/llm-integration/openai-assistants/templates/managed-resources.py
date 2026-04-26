"""Context managers for OpenAI Assistants thread and vector store lifecycle.

Usage:
    with managed_thread() as thread_id:
        result = query_assistant(assistant_id, thread_id, "question")

    with managed_vector_store("docs", ["path/to/doc.pdf"]) as vs_id:
        # use vs_id
"""
from contextlib import contextmanager
from openai import OpenAI

client = OpenAI()


@contextmanager
def managed_thread():
    """Create a thread, yield its ID, then delete on exit."""
    thread = client.beta.threads.create()
    try:
        yield thread.id
    finally:
        client.beta.threads.delete(thread.id)


@contextmanager
def managed_vector_store(name: str, file_paths: list[str]):
    """Upload files, create vector store, yield vs_id, then delete on exit.

    Args:
        name: Human-readable name for the vector store.
        file_paths: List of local file paths to upload.
    """
    files = [
        client.files.create(file=open(p, "rb"), purpose="assistants")
        for p in file_paths
    ]
    vs = client.beta.vector_stores.create(name=name)
    for f in files:
        client.beta.vector_stores.files.create(vector_store_id=vs.id, file_id=f.id)
    try:
        yield vs.id
    finally:
        client.beta.vector_stores.delete(vs.id)
        for f in files:
            client.files.delete(f.id)
