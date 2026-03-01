# Authorities (Source-of-Truth Assumptions)

This project is intentionally built around explicit, reviewable “authorities”: small matrices and written rationales that encode the priors the system uses to translate Polymarket markets into BIT-relevant signals.

## Canonical authority files

- Signal-family → domain influence:
  - `data/authorities/event_domain_scores.md`
  - `data/authorities/event_domain_rationale.md`
- Security → domain exposure (BIT priors):
  - `data/authorities/security_domain_exposure_scores.md`
  - `data/authorities/security_domain_exposure_rationale.md`

## How to read them

- Conceptual guide (what the matrices imply, and why Step 4b diversification exists): `docs/authorities/insights.md`
- Authority-layer overview: `docs/authorities/INDEX.md`
