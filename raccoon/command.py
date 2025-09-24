from pathlib import Path
from subprocess import CompletedProcess

from common.constants import (
    DIR_BIN_RACCOON,
    FILENAME_RACCOON_BIN,
)
from common.helpers import run_local_cmd
from config import cfg_obj


class Raccoon:
    def __init__(
            self,
            path_to_raccoon_bin: Path | str = DIR_BIN_RACCOON / FILENAME_RACCOON_BIN,
    ):
        self.path_bin = str(path_to_raccoon_bin)
        self.__command_base = [
            cfg_obj.java_bin, "-jar", self.path_bin,
        ]

    def download_apk(self, package_name: str, out_path: Path | str) -> CompletedProcess:
        cmd = [
            *self.__command_base,
            "--gpa-download", package_name,
            "--gpa-download-dir", str(out_path),
        ]

        return run_local_cmd(cmd)
