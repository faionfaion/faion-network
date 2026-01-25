---
id: voice-ui-patterns
name: "Voice UI Patterns & Guidelines"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Voice UI Patterns & Guidelines

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Advanced
- **Tags:** #methodology #ux #design #voice-ui #conversational
- **Agent:** faion-usability-agent

---

## Prompt Writing Guidelines

### Do's

| Guideline | Example |
|-----------|---------|
| **Be concise** | "Added." not "I have successfully added the item to your list." |
| **Be conversational** | "What's next?" not "Please state your next request." |
| **Give options** | "You can say 'today' or give a specific date." |
| **Confirm important actions** | "That's a $500 transfer. Confirm?" |
| **Use prosody** | Write for speaking rhythm |

### Don'ts

| Avoid | Why |
|-------|-----|
| **Long prompts** | Users forget the beginning |
| **Too many options** | Can't remember more than 3-4 |
| **Jargon** | Users won't know special terms |
| **Assuming context** | "It" and "that" are ambiguous |
| **Same error message** | Frustrates users who keep trying |

---

## Error Recovery

### Progressive Error Handling

```
1st error:
"Sorry, I didn't catch that. What city?"

2nd error:
"I'm still having trouble. You can say a city name
like 'New York' or 'Los Angeles'."

3rd error:
"Let me help differently. Would you like to type
the city instead, or speak to someone?"
```

### Error Types and Responses

| Error | Good Response |
|-------|--------------|
| **No input** | "I didn't hear anything. Try again?" |
| **Not understood** | "I didn't understand. Could you rephrase?" |
| **Wrong intent** | "I thought you meant X. Did you mean Y?" |
| **Invalid value** | "I don't have that option. You can choose A, B, or C." |
| **System error** | "Something went wrong on my end. Let's try again." |

---

## Multimodal Design

When voice + screen available:

### Voice + Visual Best Practices

| Element | Voice | Visual |
|---------|-------|--------|
| **Lists** | Say top 3 | Show full list |
| **Confirmation** | Speak it | Show details |
| **Input** | Voice command | Tap fallback |
| **Errors** | Speak guidance | Show options |

### Screen Companion

```
Voice: "Here are your upcoming appointments."
Screen: [Shows full calendar with details user can scan]

Voice: "Tap the one you want to reschedule."
Screen: [Each appointment is tappable]
```

---

## Platform Guidelines

### Amazon Alexa

- Custom wake word not allowed
- 8-second response limit
- Card/APL for visual companions
- Certification required

### Google Assistant

- Action invocation
- Multi-surface support
- Rich responses with cards
- Dialogflow for NLU

### Apple Siri

- SiriKit intents (limited)
- Shortcuts for custom
- HomePod integration
- Privacy-focused

---

## Common Mistakes

1. **Too much speech** - Users zone out after 15 seconds
2. **No error variety** - Same message frustrates users
3. **Expecting exact phrases** - Natural language varies
4. **Forgetting context** - Not using conversation history
5. **No escape hatch** - Users must be able to exit
6. **Visual thinking** - Designing for eye, not ear

---

## Advanced Patterns

### Context Preservation

```
User: "Set an alarm for 7 AM"
System: "Alarm set for 7 AM tomorrow."
User: "Make it 6:30"
System: "Updated to 6:30 AM."
```

### Implicit Confirmation

```
Low risk:
User: "Add milk"
System: "Added milk to your list."

High risk:
User: "Send $500 to John"
System: "That's $500 to John Smith. Should I send it?"
```

### Graceful Degradation

```
Ideal: Full voice conversation
Good: Voice + visual
Fallback: Visual input with voice output
Last resort: Full visual interface
```

---

## Voice + Screen Patterns

### List Navigation

```
Voice: "Here are the top 3 restaurants near you:
        The Italian Place, Sushi Bar, and Pizza Palace.
        You can also scroll to see more."
Screen: [Shows full list of 12 restaurants]
```

### Form Filling

```
Voice: "What's your zip code?"
Screen: [Shows numeric keypad as fallback]
User: [Can speak "90210" or tap it]
```

### Visual Disambiguation

```
User: "Navigate to Main Street"
System: "I found 3 Main Streets. Tap the one you want."
Screen: [Shows map with 3 options]
```

---

## Conversation Design Principles

### 1. Turn-Taking

```
System finishes speaking → User speaks → System responds
Avoid interrupting user mid-sentence
Support "barge-in" for impatient users
```

