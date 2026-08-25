# Matriz de requisitos — Cloud

| Requisito oficial | Implementação planejada | Evidência | Estado |
|---|---|---|---|
| Desenho em Draw.io | Arquitetura do produto e implantação acadêmica Azure | `.drawio` editável e versão exportada | Concluído |
| Resource Group | `rg-predictfy-sprint3-260823es` | Inventário real coletado antes da exclusão | Concluído |
| VM, WebApp ou ACI | Dois ACIs: API atual e bridge MySQL | Estados `Running`, FQDN e health checks | Concluído |
| Container Docker | Imagens construídas no ACR com Dockerfiles reais | Builds `ch1`/`ch2`, tags e digests | Concluído |
| Azure Database for MySQL | Flexible Server `predictfy`, B1ms mínimo | Estado `Ready`, inserção, consulta e agregação | Concluído |
| Azure Monitor | Logs KQL e métricas de ACI/MySQL | Evidências 11 a 14 | Concluído |
| Application Insights | OpenTelemetry do bridge | Consulta de requisições coletada | Concluído |
| IaC Azure CLI ou Terraform | Sete scripts shell + Bicep auxiliar | Execução real e pacote reproduzível | Concluído |
| Integração com ML | Bridge consome snapshot governado e registra execução | D+1 Total = 44,0 e SHA-256 | Concluído |
| Inserção, consulta e processamento | Captura, listagem e agregação | Fluxo executado na Azure | Concluído |
| Documento PDF sequencial | Relatório na ordem oficial | `Cloud_Locaweb_Sprint3_Predictfy.pdf`, 15 páginas A4 | Concluído |

## Regra de aceite

“Pendente de Azure” não pode ser substituído por captura simulada. O item somente passa para concluído após execução real e evidência legível.
