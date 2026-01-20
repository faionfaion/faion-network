---
id: M-DEV-023
name: "Ruby on Rails Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# M-DEV-023: Ruby on Rails Patterns

## Overview

Ruby on Rails is a full-stack web framework following convention over configuration. This methodology covers Rails architecture, best practices, and patterns for building maintainable applications.

## When to Use

- Full-stack web applications
- Rapid prototyping and MVPs
- CRUD-heavy applications
- API backends
- Applications with complex business logic

## Key Principles

1. **Convention over configuration** - Follow Rails conventions
2. **Don't Repeat Yourself (DRY)** - Extract common patterns
3. **Fat models, skinny controllers** - Business logic in models
4. **RESTful resources** - Standard CRUD operations
5. **Test-driven development** - Write tests first

## Best Practices

### Project Structure

```
app/
├── controllers/
│   ├── application_controller.rb
│   ├── concerns/
│   │   └── authenticatable.rb
│   └── api/
│       └── v1/
│           └── users_controller.rb
├── models/
│   ├── application_record.rb
│   ├── concerns/
│   │   ├── searchable.rb
│   │   └── auditable.rb
│   └── user.rb
├── services/
│   ├── users/
│   │   ├── creator.rb
│   │   └── updater.rb
│   └── base_service.rb
├── queries/
│   └── users_query.rb
├── serializers/
│   └── user_serializer.rb
├── jobs/
│   └── send_welcome_email_job.rb
├── mailers/
│   └── user_mailer.rb
└── views/
    └── layouts/
        └── application.html.erb
```

### Model Patterns

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Constants
  ROLES = %w[admin moderator member].freeze

  # Associations
  belongs_to :organization
  has_many :posts, dependent: :destroy
  has_many :comments, dependent: :destroy
  has_one :profile, dependent: :destroy

  # Validations
  validates :email, presence: true,
                    uniqueness: { case_sensitive: false },
                    format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true, length: { minimum: 2, maximum: 100 }
  validates :role, inclusion: { in: ROLES }

  # Scopes
  scope :active, -> { where(active: true) }
  scope :admins, -> { where(role: 'admin') }
  scope :created_after, ->(date) { where('created_at > ?', date) }
  scope :search, ->(query) {
    where('name ILIKE ? OR email ILIKE ?', "%#{query}%", "%#{query}%")
  }

  # Callbacks
  before_validation :normalize_email
  after_create :send_welcome_email
  after_update :notify_profile_change, if: :saved_change_to_email?

  # Class methods
  def self.find_by_credentials(email, password)
    user = find_by(email: email.downcase)
    user&.authenticate(password) ? user : nil
  end

  # Instance methods
  def admin?
    role == 'admin'
  end

  def full_name
    "#{first_name} #{last_name}".strip
  end

  private

  def normalize_email
    self.email = email&.downcase&.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end

  def notify_profile_change
    NotificationService.new(self).profile_updated
  end
end

# app/models/concerns/searchable.rb
module Searchable
  extend ActiveSupport::Concern

  included do
    scope :search, ->(query) {
      return all if query.blank?

      where(search_condition(query))
    }
  end

  class_methods do
    def searchable_columns(*columns)
      @searchable_columns = columns
    end

    def search_condition(query)
      columns = @searchable_columns || [:name]
      conditions = columns.map { |col| "#{col} ILIKE ?" }
      values = columns.map { "%#{query}%" }

      [conditions.join(' OR '), *values]
    end
  end
end
```

### Service Objects

```ruby
# app/services/base_service.rb
class BaseService
  def self.call(...)
    new(...).call
  end

  private

  def success(data = nil)
    ServiceResult.new(success: true, data: data)
  end

  def failure(errors)
    ServiceResult.new(success: false, errors: Array(errors))
  end
end

class ServiceResult
  attr_reader :data, :errors

  def initialize(success:, data: nil, errors: [])
    @success = success
    @data = data
    @errors = errors
  end

  def success?
    @success
  end

  def failure?
    !@success
  end
end

# app/services/users/creator.rb
module Users
  class Creator < BaseService
    def initialize(params:, organization:)
      @params = params
      @organization = organization
    end

    def call
      user = @organization.users.build(@params)

      if user.save
        send_notifications(user)
        success(user)
      else
        failure(user.errors.full_messages)
      end
    end

    private

    def send_notifications(user)
      UserMailer.welcome(user).deliver_later
      SlackNotifier.new_user(user).deliver_later
    end
  end
end

# Usage in controller
class UsersController < ApplicationController
  def create
    result = Users::Creator.call(
      params: user_params,
      organization: current_organization
    )

    if result.success?
      render json: result.data, status: :created
    else
      render json: { errors: result.errors }, status: :unprocessable_entity
    end
  end
end
```

### Query Objects

```ruby
# app/queries/users_query.rb
class UsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def call(params = {})
    result = @relation

    result = filter_by_role(result, params[:role])
    result = filter_by_status(result, params[:status])
    result = filter_by_date_range(result, params[:from], params[:to])
    result = search(result, params[:q])
    result = sort(result, params[:sort], params[:direction])

    result
  end

  private

  def filter_by_role(relation, role)
    return relation if role.blank?

    relation.where(role: role)
  end

  def filter_by_status(relation, status)
    return relation if status.blank?

    case status
    when 'active' then relation.active
    when 'inactive' then relation.inactive
    else relation
    end
  end

  def filter_by_date_range(relation, from, to)
    relation = relation.where('created_at >= ?', from) if from.present?
    relation = relation.where('created_at <= ?', to) if to.present?
    relation
  end

  def search(relation, query)
    return relation if query.blank?

    relation.search(query)
  end

  def sort(relation, column, direction)
    return relation.order(created_at: :desc) if column.blank?

    allowed_columns = %w[name email created_at]
    return relation unless allowed_columns.include?(column)

    direction = %w[asc desc].include?(direction) ? direction : 'asc'
    relation.order(column => direction)
  end
