# OpenAI Assistants API

**Stateful agents with file search, code interpreter, and tool use**

---

## Quick Reference

| Feature | Use Case |
|---------|----------|
| **Assistants** | Stateful AI agents with persistent context |
| **File Search** | RAG over uploaded documents |
| **Code Interpreter** | Execute Python code, analyze data |
| **Threads** | Persistent conversations |

---

## Assistants API

### Create Assistant

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model="gpt-4o",
    name="SDD Expert",
    instructions="You are an expert on Specification-Driven Development. Help users understand and apply SDD methodology.",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ],
    temperature=0.7,
    metadata={"version": "1.0"}
)
```

### Create Thread

```python
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What are the key phases of SDD?"
        }
    ]
)
```

### Run Assistant

```python
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            print(message.content[0].text.value)
```

### Streaming Run

```python
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\n[Using tool: {tool_call.type}]")

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler()
) as stream:
    stream.until_done()
```

---

## File Search (Knowledge Base)

### Create Vector Store

```python
# Create vector store
vector_store = client.beta.vector_stores.create(name="SDD Documentation")

# Upload files
file = client.files.create(
    file=open("sdd-guide.pdf", "rb"),
    purpose="assistants"
)

client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id
)

# Attach to assistant
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)
```

### Query Documents

```python
# Create thread with file search
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What does the SDD guide say about specifications?"
        }
    ]
)

# Run with file search
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Get response with citations
messages = client.beta.threads.messages.list(thread_id=thread.id)
for message in messages.data:
    if message.role == "assistant":
        print(message.content[0].text.value)
        # Check for file citations
        if message.content[0].text.annotations:
            for annotation in message.content[0].text.annotations:
                print(f"Source: {annotation.file_citation.file_id}")
```

---

## Code Interpreter

### Upload Data File

```python
# Upload data file
file = client.files.create(
    file=open("data.csv", "rb"),
    purpose="assistants"
)

# Create thread with attachment
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Analyze this data and create a chart",
            "attachments": [
                {"file_id": file.id, "tools": [{"type": "code_interpreter"}]}
            ]
        }
    ]
)
```

### Execute Code

```python
# Run assistant with code interpreter
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Get generated images and outputs
messages = client.beta.threads.messages.list(thread_id=thread.id)
for message in messages.data:
    if message.role == "assistant":
        for content in message.content:
            if content.type == "image_file":
                # Download generated chart
                image_data = client.files.content(content.image_file.file_id)
                with open("chart.png", "wb") as f:
                    f.write(image_data.read())
            elif content.type == "text":
                print(content.text.value)
```

---

## Best Practices

### 1. Use Threads for Conversations

```python
# Create thread once
thread = client.beta.threads.create()

# Add messages over time
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="First question"
)

# Run assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Continue conversation
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Follow-up question"
)
```

### 2. Stream Responses for UX

```python
class StreamHandler(AssistantEventHandler):
    def on_text_delta(self, delta, snapshot):
        # Update UI in real-time
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\n[Tool: {tool_call.type}]")

    def on_tool_call_done(self, tool_call):
        print("\n[Tool complete]")
```

### 3. Handle Rate Limits

```python
import time

def run_with_retry(thread_id, assistant_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 4. Manage Vector Stores

```python
# List all vector stores
vector_stores = client.beta.vector_stores.list()

# Delete old vector store
client.beta.vector_stores.delete(vector_store_id="vs_xxx")

# Update vector store
client.beta.vector_stores.update(
    vector_store_id="vs_xxx",
    name="Updated name"
)
```

---

## Cost Optimization

### Track Assistant Usage

```python
# Monitor run costs
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

print(f"Prompt tokens: {run.usage.prompt_tokens}")
print(f"Completion tokens: {run.usage.completion_tokens}")
print(f"Total tokens: {run.usage.total_tokens}")
```

### Cleanup Resources

```python
# Delete assistant when done
client.beta.assistants.delete(assistant.id)

# Delete thread
client.beta.threads.delete(thread.id)

# Delete files
client.files.delete(file.id)
```

---

## Quick Commands

### curl Examples

```bash
# Create assistant
curl https://api.openai.com/v1/assistants \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "model": "gpt-4o",
    "name": "SDD Expert",
    "instructions": "You are an SDD expert.",
    "tools": [{"type": "file_search"}]
  }'

# Create thread
curl https://api.openai.com/v1/threads \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Related

- [openai-chat-completions.md](openai-chat-completions.md) - Chat API basics
- [openai-function-calling.md](openai-function-calling.md) - Tool use and structured outputs
- [openai-embeddings.md](openai-embeddings.md) - Text embeddings
