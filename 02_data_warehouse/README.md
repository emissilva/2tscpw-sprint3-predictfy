# 02 — Data Warehousing & Advanced Data Integration

Entrega executada da Sprint 3 do grupo **Predictfy**. O fluxo autônomo no Azure Data Factory integrou 25.588 registros de incidentes com regras OLA, persistindo o mesmo resultado no Azure Database for MySQL e em TXT no Blob Storage.

## Resultado comprovado

- Resource Group exclusivo: `rg-predictfy-dw-sprint3-260823es`.
- ADF e Storage em East US 2; MySQL Flexible Server em Chile Central.
- Duas execuções integrais do pipeline em estado `Succeeded`.
- 25.588 linhas lidas e gravadas em cada destino, sem rejeições.
- `COUNT(*) = COUNT(DISTINCT incident_feature_id) = 25.588` após a segunda carga.
- Nenhuma prioridade P2/P3 sem regra OLA.
- TXT curated com 5.917.752 bytes e 25.588 registros.
- Infraestrutura efêmera descartada após a coleta das evidências.

## Arquivos de entrega

- `DataWarehouse_Locaweb_Sprint3_Predictfy.docx`
- `DataWarehouse_Locaweb_Sprint3_Predictfy.pdf`
- `colunas_derivadas.txt`
- `arquitetura_ingestao.drawio`
- `evidencias/azure/`: evidências brutas sanitizadas.
- `evidencias/capturas_reais/`: imagens usadas no relatório.
- `adf/`, `iac/`, `sql/` e `scripts/`: implementação reproduzível.

Execute `python3 validate_local.py` para validar a base e os nove artefatos ADF. O script `gerar_entrega.py` recompõe o DOCX, o PDF e as figuras a partir das evidências coletadas.
