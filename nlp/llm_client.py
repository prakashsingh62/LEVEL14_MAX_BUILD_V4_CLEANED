from alerts.alert_manager import alert_async
from core.stats_collector import increment
from core.token_manager import update_tokens, get_today_tokens
import time

class LLMClient:
    def classify_email(self, text):
        try:
            increment("llm_calls")
            if "quote" in text.lower(): 
                return "vendor_reply"
            if "follow" in text.lower(): 
                return "client_followup"
            return "generic"
        except Exception as e:
            alert_async(f"🤖 LLM Classification Error: {str(e)}")
            increment("llm_errors")
            return "unknown"

    def extract_entities(self, text):
        try:
            entities = {}
            if "today" in text.lower():
                entities["date_mentioned"] = "today"
            return entities
        except Exception as e:
            alert_async(f"🤖 Entity Extraction Error: {str(e)}")
            increment("llm_errors")
            return {}

    def parse_email(self, text):
        start = time.time()
        try:
            increment("parsed_emails")

            parsed = {
                "type": self.classify_email(text),
                "entities": self.extract_entities(text),
                "raw": text
            }

            cost = max(1, len(text)//50)
            update_cost(cost)
            if get_today_tokens() > 50:
                alert_async(f"⚠️ High LLM cost: {get_today_tokens()}")

            duration = time.time() - start
            if duration > 5:
                alert_async(f"⚠️ Slow LLM call: {duration:.2f}s")

            return parsed

        except Exception as e:
            alert_async(f"🤖 LLM Fatal Error: {str(e)}")
            increment("llm_errors")
            return {"type": "unknown", "entities": {}, "raw": text}
