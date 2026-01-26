# Ollama Templates

## Modelfile Templates

### General Purpose Assistant

```dockerfile
# Modelfile.assistant
FROM llama3.1:8b

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096
PARAMETER repeat_penalty 1.1

SYSTEM """You are a helpful, harmless, and honest AI assistant.

Guidelines:
- Be concise and direct in responses
- Admit uncertainty when unsure
- Provide accurate information
- Be helpful and friendly
"""
```

### Coding Assistant

```dockerfile
# Modelfile.coder
FROM qwen2.5-coder:7b

PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER num_ctx 16384
PARAMETER repeat_penalty 1.0

SYSTEM """You are an expert programmer.

Guidelines:
- Write clean, well-documented code
- Include error handling
- Follow language best practices
- Explain complex logic with comments
- Suggest improvements when relevant
"""
```

### JSON Output Model

```dockerfile
# Modelfile.json
FROM llama3.1:8b

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

SYSTEM """You are a data extraction assistant that ONLY outputs valid JSON.

Rules:
- Always respond with valid JSON
- Never include explanations outside JSON
- Use the exact schema requested
- Handle missing data with null values
"""
```

### Creative Writer

```dockerfile
# Modelfile.creative
FROM llama3.1:8b

PARAMETER temperature 0.9
PARAMETER top_p 0.95
PARAMETER top_k 100
PARAMETER num_ctx 8192
PARAMETER repeat_penalty 1.2

SYSTEM """You are a creative writer with vivid imagination.

Style:
- Use rich, descriptive language
- Create engaging narratives
- Develop unique characters
- Build immersive worlds
"""
```

### Technical Documentation

```dockerfile
# Modelfile.docs
FROM llama3.1:8b

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM """You are a technical documentation writer.

Guidelines:
- Use clear, concise language
- Structure content with headers
- Include code examples
- Explain concepts progressively
- Use consistent terminology
"""
```

### Data Analyst

```dockerfile
# Modelfile.analyst
FROM llama3.1:8b

PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM """You are a data analysis expert.

Approach:
- Analyze data systematically
- Identify patterns and trends
- Provide statistical insights
- Visualize findings clearly
- Make data-driven recommendations
"""
```

### Tool Calling Model

```dockerfile
# Modelfile.tools
FROM llama3.1:8b

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 32768
PARAMETER repeat_penalty 1.0

SYSTEM """You are an AI assistant with access to external tools.

Tool Usage Guidelines:
- Only call tools when necessary
- Provide all required parameters
- Use tools to get real-time information
- Combine tool results into helpful responses
"""
```

### RAG Assistant

```dockerfile
# Modelfile.rag
FROM llama3.1:8b

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 16384

SYSTEM """You are a knowledge assistant that answers questions based on provided context.

Guidelines:
- Base answers ONLY on the provided context
- Quote relevant sections when helpful
- Say "I don't have information about that" if context doesn't contain the answer
- Never make up information
- Cite sources when available
"""
```

## Build Commands

```bash
# Build custom models
ollama create assistant -f Modelfile.assistant
ollama create coder -f Modelfile.coder
ollama create json-output -f Modelfile.json
ollama create creative -f Modelfile.creative
ollama create docs-writer -f Modelfile.docs
ollama create analyst -f Modelfile.analyst
ollama create tool-caller -f Modelfile.tools
ollama create rag-assistant -f Modelfile.rag

# Verify models
ollama list
```

## Docker Compose Templates

### Basic Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  ollama_data:
```

### With GPU Support (NVIDIA)

```yaml
# docker-compose.gpu.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-gpu
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  ollama_data:
```

### With Open WebUI

```yaml
# docker-compose.webui.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - webui_data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
  webui_data:
