# OpenAI Function Calling & Structured Outputs

**Tool use, function calling, JSON schemas, and Pydantic validation**

---

## Quick Reference

| Feature | Use Case |
|---------|----------|
| **Function Calling** | Call external APIs, execute code, access databases |
| **Structured Outputs** | Extract data, validate schemas, enforce JSON format |
| **Parallel Tool Calls** | Execute multiple functions simultaneously |

---

## Function Calling / Tool Use

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'Kyiv'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Request with Tools

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Kyiv?"}],
    tools=tools,
    tool_choice="auto"  # "auto" | "none" | "required" | {"type": "function", "function": {"name": "get_weather"}}
)

# Check if tool call was made
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your implementation
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

# Initial request
messages = [{"role": "user", "content": "What's the weather in Kyiv?"}]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

message = response.choices[0].message
messages.append(message)  # Add assistant message

# Process tool calls
if message.tool_calls:
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
    print(final_response.choices[0].message.content)
```

### Parallel Tool Calls

Model can call multiple tools simultaneously:

```python
# Response with multiple tool calls
{
    "tool_calls": [
        {"id": "call_1", "function": {"name": "get_weather", "arguments": "{\"location\": \"Kyiv\"}"}},
        {"id": "call_2", "function": {"name": "get_weather", "arguments": "{\"location\": \"London\"}"}}
    ]
}
```

---

## Structured Outputs (Pydantic)

### Define Schema

```python
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    email: Optional[str]
    addresses: List[Address]
```

### Extract Data

```python
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30, john@example.com, lives at 123 Main St, Kyiv, Ukraine"}
    ],
    response_format=Person
)

person = response.choices[0].message.parsed
print(person.name)  # "John Doe"
print(person.addresses[0].city)  # "Kyiv"
```

### JSON Schema Validation

```python
# Force JSON output
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Generate a user profile"}
    ],
    response_format={"type": "json_object"}
)

# Parse JSON
import json
data = json.loads(response.choices[0].message.content)
```

---

## DALL-E Image Generation

### Generate Images

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene Japanese garden with a red bridge over a koi pond, photorealistic",
    size="1024x1024",      # "1024x1024" | "1792x1024" | "1024x1792"
    quality="hd",          # "standard" | "hd"
    style="vivid",         # "vivid" | "natural"
    n=1                    # DALL-E 3 only supports n=1
)

image_url = response.data[0].url
revised_prompt = response.data[0].revised_prompt  # DALL-E 3 rewrites prompts
```

### Response Formats

```python
# URL (default, expires in 1 hour)
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="url"
)

# Base64 (for immediate use)
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="b64_json"
)
image_b64 = response.data[0].b64_json
```

### Edit Images (DALL-E 2 only)

```python
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),  # Transparent areas will be regenerated
    prompt="Add a red sports car",
    size="1024x1024",
    n=1
)
```

### Create Variations (DALL-E 2 only)

```python
response = client.images.create_variation(
    model="dall-e-2",
    image=open("original.png", "rb"),
    size="1024x1024",
    n=3
)
```

### Pricing

| Model | Quality | Size | Price |
|-------|---------|------|-------|
| **DALL-E 3** | HD | 1024x1024 | $0.080 |
| **DALL-E 3** | HD | 1792x1024, 1024x1792 | $0.120 |
| **DALL-E 3** | Standard | 1024x1024 | $0.040 |
| **DALL-E 3** | Standard | 1792x1024, 1024x1792 | $0.080 |
| **DALL-E 2** | - | 1024x1024 | $0.020 |

### Prompt Tips

```
Style keywords: "photorealistic", "digital art", "oil painting", "3D render", "anime style"
Lighting: "soft lighting", "golden hour", "neon glow", "dramatic shadows"
Composition: "centered", "rule of thirds", "wide angle", "close-up", "aerial view"
Quality: "highly detailed", "8K resolution", "professional photography"
Mood: "serene", "dramatic", "playful", "mysterious", "minimalist"
```

---

## Whisper (Speech-to-Text)

### Transcription

```python
audio_file = open("speech.mp3", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="uk",           # ISO 639-1 code (optional)
    response_format="text",  # "json" | "text" | "srt" | "vtt" | "verbose_json"
    temperature=0.0,         # 0-1, lower = more deterministic
    prompt="SDD, Faion Network"  # Hints for proper nouns
)

print(transcript)  # Plain text for response_format="text"
```

### Verbose JSON (with timestamps)

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"]
)

for segment in transcript.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

### Translation (to English)

```python
# Translates any language to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=open("ukrainian_speech.mp3", "rb"),
    response_format="text"
)
```

### Supported Formats

- mp3, mp4, mpeg, mpga, m4a, wav, webm
- Max file size: 25MB
- For longer files: split or use chunking

### Pricing

| Model | Price |
|-------|-------|
| whisper-1 | $0.006 / minute |

---

## TTS (Text-to-Speech)

### Generate Speech

```python
response = client.audio.speech.create(
    model="tts-1-hd",        # "tts-1" (fast) | "tts-1-hd" (quality)
    voice="nova",            # alloy | echo | fable | onyx | nova | shimmer
    input="Hello, welcome to Faion Network!",
    speed=1.0,               # 0.25 - 4.0
    response_format="mp3"    # mp3 | opus | aac | flac | wav | pcm
)

response.stream_to_file("output.mp3")
```

### Streaming

```python
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="Long text to speak..."
) as response:
    response.stream_to_file("output.mp3")
```

### Voice Characteristics

| Voice | Description |
|-------|-------------|
| **alloy** | Neutral, balanced |
| **echo** | Warm, authoritative |
| **fable** | British, expressive |
| **onyx** | Deep, rich |
| **nova** | Young, energetic |
| **shimmer** | Soft, gentle |

### Pricing

| Model | Price |
|-------|-------|
| tts-1 | $15.00 / 1M characters |
| tts-1-hd | $30.00 / 1M characters |

---

## Related

- [openai-chat-completions.md](openai-chat-completions.md) - Chat API basics
- [openai-embeddings.md](openai-embeddings.md) - Text embeddings
- [openai-assistants.md](openai-assistants.md) - Assistants API
