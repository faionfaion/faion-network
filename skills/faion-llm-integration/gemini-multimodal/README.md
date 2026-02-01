---
name: faion-gemini-multimodal
user-invocable: false
description: "Gemini multimodal: images, video, audio, PDFs, code execution"
---

# Gemini Multimodal Capabilities

**Native support for images, video, audio, PDFs, and code execution.**

---

## Quick Reference

| Modality | Formats | Max Size | Use Cases |
|----------|---------|----------|-----------|
| **Images** | JPG, PNG, WEBP, HEIC, HEIF | 20MB | Vision, OCR, analysis |
| **Video** | MP4, MPEG, MOV, AVI, FLV, MPG, WEBM, WMV, 3GPP | 2GB | Video understanding, timestamps |
| **Audio** | MP3, WAV, AIFF, AAC, OGG, FLAC | 100MB | Transcription, analysis |
| **PDFs** | PDF | 100MB | Document Q&A, extraction |
| **Code Execution** | Python sandbox | - | Data analysis, charts |

---

## Image Analysis

### Basic Image Analysis

```python
import PIL.Image
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

# From file
image = PIL.Image.open("photo.jpg")
response = model.generate_content([
    "Describe this image in detail",
    image
])

# From URL (upload first)
image_file = genai.upload_file("photo.jpg")
response = model.generate_content([
    "What objects are in this image?",
    image_file
])
```

### Multiple Images

```python
image1 = PIL.Image.open("before.jpg")
image2 = PIL.Image.open("after.jpg")

response = model.generate_content([
    "Compare these two images and describe the differences",
    image1,
    image2
])
```

### Multimodal Chat with Images

```python
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Text message
response = chat.send_message("I'll show you some code screenshots")

# Image message
image = PIL.Image.open("code_screenshot.png")
response = chat.send_message([
    "What's wrong with this code?",
    image
])
```

---

## Video Understanding (Native)

### Basic Video Analysis

```python
# Upload video file (supports MP4, MPEG, MOV, AVI, etc.)
video_file = genai.upload_file("presentation.mp4")

# Wait for processing
import time
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = genai.get_file(video_file.name)

# Analyze video
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Summarize the key points of this video presentation",
    video_file
])
print(response.text)
```

### Video with Timestamps

```python
response = model.generate_content([
    "What happens at the 2:30 mark in this video?",
    video_file
])
```

### Video Content Extraction

```python
# Extract structured information from video
response = model.generate_content([
    """Analyze this video and extract:
    - Main topics discussed
    - Key timestamps and what happens
    - Action items mentioned
    - People appearing in the video
    Return as JSON""",
    video_file
])
```

---

## Audio Understanding (Native)

### Audio Transcription

```python
# Upload audio file (supports MP3, WAV, AIFF, AAC, OGG, FLAC)
audio_file = genai.upload_file("podcast.mp3")

# Wait for processing
while audio_file.state.name == "PROCESSING":
    time.sleep(5)
    audio_file = genai.get_file(audio_file.name)

# Transcribe
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Transcribe this audio recording",
    audio_file
])
```

### Audio Analysis

```python
# Topic extraction
response = model.generate_content([
    "What are the main topics discussed in this podcast?",
    audio_file
])

# Speaker identification
response = model.generate_content([
    "Identify the speakers and summarize what each person said",
    audio_file
])

# Sentiment analysis
response = model.generate_content([
    "What is the overall tone and sentiment of this audio?",
    audio_file
])
```

---

## PDF Processing

### Basic PDF Analysis

```python
# Upload PDF
pdf_file = genai.upload_file("document.pdf")

model = genai.GenerativeModel("gemini-1.5-pro")

# Summarize
response = model.generate_content([
    "Summarize this document",
    pdf_file
])
```

### Information Extraction from PDF

```python
# Extract specific information
response = model.generate_content([
    "Extract all dates and deadlines mentioned in this document",
    pdf_file
])

# Structured extraction
response = model.generate_content([
    """Extract the following from this contract:
    - Party names
    - Contract value
    - Key dates
    - Payment terms
    Return as JSON""",
    pdf_file
])
```

### Q&A over PDF

```python
# Question answering
response = model.generate_content([
    "What is the total budget mentioned?",
    pdf_file
])

# Multi-turn chat over document
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message([
    "I uploaded a contract",
    pdf_file
])

response = chat.send_message("What are the payment terms?")
response = chat.send_message("What happens if payment is late?")
```

---

## Combined Modalities

### Text + Image + Audio

```python
image = PIL.Image.open("chart.png")
audio_file = genai.upload_file("explanation.mp3")

response = model.generate_content([
    "This chart shows our Q4 results. Listen to the audio explanation and create a summary report.",
    image,
    audio_file
])
```