```

### Multi-Model Production Setup

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - ollama_data:/root/.ollama
      - ./modelfiles:/modelfiles:ro
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
        limits:
          memory: 32G
    environment:
      - OLLAMA_NUM_PARALLEL=2
      - OLLAMA_MAX_LOADED_MODELS=2
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"

  # Nginx reverse proxy with rate limiting
  nginx:
    image: nginx:alpine
    container_name: ollama-proxy
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

### Nginx Configuration for Production

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    limit_req_zone $binary_remote_addr zone=ollama:10m rate=10r/s;

    upstream ollama {
        server ollama:11434;
    }

    server {
        listen 80;

        location / {
            limit_req zone=ollama burst=20 nodelay;

            proxy_pass http://ollama;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # For streaming
            proxy_buffering off;
            proxy_cache off;

            # Timeouts for large models
            proxy_connect_timeout 60s;
            proxy_send_timeout 120s;
            proxy_read_timeout 120s;
        }

        # Health check endpoint
        location /health {
            proxy_pass http://ollama/api/tags;
            proxy_connect_timeout 5s;
            proxy_read_timeout 5s;
        }
    }
}
```

## Configuration Templates

### Python Config Class

```python
# config.py
from dataclasses import dataclass, field
from typing import Optional
import os

@dataclass
class OllamaConfig:
    """Ollama configuration with environment variable support."""

    # Server
    base_url: str = field(
        default_factory=lambda: os.getenv("OLLAMA_URL", "http://localhost:11434")
    )
    timeout: int = field(
        default_factory=lambda: int(os.getenv("OLLAMA_TIMEOUT", "120"))
    )
    max_retries: int = 3

    # Default model
    model: str = field(
        default_factory=lambda: os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    )

    # Generation parameters
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    num_ctx: int = 4096
    repeat_penalty: float = 1.1

    # Tool calling
    tool_model: str = field(
        default_factory=lambda: os.getenv("OLLAMA_TOOL_MODEL", "llama3.1:8b")
    )
    tool_ctx: int = 32768

    # Embedding
    embed_model: str = field(
        default_factory=lambda: os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    )

    # Vision
    vision_model: str = field(
        default_factory=lambda: os.getenv("OLLAMA_VISION_MODEL", "llava:7b")
    )

    @classmethod
    def for_coding(cls) -> "OllamaConfig":
        """Configuration optimized for code generation."""
        return cls(
            model="qwen2.5-coder:7b",
            temperature=0.2,
            num_ctx=16384,
            repeat_penalty=1.0
        )

    @classmethod
    def for_creative(cls) -> "OllamaConfig":
        """Configuration for creative writing."""
        return cls(
            temperature=0.9,
            top_p=0.95,
            top_k=100,
            num_ctx=8192,
            repeat_penalty=1.2
        )

    @classmethod
    def for_analysis(cls) -> "OllamaConfig":
        """Configuration for data analysis."""
        return cls(
            temperature=0.2,
            top_p=0.9,
            num_ctx=8192
        )
```

### Environment Variables

```bash
# .env.ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TOOL_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_VISION_MODEL=llava:7b
OLLAMA_TIMEOUT=120

# GPU settings
CUDA_VISIBLE_DEVICES=0
OLLAMA_NUM_PARALLEL=2
OLLAMA_MAX_LOADED_MODELS=2
```

## Systemd Service Template

```ini
# /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ollama
Group=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=5
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=2"

# Resource limits
LimitNOFILE=65535
LimitNPROC=65535

[Install]
WantedBy=multi-user.target
```

## Model Pull Script

```bash
#!/bin/bash
# pull-models.sh - Pull required models

set -e

MODELS=(
    "llama3.1:8b"
    "qwen2.5-coder:7b"
    "nomic-embed-text"
    "llava:7b"
)

echo "Pulling Ollama models..."

for model in "${MODELS[@]}"; do
    echo "Pulling $model..."
    ollama pull "$model"
done

echo "Building custom models..."

# Build custom models from Modelfiles
if [ -d "./modelfiles" ]; then
    for modelfile in ./modelfiles/Modelfile.*; do
        if [ -f "$modelfile" ]; then
            name=$(basename "$modelfile" | sed 's/Modelfile.//')
            echo "Building $name from $modelfile..."
            ollama create "$name" -f "$modelfile"
        fi
    done
fi

echo "Available models:"
ollama list
```
