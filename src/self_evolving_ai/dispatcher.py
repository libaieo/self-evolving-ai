"""Safe, explicit dispatcher for specialist modules."""

from __future__ import annotations

from self_evolving_ai.modules import ModuleResult
from self_evolving_ai.registry import ModuleRegistry, create_default_registry
from self_evolving_ai.validation import validate_result


def dispatch(task: str, request: str, registry: ModuleRegistry | None = None) -> ModuleResult:
    """Resolve, run, and validate one module; errors become explicit failures.

    This dispatcher never executes shell commands, network requests, or external
    side effects. A caller must explicitly select a task/module.
    """
    active_registry = registry if registry is not None else create_default_registry()
    try:
        module = active_registry.resolve(task)
    except (LookupError, ValueError) as exc:
        return ModuleResult(
            module_name="dispatcher",
            status="error",
            summary=str(exc),
            data={"error_type": type(exc).__name__, "requested_task": task},
        )

    try:
        result = module.run(request)
        errors = validate_result(result, module.name)
        if errors:
            return ModuleResult(
                module_name=module.name,
                status="error",
                summary="전문 모듈 결과 검증에 실패했습니다.",
                data={"error_type": "InvalidModuleResult", "validation_errors": errors},
            )
        return result
    except Exception as exc:  # Convert module failures into inspectable results.
        return ModuleResult(
            module_name=module.name,
            status="error",
            summary="전문 모듈 실행 중 오류가 발생했습니다.",
            data={"error_type": type(exc).__name__, "error": str(exc)},
        )
