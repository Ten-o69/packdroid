from pathlib import Path

from ten_utils.log import Logger

from common.constants import (
    PATHS_CHECK_DEFAULT,
)
from common.helpers import str_to_path

logger = Logger(__name__)


def init_check_paths(paths: list[dict[str, bool | Path]] = PATHS_CHECK_DEFAULT) -> None:
    """
    Ensure that all required paths (files or directories) exist.
    Creates them if missing.

    Args:
        paths (list[dict[str, bool | Path]]):
            List of dictionaries where:
              - "path" (Path | str): Target path.
              - "is_file" (bool): True if path should be a file, False if directory.
            Defaults to PATHS_CHECK_DEFAULT.

    Notes:
        - Uses `touch()` to create files if missing.
        - Uses `mkdir(parents=True, exist_ok=True)` to create directories.
    """
    for path_dict in paths:
        path = path_dict["path"]
        is_file = path_dict["is_file"]

        logger.debug(f"Checking {path}")
        path = str_to_path(path)

        if is_file:
            logger.debug(f"Create file: {path.__str__()}")
            path.touch()

        elif not is_file:
            logger.debug(f"Create dir: {path.__str__()}")
            path.mkdir(parents=True, exist_ok=True)
