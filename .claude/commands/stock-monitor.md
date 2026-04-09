# /stock-monitor - 증시 유튜브 모니터링 메인 오케스트레이터

등록된 한국 증시 유튜브 채널에서 새 영상을 감지하고, 자막 추출 → 요약 → Slack 알림 → Notion 저장까지 전체 파이프라인을 실행합니다.

## 전체 흐름

### Step 1: 새 영상 확인
1. `python3 scripts/fetch_feeds.py` 를 실행하여 새로운 관심 영상 목록을 가져옵니다.
2. 결과 JSON의 `new_videos_count`가 0이면 "새로운 관심 영상이 없습니다. 다음 체크까지 대기합니다."를 출력하고 종료합니다.

### Step 2: 각 영상 처리 (영상별 반복)
새 영상 각각에 대해 다음을 순서대로 수행합니다:

#### 2a. 자막 추출
```bash
mmk youtube transcript "<video_url>"
mmk youtube metadata "<video_url>" -o json
```

#### 2b. 내용 요약
추출된 자막을 아래 형식으로 요약합니다:
- **한줄 요약**: 2-3문장
- **핵심 포인트**: 3-5개 bullet points
- **시장 영향 분석**: 투자자 관점 시사점 1-2문장

#### 2c. Slack 알림 전송
MCP 도구 `slack_send_message_draft`를 사용합니다.
- `config/channels.json`에서 `slack_channel_id` 읽기
- 채널 ID가 비어있으면 이 단계를 건너뛰고 경고 메시지 출력

메시지 형식:
```
*[채널명] 새 영상 요약*

*제목:* {title}
*발행일:* {date}

*한줄 요약:*
{summary}

*핵심 포인트:*
{key_points}

*시장 영향:*
{market_impact}

<{video_url}|원본 영상 보기>
```

#### 2d. Notion 저장
MCP 도구 `notion-create-pages`를 사용합니다.
- Database ID: `4a4ce38b02334900b473aafeb2a8f2ea`
- 속성: 제목, 채널명(Select), 요약, 핵심 포인트, 영상 URL, 발행일, 처리일(오늘)

#### 2e. 처리 완료 기록
`data/processed.json` 파일을 읽고 해당 video_id를 `processed_ids` 배열에 추가하고, `last_check`를 현재 시간으로 업데이트한 뒤 저장합니다.

### Step 3: 결과 보고
모든 영상 처리 완료 후 요약 보고를 출력합니다:
```
[증시 유튜브 모니터링 완료]
- 체크 시간: YYYY-MM-DD HH:MM
- 처리된 영상: N건
  1. [채널명] 제목
  2. ...
- Slack 알림: 전송됨/건너뜀
- Notion 저장: 완료
```

## 스케줄 자동화

이 스킬을 1시간 간격으로 자동 실행하려면:
```
/loop 60m /stock-monitor
```

## 설정 파일

- `config/channels.json`: 채널 목록, 키워드, Slack/Notion ID
- `data/processed.json`: 처리 완료 영상 추적

## 주의사항

- 자막 추출 실패 시 해당 영상을 건너뛰고 다음 영상을 처리합니다.
- 투자 조언이 아닌 정보 요약임을 Slack 메시지 하단에 명시합니다.
- processed.json은 영상 처리 직후 즉시 업데이트하여 중복 방지합니다.
