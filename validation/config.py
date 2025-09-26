from typing import Union

from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
    FilePath,
)

from common.constants import (
    WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON,
    FILENAME_RACCOON_BIN,
)
from .utils import get_adb_bin_link


class Config(BaseModel):
    """
    Pydantic model for application configuration.

    Attributes:
        raccoon_bin_link (HttpUrl):
            URL for downloading raccoon.jar binary.
            Defaults to WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON.

        adb_bin_link (HttpUrl):
            Platform-specific URL for downloading ADB binary.
            Determined at runtime via get_adb_bin_link().

        java_bin (str | FilePath):
            Path to the Java executable used to run raccoon.jar.
            Defaults to FILENAME_RACCOON_BIN (can be overridden).
    """
    raccoon_bin_link: HttpUrl = Field(default=WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON)
    adb_bin_link: HttpUrl = Field(default=get_adb_bin_link())
    java_bin: Union[str, FilePath] = Field(default=FILENAME_RACCOON_BIN)
