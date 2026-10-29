"""Deterministic validation for specialist-module results."""

from __future__ import annotations

from self_evolving_ai.modules import ModuleResult


def validate_result(result: ModuleResult, expected_module_name: str) -> list[str]:
    """Return validation errors; an empty list means the result passed checks."""
    errors: list[str] = []
    if not isinstance(result, ModuleResult):
        return ["결과가 ModuleResult 형식이 아닙니다."]
    if not result.module_name.strip():
        errors.append("모듈 이름이 비어 있습니다.")
    if result.module_name != expected_module_name:
        errors.append("결과의 모듈 이름이 등록된 이름과 일치하지 않습니다.")
    if result.status not in {"success", "error"}:
        errors.append("결과 상태는 success 또는 error여야 합니다.")
    if not result.summary.strip():
        errors.append("결과 요약이 비어 있습니다.")
    if not isinstance(result.data, dict):
        errors.append("결과 데이터는 딕셔너리여야 합니다.")
    if result.status == "error" and not result.data:
        errors.append("오류 결과에는 최소한의 진단 정보가 필요합니다.")
    return errors
