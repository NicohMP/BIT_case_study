# Polymarket Signal Scanner
## Architecture and Quantitative Framework

**AI Engineering Intern Case Study**  
**Date:** March 2026

## Introduction

The goal of this case study is to design and implement a Polymarket scanning tool capable of producing automatic reports on relevant prediction markets and explaining how they inform BIT’s current holdings.

The ambition is not simply to summarize markets. The objective is to structure the reasoning process: why should a given market matter for a given stock, through which economic channel, and how much attention should it deserve right now?

The system is therefore designed as a transmission model from prediction markets to portfolio-level impact.

**Contributions (v1).** The delivered system is an end-to-end Polymarket scanning pipeline that (i) ingests active markets on a schedule, (ii) filters and matches them into a small set of economically motivated macro signal families, (iii) propagates these signals through a transparent domain–exposure model to compute security relevance, (iv) applies an explicit selection layer to produce a diversified shortlist for analysts, and (v) generates grounded, schema-constrained signal reports at request time using an LLM.

The methodological choice is to privilege **inspectability over black-box prediction**: every intermediate decision is persisted, versioned, and queryable, so that iteration can be driven by evidence rather than narrative.

### Prediction Markets as Sentiment Signals

A key modeling assumption in this project is that prediction markets are not primarily used as “truth predictors”. Their value for public markets comes from the fact that they aggregate a form of *crowd belief* and *positioning* on discrete events. Even when forecasting accuracy is imperfect, changes in implied probabilities and participation can reveal shifts in market expectations.

For this reason, the system explicitly separates (i) *structural relevance* (does this event transmit to a given stock?) from (ii) *sentiment intensity* (how much attention and belief revision is occurring right now?).

## BIT Knowledge Modeling

### Framing the Problem

The first difficulty of this project is framing.

It is impossible to account for every event that could affect BIT’s investments — there are simply too many. The complexity of equity price dynamics is such that they can almost be viewed as stochastic processes influenced by countless interacting variables.

Instead of attempting completeness, we deliberately impose structure. The idea is to focus on the main industry domains in which BIT invests and to model how major macro signals propagate into those domains.

This is a modeling choice: we trade completeness for interpretability and tractability.

### Portfolio Data Collection

To define the relevant industry domains, we:

1. Collected up-to-date information on BIT Capital’s public equity holdings (SEC filings when available, aggregated holdings from public sources, historical and current portfolio composition).
2. Selected the most significant positions based on raw investment value and relative portfolio exposure.
3. Identified recurring industry themes across major holdings.

This led to the following working taxonomy:

- AI and Data Platforms
- Semiconductors and Compute
- Cloud and Software Infrastructure
- Crypto Mining and Infrastructure
- Fintech
- Digital Health

This taxonomy is not meant to be exhaustive or permanent. It is a first structured abstraction of BIT’s investment universe.

### Stock-to-Domain Exposure

Each stock $s$ is assigned a domain exposure vector:

$$
E_D(s) \in \mathbb{R}^{D}
$$

where $D$ is the number of macro domains.

Each component reflects the relative economic exposure of the company to that domain, based on revenue drivers, strategic positioning, and business model structure.

In v1, these exposure vectors are treated as **explicit priors** rather than learned parameters: they are meant to be stable, reviewable, and open to analyst critique. The exposure scores and their written justifications are provided as artifacts (`data/authorities/security_domain_exposure_scores.md` and `data/authorities/security_domain_exposure_rationale.md`), so that the model’s assumptions are inspectable independently of any single Polymarket market.

### Signal Families

Once domains are defined, we introduce structured macro signal families that are known to materially affect them.

Examples include federal Reserve rate decisions, US–China semiconductor policy, Taiwan geopolitical risk, AI regulation, trade tariffs, etc. The purpose is to channel the diversity of Polymarket events into a finite and interpretable set of macro drivers.

The choice of this signal basis is deliberately *small*: the goal is not to enumerate all conceivable catalysts, but to cover a tractable set of recurring macro channels that (i) plausibly transmit into BIT’s core domains, (ii) appear frequently enough on Polymarket to be monitored continuously, and (iii) can be defended with explicit economic rationales rather than post-hoc narrative.

