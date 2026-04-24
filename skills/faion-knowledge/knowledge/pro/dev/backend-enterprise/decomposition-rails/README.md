# Ruby on Rails Decomposition Patterns

LLM-friendly code organization for Ruby on Rails projects.

---

## Anti-Pattern: Fat Controllers & Models

```ruby
# BAD: app/models/user.rb (500+ lines)
class User < ApplicationRecord
  # 20 associations
  # 30 validations
  # 50 methods mixing concerns
  # Callbacks doing business logic
end

# BAD: app/controllers/users_controller.rb (400+ lines)
class UsersController < ApplicationController
  # All actions with inline logic
  # Permission checks scattered
  # Email sending in controller
end
```

---

## LLM-Friendly Structure

```
app/
├── models/
│   ├── user.rb                    # User model (50-80 lines)
│   ├── profile.rb                 # Profile model (40-60 lines)
│   └── concerns/
│       ├── authenticatable.rb     # Auth concern (30-50 lines)
│       └── searchable.rb          # Search concern (20-40 lines)
├── services/
│   ├── users/
│   │   ├── create_service.rb      # Create user (40-60 lines)
│   │   ├── update_service.rb      # Update user (40-60 lines)
│   │   └── delete_service.rb      # Delete user (30-40 lines)
│   └── auth/
│       ├── login_service.rb       # Login logic (50-70 lines)
│       └── register_service.rb    # Registration (50-70 lines)
├── queries/
│   └── users/
│       ├── active_query.rb        # Active users (20-30 lines)
│       └── search_query.rb        # Search users (30-50 lines)
├── controllers/
│   ├── api/
│   │   └── v1/
│   │       ├── users_controller.rb    # User API (60-80 lines)
│   │       └── auth_controller.rb     # Auth API (50-70 lines)
│   └── concerns/
│       └── error_handling.rb      # Error handling (40-60 lines)
├── serializers/
│   ├── user_serializer.rb         # User JSON (30-50 lines)
│   └── profile_serializer.rb      # Profile JSON (20-30 lines)
├── policies/
│   └── user_policy.rb             # User permissions (40-60 lines)
└── jobs/
    └── users/
        ├── welcome_email_job.rb   # Welcome email (20-30 lines)
        └── cleanup_job.rb         # Cleanup (30-40 lines)
```

---

## Service Object Pattern

```ruby
# app/services/users/create_service.rb (~50 lines)
module Users
  class CreateService
    def initialize(params:, current_user: nil)
      @params = params
      @current_user = current_user
    end

    def call
      validate!
      create_user
      send_welcome_email
      @user
    end

    private

    attr_reader :params, :current_user

    def validate!
      raise ValidationError, "Email required" if params[:email].blank?
      raise ValidationError, "Email taken" if User.exists?(email: params[:email])
    end

    def create_user
      @user = User.create!(
        email: params[:email],
        name: params[:name],
        password: params[:password]
      )
    end

    def send_welcome_email
      Users::WelcomeEmailJob.perform_later(@user.id)
    end
  end
end
```

---

## Query Object Pattern

```ruby
# app/queries/users/search_query.rb (~40 lines)
module Users
  class SearchQuery
    def initialize(relation = User.all)
      @relation = relation
    end

    def call(params)
      @relation = filter_by_status(params[:status])
      @relation = filter_by_query(params[:query])
      @relation = order_by(params[:sort])
      @relation
    end

    private

    def filter_by_status(status)
      return @relation if status.blank?
      @relation.where(status: status)
    end

    def filter_by_query(query)
      return @relation if query.blank?
      @relation.where("name ILIKE ? OR email ILIKE ?", "%#{query}%", "%#{query}%")
    end

    def order_by(sort)
      case sort
      when "name" then @relation.order(:name)
      when "recent" then @relation.order(created_at: :desc)
      else @relation.order(:id)
      end
    end
  end
end
```

---

## Controller Pattern

```ruby
# app/controllers/api/v1/users_controller.rb (~70 lines)
module Api
  module V1
    class UsersController < ApplicationController
      before_action :authenticate_user!
      before_action :set_user, only: [:show, :update, :destroy]

      def index
        users = Users::SearchQuery.new.call(search_params)
        render json: UserSerializer.new(users).serializable_hash
      end

      def show
        authorize @user
        render json: UserSerializer.new(@user).serializable_hash
      end

      def create
        user = Users::CreateService.new(params: user_params).call
        render json: UserSerializer.new(user).serializable_hash, status: :created
      end

      def update
        authorize @user
        user = Users::UpdateService.new(user: @user, params: user_params).call
        render json: UserSerializer.new(user).serializable_hash
      end

      private

      def set_user
        @user = User.find(params[:id])
      end

      def user_params
        params.require(:user).permit(:name, :email, :avatar)
      end

      def search_params
        params.permit(:query, :status, :sort)
      end
    end
  end
end
```

---

## Key Principles

1. **Service Objects** - Business logic in dedicated classes
2. **Query Objects** - Complex queries extracted
3. **Thin Controllers** - Only HTTP handling
4. **Thin Models** - Only ActiveRecord logic
5. **Concerns** - Shared behavior

---

## File Size Guidelines

| Type | Target | Max |
|------|--------|-----|
| Model | 50-80 | 150 |
| Service | 40-60 | 100 |
| Query | 30-50 | 80 |
| Controller | 60-80 | 150 |
| Serializer | 30-50 | 100 |
| Test | 100-150 | 300 |

---

## Related

- [framework-decomposition-patterns.md](framework-decomposition-patterns.md) - All frameworks
- [decomposition-django.md](decomposition-django.md) - Django patterns
- [decomposition-react.md](decomposition-react.md) - React patterns
- [decomposition-laravel.md](decomposition-laravel.md) - Laravel patterns
- [ruby-rails.md](ruby-rails.md) - Rails reference
- [ruby-rails-patterns.md](ruby-rails-patterns.md) - Rails patterns
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM optimization
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement decomposition-rails pattern | haiku | Straightforward implementation |
| Review decomposition-rails implementation | sonnet | Requires code analysis |
| Optimize decomposition-rails design | opus | Complex trade-offs |

