# purpose: RSpec test using factory_bot + let
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for testing-backend-languages
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

require 'rails_helper'

RSpec.describe OrderService, type: :service do
  let(:customer) { create(:customer) }
  let!(:order) { create(:order, customer: customer) }

  describe '#charge' do
    it 'marks the order as charged on success' do
      result = described_class.new.charge(order)
      expect(result).to be_success
      expect(order.reload.status).to eq('charged')
    end
  end
end
