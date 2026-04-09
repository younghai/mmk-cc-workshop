# 증시 모니터링 초기 설정

이 스킬은 증시 유튜브 모니터링 시스템의 초기 설정을 수행합니다.

## 수행 절차

### 1. 설정 파일 확인

`stock-config.json` 파일을 읽어서 현재 설정 상태를 확인합니다.
`data/processed_videos.json` 파일이 없으면 `{"processed": {}}` 로 생성합니다.

### 2. Notion 데이터베이스 생성

Notion MCP 도구를 사용하여 "증시 유튜브 요약" 데이터베이스를 생성합니다.

1. `notion-search` 도구로 "증시 유튜브 요약" 데이터베이스가 이미 있는지 검색합니다.
2. 없으면 `notion-create-database` 도구로 새 데이터베이스를 생성합니다.
   - 속성:
     - **제목** (title): 영상 제목
     - **채널** (select): 채널명 (한경글로벌마켓, 한국경제TV, 증시각도기TV)
     - **게시일** (date): 영상 게시 날짜
     - **URL** (url): 유튜브 링크
     - **요약** (rich_text): 한줄 요약
     - **시장전망** (select): 긍정적 / 부정적 / 중립
     - **언급종목** (multi_select): 영상에서 언급된 종목들
3. 생성된 데이터베이스 ID를 `stock-config.json`의 `notifications.notion.database_id`에 저장합니다.
4. `notifications.notion.enabled`를 `true`로 변경합니다.

### 3. Slack 채널 설정

사용자에게 Slack 채널 이름을 물어봅니다.

1. `slack_search_channels` MCP 도구로 채널을 검색합니다.
2. 찾은 채널 ID를 `stock-config.json`의 `notifications.slack.channel_id`에 저장합니다.
3. `notifications.slack.enabled`를 `true`로 변경합니다.

### 4. 설정 확인

최종 `stock-config.json` 내용을 사용자에게 보여주고 확인합니다.

## 참고

- Notion MCP 도구: `notion-search`, `notion-create-database`, `notion-fetch`
- Slack MCP 도구: `slack_search_channels`
- 설정 파일: `stock-config.json`
