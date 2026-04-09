# /summarize-video - 유튜브 영상 자막 추출 + 요약

개별 유튜브 영상의 자막을 추출하고 내용을 요약합니다.

## 입력

사용자가 YouTube URL 또는 video ID를 제공합니다. 인자: $ARGUMENTS

## 실행 방법

1. `mmk youtube metadata "$ARGUMENTS"` 로 영상 메타데이터를 조회합니다.
2. `mmk youtube videotype "$ARGUMENTS"` 로 영상 타입을 확인합니다 (Shorts 제외).
3. `mmk youtube transcript "$ARGUMENTS"` 로 자막을 추출합니다.
4. 추출된 자막 내용을 아래 형식으로 한국어 요약합니다.

## 요약 형식

다음 구조로 요약을 작성합니다:

### 요약 결과
- **제목**: 영상 제목
- **채널**: 채널명
- **발행일**: YYYY-MM-DD
- **한줄 요약**: 2-3문장으로 핵심 내용 요약
- **핵심 포인트**:
  1. (3-5개 핵심 포인트)
- **시장 영향 분석**: 투자자 관점에서의 시사점 1-2문장
- **원본 URL**: https://...

## 주의사항

- 자막이 없는 경우 메타데이터의 description으로 대체합니다.
- 한국어로 요약합니다.
- 투자 조언이 아닌 정보 요약임을 명시합니다.
