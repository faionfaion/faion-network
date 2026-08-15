# purpose: Service object skeleton with #call + ServiceResult + transaction
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~450 tokens when loaded as context

module Orders
  class PlaceOrderService
    def initialize(user, gateway: PaymentGateway.instance, inventory: InventoryService.new, mailer: OrderMailer)
      @user = user
      @gateway = gateway
      @inventory = inventory
      @mailer = mailer
    end

    def call(params)
      ActiveRecord::Base.transaction do
        order = build_order(params)
        return ServiceResult.failure(error: :invalid_params, details: order.errors) unless order.save

        stock = @inventory.reserve(order.items)
        return ServiceResult.failure(error: :insufficient_stock) unless stock.success?

        charge = @gateway.charge(amount: order.total_cents, customer: @user)
        return ServiceResult.failure(error: :payment_declined) unless charge.success?

        order.update!(charge_id: charge.id, status: :paid)
        @mailer.confirmation(order).deliver_later

        ServiceResult.success(data: order)
      end
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(error: :validation_error, details: e.record.errors.full_messages)
    end

    private

    def build_order(params)
      @user.orders.build(params).tap do |order|
        order.status = :pending
        order.placed_at = Time.current
      end
    end
  end
end
