# Mapeamento de dados — fluxo Predictfy

Documento de apoio baseado no modelo de mapeamento ensinado nas aulas 6 e 7. O grão do destino é **uma linha da matriz histórica de features KPI do Predictfy**, e não uma previsão futura nem o identificador transacional original do incidente.

| Origem | Tipo origem | Destino | Tipo MySQL | Transformação/regra |
|---|---|---|---|---|
| `source_row_number` | inteiro | `incident_feature_id` | `CHAR(64)` | SHA-256 da versão da fonte + posição estável |
| `hora` | texto CSV | `hora` | `TINYINT` | cast inteiro; aceitar somente 0–23 |
| `dia_semana` | texto CSV | `dia_semana` | `TINYINT` | cast inteiro; 0=segunda, 6=domingo |
| `mes` | texto CSV | `mes` | `TINYINT` | cast inteiro |
| `trimestre` | texto CSV | `trimestre` | `TINYINT` | cast inteiro |
| `prioridade_bin` | texto CSV | `prioridade_codigo` | `VARCHAR(2)` | 1=P2; 0=P3 |
| TXT `prioridade_desc` | texto | `prioridade_desc` | `VARCHAR(20)` | left join por `prioridade_codigo` |
| TXT `ola_limite_horas` | texto | `ola_limite_horas` | `SMALLINT` | cast inteiro após join |
| `hora` | texto CSV | `periodo_dia_desc` | `VARCHAR(12)` | madrugada/manhã/tarde/noite |
| `rolling_7d`, `rolling_30d` | decimal | `media_movel_delta` | `DECIMAL(18,4)` | média 7d menos média 30d |
| `media_movel_delta` | derivado | `tendencia_volume` | `VARCHAR(10)` | alta acima de 2; baixa abaixo de -2; estável |
| `is_feriado`, `is_fim_de_semana` | binário | `contexto_calendario` | `VARCHAR(12)` | feriado/fim de semana/dia útil |
| `target_ola` | binário histórico | `ocorrencia_ola` | `VARCHAR(8)` | 1=VIOLADO; 0=ATENDIDO |
| constante | — | `origem_dado` | `VARCHAR(64)` | versão lógica do dataset |
| constante | — | `arquivo_origem` | `VARCHAR(128)` | nome do arquivo landing |
| relógio ADF | timestamp | `data_processamento_utc` | `DATETIME(3)` | `currentUTC()` |

## Controles de qualidade

- Rejeitar hora fora do intervalo 0–23.
- Rejeitar `target_ola` diferente de 0/1.
- Rejeitar linhas sem médias móveis 7d/30d.
- Exigir correspondência semântica P2/P3 na tabela de regras; ausência no left join deve ser investigada antes da entrega.
- Manter os dois sinks derivados do mesmo stream para evitar versões divergentes.
- Registrar contagens de leitura, rejeição e escrita a partir do ADF Monitor.