### Video + PDF Context

```python
video_file = genai.upload_file("presentation.mp4")
pdf_file = genai.upload_file("slides.pdf")

response = model.generate_content([
    "Compare the video presentation with the PDF slides. Are there any discrepancies?",
    video_file,
    pdf_file
])
```

---

## Code Execution

### Python Sandbox

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]  # Enable code execution
)

response = model.generate_content(
    "Calculate the first 20 Fibonacci numbers and show the result"
)

# Access executed code and output
for part in response.candidates[0].content.parts:
    if hasattr(part, 'executable_code'):
        print("Code:")
        print(part.executable_code.code)
    if hasattr(part, 'code_execution_result'):
        print("Output:")
        print(part.code_execution_result.output)
```

### Data Analysis

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=["code_execution"]
)

csv_file = genai.upload_file("sales_data.csv")

response = model.generate_content([
    "Analyze this sales data. Calculate averages, find trends, and create a summary.",
    csv_file
])
```

### Chart Generation

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]
)

response = model.generate_content("""
Create a bar chart showing programming language popularity:
- Python: 35%
- JavaScript: 28%
- Java: 15%
- C++: 12%
- Other: 10%
""")

# The model will generate matplotlib code and return the chart
```

---

## Context Caching

### Creating a Cache

```python
from google.generativeai import caching

# Upload large document
document = genai.upload_file("large_document.pdf")

# Create cache (minimum 32K tokens)
cache = caching.CachedContent.create(
    model="gemini-1.5-pro",
    display_name="Large document cache",
    system_instruction="You are an expert document analyzer.",
    contents=[document],
    ttl="3600s"  # Time to live: 1 hour
)

print(f"Cache created: {cache.name}")
print(f"Token count: {cache.usage_metadata.total_token_count}")
```

### Using Cached Content

```python
# Create model from cache
model = genai.GenerativeModel.from_cached_content(cache)

# Queries use cached context (faster, cheaper)
response = model.generate_content("Summarize the main points")
print(response.text)

response = model.generate_content("What are the key dates mentioned?")
print(response.text)
```

### Managing Caches

```python
# List caches
for c in caching.CachedContent.list():
    print(f"{c.name}: {c.display_name}")

# Get specific cache
cache = caching.CachedContent.get("cachedContents/xxxxx")

# Update TTL
cache.update(ttl="7200s")  # Extend to 2 hours

# Delete cache
cache.delete()
```

### Cost Savings

```
Regular input: $0.075 / 1M tokens (1.5 Pro)
Cached input:  $0.01875 / 1M tokens (75% cheaper)

Best for:
- Large documents queried multiple times
- System instructions with many examples
- RAG with frequently accessed knowledge bases
```

---

## Vertex AI Integration

### Setup

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI
vertexai.init(project="your-gcp-project", location="us-central1")

# Available locations: us-central1, europe-west4, asia-northeast1
```

### Generate Content

```python
model = GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Explain quantum computing")
print(response.text)
```

### Multimodal with GCS

```python
from vertexai.generative_models import Part

# Using Google Cloud Storage
video_part = Part.from_uri(
    uri="gs://your-bucket/video.mp4",
    mime_type="video/mp4"
)

model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Summarize this video",
    video_part
])
```

### Tuned Models

```python
from vertexai.generative_models import GenerativeModel

# Use a tuned model
model = GenerativeModel("projects/your-project/locations/us-central1/endpoints/your-tuned-model")

response = model.generate_content("Your prompt")
```

### Enterprise Features

| Feature | Description |
|---------|-------------|
| **VPC Service Controls** | Network isolation |
| **CMEK** | Customer-managed encryption keys |
| **Audit Logs** | Cloud Audit Logs integration |
| **IAM** | Fine-grained access control |
| **Model Tuning** | Supervised fine-tuning |
| **Evaluation** | Built-in evaluation metrics |

---

## API Comparison

| Feature | Gemini | OpenAI GPT-4 | Claude |
|---------|--------|--------------|--------|
| Max Context | 2M tokens | 128K tokens | 200K tokens |
| Native Video | Yes | No | No |
| Native Audio | Yes | Via Whisper | No |
| Code Execution | Yes | Via tools | No |
| Search Grounding | Yes | Via tools | Via tools |
| Context Caching | Yes | No | Yes |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Image input processing | sonnet | Multimodal handling |
| Video analysis | sonnet | Complex input |

## Sources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Gemini Cookbook](https://github.com/google-gemini/gemini-api-cookbook)

---

*Part of faion-ml-engineer skill*
*Last updated: 2026-01-23*
