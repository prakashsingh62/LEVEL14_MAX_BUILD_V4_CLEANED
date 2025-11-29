import json
import os
import threading
from datetime import datetime

TOKEN_FILE = "token_usage.json"
_lock = threading.Lock()

def _default_data():
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "used_tokens": 0
    }

def _load():
    if not os.path.exists(TOKEN_FILE):
        return _default_data()

    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except:
        return _default_data()

def _save(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _reset_if_new_day(data):
    today = datetime.now().strftime("%Y-%m-%d")
    if data["date"] != today:
        data["date"] = today
        data["used_tokens"] = 0
    return data

# ------------------------------------------------------
# PUBLIC FUNCTIONS (USE THESE)
# ------------------------------------------------------

def update_tokens(amount: int):
    """Add tokens used today."""
    with _lock:
        data = _load()
        data = _reset_if_new_day(data)

        data["used_tokens"] += amount
        _save(data)

def get_today_tokens() -> int:
    """Return total tokens used today."""
    with _lock:
        data = _load()
        data = _reset_if_new_day(data)
        return data["used_tokens"]