Concretely, each family is documented with a written justification and domain-level transmission arguments (with references) in `data/authorities/event_domain_rationale.md`. This is the layer that makes the signal set inspectable: it states *why* a given family should matter for a given domain before any market-level matching is performed.

### Signal-to-Domain Influence Matrix

We encode the structural influence of signal families on macro domains via:

$$
W_S \in \mathbb{R}^{F \times D}
$$

where $F$ is the number of signal families and $D$ the number of macro domains. Each element $W_{fd}$ represents the strength of influence (on a 0–5 scale) of signal family $f$ on domain $d$.

Each influence score is stored with:

- A written rationale
- Supporting public references

This ensures transparency and allows analysts to inspect and refine the model’s assumptions.

## Filtering Layer

### Market Fetching

Active markets are retrieved from the Polymarket Gamma API and stored in a Postgres database. For time-series analysis, the system can also persist daily snapshots (UTC day) of market probability and liquidity metrics, which later enables $\Delta p$-based movement features.

### Filtering Strategy

Filtering occurs in two stages:

1. **Hard Rule Filtering**  
   A deterministic first layer removes clearly irrelevant markets (sports, entertainment, micro-bets, etc.) based on curated rejection rules. Each decision is stored with explicit reasons and a `filter_version`, making the retained universe auditable.
2. **Signal-Family Matching (Discovery → Rule Confirmation)**  
   Each kept market is associated to one (or a few) macro signal families via a two-step mechanism:
   (i) *candidate discovery* (lexical hits and/or embedding similarity to family descriptors), followed by  
   (ii) *deterministic rule classification* that confirms strict matches and prevents broad semantic leakage.
   
   Embeddings are computed locally with a small sentence-transformer (MiniLM), which keeps this stage inexpensive and avoids relying on an LLM for discovery.

For each market $m$, we compute:

$$
r(m) \in \mathbb{R}^{F}
$$

where $r_f(m)$ captures the strength of evidence that market $m$ maps to signal family $f$ (from lexical/embedding discovery and/or strict rule matches).

This balances speed, coverage, and the ability to detect abstract relationships.

## Relevance Score

The first filtering steps aim only at removing the obviously irrelevant markets. Now using the signal families and industry domain framework, we can refine our filtering logic and align it with actual financial knowledge. The idea is to use the influence quantifiers defined earlier to build a *relevance score* for each market, with respect to the stock/company we're interested in. The transmission chain is:

$$
\text{Market} \rightarrow \text{Signal} \rightarrow \text{Domain} \rightarrow \text{Stock}
$$

Let:

- $r(m)$ = market-to-signal match evidence vector
- $W_S$ = signal-to-domain influence matrix
- $E_D(s)$ = stock-to-domain exposure vector

We define structural relevance as:

$$
\text{Relevance}(m,s) = r(m)^\top W_S E_D(s)
$$

This measures how strongly a market structurally transmits into a given stock. Using this score, the markets with most relevance are informative because:

- Their subjects can't be unrelated to the investments of BIT (hard filter).
- They are linked to a macro signal family through a versioned matching layer (lexical + embedding discovery, then deterministic rule confirmation).
- They affect one or several industry domains that the company evolves in ($r(m)^\top W_S$).
- The relevance of the signals and domains are quantified and explainable.

## Sentiment Intensity Layer

Structural relevance explains why a market matters economically. However, not all structurally relevant markets are equally informative at a given time.

We therefore define a *sentiment intensity function* $g(m)$, which measures how much informational pressure a market currently exerts. Conceptually, a prediction market is informative when: (i) participation is meaningful, (ii) beliefs are moving, and (iii) resolution is near enough to matter for positioning.

Let:

- $\mathrm{vol}_m$ = current traded volume,
- $p_t$ and $p_{t-\Delta}$ = current and lagged implied probabilities,
- $\tau_m$ = time-to-expiry in days.

Define $\Delta p_m = |p_t - p_{t-\Delta}|$. We set:

