from common.constants import (
    DIR_BIN_RACCOON,
)
from common.helpers import download_file
from config import cfg_obj

def check_raccoon_bin_install():
    if not list(DIR_BIN_RACCOON.glob("raccoon.jar")):
        download_file(
            url=cfg_obj.raccoon_bin_link,
            path=DIR_BIN_RACCOON / "raccoon.jar",
        )
