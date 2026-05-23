# purpose: RSpec skeleton for service isolation test (no rails_helper)
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~350 tokens when loaded as context

# frozen_string_literal: true

require "spec_helper"
require_relative "../../app/services/orders/place_order_service"
require_relative "../../app/services/service_result"

RSpec.describe Orders::PlaceOrderService do
  let(:user) { instance_double("User", id: 1, orders: orders_relation) }
  let(:orders_relation) { instance_double("Orders") }
  let(:gateway) { instance_double("PaymentGateway") }
  let(:inventory) { instance_double("InventoryService") }
  let(:mailer) { class_double("OrderMailer") }

  subject(:service) { described_class.new(user, gateway: gateway, inventory: inventory, mailer: mailer) }

  it "returns success when all steps succeed" do
    # Arrange
    order = build_stubbed_order
    allow(orders_relation).to receive(:build).and_return(order)
    allow(order).to receive(:save).and_return(true)
    allow(inventory).to receive(:reserve).and_return(double(success?: true))
    allow(gateway).to receive(:charge).and_return(double(success?: true, id: "ch_1"))
    allow(order).to receive(:update!)
    allow(mailer).to receive_message_chain(:confirmation, :deliver_later)

    # Act
    result = service.call(items: [{ sku: "X", qty: 1 }])

    # Assert
    expect(result.success?).to be true
    expect(result.data).to eq(order)
  end

  it "returns failure when inventory insufficient" do
    order = build_stubbed_order
    allow(orders_relation).to receive(:build).and_return(order)
    allow(order).to receive(:save).and_return(true)
    allow(inventory).to receive(:reserve).and_return(double(success?: false))

    result = service.call(items: [])
    expect(result.failure?).to be true
    expect(result.error).to eq(:insufficient_stock)
  end

  def build_stubbed_order
    instance_double("Order", id: 1, items: [], total_cents: 1000)
  end
end
