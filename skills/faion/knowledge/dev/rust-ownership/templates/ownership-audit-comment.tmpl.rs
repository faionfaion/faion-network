// purpose:   3-question ownership audit, attached above every pub fn
// consumes:  function purpose + call-site list
// produces:  documented signature decision
// depends-on: rust-ownership/content/06-decision-tree.xml
// token-budget-impact: ~30 tokens per function — keeps the design intent inline

// Ownership audit:
//   keeps_value:           false   // does this fn store / return the value?
//   modifies_value:        false   // does it write through the param?
//   shares_across_threads: false   // does any path spawn with the value?
// → param_kind: shared-ref (&T)
pub fn example(input: &str) -> usize {
    input.len()
}
