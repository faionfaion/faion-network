# purpose: RESTful routes with member/collection convention
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~300 tokens when loaded as context

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :orders, only: %i[index show create update destroy] do
        member do
          patch :cancel
          post :refund
        end

        collection do
          get :recent
        end

        resources :items, only: %i[index show create destroy], shallow: true
      end

      resource :session, only: %i[create destroy]
      resources :users, only: %i[show update]
    end
  end

  get "/health", to: "health#show"
  root "home#index"
end
