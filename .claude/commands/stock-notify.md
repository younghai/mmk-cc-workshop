# 증시 요약 알림 (Slack + Notion)

이 스킬은 처리된 영상 요약을 Slack과 Notion에 전송합니다.

## 인자

- `$ARGUMENTS`: 알림을 보낼 영상 정보 (제목, 채널, URL, 요약 내용 등)

## 수행 절차

### 0. 설정 읽기

`stock-config.json` 파일을 읽어서 Slack과 Notion 설정을 확인합니다.

### 1. Slack 알림 전송

`notifications.slack.enabled`가 `true`이고 `channel_id`가 설정되어 있으면:

`slack_send_message` MCP 도구를 사용하여 메시지를 전송합니다.

**메시지 포맷:**
```
*[채널명] 새 영상 요약*

*제목:* 영상 제목
*링크:* https://youtube.com/watch?v=...

*한줄 요약:* ...

*핵심 포인트:*
- Point 1
- Point 2
- Point 3

*언급 종목:* 삼성전자, SK하이닉스, ...
*시장 전망:* 긍정적 / 부정적 / 중립

*게시일:* 2026-04-08
```

### 2. Notion 저장

`notifications.notion.enabled`가 `true`이고 `database_id`가 설정되어 있으면:

`notion-create-pages` MCP 도구를 사용하여 데이터베이스에 새 페이지를 생성합니다.

**페이지 속성:**
- 제목: 영상 제목
- 채널: 채널명 (select)
- 게시일: 영상 게시 날짜 (date)
- URL: 유튜브 링크 (url)
- 요약: 한줄 요약 (rich_text)
- 시장전망: 긍정적/부정적/중립 (select)
- 언급종목: 종목 리스트 (multi_select)

**페이지 내용:** 전체 구조화된 요약 (핵심 포인트, 언급 종목, 시장 전망, 투자 시사점)

### 3. 상태 업데이트

영상 처리 완료를 기록합니다:

```bash
python3 scripts/state_manager.py add VIDEO_ID '{"title":"...","channel":"...","processed_at":"...","notified_slack":true,"notified_notion":true}'
```

### 4. 결과 보고

- Slack 전송 성공/실패 여부
- Notion 저장 성공/실패 여부
- 둘 중 하나라도 실패하면 에러 내용 보고 (다른 쪽은 독립적으로 시도)

## MCP 도구 참조

- Slack: `slack_send_message` (channel_id, message 필요)
- Notion: `notion-create-pages` (parent.database_id, pages 배열 필요)
- Notion DB 스키마 확인: `notion-fetch` (database_id로 조회)
