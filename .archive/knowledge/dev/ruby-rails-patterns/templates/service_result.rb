# purpose: ServiceResult value object with .success / .failure factories + predicates
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~250 tokens when loaded as context

class ServiceResult
  attr_reader :data, :error, :details

  def self.success(data: nil)
    new(success: true, data: data)
  end

  def self.failure(error:, details: nil)
    new(success: false, error: error, details: details)
  end

  def initialize(success:, data: nil, error: nil, details: nil)
    @success = success
    @data = data
    @error = error
    @details = details
  end

  def success?
    @success
  end

  def failure?
    !@success
  end
end
