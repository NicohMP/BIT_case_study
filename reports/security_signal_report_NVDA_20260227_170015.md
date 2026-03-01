# NVIDIA Corp (NVDA) Signal Report

_As of_: `2026-02-27T16:52:04.827733+00:00`
_Pipeline_: filter `hard_filters_v8`, matcher `matcher_v10`, scoring `relevance_v5`, selection `selected_v1`, prompt `security_signal_report_v1`, model `qwen2.5:7b-instruct`

<details>
<summary>Run metadata</summary>

- run_id: `6c48e142-674d-4eec-93a1-b4150fc781a9`
</details>

**Security:** `NVDA` — NVIDIA Corp (XNAS)

## Executive Summary
Key prediction-market signals for NVDA right now: Will Kevin Warsh be formally nominated to be Chair of the Federal Reserve by February 28, 2026? (p≈1%, resolves in ~0d); Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting? (p≈0%, resolves in ~18d); Fed rate cut by March 2026 meeting? (p≈2%, resolves in ~18d). Use the market write-ups below to map each event to macro domains and to identify what to monitor next.

Top signals: **Will Kevin Warsh be formally nominated to be Chair of the Federal Reserve by February 28, 2026?** (magnitude: low; timeline: weeks; actionability: High); **Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?** (magnitude: low; timeline: weeks; actionability: High); **Fed rate cut by March 2026 meeting?** (magnitude: low; timeline: weeks; actionability: Medium); **Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?** (magnitude: low; timeline: weeks; actionability: Medium); **Will China invade Taiwan by March 31, 2026?** (magnitude: low; timeline: weeks; actionability: High).

## Top Signals
### 1) Will Kevin Warsh be formally nominated to be Chair of the Federal Reserve by February 28, 2026?

**Event:** Kevin Warsh formally nominated as Fed Chair by...?
**Current probability:** 1%
_Snapshot:_ resolves `2026-02-28T00:00:00+00:00` (0d); volume $372.8k; liquidity $22.0k; structural relevance High; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=1299973, event_id=193747`

---

### 2) Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?

**Event:** Fed decision in March?
**Current probability:** 0%
_Snapshot:_ resolves `2026-03-18T00:00:00+00:00` (18d); volume $74.36M; liquidity $2.20M; structural relevance High; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=654412, event_id=67284`

---

### 3) Fed rate cut by March 2026 meeting?

**Event:** Fed rate cut by...?
**Current probability:** 2%
_Snapshot:_ resolves `2026-03-18T00:00:00+00:00` (18d); volume $226.8k; liquidity $26.6k; structural relevance High; actionability Medium; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=949493, event_id=106884`

---

### 4) Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?

**Event:** GPU rental prices (H100) hit___ in February?
**Current probability:** 1%
_Snapshot:_ resolves `2026-02-28T00:00:00+00:00` (0d); volume $46.4k; liquidity $5.2k; structural relevance Low; actionability Medium; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=1322996, event_id=197059`

---

### 5) Will China invade Taiwan by March 31, 2026?

**Current probability:** 1%
_Snapshot:_ resolves `2026-03-31T00:00:00+00:00` (31d); volume $3.47M; liquidity $156.1k; structural relevance Medium; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=701290, event_id=89456`

---

### 6) Will Trump nominate no one before 2027?

**Event:** Who will Trump nominate as Fed Chair?
**Current probability:** 0%
_Snapshot:_ resolves `2026-12-31T00:00:00+00:00` (306d); volume $20.12M; liquidity $315.8k; structural relevance High; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=572506, event_id=35908`

---

### 7) Will China blockade Taiwan by June 30?

