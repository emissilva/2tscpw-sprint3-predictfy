# Passo a passo completo — execução do projeto 01 Cloud

Este roteiro reproduz a implantação que foi executada e documentada em 23/08/2026. Ele cobre preparação, provisionamento, build, deploy, integração com Machine Learning e MySQL, monitoramento, coleta de evidências e descarte. A edição do Draw.io não faz parte deste documento.

> **Atenção a custo:** MySQL Flexible Server, ACI, ACR, Log Analytics e Application Insights podem gerar cobrança. Só inicie quando puder concluir as evidências e remover o Resource Group no mesmo período.

## 1. O que o enunciado oficial exige

O documento `../../locaweb/sprints/Regras_Gerais_Challenge_Locaweb_Fev_2026_2TSCP_F_V_W_X_Sprint_1_2_3_4_v6.pdf`, páginas 33 e 34, pede:

- recursos provisionados na Microsoft Azure por Azure CLI ou Terraform;
- aplicação em Docker, executada em VM ou em ACR + ACI;
- reaproveitamento do modelo ou da lógica de Machine Learning;
- Azure Database for MySQL com inserção, consulta e processamento;
- Azure Monitor e Application Insights, com logs e métricas;
- evidências organizadas sequencialmente em PDF.

Esta implementação usa Azure CLI, ACR, dois ACIs, MySQL Flexible Server, Log Analytics, Azure Monitor e Application Insights. O bridge lê `locaweb/outputs/previsoes_baseline.json`, grava uma previsão no MySQL, consulta o registro e produz uma agregação.

## 2. Onde executar

Todos os comandos abaixo consideram a raiz `predictfy-locaweb` como diretório atual. Partindo da raiz deste repositório de estudos:

```bash
cd predictfy-locaweb
pwd
test -f "Sprint 3/01_cloud/app_mysql/Dockerfile"
test -f locaweb/api/Dockerfile
test -f locaweb/outputs/previsoes_baseline.json
```

Os três testes devem terminar sem mensagem e com código zero. Permaneça nessa pasta, pois os contextos dos builds são relativos à raiz `predictfy-locaweb`.

## 3. Pré-requisitos

É necessário ter:

1. uma assinatura Azure ativa, com permissão para criar recursos;
2. Azure CLI instalada;
3. `curl` e Bash;
4. registros da SPA e da API no Microsoft Entra ID já usados pelo Predictfy;
5. uma origem permitida no CORS, por exemplo a URL HTTPS do frontend publicado.

Confira as ferramentas:

```bash
az version
bash --version
curl --version
```

Não é necessário instalar Docker localmente: `az acr build` envia o contexto e constrói as imagens na Azure.

## 4. Login e assinatura correta

```bash
az login
az account list --output table
az account set --subscription "NOME-OU-ID-DA-ASSINATURA"
az account show --output table
```

Antes de continuar, confira principalmente `Name`, `State` e `IsDefault`. Usar a assinatura errada é uma causa comum de falta de quota, cobrança inesperada ou recursos “desaparecidos” no Portal.

Se estiver no Azure Cloud Shell, o login normalmente já existe, mas ainda é necessário conferir e selecionar a assinatura.

## 5. Definir nomes e configurações não sensíveis

Use um sufixo novo, curto e globalmente único. O exemplo abaixo usa data e iniciais; substitua `260823es` por outro valor. O ACR aceita apenas letras e números minúsculos.

