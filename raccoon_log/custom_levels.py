import logging

IMPORTANT_LEVEL = 25
NOTIFY_LEVEL = 35

logging.addLevelName(IMPORTANT_LEVEL, "IMPORTANT")
logging.addLevelName(NOTIFY_LEVEL, "NOTIFY")


def _important(message, *args, **kwargs):
    """
    Function to log in the new level (important)

    Args:
        message: message to log;
    """
    logging.log(IMPORTANT_LEVEL, message)


def _notify(message, *args, **kwargs):
    """
    Function to log in the new level (notify)

    Args:
        message: message to log;
    """
    logging.log(NOTIFY_LEVEL, message)
