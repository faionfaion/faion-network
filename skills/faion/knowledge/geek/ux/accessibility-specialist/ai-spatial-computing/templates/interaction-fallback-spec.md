# Spatial Interaction Spec: [Feature Name]

## Primary: Gaze + Dwell
- Trigger: user gazes at element for [N]ms
- Latency requirement: &lt;50ms visual feedback
- Accessibility: supports motor impairments; adjustable dwell time setting

## Secondary: Voice Command
- Trigger: "[command phrase]"
- ASR model: on-device (Whisper tiny) | cloud (Whisper large)
- Fallback phrase: "[alternative phrasing]"
- Latency requirement: &lt;200ms response start

## Tertiary: Controller Button
- Button mapping: [button] on [controller]
- Works without head tracking: yes / no

## Not supported via
- Touch (device has no touchscreen)
- Keyboard (no physical keyboard in session)

## Privacy
- Eye tracking data: processed on-device, not stored
- Voice data: on-device | cloud — retention: [Xd]
- Scene scan: local only | uploaded for anchoring — retention: [Xd]
- Consent required: yes — presented at [onboarding / feature first-use]
