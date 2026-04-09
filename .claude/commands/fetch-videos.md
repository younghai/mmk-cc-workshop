# /fetch-videos - YouTube RSS 피드 수집 + 키워드 필터링

등록된 YouTube 채널에서 새로운 영상을 확인하고, 키워드 필터링을 적용하여 관심 영상만 추출합니다.

## 실행 방법

1. `python3 scripts/fetch_feeds.py` 스크립트를 실행합니다.
2. 출력된 JSON 결과를 확인합니다.
3. `new_videos_count`가 0이면 "새로운 관심 영상이 없습니다"라고 보고합니다.
4. 새 영상이 있으면 각 영상의 제목, 채널, 발행일, URL을 목록으로 정리하여 보고합니다.

## 설정 파일

- 채널/키워드 설정: `config/channels.json`
- 처리 완료 추적: `data/processed.json`

## 출력 형식

```
[새 영상 발견: N건]
1. [채널명] 제목 (발행일)
   URL: https://...
2. ...
```
