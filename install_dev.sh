#!/bin/bash
pip install -e "../jampy_cli"
pip install -e ".[dev]"

python _install_dependencies.py --sudo

pre-commit install
mypy --install-types