**Current probability:** 4%
_Snapshot:_ resolves `2026-06-30T00:00:00+00:00` (122d); volume $568.9k; liquidity $60.0k; structural relevance Medium; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=604470, event_id=46844`

---

### 8) Will China invade Taiwan by end of 2026?

**Current probability:** 10%
_Snapshot:_ resolves `2026-12-31T00:00:00+00:00` (306d); volume $9.56M; liquidity $534.1k; structural relevance Medium; actionability High; confidence Medium; magnitude low; timeline weeks.


_IDs:_ `market_id=567621, event_id=34044`

---

## Appendix: Evidence & Metrics

### Metrics (raw)
| market_id | event_id | final_score | base_score | quality_mult | market_strength | confidence |
|---:|---:|---:|---:|---:|---:|---:|
| 1299973 | 193747 | 0.671349935006298 | 0.771428571428572 | 0.895690567686945 | 0.7739557969157725 | 0.5 |
| 654412 | 67284 | 0.524846624244553 | 0.771428571428572 | 1.0 | 0.97 | 0.5 |
| 949493 | 106884 | 0.445027060307618 | 0.771428571428572 | 0.881672815874199 | 0.7221655936620274 | 0.5 |
| 1322996 | 197059 | 0.380313658834426 | 0.571428571428572 | 0.771588828650484 | 0.5744082837455823 | 0.5 |
| 701290 | 89456 | 0.344718452342916 | 0.631428571428572 | 0.998778021166584 | 0.9218168991658056 | 0.5 |
| 572506 | 35908 | 0.231448444262552 | 0.771428571428572 | 1.0 | 0.9107986101763585 | 0.5 |
| 604470 | 46844 | 0.218124022418638 | 0.742857142857143 | 0.941493890358632 | 0.7967636312409768 | 0.5 |
| 567621 | 34044 | 0.1894448377112 | 0.631428571428572 | 1.0 | 0.9241128017351508 | 0.5 |

### Exclusions

<details>
<summary>Raw LLM JSON</summary>

```json
{
  "title": "NVIDIA Corp (NVDA) Signal Report",
  "as_of_utc": "2026-02-27T16:52:04.827733+00:00",
  "top_take": "Key prediction-market signals for NVDA right now: Will Kevin Warsh be formally nominated to be Chair of the Federal Reserve by February 28, 2026? (p≈1%, resolves in ~0d); Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting? (p≈0%, resolves in ~18d); Fed rate cut by March 2026 meeting? (p≈2%, resolves in ~18d). Use the market write-ups below to map each event to macro domains and to identify what to monitor next.",
  "versions": {
    "run_id": "6c48e142-674d-4eec-93a1-b4150fc781a9",
    "filter_version": "hard_filters_v8",
    "matcher_version": "matcher_v10",
    "scoring_version": "relevance_v5",
    "selection_version": "selected_v1",
    "prompt_version": "security_signal_report_v1",
    "model": "qwen2.5:7b-instruct"
  },
  "security": {
    "security_id": 17,
    "ticker": "NVDA",
    "company_name": "NVIDIA Corp",
    "exchange_mic": "XNAS"
  },
  "top_markets": [
    {
      "market_id": 1299973,
      "event_id": 193747,
      "question": "Will Kevin Warsh be formally nominated to be Chair of the Federal Reserve by February 28, 2026?",
      "event_title": "Kevin Warsh formally nominated as Fed Chair by...?",
      "probability": 0.0145,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.0145,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-02-28T00:00:00+00:00",
      "volume_usd": 372836.346067,
      "liquidity_usd": 22049.26564,
      "scores": {
        "final_score": 0.671349935006298,
        "base_score": 0.771428571428572,
        "quality_multiplier": 0.895690567686945,
        "market_strength": 0.7739557969157725
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 1299973
        },
        {
          "kind": "family_match",
          "market_id": 1299973,
          "signal_family_id": 1
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 654412,
      "event_id": 67284,
      "question": "Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?",
      "event_title": "Fed decision in March?",
      "probability": 0.0045,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.0045,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-03-18T00:00:00+00:00",
      "volume_usd": 74361659.946269,
      "liquidity_usd": 2195954.07722,
      "scores": {
        "final_score": 0.524846624244553,
        "base_score": 0.771428571428572,
        "quality_multiplier": 1.0,
        "market_strength": 0.97
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 654412
        },
        {
          "kind": "family_match",
          "market_id": 654412,
          "signal_family_id": 1
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 949493,
      "event_id": 106884,
      "question": "Fed rate cut by March 2026 meeting?",
      "event_title": "Fed rate cut by...?",
      "probability": 0.0225,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.0225,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-03-18T00:00:00+00:00",
      "volume_usd": 226797.005847,
      "liquidity_usd": 26634.78671,
      "scores": {
        "final_score": 0.445027060307618,
        "base_score": 0.771428571428572,
        "quality_multiplier": 0.881672815874199,
        "market_strength": 0.7221655936620274
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 949493
        },
        {
          "kind": "family_match",
          "market_id": 949493,
          "signal_family_id": 1
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 1322996,
      "event_id": 197059,
      "question": "Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?",
      "event_title": "GPU rental prices (H100) hit___ in February?",
      "probability": 0.006,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.006,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-02-28T00:00:00+00:00",
      "volume_usd": 46439.127235,
      "liquidity_usd": 5175.10168,
      "scores": {
        "final_score": 0.380313658834426,
        "base_score": 0.571428571428572,
        "quality_multiplier": 0.771588828650484,
        "market_strength": 0.5744082837455823
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 1322996
        },
        {
          "kind": "family_match",
          "market_id": 1322996,
          "signal_family_id": 9
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 701290,
      "event_id": 89456,
      "question": "Will China invade Taiwan by March 31, 2026?",
      "event_title": "Will China invade Taiwan by March 31, 2026?",
      "probability": 0.008,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.008,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-03-31T00:00:00+00:00",
      "volume_usd": 3467812.925716,
      "liquidity_usd": 156075.81718,
      "scores": {
        "final_score": 0.344718452342916,
        "base_score": 0.631428571428572,
        "quality_multiplier": 0.998778021166584,
        "market_strength": 0.9218168991658056
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 701290
        },
        {
          "kind": "family_match",
          "market_id": 701290,
          "signal_family_id": 4
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 572506,
      "event_id": 35908,
      "question": "Will Trump nominate no one before 2027?",
      "event_title": "Who will Trump nominate as Fed Chair?",
      "probability": 0.005,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.005,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-12-31T00:00:00+00:00",
      "volume_usd": 20121292.147931,
      "liquidity_usd": 315793.92323,
      "scores": {
        "final_score": 0.231448444262552,
        "base_score": 0.771428571428572,
        "quality_multiplier": 1.0,
        "market_strength": 0.9107986101763585
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 572506
        },
        {
          "kind": "family_match",
          "market_id": 572506,
          "signal_family_id": 1
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 604470,
      "event_id": 46844,
      "question": "Will China blockade Taiwan by June 30?",
      "event_title": "Will China blockade Taiwan by June 30?",
      "probability": 0.045,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.045,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-06-30T00:00:00+00:00",
      "volume_usd": 568912.076065,
      "liquidity_usd": 60009.9845,
      "scores": {
        "final_score": 0.218124022418638,
        "base_score": 0.742857142857143,
        "quality_multiplier": 0.941493890358632,
        "market_strength": 0.7967636312409768
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 604470
        },
        {
          "kind": "family_match",
          "market_id": 604470,
          "signal_family_id": 4
        }
      ],
      "confidence": 0.5
    },
    {
      "market_id": 567621,
      "event_id": 34044,
      "question": "Will China invade Taiwan by end of 2026?",
      "event_title": "Will China invade Taiwan by end of 2026?",
      "probability": 0.0975,
      "pricing": {
        "kind": "binary",
        "yes_probability": 0.0975,
        "top_outcomes": [],
        "note": null
      },
      "end_date": "2026-12-31T00:00:00+00:00",
      "volume_usd": 9562428.602756,
      "liquidity_usd": 534130.81167,
      "scores": {
        "final_score": 0.1894448377112,
        "base_score": 0.631428571428572,
        "quality_multiplier": 1.0,
        "market_strength": 0.9241128017351508
      },
      "structural_relevance": "",
      "actionability": "",
      "transmission_chain": [],
      "magnitude_bucket": "low",
      "timeline_bucket": "weeks",
      "what_to_watch": [],
      "key_unknowns": [],
      "evidence_refs": [
        {
          "kind": "market",
          "market_id": 567621
        },
        {
          "kind": "family_match",
          "market_id": 567621,
          "signal_family_id": 4
        }
      ],
      "confidence": 0.5
    }
  ],
  "themes": [],
  "monitor_next": [],
  "exclusions": {
    "dropped_due_to_duplicate_event": [],
    "dropped_due_to_rate_cap": [],
    "dropped_due_to_low_actionability": []
  },
  "notes": []
}
```
</details>
