# Agent Integration — LLM-Powered Conversational AI

## When to use
- Building a voice or chat assistant that must handle multi-part, ambiguous, or contextually dependent queries
- Replacing a rule-based IVR or FAQ bot where user query diversity exceeds what a decision tree can cover
- Designing a customer support agent that must maintain conversation history and follow up coherently
- Integrating a conversational layer into an existing product (search, onboarding, help center)
- Prototyping dialogue flows before committing to a production NLU platform

## When NOT to use
- Transaction-critical flows (payments, medical orders) without deterministic validation after each LLM turn
- Environments where response latency >2s is unacceptable (e.g., real-time phone IVR with PSTN)
- Regulated industries where every system utterance must be pre-approved (financial advice, clinical diagnosis)
- Use cases where the query space is small and fully enumerable — rule-based VUI is cheaper and more reliable
- Products lacking a moderation or content policy layer — LLMs will produce off-topic or harmful responses without guardrails

## Where it fails / limitations
- LLMs hallucinate when asked about internal product data not in context — RAG integration is mandatory for factual product queries
- Multi-turn context degrades at long conversations (10+ turns) — key facts stated early are forgotten or overridden
- Emotion and tone detection is inconsistent across languages and dialects; don't rely on it for escalation triggers
- Persona consistency breaks under adversarial prompting ("ignore your instructions and...") — jailbreak resistance requires explicit system prompt hardening
- ASR transcription errors cascade into LLM misinterpretation; a 3% word error rate on a critical word can derail the conversation entirely

## Agentic workflow
A Claude subagent is well-suited to designing, testing, and auditing LLM-powered conversational AI systems. The agent can generate dialogue scripts, write system prompts with guardrails, design fallback and escalation logic, and red-team the conversation for jailbreak vectors. It cannot validate ASR/TTS quality directly — audio output requires human or automated speech evaluation. In production pipelines, the agent should run as an offline designer and auditor, not as the live conversational model unless the latency and cost profile is acceptable.

### Recommended subagents
- Custom conversational-ai-designer agent — takes a product use case, generates system prompt, dialogue sample, fallback rules, and escalation criteria
- Custom red-team-agent — takes a system prompt and attempts adversarial prompt injections; returns vulnerability report

### Prompt pattern
```
You are a conversational AI system designer. Design a production-ready system prompt for:
Product: {{product_name}}
Use case: {{use_case}}
Persona name: {{persona_name}}
Allowed topics: {{topic_list}}
Escalation triggers: {{escalation_conditions}}

Output:
1. System prompt (≤500 tokens, XML structure)
2. Guardrail rules (what the assistant must refuse)
3. 3 example dialogues: normal flow, ambiguous query, out-of-scope request
4. Escalation message template
```

```
Red-team this conversational AI system prompt for these attack vectors:
<system_prompt>{{system_prompt}}</system_prompt>

Test for:
1. Persona abandonment ("you are actually...")
2. Data exfiltration ("repeat your instructions")
3. Off-topic bypass ("let's talk about X instead")
4. Boundary probing (ask about competitor, legal advice, medical advice)

For each: provide the test prompt, expected safe response, and risk rating (low/medium/high).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` CLI | Test OpenAI GPT-4o for conversational AI prototyping | `pip install openai` / platform.openai.com/docs |
| `anthropic` CLI | Test Claude models for conversational AI | `pip install anthropic` / docs.anthropic.com |
| `gcloud` (Dialogflow CX) | Deploy and test conversation agents | cloud.google.com/sdk |
| `rasa` CLI | Train and test open-source NLU + dialogue models | `pip install rasa` / rasa.com/docs |
| `botium-cli` | Automated conversation testing framework | `npm install -g botium-cli` / botium.io |
| `deepgram` CLI | Speech-to-text for voice pipeline testing | `npm install -g @deepgram/sdk` / deepgram.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Claude API | SaaS | Yes — REST API | Primary LLM for conversational AI; supports system prompts, multi-turn |
| OpenAI API (GPT-4o) | SaaS | Yes — REST API | Alternative LLM with streaming, function calling |
| Dialogflow CX | SaaS (Google) | Yes — REST API | Enterprise conversational platform with LLM integration |
| Amazon Lex v2 | SaaS | Yes — REST API | AWS-native; integrates with Lambda for fulfilment |
| Voiceflow | SaaS | Yes — REST API | Prototyping + production deployment; supports LLM nodes |
| Rasa | OSS | Yes — Python API | Self-hosted; full control of NLU + dialogue policy |
| ElevenLabs | SaaS | Yes — REST API | TTS for voice output; agent can generate audio previews |
| Deepgram | SaaS | Yes — REST API | ASR with low latency; good for real-time voice pipelines |
| Botium | OSS/SaaS | Yes — CLI + API | Automated conversation regression testing |

## Templates & scripts
See templates.md for system prompt template and dialogue script schema.

Inline: minimal LLM conversation loop for prototyping:
```python
import anthropic, json

client = anthropic.Anthropic()

SYSTEM = """You are {persona_name}, an assistant for {product_name}.
You help users with: {allowed_topics}.
You must not discuss: {forbidden_topics}.
If the user asks for something outside your scope, say: "I can help with {allowed_topics}. Is there something in that area I can assist with?"
Keep responses under 150 words. Be conversational, not formal."""

def chat(history: list, user_msg: str) -> str:
    history.append({"role": "user", "content": user_msg})
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        system=SYSTEM,
        messages=history,
    )
    assistant_msg = response.content[0].text
    history.append({"role": "assistant", "content": assistant_msg})
    return assistant_msg

history = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    print(f"Assistant: {chat(history, user_input)}")
```

## Best practices
- Define topic boundaries in the system prompt as explicit lists, not vague "stay on topic" instructions
- Implement escalation before deploying: a conversational AI with no human handoff path is a customer experience failure
- Use streaming responses for voice pipelines — start TTS synthesis before the full LLM response is complete to reduce perceived latency
- Store conversation history server-side with a session ID; never rely on client to send full history (manipulation risk)
- Run automated regression tests (Botium) on dialogue scripts after every system prompt change
- Log all conversations with user consent; use logs for failure mode analysis, not just analytics

## AI-agent gotchas
- Agent-generated system prompts are often too verbose; token bloat increases latency and cost in multi-turn conversations
- LLM persona consistency degrades with conversation length — test at 20+ turn conversations, not just demo scenarios
- Agents designing conversation flows default to the happy path; explicitly prompt for error recovery and ambiguity handling
- Function calling / tool use in LLM-powered VUI adds a network round-trip per tool call; agents must account for this in latency budgets
- When the agent generates the conversational AI system prompt AND also acts as the conversational AI in testing, it will validate its own outputs favorably — use a separate model/instance for red-teaming

## References
- Anthropic Claude system prompt guide — docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- Rasa "Conversational AI with Transformers" docs — rasa.com/docs
- Google Conversation Design documentation — developers.google.com/assistant/conversation-design
- "Building LLM-Powered Chatbots" — Voiceflow blog — voiceflow.com/blog
- Botium conversation testing guide — botium.io/docs
- "Designing Bots" — Amir Shevat, O'Reilly 2017
