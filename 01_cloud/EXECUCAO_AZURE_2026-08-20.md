# Execução Azure — evidência consolidada

Data: 20/08/2026 (UTC e horário de Brasília registrados nos arquivos de evidência).

## Resultado

- Resource Group: `rg-predictfy-sprint3-260819es`.
- ACR Basic: `predictfy260819es`.
- Imagens: `predictfy-api:sprint3` e `predictfy-mysql-bridge:sprint3`.
- ACI API: `Running`, 1 vCPU, 2 GB; `/api/health` retornou `status: ok` e dez conjuntos de artefatos.
- ACI bridge: `Running`, 1 vCPU, 1,5 GB; `/health` confirmou artefato e banco.
- MySQL Flexible Server: `Ready`, `Standard_B1ms`, 32 GB, retenção 1 dia, sem alta disponibilidade e sem geobackup.
- Previsão consumida: baseline sazonal, D+1, segmento total, valor `44,0`.
- Persistência: uma inserção, uma consulta e uma agregação concluídas; proveniência por SHA-256.
- Log Analytics: KQL retornou POST/GET com HTTP 200 e erro controlado HTTP 401.
- Azure Monitor: séries reais de CPU/memória dos dois ACIs e CPU/memória/conexões/comandos do MySQL.
- Application Insights: OpenTelemetry recebido em `customMetrics`, `dependencies` e `exceptions`.

## Decisões de baixo custo

- ACR no tier Basic.
- ACI com 1 vCPU e memória mínima compatível com cada imagem.
- MySQL B1ms, 32 GB, retenção mínima de 1 dia, sem HA, sem geobackup e autogrow desabilitado.
- Nenhuma VM, AKS, gateway ou camada TLS adicional para a demonstração.
- Imagens existentes reutilizáveis com `SKIP_ACR_BUILD=true`.
- Ambiente efêmero, removido integralmente após o marcador de evidências e a revisão do PDF.

## Regiões

A política do Azure for Students permitiu os recursos gerais em East US 2. O MySQL recusou capacidade em East US 2, Canada Central, South Central US e North Central US com `ProvisionNotSupportedForRegion`; Chile Central concluiu com sucesso. A separação regional foi uma restrição comprovada da assinatura acadêmica, não uma escolha de arquitetura produtiva.

## Fontes

Os JSONs e logs em `evidencias/azure` foram gerados diretamente pela Azure CLI. Não contêm senhas, chaves de API ou connection strings. IDs de assinatura presentes em identificadores de métricas não concedem acesso e não são exibidos no PDF.
