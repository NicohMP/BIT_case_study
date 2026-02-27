from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class SentimentIntensityParamsV1:
    """Parameters for the v1 sentiment intensity function g(m)."""

    tau0_days: float = 30.0
    delta_p_half_life: float = 0.05  # 5 percentage points => movement factor ~0.5

    @property
    def k_delta(self) -> float:
        return float(math.log(2.0) / float(self.delta_p_half_life))


def _clamp(x: float, lo: float, hi: float) -> float:
    return float(max(lo, min(hi, x)))


def participation_factor(*, volume_usd: float | None, vol95_usd: float) -> float:
    vol = max(0.0, float(volume_usd or 0.0))
    denom = max(1e-9, math.log1p(max(0.0, float(vol95_usd))))
    return float(_clamp(math.log1p(vol) / denom, 0.0, 1.0))


def urgency_factor(*, tau_days: float | None, tau0_days: float) -> float:
    if tau_days is None:
        return 0.5
    return float(_clamp(math.exp(-max(0.0, float(tau_days)) / max(1e-9, float(tau0_days))), 0.0, 1.0))


def movement_factor(*, delta_p: float | None, k_delta: float) -> float | None:
    if delta_p is None:
        return None
    dp = max(0.0, float(delta_p))
    return float(_clamp(1.0 - math.exp(-float(k_delta) * dp), 0.0, 1.0))


def sentiment_intensity_g_v1(
    *,
    volume_usd: float | None,
    vol95_usd: float,
    tau_days: float | None,
    delta_p: float | None,
    params: SentimentIntensityParamsV1 | None = None,
    movement_optional: bool = True,
) -> dict[str, Any]:
    """Compute g(m) and return value + interpretable components."""

    p = params or SentimentIntensityParamsV1()

    part = participation_factor(volume_usd=volume_usd, vol95_usd=float(vol95_usd))
    urg = urgency_factor(tau_days=tau_days, tau0_days=float(p.tau0_days))
    mov = movement_factor(delta_p=delta_p, k_delta=float(p.k_delta))

    if mov is None:
        g = part * urg if movement_optional else 0.0
    else:
        g = part * float(mov) * urg

    return {
        "g": float(_clamp(float(g), 0.0, 1.0)),
        "components": {
            "participation": float(part),
            "movement": None if mov is None else float(mov),
            "urgency": float(urg),
        },
        "inputs": {
            "volume_usd": None if volume_usd is None else float(volume_usd),
            "vol95_usd": float(vol95_usd),
            "tau_days": None if tau_days is None else float(tau_days),
            "delta_p": None if delta_p is None else float(delta_p),
            "movement_optional": bool(movement_optional),
            "tau0_days": float(p.tau0_days),
            "k_delta": float(p.k_delta),
        },
    }


def sentiment_intensity_g_v1_practical(
    *,
    volume_usd: float | None,
    vol95_usd: float,
    tau_days: float | None,
    delta_p: float | None,
    params: SentimentIntensityParamsV1 | None = None,
    include_movement: bool = False,
) -> dict[str, Any]:
    """Practical v1 for production selection/reporting.

    Rationale:
    - Δp requires a mature, reliably sampled price history. Early in the project
      (or in demos with limited snapshot history), including movement can
      systematically zero out otherwise important long-dated markets.
    - We therefore compute movement for metadata/audit, but exclude it from the
      primary g(m) score by default.

    Returns:
    - g: participation × urgency (default), or × movement if include_movement=True
    - g_with_movement: the full formulation using movement when available
    """
    p = params or SentimentIntensityParamsV1()

    part = participation_factor(volume_usd=volume_usd, vol95_usd=float(vol95_usd))
    urg = urgency_factor(tau_days=tau_days, tau0_days=float(p.tau0_days))
    mov = movement_factor(delta_p=delta_p, k_delta=float(p.k_delta))

    # Default score (no movement).
    g_no_move = part * urg
    g_full = (part * float(mov) * urg) if mov is not None else g_no_move

    g = g_full if include_movement else g_no_move

    return {
        "g": float(_clamp(float(g), 0.0, 1.0)),
        "g_with_movement": float(_clamp(float(g_full), 0.0, 1.0)),
        "components": {
            "participation": float(part),
            "movement": None if mov is None else float(mov),
            "urgency": float(urg),
        },
        "inputs": {
            "volume_usd": None if volume_usd is None else float(volume_usd),
            "vol95_usd": float(vol95_usd),
            "tau_days": None if tau_days is None else float(tau_days),
            "delta_p": None if delta_p is None else float(delta_p),
            "include_movement": bool(include_movement),
            "tau0_days": float(p.tau0_days),
            "k_delta": float(p.k_delta),
        },
    }


def tau_days_from_end_date(*, end_date_iso: str | None, now: datetime) -> float | None:
    if not end_date_iso:
        return None
    try:
        end_dt = datetime.fromisoformat(str(end_date_iso).replace("Z", "+00:00"))
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)
        return float(max(0.0, (end_dt - now).total_seconds() / 86400.0))
    except Exception:
        return None


def delta_p_abs(*, p_now: float | None, p_then: float | None) -> float | None:
    if p_now is None or p_then is None:
        return None
    try:
        return float(abs(float(p_now) - float(p_then)))
    except Exception:
        return None
