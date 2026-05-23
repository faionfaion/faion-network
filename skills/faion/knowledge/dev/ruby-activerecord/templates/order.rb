# purpose: ActiveRecord model with enum, scopes, includes-friendly associations
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~400 tokens when loaded as context

class Order < ApplicationRecord
  belongs_to :customer
  has_many :items, class_name: "OrderItem", dependent: :destroy

  enum status: { pending: 0, paid: 1, shipped: 2, cancelled: 3 }, _prefix: true

  validates :status, presence: true
  validates :total_cents, numericality: { greater_than_or_equal_to: 0 }

  scope :recent, -> { where("created_at >= ?", 30.days.ago) }
  scope :for_user, ->(user) { where(customer_id: user.customer_id) }
  scope :priced, -> { where("total_cents > 0") }

  def total
    Money.new(total_cents, currency)
  end

  def cancel!
    transaction do
      update!(status: :cancelled, cancelled_at: Time.current)
      items.each(&:release_inventory!)
    end
  end
end
