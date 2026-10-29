"""Command-line entry point for the Self-Evolving AI foundation."""

import argparse
import json

from self_evolving_ai import __version__
from self_evolving_ai.planner import analyze_request, create_plan


def main() -> int:
    """Run the CLI and return a process exit code."""
    parser = argparse.ArgumentParser(description="자가혁신 시스템 개발 기반")
    parser.add_argument(
        "--analyze",
        metavar="REQUEST",
        help="사용자 요청을 구조화해 분석하고 작업 계획을 출력합니다.",
    )
    args = parser.parse_args()

    if args.analyze is not None:
        try:
            analysis = analyze_request(args.analyze)
        except ValueError as exc:
            parser.error(str(exc))
        result = {"analysis": analysis.to_dict(), "plan": create_plan(analysis).to_dict()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("자가혁신 시스템 최소 실행 기반")
    print(f"버전: {__version__}")
    print("상태: 정상적으로 시작되었습니다.")
    print("안내: --analyze 옵션으로 요청 해석 및 계획 기능을 시험할 수 있습니다.")
    print("참고: 현재 분석은 규칙 기반이며, AI 모델을 사용하지 않습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