$$
g(m)=
\mathrm{clip}\!\left(
\frac{\log(1+\mathrm{vol}_m)}{\log(1+\mathrm{vol}_{95})},0,1
\right)
\cdot
\left(1-\exp(-k_{\Delta}\Delta p_m)\right)
\cdot
\exp(-\tau_m/\tau_0).
$$

### Interpretation

The first term captures participation with log-compression to avoid heavy-tail dominance. The second term captures belief revision; the exponential form is approximately linear for small moves and saturates for large shocks. The third term discounts distant events, reflecting the greater relevance of near-term catalysts.

The final ranking score remains:

$$
\mathrm{FinalScore}(m,s)=\mathrm{Relevance}(m,s)\times g(m),
$$

which cleanly separates structural transmission from real-time informational intensity.

**Implementation note (v1):** the system currently treats $\Delta p$ as optional. Participation and urgency are always available from the live market object; movement requires a mature, reliably sampled probability history. In practice, the pipeline persists daily snapshots (when enabled) and computes $\Delta p$ when possible, but does not rely on it as a hard requirement for ranking stability.

## LLM Report Generation

The LLM is used strictly as a synthesis layer. It is not involved in ingestion, filtering, matching, ranking, or selection. All discovery and scoring logic is deterministic and stored in Postgres with explicit versioning.

At report time, the system constructs a structured context pack containing: the security exposure vector $E_D(s)$, the relevant slice of the influence matrix $W_S$ with rationales, the selected markets with probabilities and liquidity metrics, market-to-family match strengths $r(m)$, and the precomputed ranking scores.

The LLM therefore reasons on grounded, ranked inputs rather than raw Polymarket text. No external retrieval is allowed.

The model outputs structured JSON containing transmission chains, magnitude and timeline assessments, monitoring signals, and thematic synthesis. The final Markdown report is rendered deterministically from this JSON schema.

Methodologically, the LLM is treated as a constrained synthesis component with a strict contract: it only receives the deterministic context pack assembled from Postgres (no browsing, no external retrieval), and it must return a structured JSON object matching a fixed schema (transmission chain, timing, magnitude, monitoring signals, and citations to the provided markets). The output is validated and audited against the context pack, and the final report is rendered deterministically. This makes failure modes legible (schema violations, unsupported claims) rather than silently persuasive.

This separation ensures that generative reasoning is constrained to interpretation, while filtering, scoring, and prioritization remain reproducible and auditable. LLM calls are triggered only on demand, keeping background processing lightweight and operational cost predictable.

## User Interface

The web interface is intentionally minimal in v1: it acts as an analyst console on top of the versioned database tables. In practice, it supports a watchlist of securities, browsing of kept/selected markets with their scores, and inspection (and on-demand generation) of persisted signal reports.

Crucially, the UI is not the authoring surface for the economic model. Domain definitions, exposure vectors, and influence rationales are treated as explicit data artifacts (seeded into Postgres and documented in Markdown), which preserves reviewability and avoids ad-hoc UI edits.

## Pipeline Execution Summary

The system operates in two distinct modes: continuous background processing and on-demand report generation.

### Background Pipeline

At regular intervals (scheduled every 2 hours in the local demo setup), the system:

1. Fetches all active Polymarket markets via the Gamma API.
2. Applies deterministic hard filters and stores explicit keep/reject decisions with reasons.
3. Runs signal-family matching (lexical + embedding discovery, then strict rule confirmation).
4. Updates structural relevance scores, then computes a diversified selection for each monitored security.
5. Optionally records daily snapshot rows (for later $\Delta p$ / movement features).

This background layer maintains a continuously updated, structured representation of all candidate markets without requiring any LLM inference.

### On-Demand Report Generation

When an analyst requests a report for a given stock, the system:

1. Retrieves the top-ranked markets according to $\text{FinalScore}(m,s)$.
2. Gathers transmission data ($r(m)$, $W_S$, $E_D(s)$) and stored rationales.
3. Constructs a structured prompt and calls the LLM.
4. Returns a formatted analyst-ready report.