```bash
export AZ_LOCATION="eastus2"
export AZ_MYSQL_LOCATION="chilecentral"
export AZ_UNIQUE_SUFFIX="260823es"

export AZ_RESOURCE_GROUP="rg-predictfy-sprint3-${AZ_UNIQUE_SUFFIX}"
export AZ_ACR_NAME="predictfy${AZ_UNIQUE_SUFFIX}"
export AZ_MYSQL_SERVER="predictfy-${AZ_UNIQUE_SUFFIX}-cl"

export AZ_CONTAINER_NAME="aci-predictfy-api"
export AZ_BRIDGE_CONTAINER_NAME="aci-predictfy-mysql-bridge"
export AZ_DNS_LABEL="predictfy-api-${AZ_UNIQUE_SUFFIX}"
export AZ_BRIDGE_DNS_LABEL="predictfy-bridge-${AZ_UNIQUE_SUFFIX}"
export AZ_LOG_WORKSPACE="log-predictfy-sprint3"
export AZ_APP_INSIGHTS="appi-predictfy-sprint3"
export AZ_MYSQL_DATABASE="predictfy"
export AZ_MYSQL_ADMIN="predictfyadmin"
```

Na execução comprovada, os recursos gerais funcionaram em `eastus2`, enquanto a assinatura Azure for Students só aceitou o MySQL em `chilecentral`. A disponibilidade varia por assinatura e momento. Se `chilecentral` não estiver disponível, consulte:

```bash
az account list-locations --query '[].{Nome:name,Exibicao:displayName}' --output table
```

## 6. Informar os segredos sem gravá-los no Git

Não coloque valores reais em `iac/config.example.env`, documentação, prints ou histórico do shell. Digite os segredos de forma oculta na sessão atual:

```bash
read -s "MYSQL_ADMIN_PASSWORD?Senha forte do MySQL: "; export MYSQL_ADMIN_PASSWORD; echo
read -s "CHAT_SESSION_SECRET?Segredo de sessão da API: "; export CHAT_SESSION_SECRET; echo
read -s "OPENAI_API_KEY?Chave OpenAI (Enter para deixar vazia): "; export OPENAI_API_KEY; echo
read -s "BRIDGE_API_KEY?Chave do bridge: "; export BRIDGE_API_KEY; echo
```

No Bash/Linux, use a forma equivalente:

```bash
read -r -s -p "Senha forte do MySQL: " MYSQL_ADMIN_PASSWORD; export MYSQL_ADMIN_PASSWORD; echo
```

Defina também os identificadores públicos do Entra e o CORS:

```bash
export ENTRA_API_CLIENT_ID="CLIENT-ID-DO-REGISTRO-DA-API"
export ENTRA_SPA_CLIENT_ID="CLIENT-ID-DO-REGISTRO-DA-SPA"
export CORS_ALLOWED_ORIGINS="https://SEU-FRONTEND.vercel.app"
```

Os valores de `ENTRA_API_CLIENT_ID` e `ENTRA_SPA_CLIENT_ID` ficam em Microsoft Entra ID → App registrations → aplicação → Overview → Application (client) ID. Para múltiplas origens CORS, use o formato aceito pela API atual; não inclua `*` em uma demonstração autenticada.

Confira apenas se todas as variáveis existem, sem imprimir seus conteúdos:

```bash
for nome in AZ_LOCATION AZ_MYSQL_LOCATION AZ_RESOURCE_GROUP AZ_ACR_NAME \
  AZ_MYSQL_SERVER AZ_CONTAINER_NAME AZ_BRIDGE_CONTAINER_NAME AZ_DNS_LABEL \
  AZ_BRIDGE_DNS_LABEL AZ_LOG_WORKSPACE AZ_APP_INSIGHTS AZ_MYSQL_DATABASE \
  AZ_MYSQL_ADMIN MYSQL_ADMIN_PASSWORD CHAT_SESSION_SECRET \
  ENTRA_API_CLIENT_ID ENTRA_SPA_CLIENT_ID CORS_ALLOWED_ORIGINS BRIDGE_API_KEY; do
  test -n "${!nome:-}" || echo "FALTA: $nome"
done
```

Esse laço usa expansão indireta do Bash. No Zsh, use a validação equivalente: `for nome in ...; do test -n "${(P)nome}" || echo "FALTA: $nome"; done`. As etapas seguintes podem ser executadas normalmente no Zsh ou no Bash.

