from pathlib import Path

from ten_utils.log import Logger

from _utils import init_check_paths

init_check_paths()

from common.helpers import yaml_load_with_pydantic_model
from common.constants import (
    PATH_SOURCES_FILE,
)
from raccoon.install import check_raccoon_bin_install
from adb.install import check_adb_install
from adb.command import Adb
from validation.sources import (
    Sources,
    SourceUrl,
    SourceLocal,
    SourceRaccoon,
)
from install_apps import install_apk, download_with_raccoon, download_with_url

adb = Adb()
logger = Logger(__name__)


def select_device() -> None:
    """
    Interactively select a connected Android device for ADB operations.

    Workflow:
        - Retrieves the list of connected devices via `adb devices`.
        - If no devices are found → logs a critical error.
        - If one device is connected → automatically selects it.
        - If multiple devices are found → prompts user input to choose one.

    Raises:
        Logs critical error if no devices are detected.
    """
    out = adb.get_devices().splitlines()
    devices = [l.split()[0] for l in out[1:] if l.strip() and "device" in l]

    if not devices:
        logger.critical("No connected devices found!")

    if len(devices) == 1:
        adb.set_device(devices[0])
        logger.info(f"Device selected: {devices[0]}")

    else:
        logger.info("Multiple devices detected:")
        for idx, dev in enumerate(devices, start=1):
            logger.info(f"{idx}: {dev}")

        while True:
            choice = input("Select device by number: ")

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    adb.set_device(devices[idx])
                    logger.info(f"Device selected: {devices[idx]}")
                    break

            except ValueError:
                pass

            logger.warning("Invalid input, please try again.")


def resolve_source(
        entry: SourceRaccoon | SourceLocal | SourceUrl
) -> Path | None:
    """
    Resolve the installation source for a given package.

    Args:
        entry (BaseSource): One of the supported source types:
            - SourceRaccoon → Download via Raccoon tool.
            - SourceUrl → Download from a direct URL.
            - SourceLocal → Use local APK path.

    Returns:
        Path | None: Path to APK file or directory.

    Raises:
        Logs a critical error if an unknown source method is specified.
    """
    if entry.method == "raccoon":
        return download_with_raccoon(entry.package)

    elif entry.method == "url":
        return download_with_url(entry.url.__str__(), entry.package)

    elif entry.method == "local":
        return entry.path

    else:
        logger.critical(f"Unknown source method: {entry.method}")


def main() -> None:
    """
    Entry point of the application.

    Workflow:
        1. Ensure required binaries (Raccoon, ADB) are installed.
        2. Select a connected Android device.
        3. Load the `sources.yaml` file and validate it with Pydantic.
        4. For each source entry:
            - Resolve its APK source (Raccoon, URL, or local path).
            - Install the APK(s) on the selected device.
        5. Log success or errors for each package.

    Notes:
        - This function orchestrates the full flow:
          from configuration → APK retrieval → installation.
    """
    check_raccoon_bin_install()
    check_adb_install()

    logger.info("=== START ===")

    select_device()

    logger.info(f"Reading a file {PATH_SOURCES_FILE} ...")
    sources_obj = yaml_load_with_pydantic_model(
        path_to_yaml=PATH_SOURCES_FILE,
        pydantic_model=Sources
    )

    for entry in sources_obj.sources:
        try:
            source = resolve_source(entry)
            install_apk(entry.package, source, adb)

        except Exception as e:
            logger.error(f"Error for {entry.package}: {e}")

    logger.info("=== FINISHED ===")


if __name__ == "__main__":
    main()
