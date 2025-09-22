import requests

from common.constants import (
    DIR_BIN_RACCOON,
)
from config import cfg_obj

def check_raccoon_bin_install():
    if not list(DIR_BIN_RACCOON.glob("raccoon.jar")):
        file = requests.get(cfg_obj.raccoon_bin_link)

        with open(DIR_BIN_RACCOON / "raccoon.jar", "wb") as raccoon_jar:
            raccoon_jar.write(file.content)
