# Voice Flow: [Feature Name]

**Version:** [N]

## Overview

**Purpose:** [What this voice feature does]
**Trigger:** [How user starts interaction — wake word, button, API call]
**Exit:** [How interaction ends — success, timeout, user escape]

## User Context

- When: [Typical use times]
- Where: [Environment — home, car, hands-busy]
- Device: [Smart speaker / Phone / In-car / Custom]
- Hands/Eyes: [Occupied or available]

## Happy Path Dialogue

**User:** [Initial utterance]
**System:** [Response]
**User:** [Follow-up, if any]
**System:** [Final response]

## Intent Definitions

### Intent: [IntentName]

**Description:** [What user wants to do]

**Required slots:**
| Slot | Type | Prompt if missing |
|------|------|-------------------|
| [slot] | [type] | "[prompt]" |

**Sample utterances (min 5):**
- "[Utterance 1]"
- "[Utterance 2]"
- "[Utterance 3]"
- "[Utterance 4]"
- "[Utterance 5]"

**Response template:** "[Response with {slot} placeholders]"

## Error Handling

### No Input Detected
- 1st prompt: "[Reprompt — shorter than original]"
- 2nd prompt: "[Rephrase with examples]"
- 3rd prompt: "[Offer fallback — agent, visual, or help]"

### Speech Not Understood
**Response:** "[Acknowledgment + reprompt]"

### Invalid Slot Value
**Response:** "[Explain valid options]"

## Confirmation Strategy

| Action Type | Confirmation |
|-------------|--------------|
| [Low-risk reversible] | Implicit |
| [High-risk or costly] | Explicit |
| [Irreversible] | Explicit + repeat details |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| [Edge case 1] | [Response] |
| [Edge case 2] | [Response] |

## Fallbacks

- Visual fallback: [Screen content if device has display]
- Human fallback: [Transfer to human agent]
- Alternative: [Suggest different action]
