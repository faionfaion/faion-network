# VUI + IoT Integration

## Problem

Smart home devices need coherent voice control.

## Smart Home Patterns

| Pattern | Example |
|---------|---------|
| Direct control | "Turn off the lights" |
| Scene activation | "Goodnight" (triggers routine) |
| Status query | "Is the front door locked?" |
| Conditional | "Turn on AC when I get home" |
| Scheduling | "Turn off lights at 11 PM" |

## Multi-Device Coordination

**User:** "I'm leaving"

**System:**
- Locks doors
- Turns off lights
- Adjusts thermostat
- Arms security
- Confirms: "Home secured. Have a good day."

## Best Practices

- Group devices logically
- Create intuitive scene names
- Provide feedback for each action
- Handle partial failures gracefully
- Allow undo for recent actions

## Sources

- [Amazon Alexa Smart Home Skills](https://developer.amazon.com/en-US/docs/alexa/smarthome/understand-the-smart-home-skill-api.html)
- [Google Home Automation](https://developers.home.google.com/)
- [Matter Smart Home Standard](https://csa-iot.org/all-solutions/matter/)
- [Voice Control for IoT](https://www.nngroup.com/articles/voice-iot/)
- [Smart Home UX Patterns](https://www.smashingmagazine.com/2025/smart-home-voice-ux/)
