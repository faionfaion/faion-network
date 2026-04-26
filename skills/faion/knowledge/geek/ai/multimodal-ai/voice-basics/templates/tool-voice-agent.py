"""ToolEnabledVoiceAgent with function calling."""
from openai import OpenAI
from typing import Callable
import json


class ToolEnabledVoiceAgent:
    """Voice agent with tool/function calling capabilities."""

    def __init__(self, system_prompt: str, tools: list[dict],
                 tool_functions: dict[str, Callable], voice: str = "nova"):
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_functions = tool_functions
        self.voice = voice
        self.client = OpenAI()
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def process(self, user_input: str) -> str:
        """Process input with potential tool calls. Keep response short for TTS."""
        self.conversation_history.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto",
            max_tokens=150  # short for voice output
        )
        message = response.choices[0].message

        if message.tool_calls:
            self.conversation_history.append(message)
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                if func_name in self.tool_functions:
                    result = self.tool_functions[func_name](**arguments)
                else:
                    result = {"error": f"Unknown function: {func_name}"}
                self.conversation_history.append({
                    "role": "tool", "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            # Second LLM call only after tool execution
            response = self.client.chat.completions.create(
                model="gpt-4o", messages=self.conversation_history,
                max_tokens=150
            )
            message = response.choices[0].message

        msg = message.content
        self.conversation_history.append({"role": "assistant", "content": msg})
        return msg
