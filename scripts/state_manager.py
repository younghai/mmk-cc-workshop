#!/usr/bin/env python3
"""처리된 영상 상태를 관리하는 스크립트.

Usage:
    python3 state_manager.py check <video_id>
    python3 state_manager.py add <video_id> <json_metadata>
    python3 state_manager.py update <video_id> <field> <value>
"""

import json
import os
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_PATH = BASE_DIR / "data" / "processed_videos.json"


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"processed": {}}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=STATE_PATH.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, STATE_PATH)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def cmd_check(video_id):
    state = load_state()
    if video_id in state.get("processed", {}):
        print("processed")
    else:
        print("new")


def cmd_add(video_id, metadata_json):
    state = load_state()
    metadata = json.loads(metadata_json)
    state.setdefault("processed", {})[video_id] = metadata
    save_state(state)
    print(f"added {video_id}")


def cmd_update(video_id, field, value):
    state = load_state()
    processed = state.get("processed", {})
    if video_id not in processed:
        print(f"error: {video_id} not found", file=sys.stderr)
        sys.exit(1)
    processed[video_id][field] = value
    save_state(state)
    print(f"updated {video_id}.{field} = {value}")


def main():
    if len(sys.argv) < 3:
        print("Usage: state_manager.py <check|add|update> <video_id> [args...]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    video_id = sys.argv[2]

    if command == "check":
        cmd_check(video_id)
    elif command == "add":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py add <video_id> <json_metadata>", file=sys.stderr)
            sys.exit(1)
        cmd_add(video_id, sys.argv[3])
    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: state_manager.py update <video_id> <field> <value>", file=sys.stderr)
            sys.exit(1)
        cmd_update(video_id, sys.argv[3], sys.argv[4])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
