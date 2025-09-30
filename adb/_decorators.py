from typing import Callable
from functools import wraps

from ten_utils.log import Logger

logger = Logger(__name__)


def check_device_set(func: Callable) -> Callable:
    """
    Decorator that ensures an ADB command is only executed
    if a target device has been set.

    - Wraps an Adb class method.
    - If `self.device_set` is True, executes the method normally.
    - If no device is set, logs a critical error and returns None.

    Args:
        func (Callable): The decorated method.

    Returns:
        Callable: Wrapped function that performs the device check
        before executing.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        output = None

        if self.device_set:
            output = func(*args, **kwargs)

        else:
            logger.critical(
                "The device is not set! "
                "Set the device using the 'Adb.set_device' method."
            )

        return output

    return wrapper
