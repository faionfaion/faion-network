# M-RB-003: Ruby Testing with RSpec

## Metadata
- **Category:** Development/Backend/Ruby
- **Difficulty:** Intermediate
- **Tags:** #dev, #ruby, #testing, #rspec, #methodology
- **Agent:** faion-test-agent

---

## Problem

Ruby testing can be slow and flaky without proper setup. Factory data gets messy, tests become coupled, and coverage gaps appear. You need patterns that make tests fast, reliable, and maintainable.

## Promise

After this methodology, you will write RSpec tests that are fast, readable, and catch real bugs. You will use factories, mocks, and best practices effectively.

## Overview

RSpec is the Ruby community standard for testing. Combined with FactoryBot, Faker, and proper configuration, it enables comprehensive test coverage.

---

## Framework

### Step 1: RSpec Setup

**Gemfile:**

```ruby
group :development, :test do
  gem 'rspec-rails', '~> 6.0'
  gem 'factory_bot_rails'
  gem 'faker'
end

group :test do
  gem 'shoulda-matchers'
  gem 'webmock'
  gem 'vcr'
  gem 'database_cleaner-active_record'
  gem 'simplecov', require: false
end
```

**Install:**

```bash
bundle install
rails generate rspec:install
```

### Step 2: RSpec Configuration

**spec/rails_helper.rb:**

```ruby
require 'spec_helper'
ENV['RAILS_ENV'] ||= 'test'
require_relative '../config/environment'

abort('Production!') if Rails.env.production?

require 'rspec/rails'

# Add support files
Dir[Rails.root.join('spec/support/**/*.rb')].each { |f| require f }

RSpec.configure do |config|
  config.fixture_path = Rails.root.join('spec/fixtures')
  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!
  config.filter_rails_from_backtrace!

  # FactoryBot
  config.include FactoryBot::Syntax::Methods

  # Database Cleaner
  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end

  config.around do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end
end

# Shoulda Matchers
Shoulda::Matchers.configure do |config|
  config.integrate do |with|
    with.test_framework :rspec
    with.library :rails
  end
end
```

**spec/spec_helper.rb:**

```ruby
require 'simplecov'
SimpleCov.start 'rails' do
  add_filter '/spec/'
  add_filter '/config/'
  minimum_coverage 80
end

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
  config.filter_run_when_matching :focus
  config.order = :random
  Kernel.srand config.seed
end
```

### Step 3: Factories

**spec/factories/users.rb:**

```ruby
FactoryBot.define do
  factory :user do
    email { Faker::Internet.unique.email }
    name { Faker::Name.name }
    password { 'password123' }

    trait :admin do
      role { :admin }
    end

    trait :with_orders do
      transient do
        orders_count { 3 }
      end

      after(:create) do |user, evaluator|
        create_list(:order, evaluator.orders_count, user: user)
      end
    end

    trait :inactive do
      status { :inactive }
      deactivated_at { 1.day.ago }
    end

    factory :admin_user, traits: [:admin]
    factory :user_with_orders, traits: [:with_orders]
  end
end
```

**Usage:**

```ruby
# Create in memory
user = build(:user)

# Create in database
user = create(:user)

# With trait
admin = create(:user, :admin)

# With attributes
user = create(:user, email: 'specific@email.com')

# With transient
user = create(:user, :with_orders, orders_count: 5)

# Collection
users = create_list(:user, 3)
```

### Step 4: Model Specs

**spec/models/user_spec.rb:**

```ruby
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'associations' do
    it { is_expected.to have_many(:orders).dependent(:destroy) }
    it { is_expected.to belong_to(:organization).optional }
  end

  describe 'validations' do
    subject { build(:user) }

    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:active_user) { create(:user, status: :active) }
      let!(:inactive_user) { create(:user, :inactive) }

      it 'returns only active users' do
        expect(User.active).to contain_exactly(active_user)
      end
    end
  end

  describe '#full_name' do
    let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

    it 'returns first and last name' do
      expect(user.full_name).to eq('John Doe')
    end
  end

  describe '#activate!' do
    let(:user) { create(:user, :inactive) }

    it 'changes status to active' do
      expect { user.activate! }.to change(user, :status).to('active')
    end

    it 'clears deactivated_at' do
      expect { user.activate! }.to change(user, :deactivated_at).to(nil)
    end
  end
end
```

### Step 5: Service Specs

**spec/services/users/create_service_spec.rb:**

