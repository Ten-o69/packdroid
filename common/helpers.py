from pathlib import Path
import sys
import subprocess
import os
from zipfile import ZipFile
from typing import Type
import json

import requests
from ten_utils.log import Logger
from tqdm import tqdm
from pydantic import BaseModel
import yaml

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
        text: bool = True,
        check_output: bool = False,
        capture_output: bool = False,
) -> subprocess.CompletedProcess | str:
    """
    Execute a local shell command with optional output capture.

    Args:
        cmd (list[str]): Command and arguments to execute as a list.
        check (bool, optional):
            If True, raise CalledProcessError on non-zero exit code.
            Defaults to True.
        text (bool, optional):
            If True, interpret stdout/stderr as strings (decoded).
            If False, return raw bytes. Defaults to True.
        check_output (bool, optional):
            If True, execute with subprocess.check_output() and return
            command output as a string.
            If False, execute with subprocess.run() and return a
            CompletedProcess object. Defaults to False.
        capture_output (bool, optional):
            If True, capture stdout and stderr when using subprocess.run.
            Ignored if check_output=True. Defaults to False.

    Returns:
        subprocess.CompletedProcess | str:
            - CompletedProcess object when check_output=False.
            - Command output (str) when check_output=True.

    Notes:
        - Logs the executed command at debug level.
        - Always passes arguments as a list, avoiding the security risks
          of shell=True.
        - Provides flexibility: choose between silent execution, capturing
          output, or directly returning stdout as a string.
    """
    logger.debug("LOCAL CMD: " + " ".join(cmd))

    if not check_output:
        return subprocess.run(
            cmd,
            check=check,
            text=text,
            capture_output=capture_output,
        )

    else:
        return subprocess.check_output(
            cmd,
            text=text,
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


def yaml_dump_with_pydantic_model(
        path_to_yaml: Path | str,
        pydantic_model: Type[BaseModel],
) -> BaseModel:
    """
    Serialize a Pydantic model (with default values) into a YAML file.

    - Creates an instance of the given Pydantic model using default values.
    - Converts the model to a dictionary via JSON serialization.
    - Writes the dictionary into a YAML file at the given path.
    - Returns the model instance for further use.

    Args:
        path_to_yaml (Path | str): Destination path for the YAML file.
        pydantic_model (Type[BaseModel]): Any Pydantic model class.

    Returns:
        BaseModel: A newly created model instance with default values.

    Notes:
        - This function can be used to initialize YAML files for any schema.
        - Useful as a schema-driven way to bootstrap new YAML documents.
    """
    with open(path_to_yaml, "w") as yaml_file:
        data_obj = pydantic_model()

        model_data = json.loads(data_obj.model_dump_json())
        yaml.safe_dump(model_data, yaml_file, default_flow_style=False)

    return data_obj


def yaml_load_with_pydantic_model(
        path_to_yaml: Path | str,
        pydantic_model: Type[BaseModel]
) -> BaseModel | None:
    """
    Load data from a YAML file and validate it with a Pydantic model.

    Behavior:
      - If the YAML file is empty, a new one will be created with default
        values using `yaml_dump_with_pydantic_model`, and that model
        instance will be returned.
      - If the YAML contains invalid data types (not dict or list),
        logs a critical error and returns None.
      - If the YAML contains a list, the list will be broadcasted
        into each field of the model.
      - If the YAML contains a dict, it will be passed directly
        into the model constructor.

    Args:
        path_to_yaml (Path | str): Path to the YAML file to load.
        pydantic_model (Type[BaseModel]): Any Pydantic model class to validate against.

    Returns:
        BaseModel | None:
            - Instance of the given Pydantic model with loaded data.
            - None if the YAML format is invalid.

    Notes:
        - Works as a general-purpose bridge between YAML and Pydantic models.
        - Ensures that YAML data always conforms to the given schema.
        - Can be used for configs, manifests, datasets, or any structured YAML data.
    """
    with open(path_to_yaml, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

        if data is None:
            return yaml_dump_with_pydantic_model(
                path_to_yaml=path_to_yaml,
                pydantic_model=pydantic_model,
            )

        elif not isinstance(data, (dict, list)):
            logger.critical(f"Incorrect configuration format. Must be 'dict', not '{type(data)}'")
            return None

        elif isinstance(data, list):
            data_dict = {}

            for key in pydantic_model.model_fields.keys():
                data_dict[key] = data

            return pydantic_model(**data_dict)

        else:
            return pydantic_model(**data)
