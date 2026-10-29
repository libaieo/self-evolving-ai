"""Rule-based request analysis and planning for development stage 3.

This module intentionally uses transparent rules instead of an AI model so its
behavior can be tested and explained before adding model integration later.
"""

from __future__ import annotations
import re

from self_evolving_ai.request_models import RequestAnalysis, TaskPlan

_HIGH_RISK_TERMS = (
    "delete", "삭제", "결제", "송금", "비밀번호", "password", "secret",
    "토큰", "token", "배포", "deploy", "production", "운영 서버",
)
_URGENT_TERMS = ("긴급", "즉시", "urgent", "asap")
_HIGH_PRIORITY_TERMS = ("중요", "우선", "최우선", "high priority")


def analyze_request(request: str) -> RequestAnalysis:
    """Convert raw text into a small, transparent structured analysis."""
    original = request.strip()
    if not original:
        raise ValueError("요청 내용은 비어 있을 수 없습니다.")

    lowered = original.lower()
    priority = "normal"
    if any(term in lowered for term in _URGENT_TERMS):
        priority = "urgent"
    elif any(term in lowered for term in _HIGH_PRIORITY_TERMS):
        priority = "high"

    risky = any(term in lowered for term in _HIGH_RISK_TERMS)
    asks_to_change_external_state = any(
        term in lowered for term in ("삭제", "delete", "결제", "송금", "배포", "deploy")
    )

    constraints: list[str] = []
    if any(term in lowered for term in ("한국어", "한글", "korean")):
        constraints.append("한국어로 결과를 제공")
    if any(term in lowered for term in ("짧게", "간단히", "concise", "brief")):
        constraints.append("간결하게 작성")
    if any(term in lowered for term in ("출처", "근거", "citation", "source")):
        constraints.append("주요 주장에 근거 또는 출처를 포함")

    ambiguities: list[str] = []
    if len(original) < 12:
        ambiguities.append("요청이 짧아 목표나 완료 조건이 충분히 구체적이지 않을 수 있음")
    if any(term in lowered for term in ("그거", "그렇게", "저것", "이거")) or re.search(r"\b(?:it|that)\b", lowered):
        ambiguities.append("지시 대상이 현재 문장만으로 명확하지 않을 수 있음")

    criteria = ["결과가 요청의 핵심 목표를 직접 충족함"]
    if constraints:
        criteria.append("명시된 제약 조건을 모두 충족함")
    if risky:
        criteria.append("위험과 권한을 확인하고 필요한 승인 절차를 거침")

    return RequestAnalysis(
        original_request=original,
        goal=original,
        constraints=constraints,
        success_criteria=criteria,
        ambiguities=ambiguities,
        priority=priority,  # type: ignore[arg-type]
        risk_level="high" if risky else "low",
        requires_user_confirmation=asks_to_change_external_state,
    )


def create_plan(analysis: RequestAnalysis) -> TaskPlan:
    """Build a deterministic plan based on a structured request analysis."""
    steps = [
        "요청의 목표와 제약 조건을 확인한다.",
        "필요한 정보와 사용할 도구를 정한다.",
        "작업을 수행하고 결과를 성공 조건에 대조한다.",
        "오류나 누락을 수정하고 최종 결과를 정리한다.",
    ]
    if analysis.risk_level == "high" or analysis.requires_user_confirmation:
        steps.insert(2, "위험, 권한, 사용자 승인 필요 여부를 확인한다.")
    if analysis.ambiguities:
        steps.insert(0, "모호한 부분을 표시하고, 진행 가능한 범위와 확인 필요 항목을 구분한다.")

    checklist = list(analysis.success_criteria)
    checklist.append("실행 결과와 확인하지 못한 사항을 구분해 보고함")
    return TaskPlan(
        summary=f"목표: {analysis.goal}",
        steps=steps,
        completion_checklist=checklist,
        needs_clarification=bool(analysis.ambiguities),
    )
