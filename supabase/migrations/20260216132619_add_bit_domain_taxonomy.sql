
BEGIN;

-- =========================
-- 1) Domain (Level 1)
-- =========================
CREATE TABLE IF NOT EXISTS bit_domain (
    id BIGSERIAL PRIMARY KEY, -- 
    name TEXT NOT NULL UNIQUE,
    description TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================
-- 2) Subdomain (Level 2)
-- =========================
CREATE TABLE IF NOT EXISTS bit_subdomain (
    id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT NOT NULL
        REFERENCES bit_domain(id)
        ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_bit_subdomain UNIQUE (domain_id, name)
);

CREATE INDEX IF NOT EXISTS ix_bit_subdomain_domain_id
    ON bit_subdomain(domain_id);


-- =========================
-- 3) Mapping: Security ↔ Subdomain
-- =========================
CREATE TABLE IF NOT EXISTS bit_security_subdomain (
    security_id BIGINT NOT NULL
        REFERENCES bit_security(id)
        ON DELETE CASCADE,
    subdomain_id BIGINT NOT NULL
        REFERENCES bit_subdomain(id)
        ON DELETE CASCADE,

    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    weight NUMERIC(5,2) NULL, -- optional exposure weight (e.g., % revenue)

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (security_id, subdomain_id),

    CONSTRAINT chk_weight_range
        CHECK (weight IS NULL OR (weight >= 0 AND weight <= 100))
);

CREATE INDEX IF NOT EXISTS ix_bit_security_subdomain_subdomain_id
    ON bit_security_subdomain(subdomain_id);

CREATE INDEX IF NOT EXISTS ix_bit_security_subdomain_security_id
    ON bit_security_subdomain(security_id);

COMMIT;
