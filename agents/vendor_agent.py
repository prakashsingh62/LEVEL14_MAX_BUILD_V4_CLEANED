from alerts.alert_manager import alert_async
from core.stats_collector import increment
from nlp.llm_client import LLMClient

llm = LLMClient()

def process_vendor_row(row):
    try:
        increment("vendor_checks")

        if row.get("delay_flag"):
            increment("vendor_delayed")

        result = llm.classify_email(row)
        return result

    except Exception as e:
        increment("vendor_agent_errors")
        alert_async(f"⚠️ Vendor Agent Error: {str(e)}")
        return {"error": str(e), "row": row}
