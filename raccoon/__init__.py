from .install import check_raccoon_bin_install

# Ensure that raccoon.jar binary is installed/available on import.
# This check runs automatically when the raccoon package is imported.
check_raccoon_bin_install()
