from common.helpers import init_check_paths
from raccoon.install import check_raccoon_bin_install
from adb.install import check_adb_install
from install_apps import run_install

if __name__ == "__main__":
    init_check_paths()
    check_raccoon_bin_install()
    check_adb_install()

    run_install()
