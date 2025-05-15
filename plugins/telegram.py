import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)


def telegram_success_alert(context):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return "Running in development mode"

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("execution_date")
    log_url = task_instance.log_url

    message = f"""
✅ *Airflow: Task finished successfully!*
*DAG*: `{dag_id}`
*Task*: `{task_id}`
*Date*: `{execution_date}`
🔍 See log: <a href='{log_url}'>{log_url}</a>
""".strip()

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error on send message: {e}")


def telegram_error_alert(context):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return "Running in development mode"

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("execution_date")
    log_url = context.get("task_instance").log_url

    message = f"""
⚠️ *Airflow: Task failed!*
*DAG*: `{dag_id}`
*Task*: `{task_id}`
*Date*: `{execution_date}`
🔍 See log: <a href='{log_url}'>{log_url}</a>
""".strip()

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error on send message: {e}")
