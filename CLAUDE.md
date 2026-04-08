# Claude Code 워크샵 스타터

강의 실습용 Claude Code 워크샵 스타터 프로젝트입니다.

## 프로젝트 목적

이 프로젝트를 fork하여 Claude Code 웹에서 바로 자동화 바이브 코딩을 시작할 수 있습니다.

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node 버전
- 원격 환경 여부

아무것도 설치하지 않으며, 읽기 전용 체크만 수행합니다.

## 주식 유튜브 모니터링 자동화

### 구조
- `src/fetch_videos.py` - YouTube 채널에서 최신 영상 수집 (scrapetube)
- `src/filter_videos.py` - 키워드/기간/중복 기준으로 필터링
- `src/extract_subtitles.py` - 한국어 자막 추출 (youtube-transcript-api)
- `src/state.py` - 처리 상태 관리 (중복 방지)
- `config/channels.json` - 채널, 필터, Slack/Notion 설정
- `data/processed_videos.json` - 처리 완료 영상 추적 (자동 생성)
- `.claude/commands/monitor.md` - `/monitor` 오케스트레이션 커맨드

### 대상 채널
1. **한경글로벌마켓**: 빈난새의 개장전요것만, 김현석의 월스트리트나우
2. **한국경제TV**: 당잠사
3. **증시각도기TV**: 전체 콘텐츠

### 실행 방법
- `/monitor` - 수동 1회 실행
- `/loop 60m /monitor` - 매 1시간 자동 실행

### MCP 도구 사용
- Slack 전송: `slack_send_message` (channel_id, message)
- Notion 저장: `notion-create-pages` (pages, parent with database_id)

### 설정 변경
- 채널 추가/제거: `config/channels.json`의 `channels` 배열 수정
- Slack 채널: `config/channels.json`의 `slack.channel_id` 설정
- Notion DB: `config/channels.json`의 `notion.database_id` 설정

### 의존성
```bash
pip install -r requirements.txt
```
- `scrapetube` - YouTube 채널 영상 목록 (API 키 불필요)
- `youtube-transcript-api` - 자막 추출 (경량, 한국어 자동생성 자막 지원)
