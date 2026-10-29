# 설치 및 실행 안내

## 요구 사항
- Python 3.11 이상
- Git (저장소를 내려받을 경우)

## 설치
저장소를 내려받은 뒤 프로젝트 최상위 폴더에서 실행합니다.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -e .
```

## 실행
설치 후 다음 명령을 실행합니다.

```bash
self-evolving-ai
```

또는 설치 전 개발 실행 시:

```bash
python -m pip install -e .
python -m self_evolving_ai.main
```

정상 실행 시 버전과 기본 상태 안내가 출력됩니다. 이 단계의 프로그램은 실행 기반을 확인하는 용도이며, 아직 언어 모델 호출이나 자가 개선 기능은 수행하지 않습니다.

## 테스트
프로젝트 최상위 폴더에서 실행합니다.

```bash
python -m unittest discover -s tests -v
```

## 비밀정보 관리
- 실제 키나 토큰을 `pyproject.toml`, 소스 코드, 테스트, Git 커밋에 기록하지 않습니다.
- `.env.example`에는 이름 예시만 둡니다.
- `.env` 파일은 `.gitignore`에 포함되어 있습니다.
- 실제 API 연결을 추가할 때는 환경변수 또는 전용 비밀정보 관리 방식을 사용합니다.
