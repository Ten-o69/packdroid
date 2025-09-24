from pathlib import Path
from subprocess import CompletedProcess

from common.constants import (
    DIR_BIN_RACCOON,
    FILENAME_RACCOON_BIN,
)
from common.helpers import run_local_cmd
from config import cfg_obj


class Raccoon:
    """
    Wrapper class to interact with the Raccoon CLI (raccoon.jar).

    Attributes:
        path_bin (str): Path to raccoon.jar binary.
        __command_base (list[str]): Base command list with Java executable and raccoon.jar.
    """

    def __init__(
        self,
        path_to_raccoon_bin: Path | str = DIR_BIN_RACCOON / FILENAME_RACCOON_BIN,
    ):
        """
        Initialize the Raccoon wrapper.

        Args:
            path_to_raccoon_bin (Path | str, optional):
                Path to the raccoon.jar binary.
                Defaults to raccoon.jar under DIR_BIN_RACCOON.
        """
        self.path_bin = str(path_to_raccoon_bin)
        self.__command_base = [
            cfg_obj.java_bin, "-jar", self.path_bin,
        ]

    def download_apk(self, package_name: str, out_path: Path | str) -> CompletedProcess:
        """
        Download an APK from Google Play using raccoon.jar.

        Args:
            package_name (str): Target app package name (e.g., "com.example.app").
            out_path (Path | str): Directory where the APK will be saved.

        Returns:
            subprocess.CompletedProcess: Result of the executed command.

        Notes:
            - Uses raccoon.jar with `--gpa-download` and `--gpa-download-dir`.
            - Calls `run_local_cmd` to execute the command and log it.
        """
        cmd = [
            *self.__command_base,
            "--gpa-download", package_name,
            "--gpa-download-dir", str(out_path),
        ]

        return run_local_cmd(cmd)
