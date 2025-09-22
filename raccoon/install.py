import subprocess

import requests

from common.constants import (
    DIR_BIN_RACCOON,
)

def check_raccoon_bin_install():
    DIR_BIN_RACCOON.mkdir(parents=True, exist_ok=True)

    if not list(DIR_BIN_RACCOON.glob("raccoon.jar")):
        file = requests.get("https://www.dropbox.com/scl/fi/8np6usic1qu2xisgtbpsh/raccoon-4.24.0.jar?rlkey=jqzyn25ptmearic4gddd2762y&st=yt4vzyzr&dl=1")

        with open(DIR_BIN_RACCOON / "raccoon.jar", "wb") as raccoon_jar:
            raccoon_jar.write(file.content)
