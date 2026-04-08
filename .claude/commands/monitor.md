# YouTube 주식 채널 모니터링

한국 증시 유튜브 채널의 신규 영상을 수집하고, 자막을 추출하여 요약한 뒤 Slack과 Notion으로 전송한다.

다음 단계를 순서대로 실행하세요:

## 1단계: 영상 수집

```bash
cd /home/user/mmk-cc-workshop && python3 src/fetch_videos.py
```

결과를 JSON으로 파싱하세요. 에러가 발생하면 stderr 메시지를 확인하고 보고하세요.
수집된 영상이 0개이면 "채널 접속 실패"를 보고하고 종료하세요.

## 2단계: 영상 필터링

1단계 결과 JSON을 임시 파일에 저장한 후 stdin으로 전달합니다:

```bash
cd /home/user/mmk-cc-workshop && echo '<1단계_JSON>' | python3 src/filter_videos.py
```

필터링 결과가 빈 배열 `[]`이면 "새로운 영상이 없습니다"라고 보고하고 종료하세요.

## 3단계: 자막 추출

```bash
cd /home/user/mmk-cc-workshop && echo '<2단계_JSON>' | python3 src/extract_subtitles.py
```

## 4단계: AI 요약

각 영상의 `subtitle_text`를 읽고 **한국어로 요약**하세요:

각 영상별로 다음 형식으로 요약합니다:
- **핵심 내용**: 3~5개 불릿 포인트
- **언급된 종목/시장**: 관련 종목명, 지수
- **시장 전망**: 강세/약세/중립 판단 근거
- **리스크 요인**: 주의할 점

`subtitle_text`가 null인 영상은 제목만 기록하세요: "자막 없음 - 직접 시청 필요"

## 5단계: Slack 전송

`config/channels.json`의 `slack.channel_id`를 읽어서 MCP 도구 `slack_send_message`로 전송하세요.

`slack.channel_id`가 "PLACEHOLDER"이면 이 단계를 건너뛰고 "Slack 미설정 - config/channels.json에서 slack.channel_id를 설정하세요"라고 보고하세요.

메시지 포맷:
```
📈 주식 유튜브 모니터링 리포트 (YYYY-MM-DD HH:MM)

━━━━━━━━━━━━━━━━━━━━
[채널명] 영상 제목
🔗 영상 URL
━━━━━━━━━━━━━━━━━━━━
• 핵심 내용 요약 1
• 핵심 내용 요약 2
• 핵심 내용 요약 3
📊 종목/시장: 삼성전자, 코스피, S&P500 ...
📉 전망: 강세/약세/중립

(영상별로 반복)
```

메시지가 4000자를 초과하면 영상 단위로 분할하여 여러 메시지로 전송하세요.

## 6단계: Notion 저장

`config/channels.json`의 `notion.database_id`를 읽어서 MCP 도구 `notion-create-pages`로 저장하세요.

`notion.database_id`가 "PLACEHOLDER"이면 이 단계를 건너뛰고 "Notion 미설정 - config/channels.json에서 notion.database_id를 설정하세요"라고 보고하세요.

각 영상별로 Notion 페이지를 생성합니다:
- properties:
  - 제목: 영상 제목
  - 채널: 채널명
  - URL: 영상 URL
  - 날짜: 현재 날짜
- content: 요약 내용 (마크다운)

## 7단계: 상태 업데이트

처리된 영상의 상태를 업데이트합니다:

```bash
cd /home/user/mmk-cc-workshop && python3 -c "
import json, sys
sys.path.insert(0, '.')
from src.state import load_state, mark_processed, save_state
state = load_state()
videos = json.loads('''<처리된_영상_JSON>''')
for v in videos:
    mark_processed(v['video_id'], v['title'], v.get('channel_name',''), v.get('subtitle_text') is not None, state)
save_state(state)
print(f'상태 업데이트 완료: {len(videos)}개 영상')
"
```

## 완료

처리 결과를 요약하여 보고하세요:
- 수집된 채널 수
- 필터링 통과 영상 수
- 자막 추출 성공/실패 수
- Slack/Notion 전송 결과
