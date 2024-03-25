import importlib.metadata
import subprocess
from typing import Dict


def get_package_info(package_name: str) -> Dict:
    try:
        metadata = importlib.metadata.metadata(package_name)
        return metadata.json
    except importlib.metadata.PackageNotFoundError as e:
        raise e


def package_exists(package_name: str) -> bool:
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def is_dpkg_installed(package_name):
    """
    Check if a package is installed using dpkg.
    :param package_name: The name of the package to check.
    :return: True if the package is installed, False otherwise.
    """
    try:
        # If the package is installed,
        # dpkg -s will output details about it
        # If the package is not installed
        # dpkg -s will return a non-zero exit code
        result = subprocess.run(
            ['dpkg', '-s', package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
