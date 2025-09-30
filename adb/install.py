import os

from common.constants import (
    DIR_BIN_ADB,
    FILENAME_ADB_BIN_ZIP,
    FILENAME_ADB_BIN,
    BASE_SYSTEM,
)
from common.helpers import download_file, unzip, run_cmd
from config import config_obj


def check_adb_install() -> None:
    """
    Ensure that the ADB binary is installed locally.

    Workflow:
        1. Check if the ADB binary exists in DIR_BIN_ADB.
        2. If not, download the platform-specific ADB archive (ZIP).
        3. Extract the archive into DIR_BIN_ADB.
        4. Clean up by deleting the downloaded ZIP file.

    Notes:
        - Uses config_obj.adb_bin_link to determine the correct download URL.
        - Extracted files will overwrite any existing ones inside DIR_BIN_ADB.
        - The ZIP file is always removed after extraction (even if unzip fails).
    """
    if not list(DIR_BIN_ADB.rglob(FILENAME_ADB_BIN)):
        path_to_adb_bin_zip = DIR_BIN_ADB / FILENAME_ADB_BIN_ZIP

        # Download ADB binary archive from configured source
        download_file(
            url=config_obj.adb_bin_link,
            path=path_to_adb_bin_zip,
        )

        try:
            # Extract the downloaded archive into the bin directory
            unzip(path_to_adb_bin_zip, out_path=DIR_BIN_ADB)

        finally:
            # Always remove the archive after extraction to save space
            os.remove(path_to_adb_bin_zip)

        if BASE_SYSTEM == "Linux" or BASE_SYSTEM == "Darwin":
            bin_paths = [str(path) for path in DIR_BIN_ADB.glob('*')]
            cmd = ["chmod", "+x"]

            for path in bin_paths:
                run_cmd(
                    cmd=cmd + [path],
                    check=False,
                    text=False,
                )
