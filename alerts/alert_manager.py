import os, threading, requests

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "")

def _post(url, data):
    try:
        requests.post(url, json=data, timeout=4)
    except Exception:
        pass

def send_alert(message):
    if not SLACK_WEBHOOK:
        return
    payload = {
        "attachments":[{"color":"#ff0000","blocks":[{"type":"section","text":{"type":"mrkdwn","text": message}}]}]
    }
    _post(SLACK_WEBHOOK, payload)

def alert_async(message):
    threading.Thread(target=send_alert, args=(message,), daemon=True).start()