import json
import os
from core.stats_collector import increment
from alerts.alert_manager import alert_async

TOKEN_FILE = "token_usage.json"

def _read():
    if not os.path.exists(TOKEN_FILE):
        return {"today": 0}
    try:
        return json.load(open(TOKEN_FILE))
    except:
        return {"today": 0}

def _write(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def update_cost(amount):
    try:
        data = _read()
        data["today"] = data.get("today", 0) + amount
        _write(data)
        increment("llm_cost_updates")
    except Exception as e:
        alert_async(f"❌ TokenManager Error: {str(e)}")

def get_today_cost():
    try:
        data = _read()
        return data.get("today", 0)
    except:
        return 0
