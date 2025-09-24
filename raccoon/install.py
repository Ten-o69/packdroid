from common.constants import (
    DIR_BIN_RACCOON,
    FILENAME_RACCOON_BIN,
)
from common.helpers import download_file
from config import cfg_obj


def check_raccoon_bin_install() -> None:
    """
    Ensure that raccoon.jar binary is installed locally.

    Notes:
        - If the binary does not exist in DIR_BIN_RACCOON,
          it will be downloaded from cfg_obj.raccoon_bin_link.
        - The download is handled by `download_file` with a progress bar.
    """
    if not list(DIR_BIN_RACCOON.glob(FILENAME_RACCOON_BIN)):
        download_file(
            url=cfg_obj.raccoon_bin_link,
            path=DIR_BIN_RACCOON / FILENAME_RACCOON_BIN,
        )
