# M-LLM-006: Context Window Optimization

## Overview

Context window optimization maximizes the effective use of an LLM's token limit. Techniques include smart chunking, summarization, sliding windows, and hierarchical context. Critical for handling long documents, conversations, and complex tasks.

**When to use:** When working with content that exceeds model limits, long conversations, or when token costs matter.

## Core Concepts

### 1. Context Window Sizes (2025)

| Model | Context Window | Notes |
|-------|----------------|-------|
| GPT-4o | 128K tokens | ~96K words |
| GPT-4o-mini | 128K tokens | Cost-effective |
| Claude 3.5 Sonnet | 200K tokens | Extended thinking adds more |
| Claude 3 Opus | 200K tokens | Best for long reasoning |
| Gemini 1.5 Pro | 2M tokens | Largest available |
| Llama 3.1 405B | 128K tokens | Open source |

### 2. Token Estimation

| Content Type | ~Tokens per Unit |
|--------------|------------------|
| English word | 1.3 tokens |
| Code character | 0.3-0.5 tokens |
| Emoji | 1-3 tokens |
| URL | 10-20 tokens |
| JSON (per KB) | ~250 tokens |

### 3. Context Budget Allocation

```
Total Context = Input + Output Reserve + Safety Margin

Example for 128K model:
- Input Budget: 100K tokens
- Output Reserve: 20K tokens
- Safety Margin: 8K tokens
```

## Best Practices

### 1. Prioritize Information

```python
def build_context(
    system_prompt: str,      # Always include (high priority)
    current_query: str,      # Always include
    relevant_docs: list,     # Top-k most relevant
    chat_history: list,      # Recent turns only
    max_tokens: int = 100000
) -> str:
    context_parts = []
    used_tokens = 0

    # Priority 1: System prompt
    context_parts.append(system_prompt)
    used_tokens += count_tokens(system_prompt)

    # Priority 2: Current query
    context_parts.append(current_query)
    used_tokens += count_tokens(current_query)

    # Priority 3: Relevant documents (most relevant first)
    for doc in relevant_docs:
        doc_tokens = count_tokens(doc)
        if used_tokens + doc_tokens < max_tokens * 0.7:
            context_parts.append(doc)
            used_tokens += doc_tokens
        else:
            break

    # Priority 4: Recent chat history (newest first)
    for message in reversed(chat_history):
        msg_tokens = count_tokens(message)
        if used_tokens + msg_tokens < max_tokens * 0.8:
            context_parts.insert(-1, message)  # Before query
            used_tokens += msg_tokens
        else:
            break

    return "\n\n".join(context_parts)
```

### 2. Summarize Long Content

```python
def hierarchical_summarize(document: str, target_tokens: int) -> str:
    """Summarize document to fit target token count."""

    current_tokens = count_tokens(document)

    if current_tokens <= target_tokens:
        return document

    # Level 1: Chunk and summarize each section
    chunks = split_into_chunks(document, chunk_size=2000)
    summaries = []

    for chunk in chunks:
        summary = llm.summarize(
            chunk,
            instruction="Summarize key points in 2-3 sentences"
        )
        summaries.append(summary)

    combined = "\n\n".join(summaries)

    # Level 2: If still too long, summarize summaries
    if count_tokens(combined) > target_tokens:
        return llm.summarize(
            combined,
            instruction=f"Create a comprehensive summary in ~{target_tokens} tokens"
        )

    return combined
```

### 3. Use Sliding Windows

```python
class SlidingWindowContext:
    def __init__(self, max_tokens: int = 100000, overlap_tokens: int = 500):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim_if_needed()

    def _trim_if_needed(self):
        total_tokens = sum(count_tokens(m["content"]) for m in self.messages)

        while total_tokens > self.max_tokens and len(self.messages) > 2:
            # Keep system message and latest messages
            # Summarize and remove oldest non-system messages
            oldest = self.messages[1]  # Skip system message

            # Summarize before removing
            self.messages[1] = {
                "role": "system",
                "content": f"[Previous context summary: {summarize(oldest)}]"
            }

            # Remove original
            self.messages.pop(2)

            total_tokens = sum(count_tokens(m["content"]) for m in self.messages)

    def get_context(self) -> list:
        return self.messages.copy()
```

## Common Patterns

