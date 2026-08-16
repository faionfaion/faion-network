<!-- purpose: minimum viable Rails 7+ service / job / spec layout reference -->
<!-- consumes: feature spec -->
<!-- produces: directory layout conforming to one-serviceresult-class + service-call-returns-result rules -->
<!-- depends-on: content/01-core-rules.xml rules one-serviceresult-class, service-call-returns-result, sidekiq-jobs-take-ids -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# Smoke-test Rails 7+ layout

```
app/
├── services/
│   ├── service_result.rb               # single canonical class
│   └── users/
│       ├── create_service.rb           # Users::CreateService
│       └── disable_service.rb          # Users::DisableService
├── queries/                            # see ruby-activerecord
│   └── users/
│       └── active_users_query.rb
├── jobs/
│   └── users/
│       └── send_welcome_job.rb         # perform(user_id)
├── models/
│   └── user.rb                         # callbacks: after_create_commit -> WelcomeMailer
└── controllers/
    └── api/v1/users_controller.rb      # Strong Params -> Service

spec/
├── services/users/create_service_spec.rb
├── jobs/users/send_welcome_job_spec.rb
└── requests/api/v1/users_spec.rb
```

ServiceResult contract (`app/services/service_result.rb`):

```
ServiceResult = Struct.new(:success, :value, :errors) do
  def success? = success
  def failure? = !success
  def self.ok(value) = new(true, value, [])
  def self.fail(errors) = new(false, nil, Array(errors))
end
```
