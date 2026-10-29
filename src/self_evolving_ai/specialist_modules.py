"""Small deterministic specialist modules used to prove the module contract."""

from __future__ import annotations

from self_evolving_ai.modules import ModuleResult


class SummaryModule:
    name = "summary"
    description = "Produces a conservative short summary of supplied text."
    supported_tasks = ("summary", "summarize", "요약", "정리")

    def run(self, request: str) -> ModuleResult:
        text = " ".join(request.split())
        words = text.split(" ") if text else []
        summary = text if len(text) <= 180 else text[:177].rstrip() + "..."
        return ModuleResult(
            module_name=self.name,
            status="success",
            summary="입력 텍스트를 규칙 기반으로 짧게 정리했습니다.",
            data={"summary": summary, "word_count": len(words), "truncated": len(text) > 180},
        )


class ChecklistModule:
    name = "checklist"
    description = "Turns a request into a small action checklist."
    supported_tasks = ("checklist", "steps", "계획", "할 일", "절차")

    def run(self, request: str) -> ModuleResult:
        text = " ".join(request.split())
        items = [
            "요청의 목표와 완료 조건을 확인한다.",
            "필요한 정보와 준비물을 확인한다.",
            f"요청을 수행한다: {text}",
            "결과를 확인하고 빠진 항목을 보완한다.",
        ]
        return ModuleResult(
            module_name=self.name,
            status="success",
            summary="기본 작업 체크리스트를 생성했습니다.",
            data={"items": items},
        )
