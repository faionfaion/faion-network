# M-RB-002: Ruby on Rails Patterns

## Metadata
- **Category:** Development/Backend/Ruby
- **Difficulty:** Intermediate
- **Tags:** #dev, #ruby, #rails, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

Rails applications become messy when all logic lives in controllers and models. Fat models and god objects make testing and maintenance difficult. You need patterns that keep code organized as applications grow.

## Promise

After this methodology, you will structure Rails applications with clear separation of concerns. Your code will be testable, maintainable, and follow Rails best practices.

## Overview

Modern Rails uses service objects, form objects, query objects, and decorators to keep code organized. This methodology covers patterns that scale from small to large applications.

---

## Framework

### Step 1: Application Structure

```
app/
├── controllers/
│   └── api/
│       └── v1/
│           └── users_controller.rb
├── models/
│   └── user.rb
├── services/              # Business logic
│   └── users/
│       ├── create_service.rb
│       └── update_service.rb
├── queries/               # Complex queries
│   └── users/
│       └── search_query.rb
├── forms/                 # Form objects
│   └── user_registration_form.rb
├── policies/              # Authorization
│   └── user_policy.rb
├── serializers/           # JSON output
│   └── user_serializer.rb
├── jobs/                  # Background jobs
│   └── send_welcome_email_job.rb
├── validators/            # Custom validators
│   └── email_validator.rb
└── mailers/
    └── user_mailer.rb
```

### Step 2: Service Objects

**app/services/base_service.rb:**

```ruby
class BaseService
  def self.call(...)
    new(...).call
  end

  private

  def success(data = nil)
    Result.new(success: true, data: data)
  end

  def failure(error)
    Result.new(success: false, error: error)
  end

  Result = Struct.new(:success, :data, :error, keyword_init: true) do
    def success?
      success
    end

    def failure?
      !success
    end
  end
end
```

**app/services/users/create_service.rb:**

```ruby
module Users
  class CreateService < BaseService
    def initialize(params:, created_by: nil)
      @params = params
      @created_by = created_by
    end

    def call
      validate_params!
      check_email_uniqueness!

      user = User.new(@params)
      user.created_by = @created_by

      if user.save
        SendWelcomeEmailJob.perform_later(user.id)
        success(user)
      else
        failure(user.errors.full_messages)
      end
    rescue ValidationError => e
      failure(e.message)
    end

    private

    def validate_params!
      raise ValidationError, 'Email required' if @params[:email].blank?
      raise ValidationError, 'Password required' if @params[:password].blank?
    end

    def check_email_uniqueness!
      if User.exists?(email: @params[:email])
        raise ValidationError, 'Email already taken'
      end
    end
  end
end
```

**Usage in controller:**

```ruby
class Api::V1::UsersController < ApplicationController
  def create
    result = Users::CreateService.call(
      params: user_params,
      created_by: current_user
    )

    if result.success?
      render json: UserSerializer.new(result.data), status: :created
    else
      render json: { error: result.error }, status: :unprocessable_entity
    end
  end

  private

  def user_params
    params.require(:user).permit(:email, :password, :name)
  end
end
```

### Step 3: Query Objects

**app/queries/base_query.rb:**

```ruby
class BaseQuery
  def initialize(relation = default_relation)
    @relation = relation
  end

  def self.call(...)
    new(...).call
  end

  private

  def default_relation
    raise NotImplementedError
  end
end
```

**app/queries/users/search_query.rb:**

```ruby
module Users
  class SearchQuery < BaseQuery
    def initialize(relation = User.all, params: {})
      super(relation)
      @params = params
    end

    def call
      @relation
        .then { |r| filter_by_name(r) }
        .then { |r| filter_by_email(r) }
        .then { |r| filter_by_status(r) }
        .then { |r| filter_by_date_range(r) }
        .then { |r| order_by(r) }
    end

    private

    def filter_by_name(relation)
      return relation if @params[:name].blank?

      relation.where('name ILIKE ?', "%#{@params[:name]}%")
    end

    def filter_by_email(relation)
      return relation if @params[:email].blank?

      relation.where('email ILIKE ?', "%#{@params[:email]}%")
    end

    def filter_by_status(relation)
      return relation if @params[:status].blank?

      relation.where(status: @params[:status])
    end

    def filter_by_date_range(relation)
      return relation if @params[:from].blank? && @params[:to].blank?

      relation = relation.where('created_at >= ?', @params[:from]) if @params[:from]
      relation = relation.where('created_at <= ?', @params[:to]) if @params[:to]
      relation
    end

    def order_by(relation)
      column = @params[:sort_by] || 'created_at'
      direction = @params[:sort_dir] || 'desc'

      relation.order(column => direction)
    end
  end
end
```

### Step 4: Form Objects

**app/forms/user_registration_form.rb:**

