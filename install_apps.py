from pathlib import Path

from ten_utils.log import Logger

from raccoon.command import Raccoon
from adb.command import Adb
from common.constants import (
    DIR_APKS,
)
from common.helpers import download_file, str_to_path

logger = Logger(__name__)


def download_with_raccoon(package: str) -> Path:
    """
    Download an APK bundle (ABB) using the Raccoon tool.

    Args:
        package (str): Package name of the Android app.

    Returns:
        Path: Directory where APK files for the package are stored.

    Workflow:
        - Creates a directory inside DIR_APKS for the given package.
        - If no APKs are found in that directory, invokes Raccoon to download them.
        - Verifies that APK files exist and Raccoon exited successfully.
        - Logs how many APKs were downloaded.

    Raises:
        Logs a critical error if Raccoon fails to download the package.
    """
    logger.info(f"Downloading {package} via Raccoon ...")
    app_dir = DIR_APKS / package
    raccoon = Raccoon()

    app_dir.mkdir(parents=True, exist_ok=True)

    apk_files = list(app_dir.glob("*.apk"))

    if not apk_files:
        success_run = raccoon.download_apk(
            package_name=package,
            out_path=DIR_APKS
        )

        apk_files = list(app_dir.glob("*.apk"))
        if not apk_files or success_run.returncode != 0:
            logger.critical(f"Raccoon failed to download {package}")

    logger.info(f"Downloaded {len(apk_files)} apk(s) for {package}")
    return app_dir


def download_with_url(url: str, package: str) -> Path:
    """
    Download a single APK from a direct URL.

    Args:
        url (str): Direct HTTP(S) link to the APK.
        package (str): Package name used for naming the downloaded file.

    Returns:
        Path: Path to the downloaded APK file.

    Workflow:
        - Saves the APK into DIR_APKS/{package}.apk.
        - Skips download if the file already exists.
        - Logs download completion.
    """
    logger.info(f"Downloading {package} from URL ...")
    target = DIR_APKS / f"{package}.apk"

    if not target.exists():
        download_file(
            url=url,
            path=target,
        )

    logger.info(f"Downloaded: {target}")
    return target


def install_apk(
        package: str,
        source: Path | str,
        adb: Adb,
) -> None:
    """
    Install an APK (single or split) on the device using ADB.

    Args:
        package (str): Package name of the app.
        source (Path | str): Path to a single APK file or a directory with multiple APKs.
        adb (Adb): Instance of Adb client used for installation.

    Raises:
        ValueError: If the provided source is neither a file nor a directory.

    Workflow:
        - If source is a file → installs a single APK.
        - If source is a directory → installs a split APK (ABB).
        - After installation, verifies if the package is installed on the device.
        - Logs success (✅) or failure (❌).
    """
    source = str_to_path(source)

    if source.is_file():
        logger.info(f"Installing single APK for {package}")
        adb.install_apk(source)

    elif source.is_dir():
        adb.install_split_apk(package, source)

    else:
        raise ValueError(f"Invalid source: {source}")
