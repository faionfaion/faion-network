# app/jobs/process_order_job.rb
# Required: include Sidekiq::Job, sidekiq_options, idempotency, primitive args, retry backoff.

class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60 # Linear backoff for payment issues
    else
      (count**4) + 15  # Exponential backoff (15s, 31s, 96s)
    end
  end

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed? # idempotency check

    OrderProcessor.new(order).process!
    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    # Order was deleted — nothing to do; do NOT re-raise (no retry needed).
    Sidekiq.logger.warn "Order #{order_id} not found — skipping"
  rescue PaymentGatewayError => e
    raise # retry with custom backoff
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise # always re-raise so Sidekiq schedules the retry
  end
end
