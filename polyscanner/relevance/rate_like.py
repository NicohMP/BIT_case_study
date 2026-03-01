"""Rate/macro market detection shared across Step 4 and audits.

We use a deliberately simple lexical detector to classify "rate-like" markets.
This is used for diversification caps (presentation/selection), not for scoring.
"""

from __future__ import annotations

import re


RATE_MARKET_RE = re.compile(
    r"\b("
    r"fomc|federal\s+reserve|fed\b|powell|interest\s+rate|rate\s+cut|rate\s+hike|basis\s+points|bps\b|"
    r"treasury\s+yield|10[-\s]?year\s+treasury|10[-\s]?year\s+yield|2[-\s]?year\s+yield|long\s+rates|"
    r"cpi|inflation|jobs\s+report|unemployment|nonfarm|nfp|fomc\s+meeting|federal\s+funds\s+rate"
    r")\b",
    flags=re.IGNORECASE,
)


def is_rate_like(text: str) -> bool:
    return bool(RATE_MARKET_RE.search(text or ""))

