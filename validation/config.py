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


class Config(BaseModel):
    raccoon_bin_link: HttpUrl = Field(default=WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON)
    java_bin: Union[str, FilePath] = Field(default=FILENAME_RACCOON_BIN)
