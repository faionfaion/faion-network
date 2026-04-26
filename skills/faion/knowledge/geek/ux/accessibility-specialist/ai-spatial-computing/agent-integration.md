# Agent Integration — AI + Spatial Computing

## When to use
- Designing or auditing accessibility for AR/VR/MR (XR) applications targeting Apple Vision Pro, Meta Quest, or Microsoft HoloLens
- Implementing AI-driven contextual UI adaptation (environment-aware UX) in a spatial application
- Generating XR accessibility documentation against W3C XAUR (XR Accessibility User Requirements)
- Prototyping gaze-based, voice-command, or gesture-prediction interaction flows for spatial interfaces
- Evaluating privacy implications of AI + sensor data collection in a spatial product (biometrics, scene scanning)

## When NOT to use
- The product targets only 2D web or mobile — spatial computing patterns add unnecessary complexity
- The team has no access to XR hardware for validation — AI-generated spatial UX without device testing is unreliable
- Real-time AI inference latency cannot meet the <20ms threshold required for comfortable XR experiences — on-device AI is mandatory here
- Budget and timeline do not support the specialized accessibility testing XR requires (screen reader users on XR hardware)

## Where it fails / limitations
- AI scene understanding varies significantly across environments — outdoor/high-brightness or low-contrast scenes degrade accuracy
- Gesture prediction models are trained on majority-population hand shapes; users with motor differences experience higher error rates
- Gaze-based selection requires eye tracking calibration; AI cannot compensate for poor calibration
- On-device AI (required for <20ms latency) has constrained compute — model capabilities significantly limited vs. cloud
- Privacy architecture for biometric and environmental data is not solved by AI; requires explicit design and legal review
- W3C XAUR compliance audit is still manual — no automated tool covers XR accessibility criteria as of 2026
- AI companion or avatar features carry hallucination risk in high-stakes contexts (healthcare, navigation for blind users)

## Agentic workflow
A Claude subagent (Sonnet) reviews spatial UX design specs or code against W3C XAUR criteria and flags gaps in multi-modal input support, fallback strategies, and privacy controls. A Haiku subagent generates interaction pattern documentation (gaze, voice, gesture, controller fallback) from a structured design brief. For accessibility audits of existing XR apps, Sonnet produces a structured XAUR gap analysis with prioritized recommendations. Human XR accessibility specialists and users with disabilities must validate all outputs on actual hardware.

### Recommended subagents
- General Claude subagent (Sonnet) — XAUR gap analysis, interaction pattern review, privacy assessment
- General Claude subagent (Haiku) — documentation generation for spatial interaction patterns and fallback hierarchies

### Prompt pattern
```
You are a spatial computing accessibility specialist. Review the following XR application
interaction spec against W3C XAUR requirements. For each XAUR requirement category
(visual, auditory, motor, cognitive), identify:
1. Which requirements are addressed in the spec
2. Which are missing or only partially addressed
3. Concrete design changes needed for each gap
Output as a structured gap analysis: { category, requirement, status, recommendation }
```

