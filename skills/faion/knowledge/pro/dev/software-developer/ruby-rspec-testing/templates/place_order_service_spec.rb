# purpose: Isolated RSpec service spec (spec_helper only)
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~500 tokens when loaded as context

# frozen_string_literal: true

require "spec_helper"
require_relative "../../../app/services/orders/place_order_service"
require_relative "../../../app/services/service_result"

RSpec.describe Orders::PlaceOrderService do
  let(:user) { instance_double("User", id: 1) }
  let(:orders_relation) { instance_double("Orders") }
  let(:order) { instance_double("Order", id: 7, items: [], total_cents: 1000) }
  let(:gateway) { instance_double("PaymentGateway") }
  let(:inventory) { instance_double("InventoryService") }
  let(:mailer) { class_double("OrderMailer") }

  subject(:service) { described_class.new(user, gateway: gateway, inventory: inventory, mailer: mailer) }

  before do
    allow(user).to receive(:orders).and_return(orders_relation)
    allow(orders_relation).to receive(:build).and_return(order)
  end

  context "when inventory sufficient and payment succeeds" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(order).to receive(:update!)
      allow(inventory).to receive(:reserve).and_return(double(success?: true))
      allow(gateway).to receive(:charge).and_return(double(success?: true, id: "ch_1"))
      allow(mailer).to receive_message_chain(:confirmation, :deliver_later)
    end

    it "returns success with the order" do
      result = service.call(items: [{ sku: "X", qty: 1 }])
      expect(result.success?).to be true
      expect(result.data).to eq(order)
    end
  end

  context "when inventory is insufficient" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(inventory).to receive(:reserve).and_return(double(success?: false))
    end

    it "returns failure with :insufficient_stock" do
      result = service.call(items: [])
      expect(result.failure?).to be true
      expect(result.error).to eq(:insufficient_stock)
    end
  end

  context "when payment is declined" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(inventory).to receive(:reserve).and_return(double(success?: true))
      allow(gateway).to receive(:charge).and_return(double(success?: false))
    end

    it "returns failure with :payment_declined" do
      result = service.call(items: [{ sku: "X", qty: 1 }])
      expect(result.failure?).to be true
      expect(result.error).to eq(:payment_declined)
    end
  end
end