### Design Rationale

This two-speed architecture is intentional. Embedding similarity and scoring are computationally inexpensive and can be run continuously in the background. LLM inference, which is significantly more expensive and latency-sensitive, is triggered only when high-level reasoning is required.

At the current scale of Polymarket activity (tens of thousands of active markets), the background pipeline remains lightweight because it relies on local embedding similarity and deterministic database upserts, while report generation incurs a few seconds of latency per request. In practice, a representative audited run (Feb 26, 2026) confirms the intended order-of-magnitude reduction: from $10^4$–$10^5$ ingested markets down to $10^4$ kept markets, then to $10^3$–$10^4$ structurally scored rows, and finally a few hundred selected markets that are suitable as grounded inputs for report-time reasoning.

## Implementation Status and System Evidence (v1)

### Positioning

The preceding sections describe the conceptual and quantitative framework of the Polymarket Signal Scanner. This section documents the **implemented v1 system**, its current scale, artifacts, and known limitations.

### Delivered Components (as of Feb 26, 2026)

**End-to-end pipeline implemented:**

- **Ingestion:** Periodic fetch from Polymarket Gamma API (`/events`) persisted to:
  - `pm_event`
  - `pm_market`
- **Hard filtering (deterministic):** Rule-based rejection/retention decisions stored in `pm_market_filter_decision` with explicit `filter_version`.
- **Market → Signal matching:** Lexical discovery + deterministic rules (+ optional embeddings), stored in `pm_market_signal_family_match` with `matcher_version`.
- **Security relevance scoring:** Structural transmission model implemented and persisted in `pm_market_security_relevance` with `scoring_version`.
- **Selection layer:** Event-level deduplication and diversification caps stored in `pm_market_security_relevance_selection` with `selection_version`.
- **Report-time LLM (on-demand only):** Structured context pack → JSON → Markdown report, persisted in `pm_security_signal_report`.
- **Web UI (minimal demo):** FastAPI app to manage a watchlist, browse kept/selected markets, and view/generate reports.

**Reproducibility.** The concrete commands to (i) refresh the pipeline state, (ii) open the web UI, (iii) generate one report, and (iv) run audits are provided in `README.md` and in `docs/reviewer/reproducibility.md`.

**Example artifact:**

- `reports/security_signal_report_NVDA_20260226_160048.md`

### Scale and Scheduling

**Ingestion scale (order of magnitude):**

- Total active events ingested per refresh: on the order of $10^4$
- Total linked markets ingested per refresh: on the order of $10^4$–$10^5$
- Markets retained post hard-filter: on the order of $10^4$ (roughly 20% retention)

**Scheduling mechanism (local demo):**

The background refresh runs every ~2 hours via a Docker scheduler container (`ops/docker/`). Each run performs ingestion, filtering, matching, scoring, and selection. LLM inference is performed **only at report generation time**.

### Database Queryability (Proof of System Reality)

All intermediate decisions are stored and versioned.

**Example: Count relevance rows for a scoring version**

```sql
	select count(*)
	from pm_market_security_relevance
	where scoring_version='<your_scoring_version>';
```

**Example: Selected markets for NVDA**

```sql
	select rank, market_id, final_score
	from pm_market_security_relevance_selection
	where security_id = (
	  select id from bit_security where ticker='NVDA'
	)
	and scoring_version='<your_scoring_version>'
	and selection_version='<your_selection_version>'
	order by rank;
```

This ensures the system is not heuristic or opaque: every filtering, matching, and scoring decision is queryable.

### Market Strength and Sentiment Intensity (Current State)

The theoretical framework defines a sentiment intensity function $g(m)$ based on $\Delta p$ and time-to-expiry.

**Current implementation (v1):**

- A sentiment proxy (exposed as `market_strength` and a decomposed $g(m)$) based primarily on liquidity/volume and time-to-expiry (urgency).
- An optional movement factor based on $\Delta p$ when daily snapshots are available.
- Daily snapshot storage (`pm_market_daily_snapshot`) is implemented to support this, but can be toggled operationally.

