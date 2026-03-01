BEGIN;

-- =========================
-- 1) Domain
-- =========================
CREATE TABLE IF NOT EXISTS bit_domain (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- =========================
-- 2) Mapping: Security ↔ Domain
-- =========================
CREATE TABLE IF NOT EXISTS bit_security_domain (
    security_id BIGINT NOT NULL
        REFERENCES bit_security(id)
        ON DELETE CASCADE,
    domain_id BIGINT NOT NULL
        REFERENCES bit_domain(id)
        ON DELETE CASCADE,

    PRIMARY KEY (security_id, domain_id)
);

CREATE INDEX IF NOT EXISTS ix_bit_security_domain_domain_id
    ON bit_security_domain(domain_id);

CREATE INDEX IF NOT EXISTS ix_bit_security_domain_security_id
    ON bit_security_domain(security_id);

COMMIT;
