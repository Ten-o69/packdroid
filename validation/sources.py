from typing import Literal
from pathlib import Path

from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
)


class BaseSource(BaseModel):
    """
    Base schema for a source definition.

    Attributes:
        package (str): Package name of the Android app.
        method (Literal["raccoon", "url", "local"]):
            Defines the method to obtain the APK:
              - "raccoon" → download via Raccoon (Play Store client).
              - "url"     → direct download from a given URL.
              - "local"   → use a local file path.
    """
    package: str
    method: Literal["raccoon", "url", "local"]


class SourceRaccoon(BaseSource):
    """
    Schema for a Raccoon-based source.

    Inherits fields from BaseSource.
    Used when APKs are to be fetched from Google Play
    using the Raccoon JAR tool.
    """
    pass


class SourceUrl(BaseSource):
    """
    Schema for a URL-based source.

    Attributes:
        url (HttpUrl): Direct HTTP(S) link to the APK file.
    """
    url: HttpUrl


class SourceLocal(BaseSource):
    """
    Schema for a local file source.

    Attributes:
        path (Path): Filesystem path to the APK file.
    """
    path: Path


class Sources(BaseModel):
    """
    Top-level container schema for multiple sources.

    Attributes:
        sources (list[SourceRaccoon | SourceUrl | SourceLocal]):
            A list of source definitions, each describing
            how to obtain a particular package.
    """
    sources: list[SourceRaccoon | SourceUrl | SourceLocal] = Field(default=[])
