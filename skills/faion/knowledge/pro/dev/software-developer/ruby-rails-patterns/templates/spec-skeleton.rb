# spec/services/users/create_service_spec.rb
require "rails_helper"

RSpec.describe Users::CreateService do
  subject(:result) do
    described_class.new(params: params, current_user: nil).call
  end

  context "with valid params" do
    let(:params) { { name: "Alice", email: "alice@example.com", password: "secret123" } }

    it { is_expected.to be_success }

    it "creates a user" do
      expect { result }.to change(User, :count).by(1)
    end

    it "enqueues welcome email" do
      expect { result }.to have_enqueued_mail(UserMailer, :welcome)
    end
  end

  context "when email already taken" do
    before { create(:user, email: "alice@example.com") }
    let(:params) { { name: "Alice", email: "alice@example.com", password: "secret123" } }

    it { is_expected.to be_failure }

    it "rolls back the audit log" do
      expect { result }.not_to change(AuditLog, :count)
    end
  end
end
