# purpose: RSpec configuration enabling Bullet N+1 detection during test runs
# consumes: spec/rails_helper.rb RSpec.configure block
# produces: pass/fail gate per ci-gates-bullet-brakeman-audit rule
# depends-on: content/01-core-rules.xml rule ci-gates-bullet-brakeman-audit
# token-budget-impact: ~250 tokens when loaded as context
# RSpec configuration enabling Bullet N+1 detection in test mode.
# Add to spec/rails_helper.rb (inside RSpec.configure block).
#
# Bullet must be in Gemfile:
#   group :development, :test do
#     gem 'bullet'
#   end

# In config/environments/test.rb:
#   config.after_initialize do
#     Bullet.enable        = true
#     Bullet.bullet_logger = true
#     Bullet.raise         = true  # fail tests on N+1
#   end

RSpec.configure do |config|
  if Bullet.enable?
    config.before(:each) do
      Bullet.start_request
    end

    config.after(:each) do
      Bullet.perform_out_of_channel_notifications if Bullet.notification?
      Bullet.end_request
    end
  end
end
