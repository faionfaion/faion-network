# Agent Integration — Rails Patterns

## When to use
- Building Rails 7+ apps where controllers grow past 100 lines and need extraction into Service Objects, Form Objects, Query Objects, Decorators.
- Wrapping multi-step business workflows (signup, checkout, refund) that span multiple models in a transaction.
- Replacing fat models when ActiveRecord callbacks have become unmaintainable side-effect chains.
- Standardizing controller responses around a `ServiceResult` (success/failure) so JSON shapes stay consistent across endpoints.

## When NOT to use
- Tiny CRUD controllers where a `before_action` and `model.save` already do the job — service objects add overhead.
- Pure data-access logic; that belongs in Query Objects or scopes, not in services.
- One-off rake tasks or scripts — keep them as plain Ruby objects without the service/result wrapper.

## Where it fails / limitations
- "Service object" is not a Rails-blessed pattern, so naming/folder conventions vary across teams (`app/services` vs `app/use_cases` vs `app/operations`).
- Transactions inside services hide rollback behavior — a callback raising `ActiveRecord::Rollback` silently swallows the failure unless you re-raise.
- `ServiceResult` proliferation creates two error paths (exception + failure result), and devs forget which is canonical.
- Heavy nesting (`Users::Onboarding::CreateService`) makes autoloading slow and stack traces noisy.

## Agentic workflow
Treat a Rails service as a unit of work with a single public `call` method. A subagent should generate the service, the matching `ServiceResult`/Dry-Monads return type, the controller wiring, and an RSpec request+service spec in one pass. For larger refactors (extracting from a fat controller), use a planner subagent to map controller actions to services first, then a code subagent per service. Always require the diff include the spec file alongside the service.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → service → controller wiring with quality gates (matches existing `agents/faion-sdd-executor-agent.md`).
- A scoped `rails-refactor` subagent (project-local) — extract logic from controllers into `app/services/<bounded_context>/<action>_service.rb`, returning a paired RSpec.

### Prompt pattern
```
Extract the create flow in app/controllers/api/v1/users_controller.rb into
Users::CreateService. Wrap multi-record writes in ActiveRecord::Base.transaction.
Return ServiceResult. Add spec/services/users/create_service_spec.rb covering
success, validation failure, and DB rollback. Do NOT touch UserMailer.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rails g` | Scaffolds models/controllers but not services — use a custom generator | https://guides.rubyonrails.org/command_line.html |
| `rubocop-rails` | Enforce Rails idioms; add custom cop to ban service files >150 lines | `gem install rubocop-rails` |
| `bundle exec rspec` | Run service specs in isolation: `rspec spec/services` | https://rspec.info |
| `interactor` gem | Pre-built service object base with `call`/`organizer` | https://github.com/collectiveidea/interactor |
| `dry-monads` | `Result(Success/Failure)` monads — alternative to custom `ServiceResult` | https://dry-rb.org/gems/dry-monads |
| `trailblazer-operation` | Heavyweight service framework with policy/contract steps | https://trailblazer.to |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hotwire / Turbo | OSS (in Rails 7+) | Yes | Service objects pair naturally with `turbo_stream` responses |
| Sidekiq | OSS | Yes | Wrap async work in a service that the worker calls; worker stays a thin enqueue layer |
| Datadog APM (Ruby) | SaaS | Yes | Auto-traces method calls; instrument service `call` to get span per workflow |
| Honeybadger / Sentry | SaaS | Yes | Capture failures in `ServiceResult.failure` paths via a single notifier wrapper |

## Templates & scripts
See `templates.md` for `ServiceResult` shape and the controller-renders-result idiom. Inline RSpec skeleton:

```ruby
# spec/services/users/create_service_spec.rb
require "rails_helper"

RSpec.describe Users::CreateService do
  subject(:result) { described_class.new(params: params, current_user: nil).call }

  context "with valid params" do
    let(:params) { { name: "X", email: "x@y.io", password: "secret123" } }
    it { is_expected.to be_success }
    it "creates user" do
      expect { result }.to change(User, :count).by(1)
    end
    it "enqueues welcome mail" do
      expect { result }.to have_enqueued_mail(UserMailer, :welcome)
    end
  end

  context "when email taken" do
    before { create(:user, email: "x@y.io") }
    let(:params) { { name: "X", email: "x@y.io", password: "secret123" } }
    it { is_expected.to be_failure }
    it "rolls back inserts" do
      expect { result }.not_to change(AuditLog, :count)
    end
  end
end
```

## Best practices
- One public method (`call`) per service — if you need a second, extract a new service.
- Use keyword args (`initialize(params:, current_user:)`) for explicitness; positional args become hard to mock.
- Keep services free of HTTP/Rails concerns; the controller maps `result` → status code.
- Namespace by bounded context (`Users::`, `Billing::`), not by HTTP verb.
- For multi-step workflows, prefer composing small services via an Organizer rather than one 400-line service.
- Lock `ActiveRecord::Base.transaction` blocks to a single aggregate to avoid distributed-transaction bugs.

## AI-agent gotchas
- Agents often forget to wrap mailer/job calls in `deliver_later` / `perform_later`, causing service specs to send real emails or run jobs inline. Pin this in the prompt.
- Generated services frequently leak `params.require(...)` from the controller into the service. Reject diffs where the service references `params` directly — it should accept already-permitted hashes.
- LLMs write ambiguous return types (`return user` vs `return ServiceResult.success(user)`). Define and enforce a single return contract in the prompt.
- Human-in-loop checkpoint: review namespace/folder choice (`app/services/users/` vs `app/operations/users/`) before generation — renaming after the fact is painful due to constant autoload paths.
- Verify the agent didn't introduce `rescue StandardError` swallowing real bugs; only catch the documented domain exceptions.

## References
- "Sustainable Rails" — David Bryant Copeland, https://sustainable-rails.com
- "The Rails 7 Way" — Obie Fernandez
- Code Climate Engineering Blog: "7 Patterns to Refactor Fat ActiveRecord Models" — https://thoughtbot.com/blog/7-patterns-to-refactor-fat-activerecord-models
- Trailblazer Operation docs — https://trailblazer.to/2.1/docs/operation/
