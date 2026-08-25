SELECT COUNT(*) AS total_registros,
       COUNT(DISTINCT incident_feature_id) AS chaves_unicas,
       MIN(data_processamento_utc) AS primeira_carga,
       MAX(data_processamento_utc) AS ultima_carga
FROM fato_incidente_predictfy;

SELECT contexto_calendario, ocorrencia_ola,
       COUNT(*) AS quantidade,
       AVG(rolling_7d) AS media_movel_7d,
       AVG(rolling_30d) AS media_movel_30d
FROM fato_incidente_predictfy
GROUP BY contexto_calendario, ocorrencia_ola
ORDER BY contexto_calendario, ocorrencia_ola;

SELECT *
FROM fato_incidente_predictfy
ORDER BY data_processamento_utc DESC
LIMIT 20;
