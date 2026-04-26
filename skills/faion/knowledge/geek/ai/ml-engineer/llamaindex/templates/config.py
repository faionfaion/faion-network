"""LlamaIndex storage and service context configuration."""
import os
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding


def configure_llamaindex(
    model: str = "claude-opus-4-5",
    embed_model: str = "text-embedding-3-large",
    chunk_size: int = 512,
    chunk_overlap: int = 64,
) -> None:
    """Set global LlamaIndex settings."""
    Settings.llm = Anthropic(model=model, api_key=os.environ["ANTHROPIC_API_KEY"])
    Settings.embed_model = OpenAIEmbedding(
        model=embed_model,
        api_key=os.environ["OPENAI_API_KEY"],
    )
    Settings.node_parser = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    Settings.num_output = 1024
    Settings.context_window = 4096


def load_or_create_storage(persist_dir: str) -> StorageContext:
    """Load existing index or return empty storage context."""
    if os.path.exists(persist_dir):
        return StorageContext.from_defaults(persist_dir=persist_dir)
    return StorageContext.from_defaults()