### Pattern 1: Smart Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def smart_chunk(text: str, chunk_size: int = 1000, overlap: int = 200):
    """Split text respecting semantic boundaries."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n## ",      # Markdown headers
            "\n### ",
            "\n\n",       # Paragraphs
            "\n",         # Lines
            ". ",         # Sentences
            " ",          # Words
            ""            # Characters
        ],
        length_function=count_tokens
    )

    return splitter.split_text(text)
```

### Pattern 2: Context Compression

```python
from llmlingua import PromptCompressor

def compress_context(context: str, target_ratio: float = 0.5):
    """Compress context while preserving meaning."""

    compressor = PromptCompressor()

    compressed = compressor.compress_prompt(
        context,
        instruction="",
        target_token=int(count_tokens(context) * target_ratio),
        use_sentence_level_filter=True,
        use_context_level_filter=True
    )

    return compressed["compressed_prompt"]
```

### Pattern 3: Map-Reduce for Long Documents

```python
def process_long_document(document: str, query: str) -> str:
    """Process document longer than context window."""

    # Map: Process each chunk independently
    chunks = smart_chunk(document, chunk_size=50000)
    chunk_results = []

    for chunk in chunks:
        result = llm.invoke(
            system="Extract information relevant to the query.",
            user=f"Document chunk:\n{chunk}\n\nQuery: {query}"
        )
        chunk_results.append(result)

    # Reduce: Combine chunk results
    combined = "\n\n---\n\n".join(chunk_results)

    final = llm.invoke(
        system="Synthesize these partial results into a comprehensive answer.",
        user=f"Partial results:\n{combined}\n\nOriginal query: {query}"
    )

    return final
```

### Pattern 4: Relevant Context Selection

```python
def select_relevant_context(
    query: str,
    available_context: list[str],
    max_tokens: int = 50000
) -> list[str]:
    """Select most relevant context items using embeddings."""

    # Embed query
    query_embedding = embed(query)

    # Score and rank context items
    scored_items = []
    for item in available_context:
        item_embedding = embed(item)
        score = cosine_similarity(query_embedding, item_embedding)
        tokens = count_tokens(item)
        scored_items.append((item, score, tokens))

    # Sort by relevance
    scored_items.sort(key=lambda x: x[1], reverse=True)

    # Select items that fit in budget
    selected = []
    used_tokens = 0

    for item, score, tokens in scored_items:
        if used_tokens + tokens <= max_tokens:
            selected.append(item)
            used_tokens += tokens

    return selected
```

### Pattern 5: Conversation Summarization

```python
class ConversationManager:
    def __init__(self, max_history_tokens: int = 10000):
        self.max_history_tokens = max_history_tokens
        self.messages = []
        self.summary = ""

    def add_turn(self, user: str, assistant: str):
        self.messages.append({"user": user, "assistant": assistant})
        self._manage_history()

    def _manage_history(self):
        total_tokens = sum(
            count_tokens(m["user"]) + count_tokens(m["assistant"])
            for m in self.messages
        )

        if total_tokens > self.max_history_tokens:
            # Summarize older messages
            old_messages = self.messages[:-5]  # Keep last 5

            summary_input = "\n".join([
                f"User: {m['user']}\nAssistant: {m['assistant']}"
                for m in old_messages
            ])

            self.summary = llm.summarize(
                f"Previous summary: {self.summary}\n\nNew messages:\n{summary_input}",
                instruction="Update the conversation summary with key points"
            )

            self.messages = self.messages[-5:]

    def get_context(self) -> str:
        context = f"Conversation summary: {self.summary}\n\n" if self.summary else ""
        context += "\n".join([
            f"User: {m['user']}\nAssistant: {m['assistant']}"
            for m in self.messages
        ])
        return context
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Including all history | Wastes tokens | Summarize or truncate |
| No overlap in chunks | Lost context | Add overlap (10-20%) |
| Fixed chunk sizes | Breaks sentences | Use semantic chunking |
| Ignoring token costs | Expensive | Monitor and optimize |
| One-size-fits-all | Suboptimal | Adapt to content type |

## Tools & References

### Related Skills
- faion-langchain-skill
- faion-llamaindex-skill
- faion-embeddings-skill

### Related Agents
- faion-rag-agent
- faion-cost-optimizer-agent

### External Resources
- [tiktoken](https://github.com/openai/tiktoken) - OpenAI tokenizer
- [LLMLingua](https://github.com/microsoft/LLMLingua) - Prompt compression
- [LangChain Text Splitters](https://python.langchain.com/docs/concepts/text_splitters/)

## Checklist

- [ ] Identified context window limit
- [ ] Calculated token budgets
- [ ] Implemented smart chunking
- [ ] Added summarization for long content
- [ ] Set up sliding window for conversations
- [ ] Optimized for relevance (not just recency)
- [ ] Added compression if needed
- [ ] Monitoring token usage
- [ ] Tested with edge cases

---

*Methodology: M-LLM-006 | Category: LLM/Orchestration*
*Related: faion-rag-agent, faion-cost-optimizer-agent, faion-langchain-skill*