```
You are documenting spatial UI interaction patterns. For the following feature [description],
generate documentation covering:
- Primary interaction mode (gaze/voice/gesture)
- Fallback hierarchy: primary → secondary → tertiary input method
- Latency requirements per interaction type
- Accessibility considerations for vision/motor/cognitive impairments
- Privacy data collected and retention policy
Format as a structured spec section.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ARCore CLI tools | Test AR scene understanding on Android devices | developer.android.com/ar |
| Xcode Accessibility Inspector | Inspect accessibility properties of visionOS apps | Bundled with Xcode |
| `whisper.cpp` | On-device speech-to-text (C++ port, low-latency) | github.com/ggerganov/whisper.cpp |
| `mediapipe` | On-device hand/pose tracking for gesture prediction | `pip install mediapipe` / mediapipe.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apple Vision Pro SDK (visionOS) | Platform SDK | Partial — Xcode-based | AI integration via Core ML; agent can generate boilerplate |
| Meta Quest SDK | Platform SDK | Partial — Unity/Unreal | Mixed Reality Utility Kit; agent can scaffold patterns |
| Microsoft Azure Spatial Anchors | SaaS | Yes — REST API | Persistent object anchoring with cloud AI; API-driven |
| Google ARCore | Platform SDK | Yes — REST API | Scene understanding, object recognition; ML Kit integration |
| Azure AI Vision | SaaS | Yes — REST API | Scene description for blind users; spatial audio cue generation |
| OpenAI Whisper (cloud) | SaaS | Yes — REST API | High-accuracy voice commands; requires network (latency trade-off) |
| Unity Sentis | OSS/SDK | Yes — in-engine | On-device model inference in Unity XR apps |

## Templates & scripts
See `templates.md` for the spatial interaction pattern spec template and XAUR gap analysis checklist.

Interaction fallback hierarchy documentation template (inline):
```markdown
## Interaction: [Feature Name]

### Primary: Gaze + Dwell
- Trigger: User gazes at element for [N]ms
- Latency requirement: <50ms visual feedback
- Accessibility: Supports motor impairments; adjustable dwell time

### Secondary: Voice Command
- Trigger: "[command phrase]"
- ASR model: on-device (Whisper tiny) | cloud (Whisper large)
- Fallback phrase: "[alternative phrasing]"

### Tertiary: Controller Button
- Button mapping: [button] on [controller]
- Works without head tracking: yes/no

### Not supported via:
- Touch (device has no touchscreen)
- Keyboard (no physical keyboard in session)

### Privacy:
- Eye tracking data: processed on-device, not stored
- Voice data: [on-device | cloud, retention: Xd]
- Scene scan: [local only | uploaded for anchoring]
```

## Best practices
- Design all spatial interactions with a three-tier fallback: gaze → voice → controller/gesture — never assume a single input modality
- Validate AI latency on actual target hardware, not simulation — Quest 3 and Vision Pro have very different compute envelopes
- Test gaze interaction with users who wear glasses and those with nystagmus — AI calibration assumptions break here
- AI environmental adaptation (home/office/gym context switching) requires explicit user consent and opt-in, not silent inference
- For healthcare or navigation use cases, require a human expert to validate every AI-generated spatial cue before deployment
- Document privacy data flows explicitly in the spec — biometric and spatial data collection requires GDPR/CCPA disclosure even in XR apps
- Run XAUR gap analysis early in design, not after implementation — spatial accessibility retrofits are expensive

## AI-agent gotchas
- XAUR is not machine-checkable; agent gap analysis is a structured opinion, not a compliance verdict — human XR accessibility expert must validate
- AI scene understanding confidence drops in novel environments the training set did not cover — agent must flag low-confidence recommendations rather than assert them
- On-device model inference limits mean the agent cannot assume cloud-quality AI in the production XR app; recommendations must account for constrained compute
- Gesture prediction models biased toward neurotypical hand shapes — agent must explicitly flag that gesture interactions require testing with users with motor differences
- Human-in-loop checkpoint: before any XR accessibility feature ships, a user with the relevant disability must test it on the target device
- Agent hallucination risk is high for XR accessibility — this is a thin domain in LLM training data; cross-check all specific XAUR references against the actual W3C spec

## References
- W3C XR Accessibility User Requirements (XAUR): https://www.w3.org/TR/xaur/
- Apple Vision Pro accessibility: https://developer.apple.com/accessibility/visionos/
- Meta Quest accessibility: https://developer.oculus.com/resources/accessibility-overview/
- Microsoft Mixed Reality: https://learn.microsoft.com/en-us/windows/mixed-reality/
- Google ARCore: https://developers.google.com/ar
- IEEE: AI in Extended Reality: https://spectrum.ieee.org/ai-ar-vr
