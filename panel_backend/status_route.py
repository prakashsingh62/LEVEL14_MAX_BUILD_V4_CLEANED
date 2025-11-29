from flask import Blueprint, jsonify
import datetime
from core.token_manager import get_today_tokens

status_bp = Blueprint("status_bp", __name__)

@status_bp.route("/status", methods=["GET"])
def status():
    """
    Returns:
    - pythonpath (for debugging)
    - server status
    - current server time
    """
    return jsonify({
        "pythonpath": __import__("sys").path[0],
        "status": "online",
        "time": datetime.datetime.now().isoformat()
    })


@status_bp.route("/tokens", methods=["GET"])
def tokens():
    """
    Returns real-time token usage.
    """
    used = get_today_tokens()
    remaining = 50000 - used

    return jsonify({
        "used_tokens": used,
        "remaining_tokens": remaining
    })


