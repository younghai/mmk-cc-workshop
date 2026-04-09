# 증시 유튜브 모니터링 (오케스트레이터)

이 스킬은 증시 유튜브 모니터링의 전체 파이프라인을 실행합니다.
`/loop 60m /stock-monitor` 로 1시간마다 자동 실행할 수 있습니다.

## 수행 절차

### 1. 신규 영상 감지

```bash
python3 scripts/fetch_rss.py
```

출력된 JSON 배열을 파싱하여 신규 영상 목록을 확인합니다.
신규 영상이 없으면 "신규 영상이 없습니다." 라고 보고하고 종료합니다.

### 2. 각 영상 처리

신규 영상 각각에 대해 다음을 순서대로 수행합니다:

#### 2-1. 영상 타입 확인
```bash
mmk youtube videotype VIDEO_URL
```
Shorts면 스킵합니다.

#### 2-2. 메타데이터 조회
```bash
mmk youtube metadata VIDEO_URL --output json
```

#### 2-3. 자막 추출
```bash
mmk youtube transcript VIDEO_URL --format text
```
자막 추출 실패 시 해당 영상을 스킵하고 다음 영상으로 진행합니다.

#### 2-4. 요약 생성

추출한 자막과 메타데이터를 기반으로 한국어 구조화된 요약을 생성합니다:
- 한줄 요약
- 핵심 포인트 (3~5개)
- 언급 종목/섹터
- 시장 전망 (긍정적/부정적/중립)
- 투자 시사점

요약 시 유의사항:
- 한국어로 작성
- 투자자 관점에서 실용적 정보에 집중
- 종목명은 한국어+티커 병기 (예: 삼성전자(005930), 테슬라(TSLA))

#### 2-5. 알림 전송

`stock-config.json`에서 알림 설정을 읽습니다.

**Slack** (`notifications.slack.enabled`가 `true`이면):
`slack_send_message` MCP 도구로 포맷된 요약 메시지를 전송합니다.

메시지 포맷:
```
*[채널명] 새 영상 요약*

*제목:* 영상 제목
*링크:* URL

*한줄 요약:* ...

*핵심 포인트:*
- ...

*언급 종목:* ...
*시장 전망:* ...
*게시일:* ...
```

**Notion** (`notifications.notion.enabled`가 `true`이면):
`notion-create-pages` MCP 도구로 데이터베이스에 페이지를 생성합니다.
- 속성: 제목, 채널, 게시일, URL, 요약, 시장전망, 언급종목
- 내용: 전체 구조화된 요약

#### 2-6. 상태 기록

```bash
python3 scripts/state_manager.py add VIDEO_ID '{"title":"...","channel":"...","processed_at":"..."}'
```

### 3. 실행 결과 요약

모든 영상 처리 후 다음을 보고합니다:

```
## 증시 모니터링 실행 결과

- 감지된 신규 영상: N건
- 처리 완료: N건
- 스킵 (Shorts/자막없음): N건
- 에러: N건

### 처리된 영상
1. [채널명] 영상 제목 — 시장전망: 긍정적
2. [채널명] 영상 제목 — 시장전망: 중립
```

## 에러 처리

- RSS 피드 조회 실패: 해당 채널 스킵, 다음 채널 계속 진행
- 자막 추출 실패: 해당 영상 스킵, state에 기록하지 않음 (다음 실행에서 재시도)
- Slack/Notion 전송 실패: 에러 보고, state에는 기록 (재전송 방지)
- 하나의 영상 에러가 전체 실행을 중단하지 않음

## 설정 파일

- 채널/키워드 설정: `stock-config.json`
- 처리 상태: `data/processed_videos.json`
- Python 스크립트: `scripts/fetch_rss.py`, `scripts/state_manager.py`
