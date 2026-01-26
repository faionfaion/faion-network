# LLM Prompts for Speech-to-Text Tasks

## Whisper Prompts (Context Guidance)

Whisper accepts a `prompt` parameter to guide transcription. Use these patterns to improve accuracy.

### Domain-Specific Vocabulary

```python
# Medical transcription
prompt = """
Medical consultation transcript. Terms include:
hypertension, tachycardia, myocardial infarction, ECG, CBC,
metformin, lisinopril, atorvastatin, subcutaneous injection.
"""

# Legal transcription
prompt = """
Legal deposition transcript. Terms include:
plaintiff, defendant, affidavit, deposition, habeas corpus,
subpoena, voir dire, pro bono, prima facie, res judicata.
"""

# Technical/Software
prompt = """
Software engineering meeting transcript. Terms include:
Kubernetes, PostgreSQL, Redis, GraphQL, CI/CD pipeline,
microservices, containerization, API gateway, load balancer.
"""

# Financial
prompt = """
Financial earnings call transcript. Terms include:
EBITDA, revenue recognition, gross margin, operating expenses,
year-over-year growth, guidance, EPS, market capitalization.
"""
```

### Proper Nouns and Names

```python
# Company names
prompt = """
Discussion about tech companies: OpenAI, Anthropic, Google DeepMind,
Meta AI, Microsoft Azure, Amazon Web Services, NVIDIA.
"""

# Person names
prompt = """
Participants: Dr. Sarah Chen, Professor Michael O'Brien,
CEO Oleksandr Shevchenko, CFO Maria Garcia-Lopez.
"""

# Product names
prompt = """
Products discussed: iPhone 17, MacBook Pro M4, Galaxy S26,
Pixel 10, Surface Pro 11, ThinkPad X1 Carbon Gen 13.
"""
```

### Formatting Guidance

```python
# Numbers and measurements
prompt = """
Scientific discussion with precise measurements.
Use numerals: 42.5 kg, 3.14159, $1,234,567, 99.9%.
"""

# Timestamps and dates
prompt = """
Meeting scheduled for dates and times.
Format: January 15, 2026, 2:30 PM EST.
"""

# Acronyms expansion
prompt = """
Expand acronyms where appropriate:
API (Application Programming Interface),
SaaS (Software as a Service),
ROI (Return on Investment).
"""
```

### Language Mixing

```python
# English-Ukrainian mix
prompt = """
Bilingual conversation in English and Ukrainian.
Ukrainian terms: привіт, дякую, будь ласка, розробка.
"""

# English-Spanish mix
prompt = """
Bilingual conversation in English and Spanish.
Spanish terms: buenos dias, gracias, por favor, desarrollo.
"""
```

## Post-Processing Prompts

Use LLMs to enhance transcription output.

### Transcript Cleanup

```
You are a transcript editor. Clean up the following raw speech-to-text output:

1. Fix obvious transcription errors
2. Add proper punctuation and capitalization
3. Remove filler words (um, uh, like, you know) if excessive
4. Keep the original meaning intact
5. Format numbers consistently
6. Preserve speaker identities if present

Raw transcript:
{transcript}

Return the cleaned transcript only, no explanations.
```

### Speaker Identification

```
Analyze this transcript and identify distinct speakers based on context clues.

Transcript:
{transcript}

For each segment:
1. Assign speaker labels (Speaker A, Speaker B, etc.)
2. Note any names mentioned that could identify speakers
3. Identify speaker roles if apparent (interviewer, interviewee, host, guest)

Output format:
[Speaker A - Host]: text
[Speaker B - Guest]: text
```

### Summary Generation

```
Create a structured summary of this transcript.

Transcript:
{transcript}

Provide:
1. **Executive Summary** (2-3 sentences)
2. **Key Points** (bullet list, max 5)
3. **Action Items** (if any)
4. **Decisions Made** (if any)
5. **Questions Raised** (if any)

Be concise and factual.
```

### Meeting Notes

```
Convert this meeting transcript into professional meeting notes.

Transcript:
{transcript}

Format:
# Meeting Notes - {infer date if mentioned}

## Attendees
- List participants

## Agenda Items
### Item 1: {topic}
- Discussion points
- Decisions
- Action items

## Next Steps
- Action items with owners (if identifiable)

## Follow-up Items
- Unresolved questions
```

### Translation with Context

```
Translate this transcript from {source_language} to {target_language}.

Important:
1. Preserve speaker identities
2. Maintain timestamps if present
3. Keep technical terms accurate
4. Preserve tone and formality level
5. Note any culturally-specific references

Transcript:
{transcript}
```

### Content Analysis

