"""Shared data models for the MVP pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Domain:
    id: int
    name: str


@dataclass(frozen=True)
class DomainDefinition:
    """DB-backed domain 'theme' for embeddings and filtering."""

    id: int
    name: str
    description: str
    keywords: list[str]
    exclusions: list[str]

    def to_theme_text(self) -> str:
        """Canonical text used for embedding similarity."""
        kw = ", ".join(self.keywords) if self.keywords else ""
        ex = ", ".join(self.exclusions) if self.exclusions else ""
        parts = [f"{self.name}. {self.description}".strip()]
        if kw:
            parts.append(f"Keywords: {kw}.")
        if ex:
            parts.append(f"Exclusions: {ex}.")
        return " ".join(parts).strip()


@dataclass(frozen=True)
class TransmissionChannel:
    slug: str
    label: str
    description: str


@dataclass(frozen=True)
class DomainChannelExposure:
    domain_id: int
    channel_slug: str
    exposure: float
    rationale: str


@dataclass(frozen=True)
class MacroDomain:
    """Domain taxonomy used by the signal-family authority layer."""

    id: int
    name: str
    description: str


@dataclass(frozen=True)
class SignalFamily:
    """Curated macro signal family (renamed from 'macro_event' to avoid confusion)."""

    id: int
    slug: str
    title: str
    description: str
    is_active: bool


@dataclass(frozen=True)
class SignalFamilyDomainInfluence:
    signal_family_id: int
    macro_domain_id: int
    score: int  # 0..5
    rationale_md: str
    sources: list[dict[str, Any]]


@dataclass(frozen=True)
class PMMarket:
    pm_market_id: int
    question: str
    category: str | None
    probability: float | None
    volume: float | None
    raw: dict[str, Any]


@dataclass(frozen=True)
class RankedMarket:
    market: PMMarket
    score: float
    heuristic_domain: str | None
