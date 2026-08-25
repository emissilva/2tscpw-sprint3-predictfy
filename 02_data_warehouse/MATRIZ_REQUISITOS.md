# Matriz de requisitos — Data Warehouse

| Requisito oficial | Implementação e evidência | Estado |
|---|---|---|
| 1. Arquitetura e descrição | Diagrama com ícones oficiais Azure, descrição no DOCX/PDF e fonte `arquitetura_ingestao.drawio` | Concluído |
| 2. Infraestrutura PaaS | RG exclusivo com ADF, Storage e MySQL; inventário em `evidencias/azure/01_recursos_paas.*` | Concluído |
| 3. Data Flow e descrição | JSON publicado, canvas fiel reconstruído e expressões em `evidencias/azure/07_dataflow_publicado.json` | Concluído |
| 4. Colunas derivadas | Dez derivações documentadas em `colunas_derivadas.txt` e no relatório | Concluído |
| 5. Pipeline e persistência | Duas cargas `Succeeded`; MySQL e TXT com 25.588 linhas; evidências 09–14 | Concluído |
| 6. Comentários finais | Resultados, dificuldades e descarte descritos no DOCX/PDF | Concluído |

Aceites adicionais: zero prioridades sem regra, 25.588 chaves únicas, reexecução idempotente e ausência de segredos nas evidências.