Thus, v1 already supports movement-aware intensity when the data is present, while remaining robust to missing history by defaulting to participation × urgency.

### Results Snapshot (Representative Run)

Representative run (`2026-02-26T16:56:49.522177+00:00`):

| Stage | Persisted table | Typical reduction | Versioned by |
|---|---|---:|---|
| Ingestion | `pm_event`, `pm_market` | $10^4$ events; $10^4$–$10^5$ markets | (run metadata) |
| Hard filters | `pm_market_filter_decision` | $\sim 80\\%$ rejected | `filter_version` |
| Family matching | `pm_market_signal_family_match` | minority of kept markets matched | `matcher_version` |
| Relevance scoring | `pm_market_security_relevance` | $10^3$–$10^4$ scored rows | `scoring_version` |
| Diversified selection (Step 4b) | `pm_market_security_relevance_selection` | few hundred selected rows | `selection_version` |
| Reports (on demand) | `pm_security_signal_report` | per-request | `prompt_version` + model |

- Match rows generated: `7022`
- Security-market relevance rows: `3910`
- Selected rows (post dedupe/caps): `400`
- Report artifacts present in-repo: `35` Markdown reports (`11` JSON sources)

For example, for NVDA:

- Top ranked market final score: `0.771`
- Second ranked market final score: `0.771`
- Third ranked market final score: `0.765`

### Learnings and Iteration

Key implementation insights:

- **Dominant macro families (FOMC / rates) naturally crowd out others.**  
  Once the system ingests *actual* Polymarket markets (as opposed to a curated toy set), it becomes clear that rates and Fed-related templates occupy a structurally privileged position in the ranking. This is not merely a modeling artifact: these markets tend to be liquid, widely traded, and—through the discount-rate channel—have broad macro transmission to most equity domains. If one naively ranks markets by a relevance × intensity score, the resulting top-$k$ becomes a near-monoculture of rate-like questions.
  
  This observation is the direct motivation for the Step 4b *selection layer*: a diversified, event-aware shortlist is more useful to an analyst than the mechanically “top” markets. Concretely, Step 4b enforces deduplication at the event level and applies diversification caps so that high-volume, high-centrality families (rates) do not fully crowd out narrower but economically interpretable catalysts (e.g. Taiwan risk, AI regulation, crypto regime changes).
  
  In the representative audited run, this effect is visible mechanically: pre-selection top-20 lists for many tickers are dominated by rate-like questions, while the diversified selection reduces the rate-like share to a small minority and reintroduces idiosyncratic catalysts without sacrificing auditability.

- **Discovery must be permissive; confirmation must be strict.**  
  The matching layer is intentionally asymmetric: embedding/lexical discovery is designed to be high-recall (so that abstractly phrased markets are not missed), but this inevitably introduces semantic leakage—especially into macro families with broad language. The practical resolution is to separate discovery from deterministic rule confirmation and to tune thresholds with audit feedback, rather than relying on embedding similarity as a final classifier.

- **$\Delta p$ is a data constraint before it is a modeling choice.**  
  The conceptual intensity function uses belief movement, but the Gamma API is fundamentally “spot”: it provides current probabilities reliably, not a mature time series. A movement term is therefore only meaningful once the system has accumulated sufficient historical sampling.
  
  The implemented solution is to persist daily market snapshots and compute $\Delta p$ from lagged probabilities when coverage exists. This implies a cold-start period (the first days of deployment) during which movement is either unavailable or noisy; in that regime, v1 falls back to participation × urgency so that ranking remains stable. The movement factor becomes informative only after repeated ingestion iterations have produced a consistent snapshot history.

- **Audit tables accelerate iteration.**  
  Making each intermediate decision queryable (filter reasons, match methods, scoring and selection versions) turns “why are we seeing these markets?” from a subjective debate into a debuggable pipeline. In practice, this is what enables systematic refinement of thresholds, caps, and rule definitions rather than ad-hoc prompt edits.

This addendum demonstrates that the conceptual framework presented earlier is implemented as a deterministic, versioned, and queryable system.
