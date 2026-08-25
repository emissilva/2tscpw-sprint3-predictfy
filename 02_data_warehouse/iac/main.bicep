targetScope = 'resourceGroup'

@description('Sufixo globalmente único da entrega efêmera de Data Warehouse.')
@minLength(6)
@maxLength(14)
param uniqueSuffix string = '260823es'
param location string = 'eastus2'
param mysqlLocation string = 'chilecentral'
param mysqlAdministratorLogin string = 'predictfyadmin'
@secure()
param mysqlAdministratorLoginPassword string
param databaseName string = 'predictfy'

var storageName = 'pfdw${uniqueSuffix}'
var factoryName = 'adf-predictfy-dw-${uniqueSuffix}'
var mysqlName = 'mysql-predictfy-dw-${uniqueSuffix}'
var tags = {
  Project: 'Predictfy'
  Sprint: '3'
  Discipline: 'DataWarehouse'
  Environment: 'academic-ephemeral'
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}
resource landing 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'landing'
  properties: { publicAccess: 'None' }
}
resource curated 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'curated'
  properties: { publicAccess: 'None' }
}

resource factory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: factoryName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: { publicNetworkAccess: 'Enabled' }
}
resource blobContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, factory.id, 'blob-contributor')
  scope: storage
  properties: {
    principalId: factory.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  }
}

resource mysql 'Microsoft.DBforMySQL/flexibleServers@2023-12-30' = {
  name: mysqlName
  location: mysqlLocation
  tags: tags
  sku: {
    name: 'Standard_B2s'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: mysqlAdministratorLogin
    administratorLoginPassword: mysqlAdministratorLoginPassword
    version: '8.0.21'
    backup: {
      backupRetentionDays: 1
      geoRedundantBackup: 'Disabled'
    }
    dataEncryption: { type: 'SystemManaged' }
    highAvailability: { mode: 'Disabled' }
    network: { publicNetworkAccess: 'Enabled' }
    storage: {
      autoGrow: 'Disabled'
      storageSizeGB: 32
    }
  }
}
resource azureServices 'Microsoft.DBforMySQL/flexibleServers/firewallRules@2023-12-30' = {
  name: 'AllowAzureServicesForADF'
  parent: mysql
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}
resource database 'Microsoft.DBforMySQL/flexibleServers/databases@2023-12-30' = {
  name: databaseName
  parent: mysql
  properties: {
    charset: 'utf8mb4'
    collation: 'utf8mb4_0900_ai_ci'
  }
}

output dataFactoryName string = factory.name
output storageAccountName string = storage.name
output storageBlobEndpoint string = storage.properties.primaryEndpoints.blob
output mysqlServerName string = mysql.name
output mysqlFqdn string = mysql.properties.fullyQualifiedDomainName
output databaseName string = database.name
