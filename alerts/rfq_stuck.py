from alerts.alert_manager import alert_async

def rfq_stuck_alert(rfq_id, status):
    alert_async(f"📌 RFQ stuck detected: {rfq_id} status={status}")