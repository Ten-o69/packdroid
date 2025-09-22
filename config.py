import json

import yaml

from common.constants import (
    PATH_CONFIG_FILE,
)
from validation.config import Config

PATH_CONFIG_FILE.touch(exist_ok=True)


def dump_config() -> Config:
    with open(PATH_CONFIG_FILE, "w") as config_file:
        config_obj = Config()

        config_data = json.loads(config_obj.model_dump_json())
        yaml.safe_dump(config_data, config_file, default_flow_style=False)

    return config_obj


def load_config() -> Config:
    with open(PATH_CONFIG_FILE, "r") as config_file:
        config = yaml.safe_load(config_file)

        if config is None:
            return dump_config()

        elif type(config) != dict:
            raise TypeError(f"Incorrect configuration format. Must be 'dict', not '{type(config)}'")

        else:
            return Config(**config)


cfg_obj = load_config()
