from common.constants import (
    PATH_CONFIG_FILE,
)
from common.helpers import yaml_load_with_pydantic_model
from validation.config import Config


config_obj = yaml_load_with_pydantic_model(
    path_to_yaml=PATH_CONFIG_FILE,
    pydantic_model=Config,
)
