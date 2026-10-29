"""Interfaces and result models for specialist modules (development stage 4)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ModuleResult:
    """Standard output returned by every specialist module."""

    module_name: str
    status: str
    summary: str
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SpecialistModule(Protocol):
    """Contract every specialist module must satisfy."""

    name: str
    description: str
    supported_tasks: tuple[str, ...]

    def run(self, request: str) -> ModuleResult:
        """Execute a bounded task and return a standardized result."""
