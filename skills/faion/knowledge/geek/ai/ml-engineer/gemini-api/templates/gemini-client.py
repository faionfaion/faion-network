"""
purpose: Production client: retry, streaming, function calling, structured output.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for gemini-api
token-budget-impact: ≤500 tokens to fill
"""

"""
Production Gemini client: model setup, retry logic, streaming, function calling.
Requires: pip install google-generativeai
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Callable

import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, ResourceExhausted

logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def create_model(
    model_name: str = "gemini-2.0-flash",
    system_instruction: str | None = None,
    temperature: float = 1.0,
    tools: list[Callable] | None = None,
) -> genai.GenerativeModel:
    """Create a configured Gemini model instance."""
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        tools=tools,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 8192,
        },
    )


def generate_with_retry(
    model: genai.GenerativeModel,
    prompt: str,
    max_retries: int = 3,
) -> str | None:
    """Generate content with exponential backoff on rate limit errors."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            # Safety check — blocked responses have no .text
            if response.prompt_feedback.block_reason:
                logger.warning("Response blocked: %s", response.prompt_feedback.block_reason)
                return None
            return response.text

        except ResourceExhausted:
            wait = 2 ** attempt
            logger.warning("Rate limited, retry %d/%d in %ds", attempt + 1, max_retries, wait)
            time.sleep(wait)

        except InvalidArgument as exc:
            logger.error("Invalid request: %s", exc)
            return None

        except Exception as exc:
            logger.exception("Unexpected error on attempt %d", attempt + 1)
            if attempt == max_retries - 1:
                return None

    return None


class GeminiChat:
    """Multi-turn chat session with streaming support."""

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        system_instruction: str | None = None,
    ) -> None:
        self.model = create_model(model_name, system_instruction)
        self._chat = self.model.start_chat()

    def send(self, message: str) -> str | None:
        """Send message and return full response text."""
        response = self._chat.send_message(message)
        if response.prompt_feedback.block_reason:
            return None
        return response.text

    def stream(self, message: str):
        """Send message and yield response chunks as they arrive."""
        response = self._chat.send_message(message, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def history(self) -> list[dict]:
        """Return conversation history as list of {role, content} dicts."""
        return [
            {"role": msg.role, "content": msg.parts[0].text}
            for msg in self._chat.history
            if msg.parts
        ]

    def reset(self) -> None:
        """Start a fresh conversation."""
        self._chat = self.model.start_chat()


class GeminiFunctionAgent:
    """Agent with automatic function calling (Gemini auto-executes registered tools)."""

    def __init__(
        self,
        tools: list[Callable],
        model_name: str = "gemini-2.0-flash",
        system_instruction: str | None = None,
        max_iterations: int = 10,
    ) -> None:
        self.max_iterations = max_iterations
        self.model = create_model(model_name, system_instruction, tools=tools)

    def run(self, query: str) -> str | None:
        """Run agent query with automatic function dispatch."""
        chat = self.model.start_chat(enable_automatic_function_calling=True)

        for _ in range(self.max_iterations):
            response = chat.send_message(query)
            # If no more function calls pending, return final text
            has_function_call = any(
                hasattr(part, "function_call")
                for part in response.candidates[0].content.parts
            )
            if not has_function_call:
                return response.text

        logger.warning("Max iterations (%d) reached", self.max_iterations)
        return None


# ── Example tools for GeminiFunctionAgent ─────────────────────────────────────

def get_weather(location: str, unit: str = "celsius") -> dict[str, Any]:
    """Get current weather for a location.

    Args:
        location: City and country, e.g. 'Tokyo, Japan'
        unit: Temperature unit, 'celsius' or 'fahrenheit'
    """
    return {"location": location, "temperature": 22, "unit": unit, "condition": "sunny"}


def calculator(expression: str) -> dict[str, Any]:
    """Evaluate a mathematical expression safely.

    Args:
        expression: Math expression to evaluate, e.g. '2 + 2 * 3'
    """
    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307
        return {"result": result}
    except Exception as exc:
        return {"error": str(exc)}


# Usage:
# agent = GeminiFunctionAgent(tools=[get_weather, calculator])
# result = agent.run("What is 15*23 and what is the weather in Tokyo?")
