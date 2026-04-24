# Gemini API Templates

Copy-paste templates for common Gemini API use cases.

---

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Chat Application](#chat-application)
3. [Multimodal Analysis](#multimodal-analysis)
4. [Function Calling](#function-calling)
5. [RAG Application](#rag-application)
6. [Streaming Chatbot](#streaming-chatbot)
7. [Document Processor](#document-processor)
8. [Agent with Tools](#agent-with-tools)

---

## Basic Setup

### Minimal Setup Template

```python
"""Gemini API - Minimal Setup"""

import os
import google.generativeai as genai

# Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-2.0-flash"  # or gemini-3-pro, gemini-1.5-pro

# Initialize
genai.configure(api_key=API_KEY)

# Create model
model = genai.GenerativeModel(
    model_name=MODEL,
    generation_config={
        "temperature": 1.0,
        "max_output_tokens": 8192,
    }
)

# Generate
response = model.generate_content("Your prompt here")
print(response.text)
```

### Production Setup Template

```python
"""Gemini API - Production Setup"""

import os
import logging
from typing import Optional
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InvalidArgument

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class GeminiConfig:
    API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    MAX_RETRIES = 3
    TEMPERATURE = 1.0
    MAX_OUTPUT_TOKENS = 8192

# Initialize
genai.configure(api_key=GeminiConfig.API_KEY)

def create_model(
    model_name: str = GeminiConfig.MODEL,
    system_instruction: Optional[str] = None,
    temperature: float = GeminiConfig.TEMPERATURE,
) -> genai.GenerativeModel:
    """Create configured Gemini model."""
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": GeminiConfig.MAX_OUTPUT_TOKENS,
        }
    )

def generate_with_retry(
    model: genai.GenerativeModel,
    prompt: str,
    max_retries: int = GeminiConfig.MAX_RETRIES,
) -> Optional[str]:
    """Generate content with retry logic."""
    import time

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text

        except ResourceExhausted:
            wait_time = 2 ** attempt
            logger.warning(f"Rate limited, retry {attempt + 1}/{max_retries} in {wait_time}s")
            time.sleep(wait_time)

        except InvalidArgument as e:
            logger.error(f"Invalid request: {e}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    logger.error("Max retries exceeded")
    return None

# Usage
if __name__ == "__main__":
    model = create_model(
        system_instruction="You are a helpful assistant."
    )
    result = generate_with_retry(model, "Hello, how are you?")
    print(result)
```

---

## Chat Application

### Simple Chat Template

```python
"""Gemini Chat Application"""

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class GeminiChat:
    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        system_instruction: str = None,
    ):
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
        )
        self.chat = self.model.start_chat()

    def send(self, message: str) -> str:
        """Send message and get response."""
        response = self.chat.send_message(message)
        return response.text

    def send_stream(self, message: str):
        """Send message with streaming response."""
        response = self.chat.send_message(message, stream=True)
        for chunk in response:
            yield chunk.text

    def get_history(self) -> list:
        """Get conversation history."""
        return [
            {"role": m.role, "content": m.parts[0].text}
            for m in self.chat.history
        ]

    def reset(self):
        """Reset conversation."""
        self.chat = self.model.start_chat()

# Usage
if __name__ == "__main__":
    chat = GeminiChat(
        system_instruction="You are a helpful Python tutor."
    )

    print("Chat started. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        # Streaming response
        print("Assistant: ", end="", flush=True)
        for chunk in chat.send_stream(user_input):
            print(chunk, end="", flush=True)
        print("\n")
```

---

## Multimodal Analysis

### Image Analysis Template

```python
"""Gemini Image Analysis"""

import google.generativeai as genai
import PIL.Image
import os
from pathlib import Path

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ImageAnalyzer:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, image_path: str, prompt: str) -> str:
        """Analyze single image."""
        image = PIL.Image.open(image_path)
        response = self.model.generate_content([prompt, image])
        return response.text

    def compare(self, image_paths: list, prompt: str) -> str:
        """Compare multiple images."""
        images = [PIL.Image.open(p) for p in image_paths]
        response = self.model.generate_content([prompt] + images)
        return response.text

    def describe(self, image_path: str) -> str:
        """Get detailed description."""
        return self.analyze(
            image_path,
            "Describe this image in detail. Include objects, colors, composition."
        )

    def extract_text(self, image_path: str) -> str:
        """Extract text from image (OCR)."""
        return self.analyze(
            image_path,
            "Extract all text visible in this image. Format as plain text."
        )

# Usage
if __name__ == "__main__":
    analyzer = ImageAnalyzer()

    # Describe image
    description = analyzer.describe("image.jpg")
    print("Description:", description)

    # Extract text
    text = analyzer.extract_text("screenshot.png")
    print("Extracted text:", text)

    # Compare images
    comparison = analyzer.compare(
        ["before.jpg", "after.jpg"],
        "What are the differences between these images?"
    )
    print("Comparison:", comparison)
```

### Video Analysis Template

```python
"""Gemini Video Analysis"""

import google.generativeai as genai
import time
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class VideoAnalyzer:
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model = genai.GenerativeModel(model_name)

    def upload(self, video_path: str) -> genai.File:
        """Upload video and wait for processing."""
        video_file = genai.upload_file(video_path)

        while video_file.state.name == "PROCESSING":
            print("Processing video...")
            time.sleep(5)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("Video processing failed")

        return video_file

    def analyze(self, video_file: genai.File, prompt: str) -> str:
        """Analyze uploaded video."""
        response = self.model.generate_content([prompt, video_file])
        return response.text

    def summarize(self, video_path: str) -> str:
        """Upload and summarize video."""
        video_file = self.upload(video_path)
        return self.analyze(
            video_file,
            "Summarize this video. Include key points, scenes, and main message."
        )

    def timestamp_query(self, video_file: genai.File, timestamp: str) -> str:
        """Query about specific timestamp."""
        return self.analyze(
            video_file,
            f"What happens at the {timestamp} mark in this video?"
        )

    def transcribe(self, video_file: genai.File) -> str:
        """Transcribe video audio."""
        return self.analyze(
            video_file,
            "Transcribe all spoken words in this video."
        )

# Usage
if __name__ == "__main__":
    analyzer = VideoAnalyzer()

    # Summarize video
    summary = analyzer.summarize("presentation.mp4")
    print("Summary:", summary)
```

---

## Function Calling

### Function Calling Template

```python
"""Gemini Function Calling"""

import google.generativeai as genai
import json
import os
from typing import Callable, Dict, Any

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define your functions
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location.

    Args:
        location: City and country (e.g., "London, UK")
        unit: Temperature unit ("celsius" or "fahrenheit")
    """
    # Replace with actual API call
    return {"location": location, "temperature": 22, "unit": unit, "condition": "sunny"}

def search_products(query: str, max_results: int = 5) -> list:
    """Search product catalog.

    Args:
        query: Search query
        max_results: Maximum results to return
    """
    # Replace with actual search
    return [{"name": f"Product {i}", "price": i * 10} for i in range(1, max_results + 1)]

def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
    """
    # Replace with actual email sending
    return {"status": "sent", "to": to}

# Function registry
FUNCTIONS: Dict[str, Callable] = {
    "get_weather": get_weather,
    "search_products": search_products,
    "send_email": send_email,
}

class FunctionCallingBot:
    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        functions: list = None,
        auto_execute: bool = True,
    ):
        self.auto_execute = auto_execute
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=functions or list(FUNCTIONS.values()),
        )
        self.chat = self.model.start_chat(
            enable_automatic_function_calling=auto_execute
        )

    def send(self, message: str) -> str:
        """Send message with automatic function calling."""
        response = self.chat.send_message(message)
        return response.text

    def reset(self):
        """Reset conversation."""
        self.chat = self.model.start_chat(
            enable_automatic_function_calling=self.auto_execute
        )

# Usage
if __name__ == "__main__":
    bot = FunctionCallingBot()

    # Weather query
    result = bot.send("What's the weather in Tokyo?")
    print("Response:", result)

    # Product search
    result = bot.send("Find me 3 laptop products")
    print("Response:", result)
```

---

## RAG Application

### RAG Template

```python
"""Gemini RAG Application"""

import google.generativeai as genai
import numpy as np
from typing import List, Dict, Optional
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class SimpleVectorStore:
    """Simple in-memory vector store."""

    def __init__(self):
        self.documents: List[str] = []
        self.embeddings: List[List[float]] = []

    def add(self, documents: List[str], embeddings: List[List[float]]):
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

    def search(self, query_embedding: List[float], k: int = 5) -> List[str]:
        if not self.embeddings:
            return []

        # Cosine similarity
        query = np.array(query_embedding)
        scores = []
        for emb in self.embeddings:
            emb_arr = np.array(emb)
            score = np.dot(query, emb_arr) / (np.linalg.norm(query) * np.linalg.norm(emb_arr))
            scores.append(score)

        # Get top k
        indices = np.argsort(scores)[-k:][::-1]
        return [self.documents[i] for i in indices]

class GeminiRAG:
    def __init__(
        self,
        model_name: str = "gemini-1.5-pro",
        embedding_model: str = "models/text-embedding-004",
    ):
        self.model = genai.GenerativeModel(model_name)
        self.embedding_model = embedding_model
        self.vector_store = SimpleVectorStore()

    def embed(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """Generate embeddings for texts."""
        result = genai.embed_content(
            model=self.embedding_model,
            content=texts,
            task_type=task_type,
        )
        return result["embedding"]

    def index(self, documents: List[str]):
        """Index documents into vector store."""
        embeddings = self.embed(documents, "RETRIEVAL_DOCUMENT")
        self.vector_store.add(documents, embeddings)

    def query(self, question: str, k: int = 5) -> str:
        """Query with RAG."""
        # Embed question
        query_emb = self.embed([question], "RETRIEVAL_QUERY")[0]

        # Retrieve relevant docs
        relevant_docs = self.vector_store.search(query_emb, k)

        if not relevant_docs:
            return self.model.generate_content(question).text

        # Generate with context
        context = "\n\n---\n\n".join(relevant_docs)
        prompt = f"""Answer based on the following context:

Context:
{context}

Question: {question}

Answer:"""

        response = self.model.generate_content(prompt)
        return response.text

# Usage
if __name__ == "__main__":
    rag = GeminiRAG()

    # Index documents
    documents = [
        "Python is a high-level programming language known for its readability.",
        "Machine learning is a subset of artificial intelligence.",
        "Django is a Python web framework for rapid development.",
        "TensorFlow is an open-source machine learning library.",
        "FastAPI is a modern Python web framework for building APIs.",
    ]
    rag.index(documents)

    # Query
    answer = rag.query("What is Python used for?")
    print("Answer:", answer)
```

---

## Streaming Chatbot

### FastAPI Streaming Template

```python
"""Gemini Streaming Chatbot with FastAPI"""

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Session storage (use Redis in production)
sessions = {}

def get_or_create_chat(session_id: str):
    if session_id not in sessions:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction="You are a helpful assistant.",
        )
        sessions[session_id] = model.start_chat()
    return sessions[session_id]

async def stream_response(chat, message: str):
    """Generate streaming response."""
    response = chat.send_message(message, stream=True)
    for chunk in response:
        yield f"data: {json.dumps({'text': chunk.text})}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/chat/{session_id}")
async def chat_endpoint(session_id: str, request: Request):
    body = await request.json()
    message = body.get("message", "")

    chat = get_or_create_chat(session_id)

    return StreamingResponse(
        stream_response(chat, message),
        media_type="text/event-stream",
    )

@app.delete("/chat/{session_id}")
async def reset_chat(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "reset"}

# Run with: uvicorn main:app --reload
```

---

## Document Processor

### Document Processing Template

```python
"""Gemini Document Processor"""

import google.generativeai as genai
from pathlib import Path
import os
from typing import Optional, Dict, Any

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class DocumentProcessor:
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model = genai.GenerativeModel(model_name)
        self._file_cache: Dict[str, genai.File] = {}

    def upload(self, file_path: str) -> genai.File:
        """Upload document file."""
        if file_path in self._file_cache:
            return self._file_cache[file_path]

        file = genai.upload_file(file_path)
        self._file_cache[file_path] = file
        return file

    def process(self, file_path: str, prompt: str) -> str:
        """Process document with custom prompt."""
        file = self.upload(file_path)
        response = self.model.generate_content([prompt, file])
        return response.text

    def summarize(self, file_path: str, max_length: str = "medium") -> str:
        """Summarize document."""
        lengths = {
            "short": "in 2-3 sentences",
            "medium": "in 1-2 paragraphs",
            "long": "in detail with all key points",
        }
        return self.process(
            file_path,
            f"Summarize this document {lengths.get(max_length, lengths['medium'])}."
        )

    def extract_entities(self, file_path: str) -> str:
        """Extract named entities."""
        return self.process(
            file_path,
            "Extract all named entities: people, organizations, locations, dates, amounts."
        )

    def answer_question(self, file_path: str, question: str) -> str:
        """Answer question about document."""
        return self.process(
            file_path,
            f"Based on this document, answer: {question}"
        )

    def extract_structured(self, file_path: str, schema: dict) -> str:
        """Extract structured data based on schema."""
        model = genai.GenerativeModel(
            model_name=self.model._model_name,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            }
        )
        file = self.upload(file_path)
        response = model.generate_content([
            "Extract the following information from this document:",
            file,
        ])
        return response.text

# Usage
if __name__ == "__main__":
    processor = DocumentProcessor()

    # Summarize
    summary = processor.summarize("report.pdf", max_length="short")
    print("Summary:", summary)

    # Q&A
    answer = processor.answer_question("report.pdf", "What is the total budget?")
    print("Answer:", answer)

    # Extract structured data
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
            "date": {"type": "string"},
            "key_findings": {"type": "array", "items": {"type": "string"}},
        }
    }
    structured = processor.extract_structured("report.pdf", schema)
    print("Structured:", structured)
```

---

## Agent with Tools

### Agent Template

```python
"""Gemini Agent with Multiple Tools"""

import google.generativeai as genai
import os
from typing import List, Dict, Any, Callable
from dataclasses import dataclass

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@dataclass
class ToolResult:
    name: str
    result: Any

# Tool definitions
def calculator(expression: str) -> dict:
    """Evaluate mathematical expression.

    Args:
        expression: Math expression to evaluate
    """
    try:
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def web_search(query: str) -> dict:
    """Search the web for information.

    Args:
        query: Search query
    """
    # Replace with actual search API
    return {"results": [f"Result for: {query}"]}

def get_current_time(timezone: str = "UTC") -> dict:
    """Get current time in timezone.

    Args:
        timezone: Timezone name
    """
    from datetime import datetime
    import pytz

    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return {"time": now.isoformat(), "timezone": timezone}
    except Exception as e:
        return {"error": str(e)}

def file_read(filepath: str) -> dict:
    """Read content from file.

    Args:
        filepath: Path to file
    """
    try:
        with open(filepath, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e)}

# Tool registry
TOOLS: Dict[str, Callable] = {
    "calculator": calculator,
    "web_search": web_search,
    "get_current_time": get_current_time,
    "file_read": file_read,
}

class GeminiAgent:
    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        tools: List[Callable] = None,
        system_instruction: str = None,
        max_iterations: int = 10,
    ):
        self.max_iterations = max_iterations
        self.tools = tools or list(TOOLS.values())
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=self.tools,
            system_instruction=system_instruction or (
                "You are a helpful AI assistant with access to various tools. "
                "Use tools when needed to answer questions accurately."
            ),
        )

    def run(self, query: str) -> str:
        """Run agent with query."""
        chat = self.model.start_chat()
        response = chat.send_message(query)

        for _ in range(self.max_iterations):
            # Check for function calls
            function_calls = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call"):
                    function_calls.append(part.function_call)

            if not function_calls:
                # No more function calls, return final response
                return response.text

            # Execute functions and send results
            function_responses = []
            for fn_call in function_calls:
                fn_name = fn_call.name
                fn_args = dict(fn_call.args)

                if fn_name in TOOLS:
                    result = TOOLS[fn_name](**fn_args)
                else:
                    result = {"error": f"Unknown function: {fn_name}"}

                function_responses.append(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=fn_name,
                            response={"result": result}
                        )
                    )
                )

            # Send function results back
            response = chat.send_message(
                genai.protos.Content(parts=function_responses)
            )

        return "Maximum iterations reached"

# Usage
if __name__ == "__main__":
    agent = GeminiAgent()

    # Math question
    result = agent.run("What is 15 * 23 + 47?")
    print("Result:", result)

    # Time query
    result = agent.run("What time is it in Tokyo?")
    print("Result:", result)

    # Complex query
    result = agent.run(
        "Calculate the square root of 144 and search for its significance"
    )
    print("Result:", result)
```

---

*Last updated: 2026-01-25*
