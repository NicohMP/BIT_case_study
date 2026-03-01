# Documentation Index

This folder organizes reviewer-facing documentation and clarifies where the project’s “authority” assumptions live.

## Core case-study narrative

- `project_report.md` (repo root): architecture, quantitative framing, and implementation evidence.
  - Note: the internship prompt / evaluation rubric is not included in this repo.

## Authority layer (source-of-truth assumptions)

The system is intentionally built around explicit, inspectable “authorities”: small matrices and rationales that encode *priors* about how macro signals transmit into BIT’s holdings.

- Signal-family → domain influence:
  - `data/authorities/event_domain_scores.md` (0–5 influence scores)
  - `data/authorities/event_domain_rationale.md` (cell-level rationales with references)
- Security → domain exposure (BIT priors):
  - `data/authorities/security_domain_exposure_scores.md` (0–3 exposure scores)
  - `data/authorities/security_domain_exposure_rationale.md` (per-security exposure rationales)

Reading guide and distilled takeaways:
- `docs/authorities/INDEX.md`
- `docs/authorities/insights.md`

Quick entrypoint:
- `AUTHORITIES.md`

## Reviewer runbook

- `docs/reviewer/reproducibility.md`: how to reproduce one refresh + one report + audits locally, and where evidence artifacts are written.

## Repo map

- `docs/repo_structure.md`: where things live and why.
