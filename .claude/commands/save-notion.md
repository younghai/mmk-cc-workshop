# /save-notion - Notion 데이터베이스 저장

요약된 영상 데이터를 Notion 데이터베이스에 저장합니다.

## 입력

사용자가 저장할 영상 요약 데이터를 제공합니다. 인자: $ARGUMENTS

## 실행 방법

1. `config/channels.json` 에서 `notion_database_id`를 읽습니다.
2. MCP 도구 `notion-create-pages`를 사용하여 새 페이지를 생성합니다.

## Notion DB 정보

- **Database ID**: `4a4ce38b02334900b473aafeb2a8f2ea`
- **Data Source URL**: `collection://cc4edc12-bd4b-4ee5-8662-0b28ae9fff0f`

## DB 스키마

| 속성 | 타입 | 설명 |
|------|------|------|
| 제목 | Title | 영상 제목 |
| 채널명 | Select | 한경 글로벌마켓 / 증시각도기TV |
| 요약 | Rich Text | 한줄 요약 (2-3문장) |
| 핵심 포인트 | Rich Text | 핵심 포인트 목록 |
| 영상 URL | URL | YouTube 영상 링크 |
| 발행일 | Date | 영상 발행일 |
| 처리일 | Date | 요약 처리일 |

## MCP 도구 사용

`notion-create-pages` 도구로 위 스키마에 맞춰 페이지를 생성합니다.
database_id는 `4a4ce38b02334900b473aafeb2a8f2ea`를 사용합니다.

## 주의사항

- 날짜는 ISO 8601 형식을 사용합니다 (YYYY-MM-DD).
- 채널명은 Select 속성이므로 정확한 옵션명을 사용합니다.
