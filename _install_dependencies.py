import platform
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

import toml

PROJECT_DIR = Path(__file__).parent


def get_sys_dependencies() -> List[str]:
    toml_cfg = toml.loads(PROJECT_DIR.joinpath('pyproject.toml').read_text())
    return toml_cfg.get('tool', {}).get('sys-dependencies', {}).get('apt', [])


def install_sys_dependencies(
    sys_dependencies: List[str], sudo: bool = False
) -> None:
    if len(sys_dependencies) == 0:
        return

    if 'linux' in platform.system().lower():
        update_commands = ['apt', 'update', '-y']
        install_commands = ['apt', 'install', '-y'] + sys_dependencies
    else:
        raise NotImplementedError()
    if sudo is True:
        update_commands = ['sudo'] + update_commands
        install_commands = ['sudo'] + install_commands
    subprocess.run(' '.join(update_commands), shell=True)
    subprocess.run(' '.join(install_commands), shell=True)


def pars_args(arg_list: Optional[List[str]] = None):
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--sudo",
        dest="sudo",
        action="store_true",
        default=False,
        help="if set, will install system dependencies in sudo mode.",
    )
    args = parser.parse_args(arg_list)

    return args


def main(arg_list: Optional[List[str]] = None):
    args = pars_args(arg_list)
    sys_dependencies = get_sys_dependencies()
    install_sys_dependencies(sys_dependencies, sudo=args.sudo)


if __name__ == '__main__':
    main(["--sudo"])
