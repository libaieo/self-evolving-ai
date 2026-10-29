"""Typed data models for representing a user's request and its plan."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Priority = Literal["low", "normal", "high", "urgent"]
RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class RequestAnalysis:
    """Structured interpretation of the user's request."""

    original_request: str
    goal: str
    constraints: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    priority: Priority = "normal"
    risk_level: RiskLevel = "low"
    requires_user_confirmation: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)


@dataclass(frozen=True)
class TaskPlan:
    """A simple execution plan derived from a request analysis."""

    summary: str
    steps: list[str]
    completion_checklist: list[str]
    needs_clarification: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)
