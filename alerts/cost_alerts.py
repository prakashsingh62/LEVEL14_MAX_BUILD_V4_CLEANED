from alerts.alert_manager import alert_async

def cost_alert(amount):
    if amount and amount > 50:
        alert_async(f"⚠️ LLM cost alert: ₹{amount}")