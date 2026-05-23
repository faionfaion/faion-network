# purpose: Legacy template for the ruby-rspec-testing methodology.
# consumes: inputs declared in ruby-rspec-testing/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
# RSpec service spec skeleton
# Replace: Users::CreateService, :params factory hash, result shape

require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '#call' do
    subject(:service) { described_class.new(params: params) }

    context 'with valid params' do
      let(:params) { { name: 'Alice', email: 'alice@example.com', password: 'secret123' } }

      it 'creates a user' do
        expect { service.call }.to change(User, :count).by(1)
      end

      it 'returns a success result' do
        result = service.call
        expect(result).to be_success
        expect(result.data).to be_a(User)
      end

      it 'enqueues the welcome email' do
        expect { service.call }.to have_enqueued_mail(UserMailer, :welcome)
      end
    end

    context 'with invalid params (missing email)' do
      let(:params) { { name: 'Alice', email: '', password: 'secret' } }

      it 'does not create a user' do
        expect { service.call }.not_to change(User, :count)
      end

      it 'returns a failure result with errors' do
        result = service.call
        expect(result).to be_failure
        expect(result.errors).to include(/Email/)
      end
    end
  end
end
