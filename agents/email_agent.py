from alerts.alert_manager import alert_async
from core.stats_collector import increment
from core.token_manager import update_cost, get_today_cost
from nlp.email_parser import EmailParser
from nlp.llm_client import LLMClient

email_parser = EmailParser()
llm = LLMClient()

def process_email(message):
    try:
        increment("emails_processed")

        parsed = email_parser.parse_raw(message)

        if parsed.get("error") or parsed.get("type") == "unknown":
            return llm.parse_email(message)

        return parsed

    except Exception as e:
        increment("email_agent_errors")
        alert_async(f"📩 Email Agent Error: {str(e)}")
        return {"error": str(e), "raw": message}
