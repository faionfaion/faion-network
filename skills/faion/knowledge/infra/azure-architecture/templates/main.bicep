# purpose: Bicep skeleton using AVM modules (deployment-level)
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (spec)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~400 tokens when loaded

targetScope = 'subscription'

param location string = 'westeurope'
param projectName string

module rg 'br/public:avm/res/resources/resource-group:0.4.0' = {
  name: 'rg-${projectName}'
  params: {
    name: 'rg-${projectName}'
    location: location
  }
}

module vnet 'br/public:avm/res/network/virtual-network:0.5.0' = {
  name: 'vnet-${projectName}'
  scope: resourceGroup('rg-${projectName}')
  params: {
    name: 'vnet-${projectName}'
    addressPrefixes: ['10.10.0.0/16']
    subnets: [
      { name: 'app', addressPrefix: '10.10.1.0/24' }
      { name: 'data', addressPrefix: '10.10.2.0/24' }
    ]
  }
}
