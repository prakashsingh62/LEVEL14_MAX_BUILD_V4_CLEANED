from alerts.alert_manager import alert_async

def send_daily_summary(stats):
    date = stats.get("date", "")
    msg = f"*📅 Daily Summary -- {date}*\n"
    for k,v in stats.items():
        msg += f"• *{k}*: {v}\n"
    alert_async(msg)