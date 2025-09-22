from pathlib import Path

from pydantic import HttpUrl


# dir
BASE_DIR = Path(__file__).parent.parent
DIR_BIN_RACCOON = BASE_DIR / "raccoon" / "bin"
DIR_APKS = BASE_DIR / "apks"

# path
PATH_CONFIG_FILE = BASE_DIR / "config.yaml"
PATH_SOURCES_FILE = BASE_DIR / "sources.json"
PATHS_CHECK_DEFAULT = [DIR_BIN_RACCOON, DIR_APKS, PATH_CONFIG_FILE, PATH_SOURCES_FILE]

# web link
WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON = HttpUrl("https://www.dropbox.com/scl/fi/8np6usic1qu2xisgtbpsh/"
                                                "raccoon-4.24.0.jar?rlkey=jqzyn25ptmearic4gddd2762y&st=yt4vzyzr&dl=1")
