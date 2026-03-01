# Authority Insights (Reading Notes)

This note is a compact reading guide for the two authority matrices that anchor the system:

- `data/authorities/event_domain_scores.md` / `data/authorities/event_domain_rationale.md` (signal families → domains)
- `data/authorities/security_domain_exposure_scores.md` / `data/authorities/security_domain_exposure_rationale.md` (securities → domains)

The purpose is not to repeat the full rationale tables, but to make their *structure* legible at a glance.

## 1) Signal families: central vs domain-specific transmission

The influence matrix in `data/authorities/event_domain_scores.md` is intentionally interpretable: it makes explicit which macro families are broad (high influence across many domains) versus narrow (high influence in one domain).

**Broad / “central” families (high across most domains):**
- Monetary policy surprises (FOMC): high influence in AI & Big Tech and Cloud / Dev, and material influence elsewhere.
- Real yields / long rates: similarly broad.

These families are structurally high-centrality and, empirically, they also tend to be liquid on Polymarket. The combination explains why naive ranking often over-selects rate-like markets and why diversified selection (Step 4b) is necessary for analyst usefulness.

**Domain-specific families (high in a targeted domain):**
- US–China semiconductor export controls: highest in Semis & Compute.
- Taiwan geopolitical risk: highest in Semis & Compute.
- Crypto regulation regime changes: highest in Crypto Infra (and secondary in Fintech / CFP).
- Healthcare policy (reform, reimbursement): highest in Digital Health.
- Consumer credit conditions / cycle: highest in Fintech / CFP.

**“Cross-cutting but not universal” families:**
- AI regulation + Big Tech enforcement: strongest in AI & Big Tech (and material in Cloud / Dev and Digital Health).
- Antitrust (platforms, app stores, ad markets): strongest in AI & Big Tech and material in Cloud / Dev.
- Data-center power / grid constraints: material in AI & Big Tech and Cloud / Dev, and structurally strong in Crypto Infra.
- IT spending cycle (enterprise / cloud / AI): strongest in Cloud / Dev with material spillovers.

## 2) Security exposures: how BIT priors are encoded

The exposure table in `data/authorities/security_domain_exposure_scores.md` encodes a sparse, reviewable prior for each security.

Examples (illustrative rows from the table):
- NVIDIA Corp: core Semis & Compute exposure, material AI exposure.
- Microsoft / Amazon: core Cloud & Software Infra exposure with material AI adjacency.
- Taiwan Semiconductor / Micron: core Semis & Compute exposure.
- Coinbase / Hut 8 / Bitmine: core Crypto Mining & Infra exposure, with Coinbase also having material Fintech exposure.
- Oscar Health / Hinge Health: core Digital Health exposure.
- Robinhood / Lemonade / Kaspi.kz: core Fintech exposure (with varying secondary infrastructure exposure).

These priors are intentionally not optimized on outcomes: they are meant to be debated and edited by an analyst, with the rationale text serving as the audit trail of *why the prior exists*.

## Why this “authority-first” presentation matters

The system’s goal is not to predict equity returns from Polymarket, but to produce a structured monitoring surface:

- authorities define *what should matter* structurally for the fund,
- markets provide *what is currently being priced and traded*,
- selection ensures the analyst sees a diversified, interpretable subset rather than a single dominant macro cluster.
