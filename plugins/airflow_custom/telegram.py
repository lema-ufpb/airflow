import os
import requests
import logging

log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)


def telegram_alert(message):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return message

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        log.info(f"Sending Telegram message...")
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        log.error(f"Error on send message: {e}")


def telegram_success_alert(context):

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("execution_date")

    message = f"""
✅ *Airflow: Task finished successfully!*
📄 *DAG*: `{dag_id}`
🛠️ *Task*: `{task_id}`
🗓️ *Date*: `{execution_date}`
""".strip()

    telegram_alert(message)


def telegram_error_alert(context):

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("execution_date")

    message = f"""
❌ *Airflow: Task failed!*
📄 *DAG*: `{dag_id}`
🛠️ *Task*: `{task_id}`
🗓️ *Date*: `{execution_date}`
""".strip()

    telegram_alert(message)
