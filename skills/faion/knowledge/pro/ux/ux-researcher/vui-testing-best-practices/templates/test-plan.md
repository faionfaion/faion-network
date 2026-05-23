<!-- purpose: VUI test plan skeleton -->
<!-- consumes: product brief + corpus -->
<!-- produces: test-plan.md -->
<!-- depends-on: vui-conversation-design + core-vui-principles -->
<!-- token-budget-impact: ~700 -->

# VUI Test Plan — <product>

## Objectives
- ASR WER target: <X>%
- NLU intent F1 target: >=<X>
- NLU slot F1 target: >=<X>
- Dialog completion target: >=<X>%

## Fixtures
- Utterance corpus: real anonymised logs, n=<N>
- Ambient noise stems: cafe, traffic, tv
- Locales: <list>

## Tiers
- Smoke (every commit, 10 utterances)
- Full (nightly, full corpus)
- Field-replay (release, real-device farm)

## ASR version pin
<provider/model/version>
