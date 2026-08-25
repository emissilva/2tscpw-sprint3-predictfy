SELECT COUNT(*) AS total_registros,
       COUNT(DISTINCT incident_feature_id) AS chaves_unicas,
       SUM(prioridade_desc IS NULL) AS prioridades_sem_regra
FROM fato_incidente_predictfy;

SELECT prioridade_codigo,
       prioridade_desc,
       ola_limite_horas,
       COUNT(*) AS quantidade
FROM fato_incidente_predictfy
GROUP BY prioridade_codigo, prioridade_desc, ola_limite_horas
ORDER BY prioridade_codigo;
