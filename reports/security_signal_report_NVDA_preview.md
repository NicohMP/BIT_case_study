# NVIDIA (NVDA) Signal Report

_As of_: `2026-02-26T12:06:44.731316+00:00`
_Pipeline_: filter `hard_filters_v8`, matcher `matcher_v10`, scoring `relevance_v5`, selection `selected_v1`, prompt `security_signal_report_v1`, model `gemini-2.0-flash`

<details>
<summary>Run metadata</summary>

- run_id: `57bfd305-0c3c-49d4-a6c1-28d507197857`
</details>

**Security:** `NVDA` — NVIDIA Corp (XNAS)

## Executive Summary
Top signals: **Will Trump nominate Judy Shelton as the next Fed chair?** (magnitude: medium; timeline: quarters; actionability: High); **Will China blockade Taiwan by June 30?** (magnitude: medium; timeline: quarters; actionability: High); **Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?** (magnitude: low; timeline: days; actionability: Medium).

## Top Signals
### 1) Will Trump nominate Judy Shelton as the next Fed chair?

**Event:** Who will Trump nominate as Fed Chair?
_Snapshot:_ resolves `2026-12-31T00:00:00+00:00` (307d); volume $95.83M; liquidity $1.40M; structural relevance High; actionability High; confidence High; magnitude medium; timeline quarters.

**Why it matters.** This market reflects potential changes in monetary policy, which influences valuations of long-duration assets like NVDA. The base score of 0.7714 reflects this relevance.
**Why now.** With high market strength (0.94) and substantial liquidity ($1.39M), this market offers a clear signal and tradable opportunity until the end of 2026.

**Transmission chain.** Market → **Monetary policy surprises (FOMC)** → macro domains → `NVDA`.

> **AI & Big Tech** — influence: High; exposure: 29%
> _Influence rationale:_ Event‑study work on FOMC surprises shows statistically significant negative stock returns when policy tightens unexpectedly, with growth and tech sectors generally more sensitive than defensives.
> _Exposure rationale:_ 2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform
>
> **Semis & Compute** — influence: Medium; exposure: 43%
> _Influence rationale:_ Monetary policy surprise studies document broad equity sensitivity, but manufacturing and cyclicals like semis have more mixed reactions because earnings cyclicality and global trade matter alongside discount‑rate effects.
> _Exposure rationale:_ 3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products
>

**What to watch.** Trump's public statements on Fed leadership; Confirmation hearings for Fed chair nominees.
**Key unknowns.** Trump's priorities for the Fed chair; Senate confirmation prospects for nominees.
_IDs:_ `market_id=572473, event_id=35908`

---

### 2) Will China blockade Taiwan by June 30?

_Snapshot:_ resolves `2026-06-30T00:00:00+00:00` (123d); volume $563.9k; liquidity $59.2k; structural relevance High; actionability High; confidence Medium; magnitude medium; timeline quarters.

**Why it matters.** This market directly addresses geopolitical risk in Taiwan, a critical region for semiconductor manufacturing, impacting NVDA's supply chain. The base score of 0.7428 reflects this relevance.
**Why now.** The market has moderate strength (0.795) and liquidity ($59k), offering a reasonable signal with a resolution date in June 2026.

**Transmission chain.** Market → **Taiwan geopolitical risk** → macro domains → `NVDA`.

> **Semis & Compute** — influence: High; exposure: 43%
> _Influence rationale:_ Taiwan‑focused studies emphasize that a large share of advanced fabrication sits on the island, and that quarantine/blockade scenarios could significantly disrupt global semiconductor supply.
> _Exposure rationale:_ 3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products
>
> **AI & Big Tech** — influence: Medium; exposure: 29%
> _Influence rationale:_ Research on Taiwan’s semiconductor industry highlights its centrality to advanced chip fabrication and the vulnerability of global supply chains to quarantine, blockade, or conflict scenarios in the Taiwan Strait.
> _Exposure rationale:_ 2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform
>

