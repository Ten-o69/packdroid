from pathlib import Path
import sys

import requests
from ten_utils.log import Logger
from tqdm import tqdm

from common.constants import (
    PATHS_CHECK_DEFAULT,
)

logger = Logger(__name__)


def str_to_path(string: Path | str) -> Path | None:
    """
    Convert a given input to a pathlib.Path object if possible.

    Args:
        string (Path | str): Input value, either a Path object or string.

    Returns:
        Path | None: A Path object if input is str,
                     the same Path if input is already Path,
                     or None if unsupported type.

    Notes:
        - Logs a critical message if the type is not supported.
    """
    if isinstance(string, Path):
        return string

    elif isinstance(string, str):
        return Path(string)

    else:
        logger.critical(f"Unsupported type {type(string)}")


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


def sizeof_fmt(num: int | float) -> str:
    """
    Format bytes into a human-readable string.

    Args:
        num (int | float): File size in bytes.

    Returns:
        str: Formatted size string (e.g., "10.5 MB").
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%.1f %s" % (num, x)

        num /= 1024.0

    return "%.1f %s" % (num, 'TB')


def download_file(url: str, path: Path | str) -> None:
    """
    Download a file from a given URL and save it to the specified path.

    Args:
        url (str): Source URL of the file.
        path (Path | str): Local path where the file will be stored.

    Notes:
        - Uses requests with stream=True for efficient downloading.
        - Displays a progress bar using tqdm.
        - Logs file size if content-length is available.
    """
    path = str_to_path(path)
    rs = requests.get(url, stream=True)

    logger.info(f"Downloading {path.name}")

    total_size = int(rs.headers.get('content-length', 0))
    logger.info(f'From content-length: {sizeof_fmt(total_size)}')

    chunk_size = 1024 * 1024  # 1 MB per chunk
    num_bars = int(total_size / chunk_size)

    with open(path, "wb") as f:
        # tqdm shows progress bar in MB units, writing chunks into file
        for data in tqdm(rs.iter_content(chunk_size=chunk_size), total=num_bars, unit="MB", file=sys.stdout):
            f.write(data)