## 7. Provisionar a infraestrutura-base

Execute cada bloco separadamente e só avance se o comando anterior terminar sem erro:

```bash
az group create \
  --name "$AZ_RESOURCE_GROUP" --location "$AZ_LOCATION" \
  --tags Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic \
  --output table

az monitor log-analytics workspace create \
  --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" \
  --location "$AZ_LOCATION" \
  --tags Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic \
  --output table

export AZ_SUBSCRIPTION_ID="$(az account show --query id --output tsv)"
export AZ_WORKSPACE_RESOURCE_ID="/subscriptions/${AZ_SUBSCRIPTION_ID}/resourceGroups/${AZ_RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/${AZ_LOG_WORKSPACE}"

az extension add --name application-insights --upgrade --yes
az monitor app-insights component create \
  --app "$AZ_APP_INSIGHTS" --location "$AZ_LOCATION" \
  --resource-group "$AZ_RESOURCE_GROUP" --kind web --application-type web \
  --workspace "$AZ_WORKSPACE_RESOURCE_ID" \
  --tags Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic \
  --output table

az acr create \
  --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_ACR_NAME" \
  --location "$AZ_LOCATION" --sku Basic --admin-enabled true \
  --tags Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic \
  --output table

az mysql flexible-server create \
  --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --location "$AZ_MYSQL_LOCATION" --admin-user "$AZ_MYSQL_ADMIN" \
  --admin-password "$MYSQL_ADMIN_PASSWORD" --tier Burstable \
  --sku-name Standard_B1ms --storage-size 32 --backup-retention 1 \
  --version 8.0.21 --public-access 0.0.0.0 \
  --tags Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic \
  --yes --output table

az mysql flexible-server db create \
  --resource-group "$AZ_RESOURCE_GROUP" --server-name "$AZ_MYSQL_SERVER" \
  --database-name "$AZ_MYSQL_DATABASE" --output table

az mysql flexible-server firewall-rule create \
  --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --rule-name AllowAzureServicesForSprint3 \
  --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 --output table

az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table
```

Esses comandos criam, nesta ordem:

1. Resource Group;
2. Log Analytics Workspace;
3. Application Insights associado ao workspace;
4. Azure Container Registry Basic;
5. MySQL Flexible Server B1ms, banco `predictfy` e regra para serviços Azure;
6. inventário final dos recursos.

Resultado esperado: comandos com estado `Succeeded`/`Ready` e uma tabela de recursos. O provisionamento é parcialmente idempotente: pode ser reexecutado com os mesmos nomes após uma falha, mas não crie outro conjunto de nomes antes de verificar o Resource Group existente.

### Se o MySQL falhar

- `ProvisionNotSupportedForRegion`: altere somente `AZ_MYSQL_LOCATION` e repita apenas o comando `az mysql flexible-server create` e os dois comandos seguintes.
- `Incorrect value for --version`: atualize a Azure CLI e confirme que `8.0.21` aparece entre as versões aceitas.
- `InternalServerError` depois de “Creating MySQL Server”: o servidor pode ter sido criado mesmo com erro na resposta. Confira antes de repetir:

```bash
az mysql flexible-server show \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_MYSQL_SERVER" \
  --query '{Estado:state,FQDN:fullyQualifiedDomainName,Versao:version}' \
  --output table
```

Se o servidor estiver `Ready`, garanta manualmente o banco e a regra de firewall; esses comandos são seguros para a mesma implantação:

```bash
az mysql flexible-server db create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --server-name "$AZ_MYSQL_SERVER" \
  --database-name "$AZ_MYSQL_DATABASE" \
  --output table

az mysql flexible-server firewall-rule create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_MYSQL_SERVER" \
  --rule-name AllowAzureServicesForSprint3 \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0 \
  --output table
```

O valor `0.0.0.0` nessa regra representa acesso de serviços Azure. É adequado à demonstração efêmera, mas a evolução produtiva deve usar rede privada, menor privilégio e Key Vault.

