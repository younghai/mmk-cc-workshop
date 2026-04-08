"""YouTube 채널에서 최신 영상 목록을 수집하는 스크립트."""

import json
import sys
from pathlib import Path

import scrapetube


CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_duration(text):
    """'10:30' -> 630, '1:10:30' -> 4230 형태의 시간 문자열을 초로 변환."""
    if not text:
        return None
    parts = text.split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except ValueError:
        return None
    return None


def extract_text(obj, *keys):
    """중첩된 YouTube 데이터 구조에서 텍스트를 안전하게 추출."""
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and len(current) > 0:
            current = current[0].get(key) if isinstance(current[0], dict) else None
        else:
            return None
    return current


def fetch_channel_videos(channel_id, channel_name, limit=10):
    """단일 채널에서 최신 영상을 가져온다."""
    videos = []
    try:
        raw_videos = scrapetube.get_channel(channel_id=channel_id, limit=limit)
        for v in raw_videos:
            video_id = v.get("videoId", "")
            title = extract_text(v, "title", "runs") or ""
            if isinstance(title, list):
                title = title[0].get("text", "") if title else ""
            elif isinstance(title, dict):
                title = title.get("text", "")

            # title이 runs 배열인 경우
            title_obj = v.get("title", {})
            if isinstance(title_obj, dict):
                runs = title_obj.get("runs", [])
                if runs and isinstance(runs, list):
                    title = runs[0].get("text", "")
                elif "simpleText" in title_obj:
                    title = title_obj["simpleText"]

            published_text = ""
            pt_obj = v.get("publishedTimeText", {})
            if isinstance(pt_obj, dict):
                published_text = pt_obj.get("simpleText", "")

            duration_text = ""
            lt_obj = v.get("lengthText", {})
            if isinstance(lt_obj, dict):
                duration_text = lt_obj.get("simpleText", "")

            videos.append({
                "video_id": video_id,
                "title": title,
                "channel_name": channel_name,
                "channel_id": channel_id,
                "published_text": published_text,
                "duration_seconds": parse_duration(duration_text),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })
    except Exception as e:
        print(f"[ERROR] {channel_name} 채널 수집 실패: {e}", file=sys.stderr)

    return videos


def fetch_all_channels(config):
    """설정된 모든 활성 채널에서 영상을 수집한다."""
    all_videos = []
    limit = config.get("processing", {}).get("videos_per_channel", 10)

    for ch in config.get("channels", []):
        if not ch.get("enabled", True):
            continue
        name = ch["name"]
        channel_id = ch["channel_id"]
        print(f"[INFO] {name} 채널 수집 중...", file=sys.stderr)
        videos = fetch_channel_videos(channel_id, name, limit=limit)
        print(f"[INFO] {name}: {len(videos)}개 영상 수집", file=sys.stderr)
        all_videos.extend(videos)

    return all_videos


def main():
    config = load_config()
    videos = fetch_all_channels(config)
    print(json.dumps(videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
