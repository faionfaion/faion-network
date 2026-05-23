# purpose: Legacy template for the ruby-sidekiq-jobs methodology.
# consumes: inputs declared in ruby-sidekiq-jobs/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
# Sidekiq job skeleton — idempotent, ID-only args, explicit retry/dead, custom backoff
# Replace: ProcessOrderJob, Order, OrderProcessor, NotifyCustomerJob, PaymentGatewayError

class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60     # linear: 60s, 120s, 180s (rate-limit friendly)
    else
      (count ** 4) + 15    # exponential: 16s, 31s, 96s
    end
  end

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed?            # idempotency guard

    OrderProcessor.new(order).process!
    NotifyCustomerJob.perform_async(order_id)

  rescue ActiveRecord::RecordNotFound
    Sidekiq.logger.warn "Order #{order_id} not found — skipping"
  rescue PaymentGatewayError
    raise   # let Sidekiq retry with linear backoff
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise   # re-raise to trigger retry and dead-set on exhaustion
  end
end