## 8. Construir e publicar a API

```bash
az acr build \
  --registry "$AZ_ACR_NAME" --image predictfy-api:sprint3 \
  --file locaweb/api/Dockerfile locaweb

export AZ_ACR_LOGIN_SERVER="$(az acr show --name "$AZ_ACR_NAME" --query loginServer --output tsv)"
export AZ_ACR_USERNAME="$(az acr credential show --name "$AZ_ACR_NAME" --query username --output tsv)"
export AZ_ACR_PASSWORD="$(az acr credential show --name "$AZ_ACR_NAME" --query 'passwords[0].value' --output tsv)"
export AZ_WORKSPACE_ID="$(az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query customerId --output tsv)"
export AZ_WORKSPACE_KEY="$(az monitor log-analytics workspace get-shared-keys --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query primarySharedKey --output tsv)"
export APPLICATIONINSIGHTS_CONNECTION_STRING="$(az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" --query connectionString --output tsv)"

az container create \
  --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" \
  --image "${AZ_ACR_LOGIN_SERVER}/predictfy-api:sprint3" \
  --registry-login-server "$AZ_ACR_LOGIN_SERVER" \
  --registry-username "$AZ_ACR_USERNAME" --registry-password "$AZ_ACR_PASSWORD" \
  --os-type Linux --cpu 1 --memory 2 --ports 8000 \
  --ip-address Public --dns-name-label "$AZ_DNS_LABEL" --restart-policy Always \
  --log-analytics-workspace "$AZ_WORKSPACE_ID" \
  --log-analytics-workspace-key "$AZ_WORKSPACE_KEY" \
  --environment-variables CHAT_LLM_PROVIDER=openai OPENAI_MODEL=gpt-5.6-luna \
    CHAT_ALLOW_LOCAL_DEV=false ENTRA_TENANT_ID=common \
    ENTRA_API_CLIENT_ID="$ENTRA_API_CLIENT_ID" \
    ENTRA_SPA_CLIENT_ID="$ENTRA_SPA_CLIENT_ID" \
    ENTRA_REQUIRED_SCOPE=access_as_user \
    CORS_ALLOWED_ORIGINS="$CORS_ALLOWED_ORIGINS" \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$APPLICATIONINSIGHTS_CONNECTION_STRING" \
  --secure-environment-variables CHAT_SESSION_SECRET="$CHAT_SESSION_SECRET" \
    OPENAI_API_KEY="${OPENAI_API_KEY:-}" --output table
```

Os comandos:

- envia `locaweb` como contexto para o build remoto do ACR;
- cria `predictfy-api:sprint3`;
- obtém as credenciais do ACR e integra o ACI ao Log Analytics;
- publica a API na porta 8000.

Se estiver refazendo esta etapa e já existir um ACI com o mesmo nome, remova somente esse ACI antes do `az container create`:

```bash
az container delete --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --yes
```

O upload e o build podem levar vários minutos. Ao final, o terminal mostra uma URL no formato:

```text
http://predictfy-api-SUFIXO.REGIAO.azurecontainer.io:8000/api/health
```

Espere o estado ficar `Running`:

```bash
az container show \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_CONTAINER_NAME" \
  --query '{Estado:instanceView.state,FQDN:ipAddress.fqdn,Imagem:containers[0].image}' \
  --output table
```

## 9. Verificar API, ACR, MySQL e monitoramento

```bash
az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table
az acr repository show-tags --name "$AZ_ACR_NAME" \
  --repository predictfy-api --output table
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" \
  --query '{Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image}' --output table
export API_FQDN="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
curl --fail --show-error --max-time 20 "http://${API_FQDN}:8000/api/health"
az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --query '{Estado:state,FQDN:fullyQualifiedDomainName,Versao:version,BackupDias:backup.backupRetentionDays}' --output table
az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" \
  --query '{Nome:name,Estado:provisioningState,Retencao:retentionInDays}' --output table
az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --query '{Nome:name,Estado:provisioningState,Tipo:applicationType}' --output table
```

