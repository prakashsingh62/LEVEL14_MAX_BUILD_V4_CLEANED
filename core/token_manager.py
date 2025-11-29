import json
import os
import threading
from datetime import datetime

TOKEN_FILE = "token_usage.json"
_lock = threading.Lock()


def _load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return {"date": datetime.now().strftime("%Y-%m-%d"), "used": 0}

    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except:
        return {"date": datetime.now().strftime("%Y-%m-%d"), "used": 0}


def _save_tokens(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_tokens(amount):
    """Increase token usage by amount."""
    with _lock:
        data = _load_tokens()

        # Reset daily limit if date changed
        today = datetime.now().strftime("%Y-%m-%d")
        if data.get("date") != today:
            data = {"date": today, "used": 0}

        data["used"] = max(0, data.get("used", 0) + amount)
        _save_tokens(data)


def get_today_cost():
    """Return tokens used today."""
    data = _load_tokens()
    today = datetime.now().strftime("%Y-%m-%d")
    if data.get("date") != today:
        return 0
    return data.get("used", 0)