end

# Usage
users = UsersQuery.new(current_organization.users).call(
  role: params[:role],
  status: params[:status],
  q: params[:q],
  sort: params[:sort],
  direction: params[:direction]
)
```

### Controller Patterns

```ruby
# app/controllers/api/v1/users_controller.rb
module Api
  module V1
    class UsersController < ApplicationController
      before_action :authenticate_user!
      before_action :set_user, only: [:show, :update, :destroy]
      before_action :authorize_user, only: [:update, :destroy]

      def index
        users = UsersQuery.new(current_organization.users)
                         .call(filter_params)
                         .page(params[:page])
                         .per(params[:per_page] || 20)

        render json: {
          data: UserSerializer.new(users).serializable_hash,
          meta: pagination_meta(users)
        }
      end

      def show
        render json: UserSerializer.new(@user).serializable_hash
      end

      def create
        result = Users::Creator.call(
          params: user_params,
          organization: current_organization
        )

        if result.success?
          render json: UserSerializer.new(result.data).serializable_hash,
                 status: :created
        else
          render json: { errors: result.errors },
                 status: :unprocessable_entity
        end
      end

      def update
        result = Users::Updater.call(user: @user, params: user_params)

        if result.success?
          render json: UserSerializer.new(result.data).serializable_hash
        else
          render json: { errors: result.errors },
                 status: :unprocessable_entity
        end
      end

      def destroy
        @user.destroy
        head :no_content
      end

      private

      def set_user
        @user = current_organization.users.find(params[:id])
      end

      def authorize_user
        head :forbidden unless current_user.admin? || current_user == @user
      end

      def user_params
        params.require(:user).permit(:email, :name, :role)
      end

      def filter_params
        params.permit(:role, :status, :q, :sort, :direction, :from, :to)
      end

      def pagination_meta(collection)
        {
          current_page: collection.current_page,
          total_pages: collection.total_pages,
          total_count: collection.total_count
        }
      end
    end
  end
end
```

### Testing with RSpec

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    subject { build(:user) }

    it { should validate_presence_of(:email) }
    it { should validate_uniqueness_of(:email).case_insensitive }
    it { should validate_presence_of(:name) }
    it { should validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  describe 'associations' do
    it { should belong_to(:organization) }
    it { should have_many(:posts).dependent(:destroy) }
    it { should have_one(:profile).dependent(:destroy) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:active_user) { create(:user, active: true) }
      let!(:inactive_user) { create(:user, active: false) }

      it 'returns only active users' do
        expect(User.active).to include(active_user)
        expect(User.active).not_to include(inactive_user)
      end
    end
  end

  describe '#admin?' do
    it 'returns true for admin role' do
      user = build(:user, role: 'admin')
      expect(user.admin?).to be true
    end

    it 'returns false for non-admin role' do
      user = build(:user, role: 'member')
      expect(user.admin?).to be false
    end
  end
end

# spec/services/users/creator_spec.rb
require 'rails_helper'

RSpec.describe Users::Creator do
  describe '.call' do
    let(:organization) { create(:organization) }
    let(:valid_params) do
      {
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      }
    end

    context 'with valid params' do
      it 'creates a user' do
        expect {
          described_class.call(params: valid_params, organization: organization)
        }.to change(User, :count).by(1)
      end

      it 'returns success result' do
        result = described_class.call(params: valid_params, organization: organization)
        expect(result).to be_success
        expect(result.data).to be_a(User)
      end

      it 'sends welcome email' do
        expect {
          described_class.call(params: valid_params, organization: organization)
        }.to have_enqueued_mail(UserMailer, :welcome)
      end
    end

    context 'with invalid params' do
      let(:invalid_params) { { email: 'invalid' } }

      it 'returns failure result' do
        result = described_class.call(params: invalid_params, organization: organization)
        expect(result).to be_failure
        expect(result.errors).to be_present
      end
    end
  end
end
```

## Anti-patterns

### Avoid: Fat Controllers

```ruby
# BAD - business logic in controller
def create
  @user = User.new(user_params)
  @user.role = 'member'
  @user.organization = current_organization

  if @user.save
    UserMailer.welcome(@user).deliver_later
    SlackNotifier.new_user(@user)
    Analytics.track('user_created', user_id: @user.id)
    render json: @user
  end
end

# GOOD - delegate to service
def create
  result = Users::Creator.call(params: user_params, organization: current_organization)

  if result.success?
    render json: result.data
  else
    render json: { errors: result.errors }, status: :unprocessable_entity
  end
end
```

### Avoid: N+1 Queries

```ruby
# BAD - N+1 queries
def index
  @users = User.all
  # In view: user.posts.count for each user
end

# GOOD - eager loading
def index
  @users = User.includes(:posts).all
  # Or with counter cache
  @users = User.all # posts_count column on users table
end
```

## References

- [Rails Guides](https://guides.rubyonrails.org/)
- [Ruby Style Guide](https://rubystyle.guide/)
- [Rails Best Practices](https://rails-bestpractices.com/)
- [RSpec Documentation](https://rspec.info/documentation/)
