# Error Handling in VUI

## Problem

Voice recognition errors frustrate users and break conversations.

## Error Types

| Error | Cause | Solution |
|-------|-------|----------|
| No input | User silent | Repeat prompt with hint |
| No match | Unrecognized speech | Offer alternatives |
| Ambiguous | Multiple interpretations | Ask clarifying question |
| System error | Technical failure | Apologize, suggest retry |

## Progressive Disclosure

**First failure:**
"I didn't catch that. What's the city?"

**Second failure:**
"I'm having trouble understanding. Try saying something like 'New York' or 'Chicago'"

**Third failure:**
"Let me try another way. [Transfer to visual interface or agent]"

## Best Practices

- Never blame the user
- Provide immediate feedback
- Offer recovery options
- Suggest example phrases
- Know when to escalate

## Sources

- [Voice Error Handling - NNG](https://www.nngroup.com/articles/voice-error-handling/)
- [Designing Voice User Interfaces by Cathy Pearl](https://www.oreilly.com/library/view/designing-voice-user/9781491955406/)
- [Google Conversation Design](https://designguidelines.withgoogle.com/conversation/conversation-design/error-handling.html)
- [Amazon Alexa Error Handling](https://developer.amazon.com/en-US/docs/alexa/alexa-design/error-handling.html)
- [Graceful Degradation in VUI](https://www.smashingmagazine.com/2025/voice-error-recovery/)
