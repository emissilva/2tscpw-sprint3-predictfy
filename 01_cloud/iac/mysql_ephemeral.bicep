@description('Nome global do Azure Database for MySQL Flexible Server')
param serverName string

@description('Região permitida pela política da assinatura')
param location string = resourceGroup().location

@description('Usuário administrador do MySQL')
param administratorLogin string

@secure()
@description('Senha efêmera do administrador')
param administratorLoginPassword string

@description('Banco usado pela demonstração')
param databaseName string = 'predictfy'

resource mysql 'Microsoft.DBforMySQL/flexibleServers@2023-12-30' = {
  name: serverName
  location: location
  tags: {
    Project: 'Predictfy'
    Sprint: '3'
    Discipline: 'Cloud'
    Environment: 'academic-ephemeral'
  }
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    version: '8.0.21'
    backup: {
      backupRetentionDays: 1
      geoRedundantBackup: 'Disabled'
    }
    dataEncryption: {
      type: 'SystemManaged'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
    storage: {
      autoGrow: 'Disabled'
      storageSizeGB: 32
    }
  }
}

resource azureServices 'Microsoft.DBforMySQL/flexibleServers/firewallRules@2023-12-30' = {
  name: 'AllowAzureServicesForSprint3'
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

output mysqlFqdn string = mysql.properties.fullyQualifiedDomainName
output sku string = mysql.sku.name
output backupRetentionDays int = mysql.properties.backup.backupRetentionDays