O resultado esperado inclui:

- tag `sprint3` no repositório `predictfy-api`;
- ACI da API em `Running`;
- `/api/health` com `"status":"ok"` e a lista de artefatos analíticos;
- MySQL em `Ready`, versão 8.0.21;
- Log Analytics e Application Insights em `Succeeded`.

Se o health check for executado cedo demais, aguarde alguns segundos, veja os logs e tente novamente:

```bash
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME"
curl --fail --show-error --max-time 20 "http://${API_FQDN}:8000/api/health"
```

## 10. Construir e publicar o bridge de ML + MySQL

```bash
az acr build \
  --registry "$AZ_ACR_NAME" --image predictfy-mysql-bridge:sprint3 \
  --file "Sprint 3/01_cloud/app_mysql/Dockerfile" .

export AZ_MYSQL_HOST="$(az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" --query fullyQualifiedDomainName --output tsv)"

az container create \
  --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" \
  --image "${AZ_ACR_LOGIN_SERVER}/predictfy-mysql-bridge:sprint3" \
  --registry-login-server "$AZ_ACR_LOGIN_SERVER" \
  --registry-username "$AZ_ACR_USERNAME" --registry-password "$AZ_ACR_PASSWORD" \
  --os-type Linux --cpu 1 --memory 1.5 --ports 8080 \
  --ip-address Public --dns-name-label "$AZ_BRIDGE_DNS_LABEL" --restart-policy Always \
  --log-analytics-workspace "$AZ_WORKSPACE_ID" \
  --log-analytics-workspace-key "$AZ_WORKSPACE_KEY" \
  --environment-variables MYSQL_HOST="$AZ_MYSQL_HOST" MYSQL_PORT=3306 \
    MYSQL_USER="$AZ_MYSQL_ADMIN" MYSQL_DATABASE="$AZ_MYSQL_DATABASE" \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$APPLICATIONINSIGHTS_CONNECTION_STRING" \
  --secure-environment-variables MYSQL_PASSWORD="$MYSQL_ADMIN_PASSWORD" \
    BRIDGE_API_KEY="$BRIDGE_API_KEY" --output table
```

O contexto do build é a raiz `predictfy-locaweb`, pois o Dockerfile inclui o artefato real `locaweb/outputs/previsoes_baseline.json`. Os comandos criam `predictfy-mysql-bridge:sprint3`, injetam a conexão MySQL e a telemetria, e publicam o bridge na porta 8080. Em uma reexecução, remova antes apenas o bridge existente com `az container delete --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --yes`.

Confira o estado:

```bash
az container show \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_BRIDGE_CONTAINER_NAME" \
  --query '{Estado:instanceView.state,FQDN:ipAddress.fqdn,Imagem:containers[0].image}' \
  --output table
```

Se o container não iniciar, consulte:

```bash
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME"
az container attach --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME"
```

## 11. Comprovar inserção, consulta e processamento no MySQL

```bash
export BRIDGE_FQDN="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
export BRIDGE_BASE_URL="http://${BRIDGE_FQDN}:8080"

curl --fail --show-error --max-time 20 "$BRIDGE_BASE_URL/health"
curl --fail --show-error --max-time 20 --request POST \
  --header "Content-Type: application/json" \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  --data '{"horizonte":1,"segmento":"total"}' \
  "$BRIDGE_BASE_URL/executions/capture"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  "$BRIDGE_BASE_URL/executions?limit=10"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  "$BRIDGE_BASE_URL/executions/summary"
```

O roteiro faz quatro chamadas:

1. `GET /health`: deve retornar `artifact: true` e `database: true`;
2. `POST /executions/capture`: lê a previsão D+1 do segmento total e insere no MySQL;
3. `GET /executions`: consulta os registros persistidos;
4. `GET /executions/summary`: agrega por modelo, horizonte e segmento.

