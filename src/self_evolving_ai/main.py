"""Command-line entry point for the Self-Evolving AI foundation."""

import argparse
import json

from self_evolving_ai import __version__
from self_evolving_ai.dispatcher import dispatch
from self_evolving_ai.planner import analyze_request, create_plan
from self_evolving_ai.registry import create_default_registry


def main() -> int:
    """Run the CLI and return a process exit code."""
    parser = argparse.ArgumentParser(description="자가혁신 시스템 개발 기반")
    parser.add_argument("--analyze", metavar="REQUEST", help="사용자 요청을 구조화해 분석하고 작업 계획을 출력합니다.")
    parser.add_argument("--run", metavar="TASK", help="등록된 전문 모듈을 실행합니다. 예: summary, checklist, 요약, 계획")
    parser.add_argument("--request", metavar="REQUEST", help="--run에서 처리할 입력 텍스트입니다.")
    parser.add_argument("--list-modules", action="store_true", help="등록된 전문 모듈 목록을 JSON으로 출력합니다.")
    args = parser.parse_args()

    if args.analyze is not None:
        try:
            analysis = analyze_request(args.analyze)
        except ValueError as exc:
            parser.error(str(exc))
        result = {"analysis": analysis.to_dict(), "plan": create_plan(analysis).to_dict()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.list_modules:
        print(json.dumps(create_default_registry().list_modules(), ensure_ascii=False, indent=2))
        return 0

    if args.run is not None:
        if args.request is None:
            parser.error("--run을 사용할 때는 --request도 지정해야 합니다.")
        result = dispatch(args.run, args.request)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0 if result.status == "success" else 1

    if args.request is not None:
        parser.error("--request는 --run과 함께 사용해야 합니다.")

    print("자가혁신 시스템 최소 실행 기반")
    print(f"버전: {__version__}")
    print("상태: 정상적으로 시작되었습니다.")
    print("안내: --analyze로 요청 분석, --list-modules로 전문 모듈 목록, --run으로 모듈 실행을 시험할 수 있습니다.")
    print("참고: 현재 분석과 예시 모듈은 규칙 기반이며, AI 모델을 사용하지 않습니다.")
    print("AI 추론 기능은 아직 포함하지 않습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
