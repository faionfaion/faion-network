# purpose: Shared examples for the 'auditable' invariant across models
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as context

# frozen_string_literal: true

RSpec.shared_examples_for "auditable" do
  it "tracks created_by" do
    expect(subject).to respond_to(:created_by_id)
  end

  it "tracks updated_by" do
    expect(subject).to respond_to(:updated_by_id)
  end

  it "exposes audit_log association" do
    expect(subject.class.reflect_on_association(:audit_log)).not_to be_nil
  end
end
