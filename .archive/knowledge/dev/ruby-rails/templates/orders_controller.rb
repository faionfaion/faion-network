# purpose: RESTful controller with Strong Parameters + Pundit authorization
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~350 tokens when loaded as context

class Api::V1::OrdersController < Api::V1::BaseController
  before_action :set_order, only: %i[show update destroy cancel refund]

  def index
    @orders = policy_scope(Order).includes(:items).recent
    render json: OrderResource.from_collection(@orders)
  end

  def show
    authorize @order
    render json: OrderResource.from(@order)
  end

  def create
    @order = OrderService.new(current_user).create(order_params)
    render json: OrderResource.from(@order), status: :created
  end

  def update
    authorize @order
    OrderService.new(current_user).update(@order, order_params)
    render json: OrderResource.from(@order)
  end

  def cancel
    authorize @order, :cancel?
    OrderService.new(current_user).cancel(@order)
    head :no_content
  end

  private

  def set_order
    @order = Order.find(params[:id])
  end

  def order_params
    params.require(:order).permit(:note, items_attributes: %i[sku qty])
  end
end
