#!/usr/bin/env python3
"""YouTube RSS 피드에서 새 영상을 수집하고 키워드로 필터링하는 스크립트."""

import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "channels.json")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed.json")
RSS_URL_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?channel_id={}"

ATOM_NS = "http://www.w3.org/2005/Atom"
YT_NS = "http://www.youtube.com/xml/schemas/2015"
MEDIA_NS = "http://search.yahoo.com/mrss/"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_processed():
    if not os.path.exists(PROCESSED_PATH):
        return {"processed_ids": [], "last_check": ""}
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_processed(data):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_feed(channel_id):
    """채널의 RSS 피드를 가져와 영상 목록을 반환."""
    url = RSS_URL_TEMPLATE.format(channel_id)
    try:
        with urlopen(url, timeout=15) as response:
            xml_data = response.read()
    except URLError as e:
        print(f"[ERROR] RSS 피드 가져오기 실패 (channel: {channel_id}): {e}", file=sys.stderr)
        return []

    root = ET.fromstring(xml_data)
    channel_name = root.findtext(f"{{{ATOM_NS}}}title", default="Unknown")

    videos = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        video_id = entry.findtext(f"{{{YT_NS}}}videoId", default="")
        title = entry.findtext(f"{{{ATOM_NS}}}title", default="")
        published = entry.findtext(f"{{{ATOM_NS}}}published", default="")
        link_el = entry.find(f"{{{ATOM_NS}}}link[@rel='alternate']")
        url = link_el.get("href", "") if link_el is not None else ""

        media_group = entry.find(f"{{{MEDIA_NS}}}group")
        description = ""
        if media_group is not None:
            description = media_group.findtext(f"{{{MEDIA_NS}}}description", default="")

        videos.append({
            "video_id": video_id,
            "title": title,
            "url": url,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "published": published,
            "description": description,
        })

    return videos


def matches_keywords(title, keywords):
    """제목에 키워드가 하나라도 포함되면 True."""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def main():
    config = load_config()
    processed = load_processed()
    processed_ids = set(processed.get("processed_ids", []))
    keywords = config.get("keywords", [])

    all_new_videos = []

    for channel in config.get("channels", []):
        channel_id = channel["id"]
        videos = fetch_feed(channel_id)

        for video in videos:
            vid = video["video_id"]
            if vid in processed_ids:
                continue
            if not matches_keywords(video["title"], keywords):
                continue
            all_new_videos.append(video)

    # 발행일 기준 오래된 순 정렬
    all_new_videos.sort(key=lambda v: v.get("published", ""))

    # 결과 JSON 출력
    result = {
        "check_time": datetime.now(timezone.utc).isoformat(),
        "new_videos_count": len(all_new_videos),
        "videos": all_new_videos,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
