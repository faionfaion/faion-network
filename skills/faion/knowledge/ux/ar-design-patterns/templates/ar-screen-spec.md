<!-- purpose: Per-screen AR interaction spec -->
<!-- consumes: feature brief + platform target -->
<!-- produces: filled ar-screen-spec.md -->
<!-- depends-on: ARKit/ARCore/WebXR HIG -->
<!-- token-budget-impact: ~600 per screen -->

# Screen: <name>

- Runtime: <ARKit|ARCore|WebXR|Unity-ARF>
- Anchoring: <plane|saved-anchor|image>
- Occlusion: <people|depth|people+depth|none>
- Lighting: <estimated|baked|none>
- Gestures: <move|scale|rotate map>
- Track-loss path: <prompt + state preservation>
