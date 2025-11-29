from alerts.alert_manager import alert_async
from core.stats_collector import increment
from nlp.parser import EmailParser
from nlp.llm_client import LLMClient

email_parser = EmailParser()
llm = LLMClient()

def safe_parse(raw, sender, subject, body, attachments):
    try:
        increment("emails_parsed")

        if not body or not body.strip():
            alert_async("⚠️ Empty email body — using LLM fallback.")
            fallback = llm.parse_email(raw)
            fallback.update({
                "sender": sender,
                "subject": subject,
                "attachments": attachments
            })
            return fallback

        return email_parser.parse(
            raw_email=raw,
            sender=sender,
            subject=subject,
            body=body,
            attachments=attachments
        )

    except Exception as e:
        increment("email_engine_errors")
        alert_async(f"🔥 EmailEngine Error: {str(e)}")

        return {
            "type": "unknown",
            "raw": raw,
            "sender": sender,
            "subject": subject,
            "body": body,
            "attachments": attachments
        }