### 2. Repair Strategies

```
User: "Set timer for... um... 20 minutes"
System: [Ignores hesitation, extracts "20 minutes"]

User: "No wait, make it 25"
System: [Updates timer without complaint]
```

### 3. Progressive Disclosure

```
Initial: "What city?"
If error: "You can say a city like Seattle or Boston."
If error again: "Try saying just the city name, like 'Chicago'."
```

---

## Accessibility in Voice UI

### Voice-First Benefits

- No screen required
- Hands-free operation
- Faster for some tasks
- Natural for visually impaired

### Considerations

- Speech impediments
- Accent recognition
- Quiet environments
- Privacy concerns

### Inclusive Design

```
Provide:
- Visual alternative (text input)
- Audio output alternative (screen text)
- Multiple ways to activate
- Clear error messages
```

---

## Platform-Specific Features

### Alexa Skills Kit

```
Wake word: "Alexa"
Invocation: "Alexa, ask Pizza Place for a large pepperoni"
Built-in intents: AMAZON.StopIntent, AMAZON.HelpIntent
Session management
Account linking for personalization
```

### Google Actions

```
Invocation: "Hey Google, talk to Pizza Place"
Rich responses with cards
Multi-surface support (phone, speaker, display)
Conversational Actions (natural flow)
```

### Siri Shortcuts

```
User-defined phrases
Limited to SiriKit domains
Great for app integration
Shortcuts app for customization
```

---

## Performance Metrics

### Key Indicators

| Metric | Target |
|--------|--------|
| **Task completion rate** | >85% |
| **Average turns per task** | <3 |
| **Error rate** | <15% |
| **Fallback rate** | <10% |
| **User satisfaction (CSAT)** | >4.0/5 |
| **Retention (7-day)** | >40% |

### Optimization

```
High error rate → Improve utterance coverage
High turns → Simplify flow
Low completion → Better error recovery
Low retention → More value, less friction
```

---

## Testing Checklist

Functionality:
- [ ] All intents trigger correctly
- [ ] Slots captured accurately
- [ ] Error handling works
- [ ] Confirmations appropriate
- [ ] Fallbacks available

User Experience:
- [ ] Natural phrasing
- [ ] Clear prompts
- [ ] Helpful errors
- [ ] Reasonable turn count
- [ ] Exit options clear

Edge Cases:
- [ ] Ambient noise
- [ ] Multiple accents
- [ ] Fast/slow speech
- [ ] Interruptions
- [ ] Ambiguous input

Accessibility:
- [ ] Works without screen
- [ ] Text alternative available
- [ ] Privacy respected
- [ ] Multiple activation methods

---

## Implementation Tips

### Start Simple

```
Phase 1: One happy path
Phase 2: Add error handling
Phase 3: Add variations
Phase 4: Optimize based on data
```

### Iterate Based on Data

```
Track:
- Most common utterances
- Frequent errors
- Drop-off points
- User feedback

Improve:
- Add missing utterances
- Clarify confusing prompts
- Simplify complex flows
```

### Design for Failure

```
Assume:
- Recognition will fail
- Users will misspeak
- Context will be unclear

Prepare:
- Multiple reprompt strategies
- Visual fallbacks
- Human handoff option
```

---

## References

- Designing Voice User Interfaces by Cathy Pearl
- Conversational Design by Erika Hall
- VoiceFirst.fm podcast
- Amazon Alexa Design Guide
- Google Conversation Design
- Voice UX Design Patterns (Nielsen Norman Group)

## Sources

- [Google Conversation Design Guidelines](https://designguidelines.withgoogle.com/conversation/)
- [Amazon Alexa Design Guide](https://developer.amazon.com/en-US/docs/alexa/alexa-design/get-started.html)
- [Voice UX Patterns - NNG](https://www.nngroup.com/articles/voice-ux/)
- [Conversational Design by Erika Hall](https://abookapart.com/products/conversational-design)
- [Designing Voice User Interfaces](https://www.oreilly.com/library/view/designing-voice-user/9781491955406/)

---

**Related Files:**
- [voice-ui-basics.md](voice-ui-basics.md) - Framework, process, templates, examples
- [vui-conversation-design.md](vui-conversation-design.md) - Advanced conversation patterns
- [error-handling-in-vui.md](error-handling-in-vui.md) - Detailed error strategies
- [multimodal-vui-design.md](multimodal-vui-design.md) - Voice + screen patterns