**What to watch.** Chinese military activity near Taiwan; Diplomatic statements from China and Taiwan; International response to escalating tensions.
**Key unknowns.** China's strategic goals regarding Taiwan; Effectiveness of international deterrence.
_IDs:_ `market_id=604470, event_id=46844`

---

### 3) Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?

**Event:** GPU rental prices (H100) hit___ in February?
_Snapshot:_ resolves `2026-02-28T00:00:00+00:00` (1d); volume $46.2k; liquidity $5.5k; structural relevance High; actionability Medium; confidence Low; magnitude low; timeline days.

**Why it matters.** This market reflects the IT spending cycle and demand for AI infrastructure, directly impacting NVIDIA's revenue from GPU rentals. The base score of 0.5714 reflects this relevance.
**Why now.** The market has moderate strength (0.576) and limited liquidity ($5.5k), offering a signal with a resolution date in February 2026.

**Transmission chain.** Market → **IT spending cycle (enterprise / cloud / AI)** → macro domains → `NVDA`.

> **Semis & Compute** — influence: Medium; exposure: 26%
> _Influence rationale:_ For semis & compute infra, the IT cycle links directly to data‑center and enterprise hardware demand: Gartner’s tables show data‑center systems as one of the fastest‑growing segments, reflecting AI server and infra build‑out.
> _Exposure rationale:_ 3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products
>
> **AI & Big Tech** — influence: Medium; exposure: 17%
> _Influence rationale:_ Big Tech’s cloud and enterprise segments ride the global IT and AI‑infra spending cycle, while consumer ads/commerce are driven by different forces, giving a mixed but important dependence.
> _Exposure rationale:_ 2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform
>

**What to watch.** Trends in GPU rental prices; Demand for AI compute resources; IT spending forecasts.
**Key unknowns.** Pace of AI adoption; Supply of GPUs; Economic conditions affecting IT budgets.
_IDs:_ `market_id=1322996, event_id=197059`

---

## Themes

**Taiwan Geopolitical Risk.** Several markets relate to the potential for conflict involving Taiwan, which could disrupt semiconductor supplies. (markets: 604470)

## What To Monitor Next
Monitor geopolitical tensions in the Taiwan Strait; Track IT spending forecasts and AI infrastructure demand; Watch for policy changes affecting AI and semiconductor industries.

## Notes
The pack contains multiple markets related to Taiwan geopolitical risk, but only one was selected to ensure diversity; The pack contains multiple markets related to FOMC surprises, but the maximum number of rate-like markets was reached, so the rest were excluded; Several markets were excluded due to low actionability based on their scores and liquidity.

## Appendix: Evidence & Metrics

### Metrics (raw)
| market_id | event_id | final_score | base_score | quality_mult | market_strength | confidence |
|---:|---:|---:|---:|---:|---:|---:|
| 572473 | 35908 | 0.771428571428572 | 0.771428571428572 | 1.0 | 0.9400000000000001 | 0.7 |
| 604470 | 46844 | 0.698826651740332 | 0.742857142857143 | 0.940728185035062 | 0.795442884424437 | 0.6 |
| 1322996 | 197059 | 0.441822230314528 | 0.571428571428572 | 0.773188903050423 | 0.5766501947463404 | 0.4 |

### Exclusions
- dropped_due_to_duplicate_event:
  - 567621: duplicate event
  - 701290: duplicate event
  - 956590: duplicate event
  - 677407: duplicate event
- dropped_due_to_rate_cap:
  - 654412: rate cap
  - 669660: rate cap
- dropped_due_to_low_actionability:
  - 540843: low actionability
  - 957986: low actionability
  - 1322973: low actionability
  - 676842: low actionability
  - 1302430: low actionability
  - 1228017: low actionability
  - 1426260: low actionability
  - 1068733: low actionability
  - 1108760: low actionability
  - 1426021: low actionability
  - 1058192: low actionability

<details>
<summary>Raw LLM JSON</summary>

