CREATE TABLE IF NOT EXISTS execucao_analitica (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    correlation_id CHAR(36) NOT NULL,
    modelo VARCHAR(80) NOT NULL,
    horizonte VARCHAR(20) NOT NULL,
    segmento VARCHAR(40) NOT NULL,
    valor_previsto DECIMAL(14,4) NOT NULL,
    origem_artefato VARCHAR(160) NOT NULL,
    artefato_sha256 CHAR(64) NOT NULL,
    executado_em_utc TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_execucao_correlation (correlation_id),
    KEY ix_execucao_modelo_data (modelo, executado_em_utc),
    CONSTRAINT ck_execucao_valor_nao_negativo CHECK (valor_previsto >= 0)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
