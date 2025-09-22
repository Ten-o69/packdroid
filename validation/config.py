from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
)

from common.constants import (
    WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON,
)


class Config(BaseModel):
    raccoon_bin_link: HttpUrl = Field(default=WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON)