```json
{
  "title": "NVIDIA (NVDA) Signal Report",
  "as_of_utc": "2026-02-26T12:06:44.731316+00:00",
  "versions": {
    "run_id": "57bfd305-0c3c-49d4-a6c1-28d507197857",
    "filter_version": "hard_filters_v8",
    "matcher_version": "matcher_v10",
    "scoring_version": "relevance_v5",
    "selection_version": "selected_v1",
    "prompt_version": "security_signal_report_v1",
    "model": "gemini-2.0-flash"
  },
  "security": {
    "security_id": 17,
    "ticker": "NVDA",
    "company_name": "NVIDIA Corp",
    "exchange_mic": "XNAS"
  },
  "top_markets": [
    {
      "market_id": 572473,
      "event_id": 35908,
      "question": "Will Trump nominate Judy Shelton as the next Fed chair?",
      "event_title": "Who will Trump nominate as Fed Chair?",
      "probability": null,
      "end_date": "2026-12-31T00:00:00+00:00",
      "volume_usd": 95830591.522875,
      "liquidity_usd": 1396847.99502,
      "scores": {
        "final_score": 0.771428571428572,
        "base_score": 0.771428571428572,
        "quality_multiplier": 1.0,
        "market_strength": 0.9400000000000001
      },
      "structural_relevance": "This market reflects potential changes in monetary policy, which influences valuations of long-duration assets like NVDA. The base score of 0.7714 reflects this relevance.",
      "actionability": "With high market strength (0.94) and substantial liquidity ($1.39M), this market offers a clear signal and tradable opportunity until the end of 2026.",
      "transmission_chain": [
        {
          "signal_family_id": 1,
          "slug": "fomc_surprises",
          "title": "Monetary policy surprises (FOMC)",
          "method": "rule_classification",
          "match_strength": 1.0,
          "domains": [
            {
              "macro_domain_id": 1,
              "macro_domain_name": "AI & Big Tech",
              "family_influence_score": 5,
              "security_exposure_weight": 0.285714285714286,
              "edge_rationale": "Event‑study work on FOMC surprises shows statistically significant negative stock returns when policy tightens unexpectedly, with growth and tech sectors generally more sensitive than defensives.",
              "exposure_rationale": "2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform"
            },
            {
              "macro_domain_id": 2,
              "macro_domain_name": "Semis & Compute",
              "family_influence_score": 3,
              "security_exposure_weight": 0.428571428571429,
              "edge_rationale": "Monetary policy surprise studies document broad equity sensitivity, but manufacturing and cyclicals like semis have more mixed reactions because earnings cyclicality and global trade matter alongside discount‑rate effects.",
              "exposure_rationale": "3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products"
            },
            {
              "macro_domain_id": 3,
              "macro_domain_name": "Cloud / Dev",
              "family_influence_score": 5,
              "security_exposure_weight": 0.142857142857143,
              "edge_rationale": "High‑duration SaaS / cloud names behave like textbook “long‑duration equities”: event‑driven sell‑offs around hawkish surprises have repeatedly hit this segment hardest in practice.",
              "exposure_rationale": "1 – It offers DGX Cloud and enterprise AI software (NVIDIA AI Enterprise, NIM microservices), but these are still extensions riding on its hardware franchise rather than a hyperscaler‑scale cloud business, so infra SaaS is important but not dominant. NVIDIA AI Enterprise & DGX cloud pages via same hub"
            },
            {
              "macro_domain_id": 4,
              "macro_domain_name": "Crypto Infra",
              "family_influence_score": 3,
              "security_exposure_weight": 0.142857142857143,
              "edge_rationale": "Crypto infra equities are not classic DCF assets, but empirical work and market commentary show that FOMC surprises still transmit via global risk appetite and liquidity, affecting exchange volumes and miner financing conditions.",
              "exposure_rationale": "1 – Historically, NVIDIA sold large volumes of GPUs into crypto mining, and while that exposure has declined with the shift to AI, crypto demand remains a non‑zero, cyclical driver of certain product segments. (No dedicated NVIDIA‑crypto URL was in the retrieved set; this is based on widely documented past mining demand.)"
            }
          ]
        }
      ],
      "magnitude_bucket": "medium",
      "timeline_bucket": "quarters",
      "what_to_watch": [
        "Trump's public statements on Fed leadership.",
        "Confirmation hearings for Fed chair nominees."
      ],
      "key_unknowns": [
        "Trump's priorities for the Fed chair.",
        "Senate confirmation prospects for nominees."
      ],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 572473
        },
        {
          "kind": "family_match",
          "market_id": 572473,
          "signal_family_id": 1
        },
        {
          "kind": "influence_edge",
          "signal_family_id": 1,
          "macro_domain_id": 1
        },
        {
          "kind": "security_exposure",
          "macro_domain_id": 1
        }
      ],
      "confidence": 0.7
    },
    {
      "market_id": 604470,
      "event_id": 46844,
      "question": "Will China blockade Taiwan by June 30?",
      "event_title": "Will China blockade Taiwan by June 30?",
      "probability": null,
      "end_date": "2026-06-30T00:00:00+00:00",
      "volume_usd": 563927.026438,
      "liquidity_usd": 59152.1184,
      "scores": {
        "final_score": 0.698826651740332,
        "base_score": 0.742857142857143,
        "quality_multiplier": 0.940728185035062,
        "market_strength": 0.795442884424437
      },
      "structural_relevance": "This market directly addresses geopolitical risk in Taiwan, a critical region for semiconductor manufacturing, impacting NVDA's supply chain. The base score of 0.7428 reflects this relevance.",
      "actionability": "The market has moderate strength (0.795) and liquidity ($59k), offering a reasonable signal with a resolution date in June 2026.",
      "transmission_chain": [
        {
          "signal_family_id": 4,
          "slug": "taiwan_geopolitical_risk",
          "title": "Taiwan geopolitical risk",
          "method": "rule_classification",
          "match_strength": 1.0,
          "domains": [
            {
              "macro_domain_id": 2,
              "macro_domain_name": "Semis & Compute",
              "family_influence_score": 5,
              "security_exposure_weight": 0.428571428571429,
              "edge_rationale": "Taiwan‑focused studies emphasize that a large share of advanced fabrication sits on the island, and that quarantine/blockade scenarios could significantly disrupt global semiconductor supply.",
              "exposure_rationale": "3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products"
            },
            {
              "macro_domain_id": 1,
              "macro_domain_name": "AI & Big Tech",
              "family_influence_score": 3,
              "security_exposure_weight": 0.285714285714286,
              "edge_rationale": "Research on Taiwan’s semiconductor industry highlights its centrality to advanced chip fabrication and the vulnerability of global supply chains to quarantine, blockade, or conflict scenarios in the Taiwan Strait.",
              "exposure_rationale": "2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform"
            },
            {
              "macro_domain_id": 3,
              "macro_domain_name": "Cloud / Dev",
              "family_influence_score": 3,
              "security_exposure_weight": 0.142857142857143,
              "edge_rationale": "Cloud / dev‑infra depends on reliable supply of server CPUs, GPUs, and networking hardware, so the Taiwan risk literature implies medium‑to‑high exposure through potential hardware shortages and cost spikes.",
              "exposure_rationale": "1 – It offers DGX Cloud and enterprise AI software (NVIDIA AI Enterprise, NIM microservices), but these are still extensions riding on its hardware franchise rather than a hyperscaler‑scale cloud business, so infra SaaS is important but not dominant. NVIDIA AI Enterprise & DGX cloud pages via same hub"
            },
            {
              "macro_domain_id": 4,
              "macro_domain_name": "Crypto Infra",
              "family_influence_score": 2,
              "security_exposure_weight": 0.142857142857143,
              "edge_rationale": "Crypto infra is linked more weakly: mining hardware and some infra equipment would face supply disruptions, but miners can shift to non‑Taiwan fabs over time, and the main risk comes via global macro stress.",
              "exposure_rationale": "1 – Historically, NVIDIA sold large volumes of GPUs into crypto mining, and while that exposure has declined with the shift to AI, crypto demand remains a non‑zero, cyclical driver of certain product segments. (No dedicated NVIDIA‑crypto URL was in the retrieved set; this is based on widely documented past mining demand.)"
            }
          ]
        }
      ],
      "magnitude_bucket": "medium",
      "timeline_bucket": "quarters",
      "what_to_watch": [
        "Chinese military activity near Taiwan.",
        "Diplomatic statements from China and Taiwan.",
        "International response to escalating tensions."
      ],
      "key_unknowns": [
        "China's strategic goals regarding Taiwan.",
        "Effectiveness of international deterrence."
      ],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 604470
        },
        {
          "kind": "family_match",
          "market_id": 604470,
          "signal_family_id": 4
        },
        {
          "kind": "influence_edge",
          "signal_family_id": 4,
          "macro_domain_id": 2
        },
        {
          "kind": "security_exposure",
          "macro_domain_id": 2
        }
      ],
      "confidence": 0.6
    },
    {
      "market_id": 1322996,
      "event_id": 197059,
      "question": "Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?",
      "event_title": "GPU rental prices (H100) hit___ in February?",
      "probability": null,
      "end_date": "2026-02-28T00:00:00+00:00",
      "volume_usd": 46187.97339,
      "liquidity_usd": 5507.07982,
      "scores": {
        "final_score": 0.441822230314528,
        "base_score": 0.571428571428572,
        "quality_multiplier": 0.773188903050423,
        "market_strength": 0.5766501947463404
      },
      "structural_relevance": "This market reflects the IT spending cycle and demand for AI infrastructure, directly impacting NVIDIA's revenue from GPU rentals. The base score of 0.5714 reflects this relevance.",
      "actionability": "The market has moderate strength (0.576) and limited liquidity ($5.5k), offering a signal with a resolution date in February 2026.",
      "transmission_chain": [
        {
          "signal_family_id": 9,
          "slug": "it_spending_cycle_enterprise_cloud_ai",
          "title": "IT spending cycle (enterprise / cloud / AI)",
          "method": "rule_classification",
          "match_strength": 1.0,
          "domains": [
            {
              "macro_domain_id": 2,
              "macro_domain_name": "Semis & Compute",
              "family_influence_score": 3,
              "security_exposure_weight": 0.257142857142857,
              "edge_rationale": "For semis & compute infra, the IT cycle links directly to data‑center and enterprise hardware demand: Gartner’s tables show data‑center systems as one of the fastest‑growing segments, reflecting AI server and infra build‑out.",
              "exposure_rationale": "3 – NVIDIA is fundamentally a **semiconductor and compute platform company**, with GPUs, accelerated systems and networking at the heart of its P&L; nearly all value creation is tied to designing and selling compute hardware for AI/HPC/graphics. NVIDIA data center & GPU products"
            },
            {
              "macro_domain_id": 1,
              "macro_domain_name": "AI & Big Tech",
              "family_influence_score": 3,
              "security_exposure_weight": 0.171428571428572,
              "edge_rationale": "Big Tech’s cloud and enterprise segments ride the global IT and AI‑infra spending cycle, while consumer ads/commerce are driven by different forces, giving a mixed but important dependence.",
              "exposure_rationale": "2 – NVIDIA’s data‑center business is now dominated by **AI training and inference workloads**, and it ships a full AI data platform stack (Blackwell, NIM, NeMo, CUDA‑X), so AI & data platforms are a major growth and strategy pillar, though revenue is still booked primarily as hardware and platform sales. NVIDIA AI Data Platform"
            },
            {
              "macro_domain_id": 3,
              "macro_domain_name": "Cloud / Dev",
              "family_influence_score": 4,
              "security_exposure_weight": 0.114285714285714,
              "edge_rationale": "Cloud / enterprise / dev‑infra vendors are effectively a leveraged play on the IT‑budget and AI‑infra cycle: Gartner’s projections show software and IT services (where enterprise SaaS, devtools, and cloud live) growing in the low‑teens and reaching well over $1.4tn in software alone.",
              "exposure_rationale": "1 – It offers DGX Cloud and enterprise AI software (NVIDIA AI Enterprise, NIM microservices), but these are still extensions riding on its hardware franchise rather than a hyperscaler‑scale cloud business, so infra SaaS is important but not dominant. NVIDIA AI Enterprise & DGX cloud pages via same hub"
            },
            {
              "macro_domain_id": 4,
              "macro_domain_name": "Crypto Infra",
              "family_influence_score": 1,
              "security_exposure_weight": 0.028571428571429,
              "edge_rationale": "Crypto infra has some exposure to IT/capex cycles where institutional adoption, custody solutions, and security systems are line items in broader IT budgets, but these remain niche relative to the main crypto price/volume cycle.",
              "exposure_rationale": "1 – Historically, NVIDIA sold large volumes of GPUs into crypto mining, and while that exposure has declined with the shift to AI, crypto demand remains a non‑zero, cyclical driver of certain product segments. (No dedicated NVIDIA‑crypto URL was in the retrieved set; this is based on widely documented past mining demand.)"
            }
          ]
        }
      ],
      "magnitude_bucket": "low",
      "timeline_bucket": "days",
      "what_to_watch": [
        "Trends in GPU rental prices.",
        "Demand for AI compute resources.",
        "IT spending forecasts."
      ],
      "key_unknowns": [
        "Pace of AI adoption.",
        "Supply of GPUs.",
        "Economic conditions affecting IT budgets."
      ],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 1322996
        },
        {
          "kind": "family_match",
          "market_id": 1322996,
          "signal_family_id": 9
        },
        {
          "kind": "influence_edge",
          "signal_family_id": 9,
          "macro_domain_id": 2
        },
        {
          "kind": "security_exposure",
          "macro_domain_id": 2
        }
      ],
      "confidence": 0.4
    }
  ],
  "themes": [
    {
      "title": "Taiwan Geopolitical Risk",
      "why": "Several markets relate to the potential for conflict involving Taiwan, which could disrupt semiconductor supplies.",
      "market_ids": [
        604470
      ]
    }
  ],
  "monitor_next": [
    "Monitor geopolitical tensions in the Taiwan Strait.",
    "Track IT spending forecasts and AI infrastructure demand.",
    "Watch for policy changes affecting AI and semiconductor industries."
  ],
  "exclusions": {
    "dropped_due_to_duplicate_event": [
      {
        "market_id": 567621,
        "reason": "duplicate event"
      },
      {
        "market_id": 701290,
        "reason": "duplicate event"
      },
      {
        "market_id": 956590,
        "reason": "duplicate event"
      },
      {
        "market_id": 677407,
        "reason": "duplicate event"
      }
    ],
    "dropped_due_to_rate_cap": [
      {
        "market_id": 654412,
        "reason": "rate cap"
      },
      {
        "market_id": 669660,
        "reason": "rate cap"
      }
    ],
    "dropped_due_to_low_actionability": [
      {
        "market_id": 540843,
        "reason": "low actionability"
      },
      {
        "market_id": 957986,
        "reason": "low actionability"
      },
      {
        "market_id": 1322973,
        "reason": "low actionability"
      },
      {
        "market_id": 676842,
        "reason": "low actionability"
      },
      {
        "market_id": 1302430,
        "reason": "low actionability"
      },
      {
        "market_id": 1228017,
        "reason": "low actionability"
      },
      {
        "market_id": 1426260,
        "reason": "low actionability"
      },
      {
        "market_id": 1068733,
        "reason": "low actionability"
      },
      {
        "market_id": 1108760,
        "reason": "low actionability"
      },
      {
        "market_id": 1426021,
        "reason": "low actionability"
      },
      {
        "market_id": 1058192,
        "reason": "low actionability"
      }
    ]
  },
  "notes": [
    "The pack contains multiple markets related to Taiwan geopolitical risk, but only one was selected to ensure diversity.",
    "The pack contains multiple markets related to FOMC surprises, but the maximum number of rate-like markets was reached, so the rest were excluded.",
    "Several markets were excluded due to low actionability based on their scores and liquidity."
  ]
}
```
</details>
