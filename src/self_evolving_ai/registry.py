"""Registration and deterministic selection of specialist modules."""

from __future__ import annotations

from self_evolving_ai.modules import SpecialistModule
from self_evolving_ai.specialist_modules import ChecklistModule, SummaryModule


class ModuleNotFoundError(LookupError):
    """Raised when no registered module matches a requested task."""


class ModuleRegistry:
    """Stores modules by unique name and resolves explicit task requests."""

    def __init__(self) -> None:
        self._modules: dict[str, SpecialistModule] = {}

    def register(self, module: SpecialistModule) -> None:
        if not module.name.strip():
            raise ValueError("모듈 이름은 비어 있을 수 없습니다.")
        if module.name in self._modules:
            raise ValueError(f"이미 등록된 모듈입니다: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> SpecialistModule:
        try:
            return self._modules[name]
        except KeyError as exc:
            raise ModuleNotFoundError(f"등록된 모듈을 찾을 수 없습니다: {name}") from exc

    def list_modules(self) -> list[dict[str, object]]:
        return [
            {"name": m.name, "description": m.description, "supported_tasks": list(m.supported_tasks)}
            for m in self._modules.values()
        ]

    def resolve(self, task: str) -> SpecialistModule:
        normalized = task.strip().lower()
        for module in self._modules.values():
            if normalized == module.name.lower() or normalized in (term.lower() for term in module.supported_tasks):
                return module
        raise ModuleNotFoundError(f"'{task}' 작업을 처리할 모듈이 없습니다.")


def create_default_registry() -> ModuleRegistry:
    registry = ModuleRegistry()
    registry.register(SummaryModule())
    registry.register(ChecklistModule())
    return registry