Na execução de referência, o resultado foi modelo `baseline_sazonal_7d`, horizonte `D+1`, segmento `total` e valor previsto `44.0`. O valor pode mudar se o artefato de ML for atualizado; o importante é que captura, consulta e agregação sejam coerentes e tragam a proveniência SHA-256.

Comprove também que a rota protegida rejeita uma chamada sem chave:

```bash
curl -i "http://${BRIDGE_FQDN}:8080/executions"
```

Resultado esperado: `HTTP/1.1 401 Unauthorized` e `{"detail":"Chave inválida."}`.

## 12. Gerar atividade para logs e telemetria

Antes da coleta, execute novamente o exercício autorizado e a chamada 401:

```bash
curl --fail --show-error --max-time 20 --request POST \
  --header "Content-Type: application/json" \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  --data '{"horizonte":1,"segmento":"total"}' \
  "$BRIDGE_BASE_URL/executions/capture"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" "$BRIDGE_BASE_URL/executions?limit=10"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" "$BRIDGE_BASE_URL/executions/summary"
curl -i "http://${BRIDGE_FQDN}:8080/executions"
```

A ingestão no Log Analytics e no Application Insights não é instantânea. Espere alguns minutos se a primeira consulta retornar vazia. Não provoque indisponibilidade de propósito; sucessos, consultas SQL e o bloqueio 401 já geram sinais suficientes.

## 13. Coletar evidências pela Azure CLI

Para preservar a execução atual em uma pasta nova:

```bash
export EVIDENCE_DIR="Sprint 3/01_cloud/evidencias/reexecucao_$(date +%Y-%m-%d_%H%M)/azure"
mkdir -p "$EVIDENCE_DIR"

az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output json > "$EVIDENCE_DIR/01_recursos.json"
az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table > "$EVIDENCE_DIR/01_recursos.txt"
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-api \
  --output json > "$EVIDENCE_DIR/02_acr_api_tags.json"
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-mysql-bridge \
  --output json > "$EVIDENCE_DIR/03_acr_bridge_tags.json"
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" \
  --query '{Nome:name,Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image,CPU:containers[0].resources.requests.cpu,MemoriaGB:containers[0].resources.requests.memoryInGb}' \
  --output json > "$EVIDENCE_DIR/04_aci_api.json"
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" \
  --query '{Nome:name,Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image,CPU:containers[0].resources.requests.cpu,MemoriaGB:containers[0].resources.requests.memoryInGb}' \
  --output json > "$EVIDENCE_DIR/05_aci_bridge.json"
az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --query '{Nome:name,Estado:state,FQDN:fullyQualifiedDomainName,Versao:version,Tier:sku.tier,SKU:sku.name,StorageGB:storage.storageSizeGb,RetencaoDias:backup.backupRetentionDays,GeoBackup:backup.geoRedundantBackup}' \
  --output json > "$EVIDENCE_DIR/06_mysql.json"
az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" \
  --query '{Nome:name,Estado:provisioningState,RetencaoDias:retentionInDays,Regiao:location}' \
  --output json > "$EVIDENCE_DIR/07_log_analytics.json"
az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --query '{Nome:name,Estado:provisioningState,Tipo:applicationType,Regiao:location}' \
  --output json > "$EVIDENCE_DIR/08_application_insights.json"
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" > "$EVIDENCE_DIR/09_api_logs.txt"
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" > "$EVIDENCE_DIR/10_bridge_logs.txt"

az monitor log-analytics query --workspace "$AZ_WORKSPACE_ID" \
  --analytics-query "ContainerInstanceLog_CL | where TimeGenerated > ago(2h) | project TimeGenerated, ContainerGroup_s, Message | order by TimeGenerated desc | take 100" \
  --output json > "$EVIDENCE_DIR/11_log_analytics_query.json"

export API_RESOURCE_ID="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --query id --output tsv)"
export BRIDGE_RESOURCE_ID="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --query id --output tsv)"
export MYSQL_RESOURCE_ID="$(az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" --query id --output tsv)"

az monitor metrics list --resource "$API_RESOURCE_ID" --metric CpuUsage MemoryUsage \
  --interval PT1M --aggregation Average --output json > "$EVIDENCE_DIR/12_metricas_aci_api.json"
az monitor metrics list --resource "$BRIDGE_RESOURCE_ID" --metric CpuUsage MemoryUsage \
  --interval PT1M --aggregation Average --output json > "$EVIDENCE_DIR/13_metricas_aci_bridge.json"
az monitor metrics list --resource "$MYSQL_RESOURCE_ID" \
  --metric cpu_percent memory_percent active_connections Com_insert Com_select \
  --interval PT1M --aggregation Average --output json > "$EVIDENCE_DIR/14_metricas_mysql.json"
az monitor app-insights query --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --analytics-query "union withsource=Tabela dependencies, exceptions, customMetrics | where timestamp > ago(2h) | summarize Registros=count() by Tabela | order by Tabela asc" \
  --output json > "$EVIDENCE_DIR/15_app_insights_telemetria.json"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$EVIDENCE_DIR/COLETADO_EM_UTC.txt"
find "$EVIDENCE_DIR" -maxdepth 1 -type f -print | sort
```

