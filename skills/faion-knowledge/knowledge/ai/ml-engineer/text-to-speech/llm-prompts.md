# TTS LLM Prompts

## Provider Selection

### Select TTS Provider

```
Given these requirements, recommend the best TTS provider:

Use case: {use_case}
Latency requirement: {latency_ms}ms
Quality priority: {quality_1_to_10}
Voice cloning needed: {yes_no}
Languages: {languages}
Monthly volume: {characters_per_month}
Budget: ${budget_per_month}

Consider:
1. ElevenLabs - Best quality, voice cloning, 75ms Flash model
2. OpenAI TTS - Good quality, steerability, 6 preset voices
3. Google Cloud TTS - Widest language support, SSML
4. Azure TTS - Custom Neural Voice, 500+ voices
5. Coqui/XTTS - Open source, self-hosted, free

Provide:
- Recommended provider with rationale
- Specific model/tier recommendation
- Voice suggestions
- Cost estimate
- Fallback option
```

### Compare Providers for Use Case

```
Compare TTS providers for: {use_case}

Evaluate on:
1. Voice quality and naturalness
2. Latency (real-time capability)
3. Language support
4. Voice cloning/customization
5. SSML/pronunciation control
6. Streaming support
7. Cost per 1000 characters
8. API reliability/uptime

Output format:
| Provider | Quality | Latency | Languages | Cloning | Cost | Best For |
|----------|---------|---------|-----------|---------|------|----------|
```

## Voice Selection

### Choose Voice for Content

```
Select the best TTS voice for this content:

Content type: {content_type}
Target audience: {audience}
Tone desired: {tone}
Language: {language}
Duration: {short_medium_long}

Content sample:
"""
{content_sample}
"""

Recommend:
1. Provider and voice ID
2. Voice settings (speed, pitch, stability)
3. Alternative voices for A/B testing
4. SSML recommendations if applicable
```

### Voice Cloning Requirements

```
Evaluate voice cloning feasibility:

Source audio available: {duration_seconds} seconds
Audio quality: {high_medium_low}
Background noise: {yes_no}
Consistent speaker: {yes_no}
Legal consent obtained: {yes_no}

Intended use:
- {use_case_1}
- {use_case_2}

Provide:
1. Cloning method recommendation (instant vs professional)
2. Audio preparation steps
3. Expected quality assessment
4. Legal/ethical considerations
5. Provider recommendation
```

## Implementation Guidance

### Design TTS Architecture

```
Design a TTS architecture for:

Application: {application_type}
Scale: {requests_per_day}
Latency SLA: {max_latency_ms}ms
Availability SLA: {uptime_percent}%
Budget: ${monthly_budget}

Requirements:
- {requirement_1}
- {requirement_2}
- {requirement_3}

Provide:
1. Architecture diagram (text-based)
2. Provider selection with justification
3. Caching strategy
4. Fallback/redundancy approach
5. Cost optimization recommendations
6. Monitoring points
```

### Implement Streaming TTS

```
Design streaming TTS implementation for:

Use case: {real_time_conversation | live_narration | voice_assistant}
Target latency: {latency_ms}ms
Audio format: {format}
Playback environment: {browser | mobile | server}

Considerations:
- First byte latency
- Chunk size optimization
- Buffer management
- Error recovery
- Network interruption handling

Provide:
1. Code architecture
2. Provider recommendation
3. Streaming protocol
4. Buffer strategy
5. Error handling approach
```

### Long-form Content Strategy

```
Design TTS strategy for long-form content:

Content type: {audiobook | podcast | documentation}
Average length: {word_count} words
Output format: {format}
Chapter/section markers: {yes_no}

Requirements:
- Consistent voice throughout
- Chapter navigation
- Pause/resume capability
- Metadata embedding

Provide:
1. Chunking strategy
2. Audio stitching approach
3. Metadata handling
4. Quality assurance steps
5. Cost optimization
```

## Text Preprocessing

### Prepare Text for TTS

```
Prepare this text for TTS synthesis:

"""
{raw_text}
"""

Tasks:
1. Expand abbreviations
2. Handle numbers (currency, dates, times)
3. Mark pronunciation issues
4. Identify SSML opportunities
5. Suggest chunking points

Output:
- Preprocessed text
- SSML version (if applicable)
- Pronunciation notes
- Chunk boundaries
```

### Create SSML Markup

```
Convert this text to SSML for natural speech:

Plain text:
"""
{text}
"""

Requirements:
- Natural pauses
- Emphasis on key points
- Correct number pronunciation
- Appropriate pacing

Target provider: {google | azure | amazon}

Provide:
1. Full SSML markup
2. Explanation of SSML elements used
3. Provider-specific notes
```

## Troubleshooting

### Diagnose TTS Quality Issues

```
Diagnose TTS quality problem:

Issue: {issue_description}

Current configuration:
- Provider: {provider}
- Model: {model}
- Voice: {voice}
- Settings: {settings}

Sample text causing issue:
"""
{problem_text}
"""

Expected vs Actual:
- Expected: {expected_result}
- Actual: {actual_result}

Analyze:
1. Root cause
2. Provider-specific quirks
3. Text preprocessing fixes
4. SSML solutions
5. Voice/model alternatives
```

### Optimize TTS Latency

```
Optimize TTS latency for:

Current latency: {current_ms}ms
Target latency: {target_ms}ms

Current setup:
- Provider: {provider}
- Model: {model}
- Format: {format}
- Network: {network_description}

Optimization areas:
1. Model selection
2. Audio format
3. Streaming configuration
4. Network optimization
5. Caching opportunities
6. Pre-generation strategies
```

## Cost Optimization

### Reduce TTS Costs

```
Optimize TTS costs for:

Current monthly spend: ${current_cost}
Target monthly spend: ${target_cost}
Monthly character volume: {volume}

Current usage pattern:
- Provider: {provider}
- Cached content: {cache_rate}%
- Repeated phrases: {repeated_content_percent}%
- Real-time vs batch: {real_time_percent}%

Analyze:
1. Caching opportunities
2. Provider tier optimization
3. Batch processing potential
4. Content deduplication
5. Format/quality tradeoffs
6. Alternative providers for specific use cases
```

### Calculate TTS ROI

```
Calculate TTS implementation ROI:

Use case: {use_case}
Current solution: {current_solution}
Current cost: ${current_cost}

Proposed TTS implementation:
- Provider: {provider}
- Volume: {characters_per_month}
- Cost per 1K chars: ${cost}

Benefits to quantify:
- Time savings
- Quality improvement
- Scalability
- User experience

Provide:
1. Monthly cost projection
2. Implementation cost
3. Time to ROI
4. Risk assessment
```

## Integration Patterns

### Design TTS for Conversational AI

```
Design TTS integration for conversational AI:

Platform: {platform}
LLM: {llm_provider}
Response length: {avg_words}
Latency budget: {total_latency_ms}ms

Requirements:
- Natural conversational flow
- Emotion/tone matching
- Interrupt handling
- Multi-turn context

Provide:
1. Architecture for LLM + TTS pipeline
2. Streaming strategy
3. Voice selection for conversation
4. Latency optimization
5. Error handling
6. Fallback strategies
```

### Integrate TTS with Video

```
Design TTS for video narration:

Video type: {type}
Duration: {duration}
Narration style: {style}
Timing requirements: {timing}

Requirements:
- Sync with visual content
- Natural pacing
- Chapter markers
- Multiple languages (optional)

Provide:
1. Audio generation workflow
2. Timing/sync approach
3. Voice recommendations
4. Post-processing steps
5. Quality assurance checklist
```
