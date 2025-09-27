from pathlib import Path
from subprocess import CompletedProcess

from ten_utils.log import Logger

from common.constants import (
    DIR_BIN_ADB,
    FILENAME_ADB_BIN,
)
from common.helpers import str_to_path, run_cmd
from .decorators import check_device_set

logger = Logger(__name__)


class Adb:
    """
    Wrapper class for executing ADB (Android Debug Bridge) commands.

    Provides methods for:
      - Selecting a target device.
      - Installing APKs (single or split).
      - Querying connected devices.
      - Listing installed packages.

    Attributes:
        path_adb_bin (str): Path to the adb binary.
        __command_base (list[str]): Base adb command (binary + optional device flag).
        device_set (bool): Whether a device has been set with `set_device`.
    """

    def __init__(
            self,
            path_to_adb_bin: str | Path = DIR_BIN_ADB / FILENAME_ADB_BIN,
    ):
        """
        Initialize the Adb wrapper.

        Args:
            path_to_adb_bin (str | Path, optional):
                Path to adb binary. Defaults to the bundled adb in /bin.
        """
        self.path_adb_bin = str(path_to_adb_bin)
        self.__command_base = [self.path_adb_bin]
        self.device_set: bool = False

    def set_device(self, device: str) -> None:
        """
        Set the target device for adb commands.

        Args:
            device (str): Device identifier (from `adb devices`).
        """
        self.__command_base = [
            *self.__command_base,
            "-s", device,
        ]
        self.device_set = True

    @check_device_set
    def install_split_apk(self, package_name: str, app_dir: Path | str) -> CompletedProcess:
        """
        Install an app consisting of multiple APKs (split APK / ABB).

        Args:
            package_name (str): Name of the application package.
            app_dir (Path | str): Path to directory containing APK files.

        Returns:
            CompletedProcess: Result of the adb command.
        """
        app_dir = str_to_path(app_dir)
        apk_files = sorted(app_dir.rglob("*.apk"))
        if not apk_files:
            logger.critical(f"No APK files found in {app_dir}")

        logger.info(f"Installing ABB ({len(apk_files)} files) for {package_name}")

        apk_files = [str(f) for f in apk_files]
        cmd = [*self.__command_base, "install-multiple", "-r", *apk_files]

        return run_cmd(cmd)

    @check_device_set
    def install_apk(self, source: str | Path) -> CompletedProcess:
        """
        Install a single APK on the target device.

        Args:
            source (str | Path): Path to the APK file.

        Returns:
            CompletedProcess: Result of the adb command.
        """
        cmd = [*self.__command_base, "install", "-r", str(source)]
        return run_cmd(cmd)

    def get_devices(self) -> str:
        """
        List all connected devices visible to adb.

        Returns:
            str: Command output (list of devices).
        """
        cmd = [*self.__command_base, "devices"]
        return run_cmd(cmd, check_output=True)

    @check_device_set
    def get_packages(self) -> CompletedProcess:
        """
        List all installed packages on the target device.

        Returns:
            CompletedProcess: Result containing package list in stdout.
        """
        cmd = [*self.__command_base, "shell", "pm", "list", "packages"]
        return run_cmd(cmd, capture_output=True)
