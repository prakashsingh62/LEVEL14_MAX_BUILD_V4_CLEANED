from alerts.alert_manager import alert_async
from core.stats_collector import increment
from .llm_client import LLMClient

class EmailParser:
    def parse(self, raw_email="", sender="", subject="", body="", attachments=None):
        if attachments is None:
            attachments = []
        try:
            increment("parsed_emails")
            if not body.strip():
                alert_async("⚠️ Empty email body — LLM fallback triggered.")
                llm = LLMClient()
                fallback = llm.parse_email(raw_email)
                fallback.update({
                    "sender": sender,
                    "subject": subject,
                    "attachments": attachments
                })
                return fallback
            return {
                "sender": sender,
                "subject": subject,
                "body": raw_email,
                "attachments": attachments,
                "type": "raw_email",
                "entities": {}
            }
        except Exception as e:
            alert_async(f"🔎 Parser Error: {str(e)}")
            increment("parser_errors")
            return {
                "sender": sender,
                "subject": subject,
                "body": raw_email,
                "attachments": attachments,
                "type": "unknown",
                "entities": {}
            }