```ruby
class UserRegistrationForm
  include ActiveModel::Model
  include ActiveModel::Validations

  attr_accessor :email, :password, :password_confirmation,
                :name, :terms_accepted

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :name, presence: true, length: { minimum: 2, maximum: 100 }
  validates :terms_accepted, acceptance: true

  validate :passwords_match
  validate :email_unique

  def save
    return false unless valid?

    user = User.new(
      email: email,
      password: password,
      name: name
    )

    user.save
  end

  def user
    @user ||= User.new
  end

  private

  def passwords_match
    return if password == password_confirmation

    errors.add(:password_confirmation, "doesn't match password")
  end

  def email_unique
    return unless User.exists?(email: email)

    errors.add(:email, 'is already taken')
  end
end
```

### Step 5: Serializers (Blueprinter)

```bash
# Add to Gemfile
gem 'blueprinter'
```

**app/serializers/user_serializer.rb:**

```ruby
class UserSerializer < Blueprinter::Base
  identifier :id

  fields :email, :name, :created_at

  field :full_name do |user|
    "#{user.first_name} #{user.last_name}"
  end

  view :detailed do
    fields :phone, :address, :updated_at

    association :orders, blueprint: OrderSerializer
  end

  view :admin do
    include_view :detailed
    fields :admin_notes, :internal_id
  end
end

# Usage
UserSerializer.render(user)                    # Default view
UserSerializer.render(user, view: :detailed)   # Detailed view
UserSerializer.render(users, view: :admin)     # Collection
```

### Step 6: Concerns for Shared Behavior

**app/models/concerns/searchable.rb:**

```ruby
module Searchable
  extend ActiveSupport::Concern

  included do
    scope :search, ->(query) {
      return all if query.blank?

      where("#{searchable_columns.map { |c| "#{c} ILIKE ?" }.join(' OR ')}",
            *searchable_columns.map { "%#{query}%" })
    }
  end

  class_methods do
    def searchable_columns
      @searchable_columns ||= []
    end

    def searchable(*columns)
      @searchable_columns = columns.map(&:to_s)
    end
  end
end

# Usage in model
class User < ApplicationRecord
  include Searchable

  searchable :name, :email
end

# In controller
User.search(params[:q])
```

---

## Templates

### Controller Template

```ruby
module Api
  module V1
    class UsersController < ApplicationController
      before_action :authenticate!
      before_action :set_user, only: [:show, :update, :destroy]

      def index
        users = Users::SearchQuery.call(params: search_params)
        users = users.page(params[:page]).per(params[:per_page])

        render json: UserSerializer.render(users, view: :list)
      end

      def show
        render json: UserSerializer.render(@user, view: :detailed)
      end

      def create
        result = Users::CreateService.call(params: user_params)

        if result.success?
          render json: UserSerializer.render(result.data), status: :created
        else
          render_error(result.error, :unprocessable_entity)
        end
      end

      def update
        result = Users::UpdateService.call(user: @user, params: user_params)

        if result.success?
          render json: UserSerializer.render(result.data)
        else
          render_error(result.error, :unprocessable_entity)
        end
      end

      def destroy
        @user.destroy
        head :no_content
      end

      private

      def set_user
        @user = User.find(params[:id])
      end

      def user_params
        params.require(:user).permit(:email, :name, :password)
      end

      def search_params
        params.permit(:q, :status, :sort_by, :sort_dir)
      end

      def render_error(error, status)
        render json: { error: error }, status: status
      end
    end
  end
end
```

---

## Examples

### Interactor Pattern

```bash
gem 'interactor'
```

```ruby
class CreateOrder
  include Interactor::Organizer

  organize ValidateOrder, ChargePayment, CreateOrderRecord, SendConfirmation
end

class ValidateOrder
  include Interactor

  def call
    order = context.order_params

    unless order[:items].present?
      context.fail!(error: 'Order must have items')
    end
  end
end

class ChargePayment
  include Interactor

  def call
    result = PaymentGateway.charge(
      amount: context.total,
      token: context.payment_token
    )

    if result.success?
      context.payment_id = result.id
    else
      context.fail!(error: result.error)
    end
  end

  def rollback
    PaymentGateway.refund(context.payment_id)
  end
end

# Usage
result = CreateOrder.call(order_params: params, payment_token: token)

if result.success?
  render json: result.order
else
  render json: { error: result.error }, status: :unprocessable_entity
end
```

---

## Common Mistakes

1. **Fat controllers** - Move logic to services
2. **Fat models** - Use concerns and service objects
3. **N+1 queries** - Use includes/eager_load
4. **Callbacks for business logic** - Use service objects
5. **String SQL** - Use Arel or query objects

---

## Checklist

- [ ] Controllers are thin (< 100 lines)
- [ ] Business logic in service objects
- [ ] Complex queries in query objects
- [ ] Forms for multi-model operations
- [ ] Serializers for JSON output
- [ ] Concerns for shared model behavior
- [ ] Background jobs for async work

---

## Next Steps

- M-RB-003: Ruby Testing with RSpec
- M-RB-004: Ruby Code Quality
- M-API-001: REST API Design

---

*Methodology M-RB-002 v1.0*
