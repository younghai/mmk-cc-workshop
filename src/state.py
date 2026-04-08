"""처리 상태 관리 모듈 - 중복 처리 방지를 위한 영상 ID 추적."""

import json
import os
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "data"
DEFAULT_STATE_FILE = STATE_DIR / "processed_videos.json"


def load_state(state_file=DEFAULT_STATE_FILE):
    """처리 상태를 디스크에서 로드한다. 파일이 없으면 빈 상태를 생성한다."""
    state_file = Path(state_file)
    state_file.parent.mkdir(parents=True, exist_ok=True)

    if not state_file.exists():
        return {"processed": {}, "last_run": None}

    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        backup = state_file.with_suffix(".json.bak")
        state_file.rename(backup)
        return {"processed": {}, "last_run": None}


def save_state(state, state_file=DEFAULT_STATE_FILE):
    """상태를 디스크에 원자적으로 저장한다 (tmp 파일 후 rename)."""
    state_file = Path(state_file)
    state_file.parent.mkdir(parents=True, exist_ok=True)

    state["last_run"] = datetime.now().isoformat()

    tmp_file = state_file.with_suffix(".json.tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, state_file)


def is_processed(video_id, state):
    """영상이 이미 처리되었는지 확인한다."""
    return video_id in state.get("processed", {})


def mark_processed(video_id, title, channel, had_subtitles, state):
    """영상을 처리 완료로 표시한다 (메모리 내). save_state()를 별도 호출해야 디스크에 반영된다."""
    if "processed" not in state:
        state["processed"] = {}

    state["processed"][video_id] = {
        "title": title,
        "channel": channel,
        "processed_at": datetime.now().isoformat(),
        "had_subtitles": had_subtitles,
    }
    return state


if __name__ == "__main__":
    s = load_state()
    print(json.dumps(s, ensure_ascii=False, indent=2))
