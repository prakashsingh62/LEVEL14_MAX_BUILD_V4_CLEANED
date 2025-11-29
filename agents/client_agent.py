from alerts.alert_manager import alert_async
from core.stats_collector import increment
from core.token_manager import update_cost, get_today_cost
from nlp.llm_client import LLMClient

llm = LLMClient()

def process_client_row(row):
    try:
        increment("client_checks")

        if row.get("status") == "PENDING":
            increment("client_pending")

        # LLM classification
        result = llm.classify_email(row)
        return result

    except Exception as e:
        increment("client_agent_errors")
        alert_async(f"❌ Client Agent Error: {str(e)}")
        return {"error": str(e), "row": row}
