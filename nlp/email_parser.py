from core.stats_collector import increment
from alerts.alert_manager import alert_async

class EmailParser:
    def parse_raw(self, message):
        try:
            increment("parsed_emails")

            # Example parsing logic
            body = message.get("body", "")
            subject = message.get("subject", "")
            sender = message.get("from", "")

            if not body.strip():
                increment("parser_errors")
                return {"type": "unknown", "body": body}

            return {
                "type": "parsed",
                "sender": sender,
                "subject": subject,
                "body": body
            }

        except Exception as e:
            increment("parser_errors")
            alert_async(f"❌ EmailParser Error: {str(e)}")
            return {"error": str(e), "raw": message}