Os comandos registram inventário, tags das imagens, estado dos ACIs, configuração do MySQL, Log Analytics, Application Insights, logs dos containers, consulta KQL, métricas de CPU/memória e telemetria.

Confira se os arquivos existem e não estão vazios:

```bash
find "$EVIDENCE_DIR" -maxdepth 1 -type f -size 0 -print
```

O resultado ideal é vazio. Um JSON de consulta pode ser válido mesmo sem linhas; abra os arquivos 11 a 15 e confirme que há dados úteis antes do descarte:

```bash
for arquivo in "$EVIDENCE_DIR"/{11,12,13,14,15}_*.json; do
  echo "===== $arquivo ====="
  python3 -m json.tool "$arquivo" | sed -n '1,80p'
done
```

Se a telemetria ainda estiver vazia, espere a ingestão, gere novas chamadas e repita os comandos de coleta correspondentes. Eles sobrescrevem os arquivos no `EVIDENCE_DIR` escolhido.

## 14. Evidências no Portal Azure

Além dos arquivos brutos, capture telas reais e legíveis, sem exibir segredos:

1. Resource Group → visão geral com todos os recursos;
2. ACR → Repositories → as duas imagens e a tag `sprint3`;
3. cada Container Instance → Overview, estado `Running`, imagem, CPU e memória;
4. API e bridge respondendo aos health checks;
5. respostas de inserção, consulta, agregação e bloqueio 401 no terminal;
6. MySQL Flexible Server → Overview e Databases;
7. Log Analytics → Logs, com consulta dos dois containers;
8. Azure Monitor → Metrics para os ACIs e o MySQL;
9. Application Insights → Logs/Transaction search, com telemetria do bridge.

Uma consulta KQL útil no workspace é:

```kusto
ContainerInstanceLog_CL
| where TimeGenerated > ago(2h)
| project TimeGenerated, ContainerGroup_s, Message
| order by TimeGenerated desc
| take 100
```

As evidências devem mostrar o que cada serviço comprova, e não apenas que a tela existe. O PDF oficial desta pasta serve como referência da sequência final.

## 15. Conferência antes de apagar

Só prossiga quando tiver confirmado:

- os dois ACIs em `Running`;
- os dois repositórios/tag no ACR;
- health da API e do bridge;
- inserção, consulta e agregação no MySQL;
- bloqueio 401;
- logs dos dois containers;
- métricas dos ACIs e MySQL;
- telemetria do Application Insights;
- arquivos brutos e capturas salvos fora dos recursos Azure.

