#!/usr/bin/env python3
"""YouTube RSS 피드에서 신규 영상을 감지하고 키워드 필터링하는 스크립트."""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "stock-config.json"
STATE_PATH = BASE_DIR / "data" / "processed_videos.json"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

ATOM_NS = "http://www.w3.org/2005/Atom"
YT_NS = "http://www.youtube.com/xml/schemas/2015"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_processed():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f).get("processed", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def fetch_rss(channel_id):
    url = RSS_URL.format(channel_id=channel_id)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"[ERROR] RSS fetch failed for {channel_id}: {e}", file=sys.stderr)
        return None


def parse_feed(xml_text):
    entries = []
    root = ET.fromstring(xml_text)
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        video_id = entry.find(f"{{{YT_NS}}}videoId")
        title = entry.find(f"{{{ATOM_NS}}}title")
        published = entry.find(f"{{{ATOM_NS}}}published")
        if video_id is not None and title is not None:
            entries.append({
                "id": video_id.text,
                "title": title.text,
                "url": f"https://www.youtube.com/watch?v={video_id.text}",
                "published": published.text if published is not None else "",
            })
    return entries


def matches_keywords(title, keywords, exclude_keywords):
    title_lower = title.lower()
    for ex in exclude_keywords:
        if ex.lower() in title_lower:
            return False
    if not keywords:
        return True
    return any(kw.lower() in title_lower for kw in keywords)


def main():
    config = load_config()
    processed = load_processed()
    exclude_keywords = config.get("filter", {}).get("exclude_keywords", [])

    new_videos = []
    for channel in config.get("channels", []):
        channel_id = channel["id"]
        channel_name = channel["name"]
        keywords = channel.get("keywords", [])

        xml_text = fetch_rss(channel_id)
        if xml_text is None:
            continue

        entries = parse_feed(xml_text)
        for entry in entries:
            if entry["id"] in processed:
                continue
            if not matches_keywords(entry["title"], keywords, exclude_keywords):
                continue
            entry["channel"] = channel_name
            entry["channel_id"] = channel_id
            new_videos.append(entry)

    print(json.dumps(new_videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
