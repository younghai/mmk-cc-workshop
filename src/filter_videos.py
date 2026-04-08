"""영상 필터링 스크립트 - 키워드, 기간, 중복 기준으로 필터링."""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.state import load_state, is_processed


CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_relative_time(text):
    """상대 시간 문자열을 datetime으로 변환. '3시간 전' 또는 '3 hours ago' -> datetime."""
    if not text:
        return None

    # 한국어 패턴
    ko_patterns = {
        "초": "seconds", "분": "minutes", "시간": "hours",
        "일": "days", "주": "weeks", "개월": "months", "년": "years",
    }
    match = re.match(r"(\d+)\s*(초|분|시간|일|주|개월|년)\s*전", text)
    if match:
        value = int(match.group(1))
        en_unit = ko_patterns.get(match.group(2))
    else:
        # 영어 패턴
        en_patterns = {
            "second": "seconds", "seconds": "seconds",
            "minute": "minutes", "minutes": "minutes",
            "hour": "hours", "hours": "hours",
            "day": "days", "days": "days",
            "week": "weeks", "weeks": "weeks",
            "month": "months", "months": "months",
            "year": "years", "years": "years",
        }
        match = re.match(r"(\d+)\s+(second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\s+ago", text)
        if not match:
            return None
        value = int(match.group(1))
        en_unit = en_patterns.get(match.group(2))

    if not en_unit:
        return None

    now = datetime.now()
    if en_unit == "months":
        return now - timedelta(days=value * 30)
    elif en_unit == "years":
        return now - timedelta(days=value * 365)
    else:
        return now - timedelta(**{en_unit: value})


def get_channel_config(channel_name, config):
    """채널 이름으로 채널 설정을 찾는다."""
    for ch in config.get("channels", []):
        if ch["name"] == channel_name:
            return ch
    return None


def filter_videos(videos, config):
    """모든 필터 조건을 적용하여 영상을 필터링한다."""
    state = load_state()
    filter_cfg = config.get("filter", {})
    exclude_keywords = [kw.lower() for kw in filter_cfg.get("exclude_keywords", [])]
    max_age_hours = filter_cfg.get("max_age_hours", 24)
    min_duration = filter_cfg.get("min_duration_seconds", 0)
    max_duration = filter_cfg.get("max_duration_seconds", 99999)

    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
    filtered = []

    for video in videos:
        video_id = video.get("video_id", "")
        title = video.get("title", "")
        title_lower = title.lower()
        channel_name = video.get("channel_name", "")

        # 1. 이미 처리된 영상 스킵
        if is_processed(video_id, state):
            continue

        # 2. 제외 키워드 체크
        if any(kw in title_lower for kw in exclude_keywords):
            continue

        # 3. 영상 길이 체크
        duration = video.get("duration_seconds")
        if duration is not None:
            if duration < min_duration or duration > max_duration:
                continue

        # 4. 게시 시간 체크 (max_age_hours 이내)
        published_time = parse_relative_time(video.get("published_text", ""))
        if published_time and published_time < cutoff_time:
            continue

        # 5. 채널별 키워드 매칭
        ch_config = get_channel_config(channel_name, config)
        if ch_config:
            keywords = ch_config.get("keywords", [])
            if keywords:  # 키워드가 설정된 경우에만 필터링
                if not any(kw.lower() in title_lower for kw in keywords):
                    continue
            # keywords가 빈 배열이면 전체 수집 (증시각도기TV)

        filtered.append(video)

    return filtered


def main():
    parser = argparse.ArgumentParser(description="영상 필터링")
    parser.add_argument("--input", type=str, help="영상 목록 JSON 문자열")
    args = parser.parse_args()

    if args.input:
        videos = json.loads(args.input)
    else:
        videos = json.load(sys.stdin)

    config = load_config()
    result = filter_videos(videos, config)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
