from pydantic import HttpUrl
from ten_utils.log import Logger

from common.constants import (
    WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_WINDOWS,
    WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_DARWIN,
    WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_LINUX,
    BASE_SYSTEM,
)

logger = Logger(__name__)


def get_adb_bin_link() -> HttpUrl | None:
    """
    Return the platform-specific URL for downloading the ADB binary.

    Returns:
        HttpUrl | None: Download link for ADB, or None if the OS is unsupported.

    Notes:
        - Supports "Windows", "Darwin" (macOS), and "Linux".
        - Logs a critical error if the operating system is not supported.
    """
    if BASE_SYSTEM == "Windows":
        return WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_WINDOWS

    elif BASE_SYSTEM == "Darwin":
        return WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_DARWIN

    elif BASE_SYSTEM == "Linux":
        return WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_LINUX

    else:
        logger.critical(f"Unsupported system: {BASE_SYSTEM}")
