# Repository Structure (Cleanup Notes)

This repo is still in a development phase, but it follows a stable separation between:

- **Core library code** (`polyscanner/`): ingestion, filtering, matching, scoring, reporting, and the web UI.
- **Operational entrypoints** (`scripts/`, `ops/`): CLI scripts and a Docker-based scheduler to run Steps 1→4b and generate reports.
- **Database schema** (`supabase/`): migrations and seeds.
- **Authorities (explicit assumptions)** (repo root markdown files): small matrices + rationales that encode the fund’s priors.
- **Reviewer docs** (`docs/`): navigation, reproducibility, and reading notes.

## Why some “knowledge” files live at repo root

The authority markdown files are referenced by seeding scripts and report-pack construction using default paths under:

- `data/authorities/event_domain_scores.md`, `data/authorities/event_domain_rationale.md`
- `data/authorities/security_domain_exposure_scores.md`, `data/authorities/security_domain_exposure_rationale.md`

They should be read conceptually as part of the authority layer. The curated reading guide is in `docs/authorities/`.

## Generated artifacts

- `reports/`: run outputs (context packs, audits, rendered reports). Typically not committed.
- `logs/`: scheduler logs. Local only.
