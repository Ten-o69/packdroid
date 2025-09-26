from pathlib import Path
import sys
import subprocess
import os
from zipfile import ZipFile

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


def run_cmd(
        cmd: list[str],
        check: bool = True,
        check_output: bool = False,
) -> subprocess.CompletedProcess | str:
    """
    Execute a local shell command with optional output capture.

    Args:
        cmd (list[str]): Command and arguments to execute as a list.
        check (bool, optional):
            If True, raise CalledProcessError on non-zero exit code.
            Defaults to True.
        check_output (bool, optional):
            If True, capture and return command output as a string
            using subprocess.check_output.
            If False, return a CompletedProcess object from subprocess.run.
            Defaults to False.

    Returns:
        subprocess.CompletedProcess | str:
            - CompletedProcess if check_output is False.
            - Command output (str) if check_output is True.

    Notes:
        - Logs the executed command at debug level.
        - Uses text mode to ensure stdout/stderr are returned as strings.
        - Safer than shell=True since the command is passed as a list.
    """
    logger.debug("LOCAL CMD: " + " ".join(cmd))

    if not check_output:
        return subprocess.run(
            cmd,
            check=check,
            text=True
        )

    else:
        return subprocess.check_output(
            cmd,
            text=True
        )


def unzip(path_to_zip: Path | str, out_path: Path | str) -> None:
    """
    Extract the contents of a ZIP archive to a specified output directory.

    Args:
        path_to_zip (Path | str): Path to the ZIP file to be extracted.
        out_path (Path | str): Target directory where files will be extracted.

    Notes:
        - Creates directories recursively if they do not exist.
        - Skips directory entries inside the archive (only extracts files).
        - Overwrites existing files with the same name.
    """
    path_to_zip = str_to_path(path_to_zip)
    out_path = str_to_path(out_path)

    with ZipFile(path_to_zip, "r") as zip_file:
        for member in zip_file.namelist():
            # Remove folder prefix, keep only the file name/relative path
            filename = member.split("/", 1)[-1]

            if not filename:
                # Skip directory entries
                continue

            target_path = out_path / filename
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Extract file contents safely
            with zip_file.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())