Crie um marcador local para registrar que a conferência foi concluída:

```bash
touch "$EVIDENCE_DIR/EVIDENCIAS_COLETADAS.ok"
export EVIDENCE_MARKER="$EVIDENCE_DIR/EVIDENCIAS_COLETADAS.ok"
```

## 16. Remover o ambiente e encerrar a cobrança

O comando `az group delete` abaixo exclui todo o Resource Group e seus recursos. Confira o nome e o marcador antes:

```bash
printf 'Resource Group que será removido: %s\n' "$AZ_RESOURCE_GROUP"
az resource list --resource-group "$AZ_RESOURCE_GROUP" --output table
case "$AZ_RESOURCE_GROUP" in
  rg-predictfy-sprint3-*) echo "Nome do Resource Group aprovado" ;;
  *) echo "RECUSA: nome fora do padrão seguro"; return 2 2>/dev/null || exit 2 ;;
esac
test -f "$EVIDENCE_MARKER" || { echo "RECUSA: marcador de evidências ausente"; return 2 2>/dev/null || exit 2; }
az group delete --name "$AZ_RESOURCE_GROUP" --yes
```

As validações recusam nomes fora do padrão `rg-predictfy-sprint3-*` e exigem o marcador de evidências. O `az group delete` pode demorar e normalmente não imprime confirmação. Verifique de forma independente:

```bash
az group exists --name "$AZ_RESOURCE_GROUP"
```

O retorno deve ser `false`. Depois, remova os segredos somente da sessão atual:

```bash
unset MYSQL_ADMIN_PASSWORD CHAT_SESSION_SECRET OPENAI_API_KEY BRIDGE_API_KEY
```

## 17. Reexecução mais rápida

Se as imagens já existirem no mesmo ACR, é possível evitar novos builds. Nesse caso, pule somente os dois comandos `az acr build` e execute normalmente os comandos de obtenção de credenciais e `az container create` das seções 8 e 10.

```bash
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-api --output table
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-mysql-bridge --output table
```

Isso só funciona se os repositórios `predictfy-api:sprint3` e `predictfy-mysql-bridge:sprint3` ainda estiverem no ACR. Após excluir o Resource Group, as imagens também deixam de existir.

## 18. Ordem resumida das etapas manuais

1. entrar em `predictfy-locaweb`, fazer login e selecionar a assinatura;
2. exportar nomes, configurações e segredos da sessão;
3. executar, um a um, os comandos de provisionamento da seção 7;
4. executar o build e o deploy da API da seção 8 e validá-la na seção 9;
5. executar o build e o deploy do bridge da seção 10;
6. executar as quatro chamadas de banco da seção 11 e gerar telemetria;
7. executar, um a um, os comandos de coleta da seção 13 e fazer as capturas da seção 14;
8. conferir todos os arquivos e criar o marcador;
9. executar a validação de nome e o `az group delete` da seção 16;
10. confirmar que `az group exists` retorna `false`.

Esta lista é apenas um índice. Use os blocos completos das seções correspondentes, sem pular as conferências e capturas.

## 19. O que já foi comprovado neste projeto

A execução real de 23/08/2026 está preservada em `evidencias/reexecucao_2026-08-23/`. Ela comprova:

- ACR com builds `ch1` e `ch2` e duas imagens `sprint3`;
- API e bridge em ACI, ambos `Running`;
- API com dez conjuntos de artefatos analíticos;
- MySQL `Ready`, B1ms, 32 GB, versão 8.0.21;
- previsão D+1 total igual a `44.0` naquela versão do artefato;
- inserção, consulta e agregação reais;
- resposta 401 sem `X-Bridge-Key`;
- logs, métricas e telemetria;
- remoção final do Resource Group confirmada.

Esses registros explicam como a entrega atual foi feita; uma nova entrega deve usar evidências da nova execução, não reutilizar resultados antigos como se fossem atuais.
