from opentelemetry import trace
from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as gai
from anthropic import Anthropic

tracer = trace.get_tracer("agent")
client = Anthropic()

def call_claude(messages, tools, model="claude-sonnet-..."):
    with tracer.start_as_current_span("agent.llm_call") as span:
        span.set_attribute(gai.GEN_AI_SYSTEM, "anthropic")
        span.set_attribute(gai.GEN_AI_REQUEST_MODEL, model)

        resp = client.messages.create(
            model=model, messages=messages, tools=tools, max_tokens=2048
        )

        span.set_attribute(gai.GEN_AI_USAGE_INPUT_TOKENS, resp.usage.input_tokens)
        span.set_attribute(gai.GEN_AI_USAGE_OUTPUT_TOKENS, resp.usage.output_tokens)
        span.set_attribute("gen_ai.usage.cache_read_tokens", resp.usage.cache_read_input_tokens or 0)
        span.set_attribute(gai.GEN_AI_RESPONSE_FINISH_REASONS, [resp.stop_reason])
        return resp
