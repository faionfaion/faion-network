# purpose: Sidekiq Background Jobs Ruby skeleton
# consumes: Prerequisites bundle (see AGENTS.md)
# produces: artefact conforming to content/02-output-contract.xml (code)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

# ProcessOrderJob — required: include Sidekiq::Job, sidekiq_options, idempotency, primitive args, retry backoff.

class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60         # linear backoff for transient payment issues
    else
      (count**4) + 15          # exponential backoff (15s, 31s, 96s)
    end
  end

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed?  # idempotency check at top of perform

    OrderProcessor.new(order).process!
    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    Sidekiq.logger.warn "Order \#{order_id} not found — skipping (no retry)"
  rescue PaymentGatewayError => e
    raise                       # retry with custom backoff
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise                       # always re-raise so Sidekiq schedules the retry
  end
end

