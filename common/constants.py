from pathlib import Path

from pydantic import HttpUrl


# dir
BASE_DIR = Path(__file__).parent.parent
DIR_BIN = BASE_DIR / "bin"
DIR_BIN_RACCOON = DIR_BIN / "raccoon"
DIR_APKS = BASE_DIR / "apks"

# path
PATH_CONFIG_FILE = BASE_DIR / "config.yaml"
PATH_SOURCES_FILE = BASE_DIR / "sources.json"
PATHS_CHECK_DEFAULT = [
    {
        "path": DIR_BIN,
        "is_file": False,
    },
    {
        "path": DIR_BIN_RACCOON,
        "is_file": False,
    },
    {
        "path": DIR_APKS,
        "is_file": False,
    },
    {
        "path": PATH_CONFIG_FILE,
        "is_file": True,
    },
    {
        "path": PATH_SOURCES_FILE,
        "is_file": True,
    },
]

# filename
FILENAME_RACCOON_BIN = "raccoon.jar"
FILENAME_JAVA_BIN = "java"

# web link
WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON = HttpUrl("https://www.dropbox.com/scl/fi/8np6usic1qu2xisgtbpsh/"
                                                "raccoon-4.24.0.jar?rlkey=jqzyn25ptmearic4gddd2762y&st=yt4vzyzr&dl=1")
