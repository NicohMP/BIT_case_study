# Authorities (Canonical Inputs)

This directory contains the **canonical authority inputs** used by the pipeline.

These files are intentionally human-readable and version-controlled: they encode the priors the system uses to translate Polymarket markets into BIT-relevant signals.

## Files

### Signal-family → domain influence (0–5)

- `event_domain_scores.md`: numeric influence scores (0..5) for each (signal family, domain) pair.
- `event_domain_rationale.md`: written rationales (with references) for each cell of the matrix.

### Security → domain exposure (0–3)

- `security_domain_exposure_scores.md`: exposure scores (0..3) per BIT security and macro domain.
- `security_domain_exposure_rationale.md`: per-security exposure rationales (why each exposure prior is assigned).

## Notes

- The seeding scripts default to these paths, but accept overrides via CLI flags.
- For a conceptual reading guide, see `docs/authorities/insights.md`.
