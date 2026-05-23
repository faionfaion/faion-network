// purpose: Rust proptest! skeleton with persisted-regression config + approx for floats.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml (rust-testing-property)
// depends-on: content/01-core-rules.xml
// token-budget-impact: small (template is loaded only when an artefact is being authored)
use proptest::prelude::*;
use proptest::test_runner::{Config, FileFailurePersistence};

proptest! {
    #![proptest_config(Config {
        failure_persistence: Some(Box::new(FileFailurePersistence::WithSource("regression"))),
        cases: 256,
        .. Config::default()
    })]

    #[test]
    fn roundtrip(s in "\\PC*") {
        let bytes = my_codec::encode(&s);
        let back = my_codec::decode(&bytes).expect("decode should succeed for any input");
        prop_assert_eq!(back, s);
    }
}

// For float invariants:
//   use approx::assert_relative_eq;
//   assert_relative_eq!(actual, expected, epsilon = 1e-9);
