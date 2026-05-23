// purpose: minimum-viable scaffold for the methodology's produces type
// consumes: inputs listed in AGENTS.md Prerequisites table
// produces: config
// depends-on: content/02-output-contract.xml (schema)
// token-budget-impact: low — ~100-400 tokens when loaded as context
//
// ADR: docs/decisions/0001-layer-boundaries.md
import Testing
import Harmonize
import HarmonizeSwiftSyntax

@Suite
struct LayerBoundariesTests {
    @Test func uiDoesNotImportData() {
        let violations = Harmonize
            .productionCode()
            .imports()
            .from(layer: "UI")
            .into(layer: "Data")
        #expect(violations.isEmpty)
    }
}
