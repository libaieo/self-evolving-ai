"""Minimal command-line entry point for the project."""

from self_evolving_ai import __version__


def main() -> int:
    """Print a basic status message and return a process exit code."""
    print("자가혁신 시스템 최소 실행 기반")
    print(f"버전: {__version__}")
    print("상태: 정상적으로 시작되었습니다.")
    print("안내: 현재 버전은 실행 기반만 제공하며 AI 추론 기능은 아직 포함하지 않습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
