# /notify-slack - Slack 알림 전송

요약된 영상 정보를 Slack 채널에 알림으로 전송합니다.

## 입력

사용자가 전송할 메시지 내용을 제공합니다. 인자: $ARGUMENTS

## 실행 방법

1. `config/channels.json` 에서 `slack_channel_id`를 읽습니다.
2. `slack_channel_id`가 비어있으면 사용자에게 Slack 채널 ID를 요청합니다.
3. MCP 도구 `slack_send_message_draft`를 사용하여 메시지를 전송합니다.

## 메시지 형식

```markdown
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

## MCP 도구 사용

```
slack_send_message_draft:
  channel_id: config에서 읽은 slack_channel_id
  message: 위 형식의 메시지
```

## 주의사항

- 메시지는 Slack markdown 형식을 사용합니다.
- 채널 ID가 설정되지 않은 경우 사용자에게 먼저 설정을 요청합니다.