```
Analyze this transcript for key information extraction.

Transcript:
{transcript}

Extract:
1. **Topics Discussed**: Main themes covered
2. **Entities**: People, organizations, products mentioned
3. **Sentiment**: Overall tone (positive/negative/neutral)
4. **Key Quotes**: Notable statements (max 3)
5. **Technical Terms**: Domain-specific vocabulary used
6. **Timestamps**: Important moments (if timestamps present)

Format as JSON.
```

### Q&A Extraction

```
Extract questions and answers from this transcript.

Transcript:
{transcript}

Format each Q&A pair:
Q: [Question text]
A: [Answer text]
Context: [Brief context if needed]

Only include clear question-answer pairs, not rhetorical questions.
```

## Quality Assessment Prompts

### Transcription Quality Check

```
Evaluate the quality of this speech-to-text transcription.

Transcript:
{transcript}

Check for:
1. **Coherence**: Does the text flow logically? (1-5)
2. **Completeness**: Are there obvious gaps? (1-5)
3. **Accuracy indicators**: Are there nonsensical phrases? (1-5)
4. **Formatting**: Is punctuation reasonable? (1-5)

Provide:
- Overall quality score (1-5)
- Specific issues found
- Segments needing review (quote problematic parts)
```

### Error Detection

```
Identify potential transcription errors in this text.

Transcript:
{transcript}

Flag:
1. Words that seem out of context
2. Incomplete sentences
3. Repeated words/phrases (disfluencies vs errors)
4. Numbers that seem incorrect
5. Names that might be misspelled

For each issue:
- Quote the problematic text
- Suggest possible correction
- Confidence level (high/medium/low)
```

## Specialized Prompts

### Interview Transcript

```
Format this interview transcript professionally.

Raw transcript:
{transcript}

Requirements:
1. Identify interviewer (Q:) and interviewee (A:)
2. Clean up speech disfluencies
3. Preserve important pauses with [pause]
4. Note non-verbal cues if apparent [laughs], [sighs]
5. Format for publication readiness
```

### Podcast Show Notes

```
Create show notes from this podcast transcript.

Transcript:
{transcript}

Include:
1. **Episode Title** (suggest based on content)
2. **Episode Summary** (2-3 sentences)
3. **Timestamps** (link to key moments)
   - 00:00 Introduction
   - MM:SS Topic discussed
4. **Guest Bio** (if applicable)
5. **Resources Mentioned** (links, books, tools)
6. **Key Takeaways** (3-5 bullet points)
```

### Call Center Analysis

```
Analyze this customer service call transcript.

Transcript:
{transcript}

Provide:
1. **Call Classification**: (inquiry/complaint/support/sales)
2. **Customer Sentiment**: throughout the call
3. **Issue Summary**: what the customer needed
4. **Resolution Status**: (resolved/escalated/pending)
5. **Agent Performance**:
   - Empathy demonstrated
   - Solution provided
   - Follow-up offered
6. **Improvement Suggestions**: for agent training
```

### Lecture Notes

```
Convert this lecture transcript into study notes.

Transcript:
{transcript}

Format:
# {Lecture Topic}

## Learning Objectives
- What students should understand

## Key Concepts
### Concept 1
- Definition
- Examples
- Related terms

## Important Quotes
> "Notable quotes from the lecture"

## Review Questions
1. Questions to test understanding

## Further Reading
- Topics to explore
```

## Prompt Templates for Code

```python
class TranscriptionPrompts:
    """Reusable prompts for STT post-processing."""

    CLEANUP = """Clean up this transcript. Fix errors, add punctuation,
remove excessive filler words. Keep meaning intact.

Transcript:
{transcript}"""

    SUMMARIZE = """Summarize this transcript in {length} sentences.
Focus on key points and decisions.

Transcript:
{transcript}"""

    EXTRACT_ACTIONS = """Extract action items from this meeting transcript.
Format: - [Owner] Action item (deadline if mentioned)

Transcript:
{transcript}"""

    IDENTIFY_SPEAKERS = """Identify and label speakers in this transcript.
Use context clues to determine roles.

Transcript:
{transcript}"""

    @classmethod
    def get_domain_prompt(cls, domain: str) -> str:
        """Get domain-specific vocabulary prompt."""
        domains = {
            "medical": "Medical terms: diagnosis, treatment, medication, symptoms...",
            "legal": "Legal terms: plaintiff, defendant, jurisdiction, statute...",
            "tech": "Technical terms: API, database, deployment, infrastructure...",
            "finance": "Financial terms: revenue, EBITDA, equity, liabilities...",
        }
        return domains.get(domain, "")
```
