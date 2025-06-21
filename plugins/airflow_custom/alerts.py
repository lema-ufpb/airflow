import os
import requests
import logging

log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)


def telegram_alert(message):
    """
    Send a message to a Telegram chat using the bot API.
    Args:
        message (str): The message to send.
    Raises:
        Exception: If there is an error sending the message.
    """

    if not TELEGRAM_TOKEN or not CHAT_ID:
        log.info(message)
        return message

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        log.info(f"Sending message to Telegram...")
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        raise Exception(f"Error on send message: {e}")


def telegram_success_alert(context):
    """
    Send a success alert to Telegram when a task finishes successfully.
    Args:
        context (dict): The context dictionary provided by Airflow.
    Raises:
        Exception: If there is an error sending the alert.
    """

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = task_instance.start_date

    message = f"""
✅ *Airflow: Task finished successfully!*
📄 *DAG*: `{dag_id}`
🛠️ *Task*: `{task_id}`
🗓️ *Date*: `{execution_date}`
""".strip()

    telegram_alert(message)


def telegram_error_alert(context):
    """
    Send an error alert to Telegram when a task fails.
    Args:
        context (dict): The context dictionary provided by Airflow.
    Raises:
        Exception: If there is an error sending the alert.
    """

    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = task_instance.start_date

    message = f"""
❌ *Airflow: Task failed!*
📄 *DAG*: `{dag_id}`
🛠️ *Task*: `{task_id}`
🗓️ *Date*: `{execution_date}`
""".strip()

    telegram_alert(message)
