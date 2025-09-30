from pathlib import Path
import platform

from pydantic import HttpUrl

# base
BASE_DIR = Path(__file__).parent.parent
BASE_SYSTEM = platform.system()

# dir
DIR_BIN = BASE_DIR / "bin"
DIR_BIN_RACCOON = DIR_BIN / "raccoon"
DIR_BIN_ADB = DIR_BIN / "adb"
DIR_APKS = BASE_DIR / "apks"

# path
PATH_CONFIG_FILE = BASE_DIR / "config.yaml"
PATH_SOURCES_FILE = BASE_DIR / "sources.yaml"
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
        "path": DIR_BIN_ADB,
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
FILENAME_ADB_BIN_ZIP = "adb.zip"
FILENAME_ADB_BIN = "adb.exe" if BASE_SYSTEM == "Windows" else "adb"

# web link
WEB_LINK_DEFAULT_DOWNLOAD_BIN_RACCOON: HttpUrl = HttpUrl("https://www.dropbox.com/scl/fi/8np6usic1qu2xisgtbpsh/"
                                                         "raccoon-4.24.0.jar?rlkey="
                                                         "jqzyn25ptmearic4gddd2762y&st=yt4vzyzr&dl=1")
WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_WINDOWS: HttpUrl = HttpUrl("https://www.dropbox.com/scl/fi/48ra9r4rgliw1zt5pwe7z/"
                                                                 "platform-tools-latest-windows.zip?rlkey="
                                                                 "ayg3177h9fd9dqkd2nse6kwqa&st=24n561c3&dl=1")
WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_DARWIN: HttpUrl = HttpUrl("https://www.dropbox.com/scl/fi/0m421bmeahkwcky6z6udi/"
                                                                "platform-tools-latest-darwin.zip?rlkey="
                                                                "uh7pko39a7nehe6qxcotdo8h7&st=bi3epald&dl=1")
WEB_LINK_DEFAULT_DOWNLOAD_BIN_ADB_FOR_LINUX: HttpUrl = HttpUrl("https://www.dropbox.com/scl/fi/nu3phl7bn8l2gn1syeuqk/"
                                                               "platform-tools-latest-linux.zip?rlkey="
                                                               "5sz131offsnuwci4x894529du&st=i0dgp5l7&dl=1")
