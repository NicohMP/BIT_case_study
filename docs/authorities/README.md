# Authorities (Knowledge Layer)

This project separates **model authorities** (explicit priors and rationales) from **market evidence** (Polymarket markets and their observed probabilities/volume).

The intent is methodological: if a reviewer disagrees with the system’s conclusions, they should be able to trace the disagreement to one of two places:

1) *Authority assumptions* (what the fund is exposed to; which macro families matter for which domains), or  
2) *Market evidence* (which markets were selected; what probabilities and liquidity were observed).

## What counts as an authority in this repo

### 1) Security → domain exposure (BIT priors)

- Scores: `data/authorities/security_domain_exposure_scores.md` (0–3)
- Rationales: `data/authorities/security_domain_exposure_rationale.md`

These encode the prior that a given security is structurally exposed to a macro domain (e.g. NVDA → Semis & Compute).

### 2) Signal-family → domain influence (macro transmission priors)

- Scores: `data/authorities/event_domain_scores.md` (0–5)
- Rationales: `data/authorities/event_domain_rationale.md`

These encode the prior that a given macro signal family transmits into a given domain (e.g. Taiwan risk → Semis & Compute).

## How these authorities are used

Operationally, the pipeline uses these artifacts to compute structural relevance:

- Market → Signal family (matching layer)
- Signal family → Domain (influence authority)
- Domain → Security (exposure authority)

The report generation step is downstream: the LLM is only asked to synthesize *from* the selected markets and these explicit authorities; it does not invent the authorities.

## Reading guide

- For a distilled interpretation of the matrices (what is “central” vs “domain-specific”), see `docs/authorities/insights.md`.
