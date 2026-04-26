# Voice Flow: [Feature Name]

**Version:** [Number]
**Date:** [Date]

## Overview

**Purpose:** [What this voice feature does]
**Trigger:** [How user starts interaction — wake word, button, context]
**Exit:** [How interaction ends — completion, cancellation, timeout, fallback]

## User Context

- When: [Typical use times / situations]
- Where: [Environment — home, car, office, noisy public]
- Device: [Smart speaker / Phone / In-car / Headset]
- Hands/Eyes: [Occupied or available]

## Happy Path Dialogue

**User:** [Initial utterance]
**System:** [Response — under 20 words for smart speakers]
**User:** [Follow-up if needed]
**System:** [Final response with implicit or explicit confirmation]

## Intent Definitions

### Intent: [IntentName]

**Description:** [What user wants to do]

**Required slots:**
| Slot | Type | Reprompt if missing |
|------|------|---------------------|
| [slot] | [type] | "[prompt — under 20 words]" |

**Sample utterances (minimum 10):**
- "[Utterance 1]"
- "[Utterance 2]"
- "[Utterance 3]"

**Response template:** "[Response with {slot} placeholders]"

## Error Handling

### No Input Detected
**1st prompt:** "[Rephrase — shorter than original]"
**2nd prompt:** "[Offer examples: You can say X or Y]"
**3rd prompt:** "[Offer fallback: different modality or human transfer]"

### Speech Not Recognized
**Response:** "[Acknowledgment + shorter reprompt]"

### Invalid Slot Value
**Response:** "[Explain valid options with examples]"

### Confirmation Denied
**Response:** "[Acknowledge denial + offer alternative or exit]"

## Confirmation Strategy

| Action Type | Confirmation |
|-------------|--------------|
| Low-risk (reversible) | Implicit — just do it |
| High-risk (costly) | Explicit — repeat details + confirm |
| Irreversible | Explicit + repeat all details |

## Fallbacks

- Visual fallback: [Screen if available]
- Human fallback: [Transfer to agent]
- Alternative: [Suggest different action]
