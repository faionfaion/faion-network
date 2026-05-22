"""
purpose: Auditable manual-mode Gemini function calling with name + arg validation.
consumes: Python function with docstring + type hints; user query string
produces: tool result + final model response
depends-on: content/01-core-rules.xml r3, r4
token-budget-impact: per-call; bounded by loop iterations

Usage:
    result = call_with_tool("What's the weather in Tokyo?", get_current_weather)
"""
import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")


def call_with_tool(user_query: str, fn) -> str:
    """Manual function calling with explicit validation before execution.

    Args:
        user_query: The user's question.
        fn: A Python function with type hints and docstring (used as tool schema).

    Returns:
        Final model response after function execution.
    """
    model = genai.GenerativeModel("gemini-2.0-flash", tools=[fn])
    chat = model.start_chat()  # enable_automatic_function_calling=False (default)
    resp = chat.send_message(user_query)

    for part in resp.candidates[0].content.parts:
        if hasattr(part, "function_call"):
            fc = part.function_call
            # Validate before executing
            assert fc.name == fn.__name__, f"Unexpected tool: {fc.name}"
            result = fn(**dict(fc.args))
            # Return result to model
            follow = chat.send_message(genai.protos.Content(parts=[
                genai.protos.Part(function_response=genai.protos.FunctionResponse(
                    name=fc.name, response={"result": result}
                ))
            ]))
            return follow.text
    return resp.text
