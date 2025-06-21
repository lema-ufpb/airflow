import logging

log = logging.getLogger(__name__)

ANSI_STYLES = {
    "bold": "\033[1m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "bold_red": "\033[1m\033[31m",
    "bold_green": "\033[1m\033[32m",
    "bold_yellow": "\033[1m\033[33m",
    "bold_blue": "\033[1m\033[34m",
}

RESET = "\033[0m"


def styled_log(message, style="bold"):
    """Log a message with a specific ANSI style."""
    style_code = ANSI_STYLES.get(style, "")
    log.info(f"{style_code}{message}{RESET}")