```ruby
require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '.call' do
    subject(:result) { described_class.call(params: params) }

    context 'with valid params' do
      let(:params) do
        {
          email: 'new@example.com',
          password: 'password123',
          name: 'New User'
        }
      end

      it 'creates a user' do
        expect { result }.to change(User, :count).by(1)
      end

      it 'returns success' do
        expect(result).to be_success
      end

      it 'returns the user' do
        expect(result.data).to be_a(User)
        expect(result.data.email).to eq('new@example.com')
      end

      it 'enqueues welcome email job' do
        expect { result }.to have_enqueued_job(SendWelcomeEmailJob)
      end
    end

    context 'with duplicate email' do
      let!(:existing_user) { create(:user, email: 'existing@example.com') }
      let(:params) do
        {
          email: 'existing@example.com',
          password: 'password123',
          name: 'New User'
        }
      end

      it 'does not create a user' do
        expect { result }.not_to change(User, :count)
      end

      it 'returns failure' do
        expect(result).to be_failure
        expect(result.error).to include('Email already taken')
      end
    end

    context 'with invalid params' do
      let(:params) { { email: '' } }

      it 'returns failure' do
        expect(result).to be_failure
        expect(result.error).to include('Email required')
      end
    end
  end
end
```

### Step 6: Request Specs

**spec/requests/api/v1/users_spec.rb:**

```ruby
require 'rails_helper'

RSpec.describe 'Api::V1::Users', type: :request do
  let(:headers) { { 'Authorization' => "Bearer #{token}" } }
  let(:token) { create(:user).auth_token }

  describe 'GET /api/v1/users' do
    let!(:users) { create_list(:user, 3) }

    before { get '/api/v1/users', headers: headers }

    it 'returns success' do
      expect(response).to have_http_status(:ok)
    end

    it 'returns users' do
      expect(json_response['data'].size).to eq(3)
    end
  end

  describe 'POST /api/v1/users' do
    let(:valid_params) do
      {
        user: {
          email: 'new@example.com',
          password: 'password123',
          name: 'New User'
        }
      }
    end

    context 'with valid params' do
      it 'creates a user' do
        expect {
          post '/api/v1/users', params: valid_params, headers: headers
        }.to change(User, :count).by(1)
      end

      it 'returns created status' do
        post '/api/v1/users', params: valid_params, headers: headers
        expect(response).to have_http_status(:created)
      end
    end

    context 'with invalid params' do
      let(:invalid_params) { { user: { email: '' } } }

      it 'returns unprocessable entity' do
        post '/api/v1/users', params: invalid_params, headers: headers
        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end

  private

  def json_response
    JSON.parse(response.body)
  end
end
```

---

## Templates

### Shared Examples

```ruby
# spec/support/shared_examples/authenticatable.rb
RSpec.shared_examples 'authenticatable' do
  context 'without authentication' do
    let(:headers) { {} }

    it 'returns unauthorized' do
      subject
      expect(response).to have_http_status(:unauthorized)
    end
  end
end

# Usage
describe 'GET /api/v1/users' do
  subject { get '/api/v1/users', headers: headers }

  it_behaves_like 'authenticatable'
end
```

### Custom Matchers

```ruby
# spec/support/matchers/json_matchers.rb
RSpec::Matchers.define :have_json_key do |expected_key|
  match do |response|
    json = JSON.parse(response.body)
    json.key?(expected_key.to_s)
  end
end

# Usage
expect(response).to have_json_key(:data)
```

---

## Examples

### VCR for External APIs

```ruby
# spec/support/vcr.rb
VCR.configure do |config|
  config.cassette_library_dir = 'spec/cassettes'
  config.hook_into :webmock
  config.configure_rspec_metadata!
  config.filter_sensitive_data('<API_KEY>') { ENV['API_KEY'] }
end

# Usage
describe 'external API' do
  it 'fetches data', :vcr do
    result = ExternalApi.fetch_data
    expect(result).to be_present
  end
end
```

### Mocking Time

```ruby
describe 'time-dependent feature' do
  it 'expires after 24 hours' do
    token = create(:token)

    travel_to 25.hours.from_now do
      expect(token).to be_expired
    end
  end
end
```

---

## Common Mistakes

1. **Testing implementation** - Test behavior, not internals
2. **Shared database state** - Use database cleaner
3. **Slow factories** - Use build when possible
4. **Mystery guests** - Be explicit about test data
5. **Not using let/let!** - Use lazy evaluation

---

## Checklist

- [ ] RSpec configured with proper helpers
- [ ] Factories for all models
- [ ] SimpleCov for coverage
- [ ] Model specs with validations and scopes
- [ ] Service specs with all paths
- [ ] Request specs for API endpoints
- [ ] Shared examples for common behavior
- [ ] VCR/WebMock for external APIs

---

## Next Steps

- M-RB-004: Ruby Code Quality
- M-RB-002: Rails Patterns
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-RB-003 v1.0*
