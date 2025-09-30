from typing import Literal
from pathlib import Path

from pydantic import (
    BaseModel,
    HttpUrl,
)


class BaseSource(BaseModel):
    package: str
    method: Literal["raccoon", "url", "local"]


class SourceRaccoon(BaseSource): pass


class SourceUrl(BaseSource):
    url: HttpUrl


class SourceLocal(BaseSource):
    path: Path


class Sources(BaseModel):
    sources: list[SourceRaccoon | SourceUrl | SourceLocal]
