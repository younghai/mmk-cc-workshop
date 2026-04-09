# Claude Code 워크샵 스타터

강의 실습용 Claude Code 워크샵 스타터 프로젝트입니다.

## 프로젝트 목적

이 프로젝트를 fork하여 Claude Code 웹에서 바로 자동화 바이브 코딩을 시작할 수 있습니다.

## mmk CLI

mmk (Magic Meal Kits)는 YouTube 자막 추출, 메타데이터 조회 등을 지원하는 CLI 도구입니다.

**중요: 현재 토큰은 YouTube 전용입니다. `mmk youtube` 명령어만 사용하세요.**
`mmk notion`, `mmk paymint` 등 다른 명령어는 권한이 없어 실패합니다 (403 insufficient_scope).

### 설정

```bash
export MMK_SERVER="https://magic-meal-kits-r7fpfharja-uw.a.run.app"
export MMK_TOKEN="<강사가 제공한 토큰>"
```

### 사용 가능한 명령어

```bash
# YouTube 자막 추출
mmk youtube transcript <youtube-url>
mmk youtube transcript <youtube-url> --format json
mmk youtube transcript <youtube-url> --format srt

# YouTube 메타데이터 조회
mmk youtube metadata <youtube-url>

# YouTube 영상 타입 확인 (일반 영상 vs Short)
mmk youtube videotype <youtube-url>
```

### 사용 불가 명령어 (토큰 권한 없음)

- `mmk notion ...` — 사용 불가
- `mmk paymint ...` — 사용 불가
- `mmk threads ...` — 사용 불가

## 증시 유튜브 모니터링 자동화

한국 증시 유튜브 채널을 모니터링하여 키워드 매칭 영상을 자막 추출 → 요약 → Slack 알림 → Notion 저장하는 자동화 시스템입니다.

### 커스텀 스킬 (슬래시 커맨드)

| 스킬 | 설명 |
|------|------|
| `/stock-monitor` | 전체 파이프라인 실행 (메인 오케스트레이터) |
| `/fetch-videos` | YouTube RSS 피드 수집 + 키워드 필터링 |
| `/summarize-video <url>` | 개별 영상 자막 추출 + 요약 |
| `/notify-slack` | Slack 채널에 요약 알림 전송 |
| `/save-notion` | Notion 데이터베이스에 요약 저장 |

### 자동 스케줄 실행

```
/loop 60m /stock-monitor
```

### 설정 파일

- `config/channels.json` — 모니터링 채널, 키워드, Slack/Notion ID
- `data/processed.json` — 처리 완료 영상 추적 (중복 방지)

### 모니터링 채널

- 한경 글로벌마켓 (`UCWskYkV4c4S9D__rsfOl2JA`)
- 증시각도기TV (`UCdOjVxkj5JA0iDu3_xcsTyQ`)

### 필터 키워드

경제, 금리, 환율, 물가, 공급망, 무역, 분석, 전망

### Notion DB

- DB: "증시 유튜브 영상 요약" (`4a4ce38b02334900b473aafeb2a8f2ea`)
- 속성: 제목, 채널명, 요약, 핵심 포인트, 영상 URL, 발행일, 처리일

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부
